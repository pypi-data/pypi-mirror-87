import abc
import copy
import struct
import ujson

from .exceptions import ParamError

from ..grpc_gen import milvus_pb2 as grpc_types
from ..grpc_gen import status_pb2

# for milvus-distributed
from ..grpc_gen import common_pb2 as common_types
from ..grpc_gen import schema_pb2 as schema_types
from ..grpc_gen import service_pb2 as service_types
from ..grpc_gen import service_msg_pb2 as service_msg_types

from . import blob

from .types import RangeType, DataType, MetricType, IndexType

BoolOccurMap = {
    "must": grpc_types.MUST,
    "must_not": grpc_types.MUST_NOT,
    "should": grpc_types.SHOULD
}

RangeOperatorMap = {
    RangeType.LT: grpc_types.LT,
    RangeType.LTE: grpc_types.LTE,
    RangeType.EQ: grpc_types.EQ,
    RangeType.GT: grpc_types.GT,
    RangeType.GTE: grpc_types.GTE,
    RangeType.NE: grpc_types.NE
}


class Prepare:

    @classmethod
    def collection_name(cls, collection_name):

        return service_msg_types.CollectionName(collection_name=collection_name)

    @classmethod
    def collection_schema(cls, collection_name, fields):
        """
        :type param: dict
        :param param: (Required)

            ` {"fields": [
                    {"field": "A", "type": DataType.INT64, "index": {"name":"", "type":"", "params": {..}}}
                    {"field": "B", "type": DataType.INT64},
                    {"field": "C", "type": DataType.INT64},
                    {"field": "Vec", "type": DataType.BINARY_VECTOR,
                     "params": {"metric_type": MetricType.L2, "dimension": 128}}
                ],
            "segment_size": 100}`

        :return: ttypes.TableSchema object
        """

        if not isinstance(fields, dict):
            raise ParamError("Param fields must be a dict")

        if "fields" not in fields:
            raise ParamError("Param fields must contains key 'fields'")

        schema = schema_types.CollectionSchema(name=collection_name)

        auto_id = fields.get('auto_id', True)
        schema.autoID = auto_id

        for fk, fv in fields.items():
            if fk != 'fields':
                # TODO: add extra_params
                continue

            for field in fv:
                field_schema = schema_types.FieldSchema()

                field_name = field.get('name')
                if field_name is None:
                    raise ParamError("You should specify the name of field!")
                field_schema.name = field_name

                is_primary_key = field.get('is_primary_key', False)
                if is_primary_key and auto_id:
                    raise ParamError("primary key is not supported when auto_id is True")
                field_schema.is_primary_key = is_primary_key

                field_schema.description = field.get('description', "")

                data_type = field.get('type')
                if data_type is None:
                    raise ParamError("You should specify the data type of field!")
                if not isinstance(data_type, (int, DataType)):
                    raise ParamError("Field type must be of DataType!")
                field_schema.data_type = data_type

                type_params = field.get('params')
                if isinstance(type_params, dict):
                    for tk, tv in type_params.items():
                        if tk == "dim":
                            if not tv or not isinstance(tv, int):
                                raise ParamError("dim must be of int!")
                        kv_pair = common_types.KeyValuePair(key=str(tk), value=str(tv))
                        field_schema.type_params.append(kv_pair)

                index_params = field.get('indexes')
                if isinstance(index_params, list):
                    for index_param in index_params:
                        if not isinstance(index_param, dict):
                            raise ParamError("Every index param must be of dict type!")
                        for ik, iv in index_param.items():
                            if ik == "metric_type":
                                if not isinstance(iv, MetricType) and not isinstance(iv, str):
                                    raise ParamError("metric_type must be of Milvus.MetricType or str!")
                            kv_pair = common_types.KeyValuePair(key=str(ik), value=str(iv))
                            field_schema.index_params.append(kv_pair)
                
                schema.fields.append(field_schema)

        return schema

    @classmethod
    def empty(cls):
        return common_types.Empty()

    @classmethod
    def partition_name(cls, collection_name, partition_tag):
        if not isinstance(collection_name, str):
            raise ParamError("collection_name must be of str type")
        if not isinstance(partition_tag, str):
            raise ParamError("partition_tag must be of str type")
        return service_msg_types.PartitionName(collection_name=collection_name,
                                               tag=partition_tag)

    @classmethod
    def bulk_insert_param(cls, collection_name, entities, partition_tag, ids=None, params=None, fields_info=None, **kwargs):
        row_batch = service_msg_types.RowBatch()
        row_batch.collection_name = collection_name
        default_partition_tag = "_default" # should here?
        row_batch.partition_tag = partition_tag or default_partition_tag

        row_data = list()
        fields_type = list()
        fields_len = len(entities)
        for i in range(fields_len):
            fields_type.append(entities[i]["type"])
        row_num = len(entities[0]["values"]) if fields_len > 0 else 0

        if fields_info is None:
            # this case, we assume the order of entities is same to schema
            for i in range(row_num):
                row = []
                for j in range(fields_len):
                    row.append(entities[j]["values"][i])
                row_data.append(row)
        else:
            # field name & type must match fields info
            location = dict()
            if fields_len != len(fields_info):
                raise ParamError("The length of entities must be equal to the number of fields!")
            for i, field in enumerate(fields_info):
                match_flag = False
                for j in range(fields_len):
                    # if field["name"] == entities[j]["name"] and field["type"] == entities[j]["type"]:
                    if field["name"] == entities[j]["name"]:
                        location[field["name"]] = j
                        fields_type[i] = entities[j]["type"]
                        match_flag = True
                        break
                if not match_flag:
                    raise ParamError("Field {} don't match in entities".format(field["name"]))
            for i in range(row_num):
                row = []
                for j in range(fields_len):
                    field_name = fields_info[j]["name"]
                    loc = location[field_name]
                    row.append(entities[loc]["values"][i])
                row_data.append(row)

        # fill row_data in bytes format
        auto_id = kwargs.get("auto_id", True)
        if not auto_id:
            id_type = DataType.INT64 # int64_t is supported by default
            fields_type.insert(0, id_type)
            for i in range(row_num):
                row_data[i].insert(0, ids[i]) # fill id

        for i in range(row_num):
            blob_row_data = common_types.Blob()
            blob_row_data.value = bytes()
            for field_value, field_type in zip(row_data[i], fields_type):
                if field_type in (DataType.BOOL,):
                    blob_row_data.value += blob.boolToBytes(field_value)
                elif field_type in (DataType.INT8,):
                    blob_row_data.value += blob.int8ToBytes(field_value)
                elif field_type in (DataType.INT16,):
                    blob_row_data.value += blob.int16ToBytes(field_value)
                elif field_type in (DataType.INT32,):
                    blob_row_data.value += blob.int32ToBytes(field_value)
                elif field_type in (DataType.INT64,):
                    blob_row_data.value += blob.int64ToBytes(field_value)
                elif field_type in (DataType.FLOAT,):
                    blob_row_data.value += blob.floatToBytes(field_value)
                elif field_type in (DataType.DOUBLE,):
                    blob_row_data.value += blob.doubleToBytes(field_value)
                elif field_type in (DataType.STRING,):
                    blob_row_data.value += blob.stringToBytes(field_value)
                elif field_type in (DataType.BINARY_VECTOR,):
                    blob_row_data.value += blob.vectorBinaryToBytes(field_value)
                elif field_type in (DataType.FLOAT_VECTOR,):
                    blob_row_data.value += blob.vectorFloatToBytes(field_value)
                else:
                    raise ParamError("Unsupported data type!")
            row_batch.row_data.append(blob_row_data)

        # generate hash keys, TODO: better hash function
        if ids is not None:
            hash_keys = [len(str(e)) for e in ids]
            row_batch.hash_keys.extend(hash_keys)

        return row_batch

    @classmethod
    def insert_param(cls, collection_name, entities, partition_tag, ids=None, params=None, fields_info=None, **kwargs):
        row_batch = service_msg_types.RowBatch()
        row_batch.collection_name = collection_name
        default_partition_tag = "_default" # should here?
        row_batch.partition_tag = partition_tag or default_partition_tag

        row_data = list()
        fields_type = list()
        row_num = len(entities)
        fields_len = len(entities[0]) if row_num > 0 else 0

        if row_num <= 0 or fields_len <= 0:
            return ParamError("insert empty entity is unnecessary")

        if fields_info is None or True:
            # this case, we assume the order of entities is same to schema
            entity = entities[0]
            for _, value in entity.items():
                if isinstance(value, bool):
                    fields_type.append(DataType.BOOL)
                elif isinstance(value, int):
                    fields_type.append(DataType.INT64) # or int32?
                elif isinstance(value, float):
                    fields_type.append(DataType.FLOAT) # or double?
                elif isinstance(value, str):
                    fields_type.append(DataType.STRING)
                elif isinstance(value, list):
                    if len(value) <= 0:
                        raise ParamError("the dim of vectors must greater than zero")
                    if isinstance(value, float):
                        fields_type.append(DataType.FLOAT_VECTOR)
                    # TODO: BINARY_FLOAT
                elif isinstance(value, bytes):
                    fields_type.append(DataType.BINARY_VECTOR)
                else:
                    raise ParamError("unsupported data type")
            row_data = [[value for _, value in entity.items()]
                        for entity in entities]
        else:
            # fields_info now doesn't contain type info
            pass

        # fill row_data in bytes format
        auto_id = kwargs.get("auto_id", True)
        if not auto_id:
            id_type = DataType.INT64 # int64_t is supported by default
            fields_type.insert(0, id_type)
            for i in range(row_num):
                row_data[i].insert(0, ids[i]) # fill id

        for i in range(row_num):
            blob_row_data = common_types.Blob()
            blob_row_data.value = bytes()
            for field_value, field_type in zip(row_data[i], fields_type):
                if field_type in (DataType.BOOL,):
                    blob_row_data.value += blob.boolToBytes(field_value)
                elif field_type in (DataType.INT8,):
                    blob_row_data.value += blob.int8ToBytes(field_value)
                elif field_type in (DataType.INT16,):
                    blob_row_data.value += blob.int16ToBytes(field_value)
                elif field_type in (DataType.INT32,):
                    blob_row_data.value += blob.int32ToBytes(field_value)
                elif field_type in (DataType.INT64,):
                    blob_row_data.value += blob.int64ToBytes(field_value)
                elif field_type in (DataType.FLOAT,):
                    blob_row_data.value += blob.floatToBytes(field_value)
                elif field_type in (DataType.DOUBLE,):
                    blob_row_data.value += blob.doubleToBytes(field_value)
                elif field_type in (DataType.STRING,):
                    blob_row_data.value += blob.stringToBytes(field_value)
                elif field_type in (DataType.BINARY_VECTOR,):
                    blob_row_data.value += blob.vectorBinaryToBytes(field_value)
                elif field_type in (DataType.FLOAT_VECTOR,):
                    blob_row_data.value += blob.vectorFloatToBytes(field_value)
                else:
                    raise ParamError("Unsupported data type!")
            row_batch.row_data.append(blob_row_data)

        # generate hash keys, TODO: better hash function
        if ids is not None:
            hash_keys = [len(str(e)) for e in ids]
            row_batch.hash_keys.extend(hash_keys)

        return row_batch

    @classmethod
    def search_param(cls, collection_name, query_entities, partition_tags=None, fields=None, **kwargs):
        if not isinstance(query_entities, (dict,)):
            raise ParamError("Invalid query format. 'query_entities' must be a dict")

        query = service_msg_types.Query(
            collection_name=collection_name,
            partition_tags=partition_tags or "",
        )

        duplicated_entities = copy.deepcopy(query_entities)
        vector_placeholders = dict()

        def extract_vectors_param(param, placeholders):
            if not isinstance(param, (dict, list)):
                return

            if isinstance(param, dict):
                if "vector" in param:
                    # TODO: Here may not replace ph
                    ph = "$" + str(len(placeholders))

                    for pk, pv in param["vector"].items():
                        if "query" not in pv:
                            raise ParamError("param vector must contain 'query'")
                        placeholders[ph] = pv["query"]
                        param["vector"][pk]["query"] = ph

                    return
                else:
                    for _, v in param.items():
                        extract_vectors_param(v, placeholders)

            if isinstance(param, list):
                for item in param:
                    extract_vectors_param(item, placeholders)
        
        extract_vectors_param(duplicated_entities, vector_placeholders)
        query.dsl = ujson.dumps(duplicated_entities)

        plg = service_msg_types.PlaceholderGroup()
        for tag, vectors in vector_placeholders.items():
            if len(vectors) <= 0:
                continue
            pl = service_msg_types.PlaceholderValue(tag=tag)

            if isinstance(vectors[0], bytes):
                pl.type = service_msg_types.PlaceholderType.VECTOR_BINARY
                for vector in vectors:
                    pl.values.append(blob.vectorBinaryToBytes(vector))
            else:
                pl.type = service_msg_types.PlaceholderType.VECTOR_FLOAT
                for vector in vectors:
                    pl.values.append(blob.vectorFloatToBytes(vector))
            # vector_values_bytes = service_msg_types.VectorValues.SerializeToString(vector_values)

            plg.placeholders.append(pl)
        plg_str = service_msg_types.PlaceholderGroup.SerializeToString(plg)
        query.placeholder_group = plg_str

        return query
