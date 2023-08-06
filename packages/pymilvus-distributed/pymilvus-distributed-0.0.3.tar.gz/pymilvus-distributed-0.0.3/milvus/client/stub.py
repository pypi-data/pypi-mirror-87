# -*- coding: UTF-8 -*-

import collections
import functools
import logging

from urllib.parse import urlparse

from . import __version__
from .types import Status
from .check import check_pass_param, is_legal_host, is_legal_port
from .pool import ConnectionPool, SingleConnectionPool, SingletonThreadPool
from .exceptions import ParamError, DeprecatedError

from ..settings import DefaultConfig as config

LOGGER = logging.getLogger(__name__)


def deprecated(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        error_str = "Function {} has been deprecated".format(func.__name__)
        LOGGER.error(error_str)
        raise DeprecatedError(error_str)

    return inner


def check_connect(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return inner


def _pool_args(**kwargs):
    pool_kwargs = dict()
    for k, v in kwargs.items():
        if k in ("pool_size", "wait_timeout", "handler", "try_connect", "pre_ping", "max_retry"):
            pool_kwargs[k] = v

    return pool_kwargs


def _set_uri(host, port, uri, handler="GRPC"):
    default_port = config.GRPC_PORT if handler == "GRPC" else config.HTTP_PORT
    default_uri = config.GRPC_URI if handler == "GRPC" else config.HTTP_URI
    uri_prefix = "tcp://" if handler == "GRPC" else "http://"

    if host is not None:
        _port = port if port is not None else default_port
        _host = host
    elif port is None:
        try:
            _uri = urlparse(uri) if uri else urlparse(default_uri)
            _host = _uri.hostname
            _port = _uri.port
        except (AttributeError, ValueError, TypeError) as e:
            raise ParamError("uri is illegal: {}".format(e))
    else:
        raise ParamError("Param is not complete. Please invoke as follow:\n"
                         "\t(host = ${HOST}, port = ${PORT})\n"
                         "\t(uri = ${URI})\n")

    if not is_legal_host(_host) or not is_legal_port(_port):
        raise ParamError("host {} or port {} is illegal".format(_host, _port))

    return "{}{}:{}".format(uri_prefix, str(_host), str(_port))


class Milvus:
    def __init__(self, host=None, port=None, handler="GRPC", pool="SingletonThread", **kwargs):
        self._name = kwargs.get('name', None)
        self._uri = None
        self._status = None
        self._connected = False
        self._handler = handler

        if handler != "GRPC":
            raise NotImplementedError("only grpc handler is supported now!")

        _uri = kwargs.get('uri', None)
        pool_uri = _set_uri(host, port, _uri, self._handler)
        pool_kwargs = _pool_args(handler=handler, **kwargs)
        # self._pool = SingleConnectionPool(pool_uri, **pool_kwargs)
        if pool == "QueuePool":
            self._pool = ConnectionPool(pool_uri, **pool_kwargs)
        elif pool == "SingletonThread":
            self._pool = SingletonThreadPool(pool_uri, **pool_kwargs)
        elif pool == "Singleton":
            self._pool = SingleConnectionPool(pool_uri, **pool_kwargs)
        else:
            raise ParamError("Unknown pool value: {}".format(pool))

        # store extra key-words arguments
        self._kw = kwargs
        self._hooks = collections.defaultdict()

    def __enter__(self):
        self._conn = self._pool.fetch()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()
        self._conn = None

    def __del__(self):
        return self.close()

    def _connection(self):
        return self._pool.fetch()

    @property
    def name(self):
        return self._name

    @property
    def handler(self):
        return self._handler

    def close(self):
        """
        Close client instance
        """
        self._pool = None

    @check_connect
    def create_collection(self, collection_name, fields, timeout=30):
        '''
        Creates a collection.

        :param collection_name: The name of the collection. A collection name can only include
        numbers, letters, and underscores, and must not begin with a number.
        :type  str
        :param fields: Field parameters.
        :type  fields: str

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        '''
        with self._connection() as handler:
            return handler.create_collection(collection_name, fields, timeout)

    @check_connect
    def drop_collection(self, collection_name, timeout=30):
        """
        Deletes a specified collection.

        :param collection_name: The name of the collection to delete.
        :type  collection_name: str

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        check_pass_param(collection_name=collection_name)
        with self._connection() as handler:
            return handler.drop_collection(collection_name, timeout)

    @check_connect
    def has_collection(self, collection_name, timeout=30):
        """
        Checks whether a specified collection exists.

        :param collection_name: The name of the collection to check.
        :type  collection_name: str

        :return: If specified collection exists
        :rtype: bool

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        check_pass_param(collection_name=collection_name)
        with self._connection() as handler:
            return handler.has_collection(collection_name, timeout)

    @check_connect
    def get_collection_info(self, collection_name, timeout=30):
        """
        Returns information of a specified collection, including field
        information of the collection and index information of fields.

        :param collection_name: The name of the collection to describe.
        :type  collection_name: str

        :return: The information of collection to describe.
        :rtype: dict

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        check_pass_param(collection_name=collection_name)
        with self._connection() as handler:
            return handler.get_collection_info(collection_name, timeout)

    @check_connect
    def list_collections(self, timeout=30):
        """
        Returns a list of all collection names.

        :return: List of collection names, return when operation is successful
        :rtype: list[str]

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        with self._connection() as handler:
            return handler.list_collections(timeout)

    @check_connect
    def create_partition(self, collection_name, partition_tag, timeout=30):
        """
        Creates a partition in a specified collection. You only need to import the
        parameters of partition_tag to create a partition. A collection cannot hold
        partitions of the same tag, whilst you can insert the same tag in different collections.

        :param collection_name: The name of the collection to create partitions in.
        :type  collection_name: str

        :param partition_tag: Name of the partition.
        :type  partition_tag: str

        :param partition_tag: The tag name of the partition.
        :type  partition_tag: str

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        check_pass_param(collection_name=collection_name, partition_tag=partition_tag)
        with self._connection() as handler:
            return handler.create_partition(collection_name, partition_tag, timeout)

    @check_connect
    def drop_partition(self, collection_name, partition_tag, timeout=30):
        """
        Deletes the specified partitions in a collection.

        :param collection_name: The name of the collection to delete partitions from.
        :type  collection_name: str

        :param partition_tag: The tag name of the partition to delete.
        :type  partition_tag: str

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        check_pass_param(collection_name=collection_name, partition_tag=partition_tag)
        with self._connection() as handler:
            return handler.drop_partition(collection_name, partition_tag, timeout)

    @check_connect
    def has_partition(self, collection_name, partition_tag, timeout=30):
        """
        Checks if a specified partition exists in a collection.

        :param collection_name: The name of the collection to find the partition in.
        :type  collection_name: str

        :param partition_tag: The tag name of the partition to check
        :type  partition_tag: str

        :return: Whether a specified partition exists in a collection.
        :rtype: bool

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        check_pass_param(collection_name=collection_name, partition_tag=partition_tag)
        with self._connection() as handler:
            return handler.has_partition(collection_name, partition_tag, timeout)

    @check_connect
    def get_partition_info(self, collection_name, partition_tag, timeout=30):
        check_pass_param(collection_name=collection_name, partition_tag=partition_tag)
        with self._connection() as handler:
            return handler.get_partition_info(collection_name, partition_tag, timeout)

    @check_connect
    def list_partitions(self, collection_name, timeout=30):
        """
        Returns a list of all partition tags in a specified collection.

        :param collection_name: The name of the collection to retrieve partition tags from.
        :type  collection_name: str

        :return: A list of all partition tags in specified collection.
        :rtype: list[str]

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        check_pass_param(collection_name=collection_name)

        with self._connection() as handler:
            return handler.list_partitions(collection_name, timeout)

    @check_connect
    def bulk_insert(self, collection_name, entities, ids=None, partition_tag=None, params=None, timeout=None, **kwargs):
        """
        Inserts entities in a specified collection.

        :param collection_name: The name of the collection to insert entities in.
        :type  collection_name: str.
        :param entities: The entities to insert.
        :type  entities: list
        :param ids: The list of ids corresponding to the inserted entities.
        :type  ids: list[int]
        :param partition_tag: The name of the partition to insert entities in. The default value is
         None. The server stores entities in the “_default” partition by default.
        :type  partition_tag: str

        :return: list of ids of the inserted vectors.
        :rtype: list[int]

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        if kwargs.get("insert_param", None) is not None:
            with self._connection() as handler:
                return handler.bulk_insert(None, None, timeout=timeout, **kwargs)

        if ids is not None:
            check_pass_param(ids=ids)
        with self._connection() as handler:
            return handler.bulk_insert(collection_name, entities, ids, partition_tag, params, timeout, **kwargs)

    @check_connect
    def insert(self, collection_name, entities, ids=None, partition_tag=None, params=None, timeout=None, **kwargs):
        """
        Inserts entities in a specified collection.

        :param collection_name: The name of the collection to insert entities in.
        :type  collection_name: str.
        :param entities: The entities to insert.
        :type  entities: list
        :param ids: The list of ids corresponding to the inserted entities.
        :type  ids: list[int]
        :param partition_tag: The name of the partition to insert entities in. The default value is
         None. The server stores entities in the “_default” partition by default.
        :type  partition_tag: str

        :return: list of ids of the inserted vectors.
        :rtype: list[int]

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        if kwargs.get("insert_param", None) is not None:
            with self._connection() as handler:
                return handler.insert(None, None, timeout=timeout, **kwargs)

        if ids is not None:
            check_pass_param(ids=ids)
        with self._connection() as handler:
            return handler.insert(collection_name, entities, ids, partition_tag, params, timeout, **kwargs)

    @check_connect
    def search(self, collection_name, dsl, partition_tags=None, fields=None, timeout=None, **kwargs):
        """
        Searches a collection based on the given DSL clauses and returns query results.

        :param collection_name: The name of the collection to search.
        :type  collection_name: str
        :param dsl: The DSL that defines the query.
        :type  dsl: dict
        :param partition_tags: The tags of partitions to search.
        :type  partition_tags: list[str]
        :param fields: The fields to return in the search result
        :type  fields: list[str]

        :return: Query result.
        :rtype: QueryResult

        :raises:
            RpcError: If grpc encounter an error
            ParamError: If parameters are invalid
            BaseException: If the return result from server is not ok
        """
        with self._connection() as handler:
            return handler.search(collection_name, dsl, partition_tags, fields, timeout=timeout, **kwargs)

    @check_connect
    def flush(self, collection_names=None, timeout=None, **kwargs):
        pass