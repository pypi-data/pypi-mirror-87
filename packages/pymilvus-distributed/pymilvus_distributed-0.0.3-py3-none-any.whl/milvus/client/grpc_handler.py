import datetime
from urllib.parse import urlparse
import logging
import threading
import ujson

import grpc
from grpc._cython import cygrpc

from ..grpc_gen import milvus_pb2_grpc
from ..grpc_gen import milvus_pb2 as grpc_types
from ..grpc_gen import service_pb2_grpc
from ..grpc_gen import service_pb2 as service_types
from ..grpc_gen import service_pb2_grpc
from ..grpc_gen import service_msg_pb2 as service_msg_types
from .abstract import QueryResult, CollectionSchema
from .prepare import Prepare
from .types import Status
from .check import (
    int_or_str,
    is_legal_host,
    is_legal_port,
)

from .abs_client import AbsMilvus
from .asynch import SearchFuture, InsertFuture, CreateIndexFuture, CompactFuture, FlushFuture

from .hooks import BaseSearchHook
from .client_hooks import SearchHook, HybridSearchHook
from .exceptions import *
from ..settings import DefaultConfig as config
from . import __version__

LOGGER = logging.getLogger(__name__)


def error_handler(*rargs):
    def wrapper(func):
        def handler(self, *args, **kwargs):
            record_dict = {}
            try:
                record_dict["API start"] = str(datetime.datetime.now())
                if self._pre_ping:
                    self.ping()
                record_dict["RPC start"] = str(datetime.datetime.now())
                return func(self, *args, **kwargs)
            except BaseException as e:
                LOGGER.error("Error: {}".format(e))
                if e.code == Status.ILLEGAL_COLLECTION_NAME:
                    raise IllegalCollectionNameException(e.code, e.message)
                if e.code == Status.COLLECTION_NOT_EXISTS:
                    raise CollectionNotExistException(e.code, e.message)

                raise e

            except grpc.FutureTimeoutError as e:
                record_dict["RPC timeout"] = str(datetime.datetime.now())
                LOGGER.error("\nAddr [{}] {}\nRequest timeout: {}\n\t{}".format(self.server_address, func.__name__, e, record_dict))
                raise e
            except grpc.RpcError as e:
                record_dict["RPC error"] = str(datetime.datetime.now())
                LOGGER.error("\nAddr [{}] {}\nRPC error: {}\n\t{}".format(self.server_address, func.__name__, e, record_dict))
                raise e
            except Exception as e:
                record_dict["Exception"] = str(datetime.datetime.now())
                LOGGER.error("\nAddr [{}] {}\nExcepted error: {}\n\t{}".format(self.server_address, func.__name__, e, record_dict))
                raise e

        return handler

    return wrapper


def set_uri(host, port, uri):
    if host is not None:
        _port = port if port is not None else config.GRPC_PORT
        _host = host
    elif port is None:
        try:
            _uri = urlparse(uri) if uri else urlparse(config.GRPC_URI)
            _host = _uri.hostname
            _port = _uri.port
        except (AttributeError, ValueError, TypeError) as e:
            raise ParamError("uri is illegal: {}".format(e))
    else:
        raise ParamError("Param is not complete. Please invoke as follow:\n"
                         "\t(host = ${HOST}, port = ${PORT})\n"
                         "\t(uri = ${URI})\n")

    if not is_legal_host(_host) or not is_legal_port(_port):
        raise ParamError("host or port is illeagl")

    return "{}:{}".format(str(_host), str(_port))


class GrpcHandler(AbsMilvus):
    def __init__(self, host=None, port=None, pre_ping=True, **kwargs):
        self._channel = None
        self._stub = None
        self._uri = None
        self.status = None
        self._connected = False
        self._pre_ping = pre_ping
        # if self._pre_ping:
        self._max_retry = kwargs.get("max_retry", 5)

        # record
        self._id = kwargs.get("conn_id", 0)

        # condition
        self._condition = threading.Condition()
        self._request_id = 0

        # client hook
        self._search_hook = SearchHook()
        self._hybrid_search_hook = HybridSearchHook()
        self._search_file_hook = SearchHook()

        # set server uri if object is initialized with parameter
        _uri = kwargs.get("uri", None)
        self._setup(host, port, _uri, pre_ping)

    def __str__(self):
        attr_list = ['%s=%r' % (key, value)
                     for key, value in self.__dict__.items() if not key.startswith('_')]
        return '<Milvus: {}>'.format(', '.join(attr_list))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _setup(self, host, port, uri, pre_ping=False):
        """
        Create a grpc channel and a stub

        :raises: NotConnectError

        """
        self._uri = set_uri(host, port, uri)
        self._channel = grpc.insecure_channel(
            self._uri,
            options=[(cygrpc.ChannelArgKey.max_send_message_length, -1),
                     (cygrpc.ChannelArgKey.max_receive_message_length, -1),
                     ('grpc.enable_retries', 1),
                     ('grpc.keepalive_time_ms', 55000)]
        )
        # self._stub = milvus_pb2_grpc.MilvusServiceStub(self._channel)
        self._stub = service_pb2_grpc.MilvusServiceStub(self._channel)
        self.status = Status()

    def _pre_request(self):
        if self._pre_ping:
            self.ping()

    def _get_request_id(self):
        with self._condition:
            _id = self._request_id
            self._request_id += 1
            return _id

    def set_hook(self, **kwargs):
        """
        specify client hooks.
        The client hooks are used in methods which interact with server.
        Use key-value method to set hooks. Supported hook setting currently is as follow.

            search hook,
            search-in-file hook

        """

        # config search hook
        _search_hook = kwargs.get('search', None)
        if _search_hook:
            if not isinstance(_search_hook, BaseSearchHook):
                raise ParamError("search hook must be a subclass of `BaseSearchHook`")

            self._search_hook = _search_hook

        _search_file_hook = kwargs.get('search_in_file', None)
        if _search_file_hook:
            if not isinstance(_search_file_hook, BaseSearchHook):
                raise ParamError("search hook must be a subclass of `BaseSearchHook`")

            self._search_file_hook = _search_file_hook

    def ping(self):
        begin_timeout = 1
        timeout = begin_timeout
        ft = grpc.channel_ready_future(self._channel)
        retry = self._max_retry
        try:
            while retry > 0:
                try:
                    ft.result(timeout=timeout)
                    return True
                except:
                    retry -= 1
                    LOGGER.debug("Retry connect addr <{}> {} times".format(self._uri, self._max_retry - retry))
                    if retry > 0:
                        timeout *= 2
                        continue
                    else:
                        LOGGER.error("Retry to connect server {} failed.".format(self._uri))
                        raise
        except grpc.FutureTimeoutError:
            raise NotConnectError('Fail connecting to server on {}. Timeout'.format(self._uri))
        except grpc.RpcError as e:
            raise NotConnectError("Connect error: <{}>".format(e))
        # Unexpected error
        except Exception as e:
            raise NotConnectError("Error occurred when trying to connect server:\n"
                                  "\t<{}>".format(str(e)))

    @property
    def server_address(self):
        """
        Server network address
        """
        return self._uri

    @error_handler()
    def create_collection(self, collection_name, fields, timeout=30):
        collection_schema = Prepare.collection_schema(collection_name, fields)

        rf = self._stub.CreateCollection.future(collection_schema, wait_for_ready=True, timeout=timeout)
        status = rf.result()
        if status.error_code != 0:
            LOGGER.error(status)
            raise BaseException(status.error_code, status.reason)

        # return Status(status.error_code, status.reason)

    @error_handler()
    def drop_collection(self, collection_name, timeout=20):
        collection_name = Prepare.collection_name(collection_name)

        rf = self._stub.DropCollection.future(collection_name, wait_for_ready=True, timeout=timeout)
        status = rf.result()
        if status.error_code != 0:
            raise BaseException(status.error_code, status.reason)

        # return Status(status.error_code, status.reason)

    @error_handler(False)
    def has_collection(self, collection_name, timeout=30, **kwargs):
        collection_name = Prepare.collection_name(collection_name)

        rf = self._stub.HasCollection.future(collection_name, wait_for_ready=True, timeout=timeout)
        reply = rf.result()
        if reply.status.error_code == 0:
            # return Status(reply.status.error_code, reply.status.reason), reply.value
            return reply.value

        raise BaseException(reply.status.error_code, reply.status.reason)

    @error_handler(None)
    def get_collection_info(self, collection_name, timeout=30, **kwargs):
        collection_name = Prepare.collection_name(collection_name)
        rf = self._stub.DescribeCollection.future(collection_name, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status

        if response.status.error_code == 0:
            # return Status(status.error_code, status.reason), CollectionSchema(raw=response).dict()
            return CollectionSchema(raw=response).dict()

        LOGGER.error(response.status)
        raise BaseException(response.status.error_code, response.status.reason)
        # return Status(status.error_code, status.reason), CollectionSchema(None)

    @error_handler([])
    def list_collections(self, timeout=30):
        empty = Prepare.empty()
        rf = self._stub.ShowCollections.future(empty, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if response.status.error_code == 0:
            # return Status(status.error_code, status.reason), [name for name in response.values if len(name) > 0]
            return [name for name in response.values if len(name) > 0]
        raise BaseException(status.error_code, status.reason)

    @error_handler()
    def create_partition(self, collection_name, partition_tag, timeout=30):
        request = Prepare.partition_name(collection_name, partition_tag)
        rf = self._stub.CreatePartition.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)
        # return Status(response.status.error_code, response.status.reason)

    @error_handler()
    def drop_partition(self, collection_name, partition_tag, timeout=30):
        request = Prepare.partition_name(collection_name, partition_tag)

        rf = self._stub.DropPartition.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()

        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)

        # return Status(response.error_code, response.reason)

    @error_handler(False)
    def has_partition(self, collection_name, partition_tag, timeout=30):
        request = Prepare.partition_name(collection_name, partition_tag)
        rf = self._stub.HasPartition.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if status.error_code == 0:
            return response.value

        raise BaseException(status.error_code, status.reason)

    @error_handler(None)
    def get_partition_info(self, collection_name, partition_tag, timeout=30):
        request = Prepare.partition_name(collection_name, partition_tag)
        rf = self._stub.DescribePartition.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if status.error_code == 0:
            statistics = response.statistics
            info_dict = dict()
            for kv in statistics:
                info_dict[kv.key] = kv.value
            return info_dict
        raise BaseException(status.error_code, status.reason)

    @error_handler([])
    def list_partitions(self, collection_name, timeout=30):
        request = Prepare.collection_name(collection_name)

        rf = self._stub.ShowPartitions.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if status.error_code == 0:
            return [p for p in response.values]

        raise BaseException(status.error_code, status.reason)

    @error_handler([])
    def bulk_insert(self, collection_name, entities, ids=None, partition_tag=None, params=None, timeout=None, **kwargs):
        insert_param = kwargs.get('insert_param', None)

        # if insert_param and not isinstance(insert_param, grpc_types.InsertParam):
        #     raise ParamError("The value of key 'insert_param' is invalid")
        if insert_param and not isinstance(insert_param, service_msg_types.RowBatch):
            raise ParamError("The value of key 'insert_param' is invalid")

        collection = Prepare.collection_name(collection_name)
        rf = self._stub.DescribeCollection.future(collection, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.status.error_code != 0:
            raise BaseException(response.status.error_code, response.status.reason)
        collection_schema = CollectionSchema(raw=response).dict()

        if ids is None:
            ids = []
            for entity in entities:
                if "_id" in entity:
                    ids.append(entity["_id"])
            if not ids:
                ids = None

        auto_id = collection_schema["auto_id"]
        if not auto_id and ids is None:
            raise ParamError("You should specify the ids of entities!")
        fields_info = collection_schema["fields"]

        body = insert_param if insert_param \
            else Prepare.bulk_insert_param(collection_name, entities, partition_tag, ids, params, fields_info, auto_id=auto_id)

        rf = self._stub.Insert.future(body, wait_for_ready=True, timeout=timeout)
        if kwargs.get("_async", False) is True:
            cb = kwargs.get("_callback", None)
            return InsertFuture(rf, cb)

        response = rf.result()
        if response.status.error_code == 0:
            if auto_id:
                return list(range(response.begin, response.end))
            return list(ids)

        raise BaseException(response.status.error_code, response.status.reason)

    @error_handler([])
    def insert(self, collection_name, entities, ids=None, partition_tag=None, params=None, timeout=None, **kwargs):
        insert_param = kwargs.get('insert_param', None)

        # if insert_param and not isinstance(insert_param, grpc_types.InsertParam):
        #     raise ParamError("The value of key 'insert_param' is invalid")
        if insert_param and not isinstance(insert_param, service_msg_types.RowBatch):
            raise ParamError("The value of key 'insert_param' is invalid")

        collection = Prepare.collection_name(collection_name)
        rf = self._stub.DescribeCollection.future(collection, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.status.error_code != 0:
            raise BaseException(response.status.error_code, response.status.reason)
        collection_schema = CollectionSchema(raw=response).dict()

        if ids is None:
            ids = []
            for entity in entities:
                if "_id" in entity:
                    ids.append(entity["_id"])
            if not ids:
                ids = None

        auto_id = collection_schema["auto_id"]
        if not auto_id and ids is None:
            raise ParamError("You should specify the ids of entities!")
        fields_info = collection_schema["fields"]

        body = insert_param if insert_param \
            else Prepare.insert_param(collection_name, entities, partition_tag, ids, params, fields_info, auto_id=auto_id)

        rf = self._stub.Insert.future(body, wait_for_ready=True, timeout=timeout)
        if kwargs.get("_async", False) is True:
            cb = kwargs.get("_callback", None)
            return InsertFuture(rf, cb)

        response = rf.result()
        if response.status.error_code == 0:
            if auto_id:
                return list(range(response.begin, response.end))
            return list(ids)

        raise BaseException(response.status.error_code, response.status.reason)

    @error_handler(None)
    def search(self, collection_name, query_entities, partition_tags=None, fields=None, **kwargs):
        to = kwargs.get("timeout", None)
        rf = self._stub.HasCollection.future(Prepare.collection_name(collection_name), wait_for_ready=True, timeout=to)
        reply = rf.result()
        if reply.status.error_code != 0 or not reply.value:
            raise BaseException(reply.status.error_code, "collection not exists")

        request = Prepare.search_param(collection_name, query_entities, partition_tags, fields)
        self._search_hook.pre_search()
        ft = self._stub.Search.future(request, wait_for_ready=True, timeout=to)
        if kwargs.get("_async", False) is True:
            func = kwargs.get("_callback", None)
            return SearchFuture(ft, func)

        response = ft.result()
        self._search_hook.aft_search()

        if self._search_hook.on_response():
            return response

        if response.status.error_code != 0:
            raise BaseException(response.status.error_code, response.status.reason)

        # TODO: handler response
        # resutls = self._search_hook.handle_response(response)

        return QueryResult(response)
