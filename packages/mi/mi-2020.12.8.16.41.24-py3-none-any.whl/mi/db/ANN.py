#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2020-02-14 11:52
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
# https://github.com/milvus-io/docs/blob/master/site/en/guides/milvus_operation.md#createdrop-indexes-in-a-collection
# https://github.com/milvus-io/pymilvus/tree/master/examples/indexes
# https://raw.githubusercontent.com/milvus-io/pymilvus/0.7.0/examples/example.py
# TODO:
# m.milvus.preload_table


import numpy as np
from milvus import Milvus

"""
client.count_entities

client.create_collection
client.create_index
client.create_partition

client.get_collection_info
client.get_collection_stats
client.get_config
client.get_entity_by_id

client.list_id_in_segment
client.list_partitions

client.delete_entity_by_id
client.drop_collection
client.drop_index
client.drop_partition

client.load_collection???

"""


class ANN(object):

    def __init__(self, host='10.119.33.90', port='19530'):
        self.client = Milvus(host, port)

        print("Client Version:", self.client.client_version())
        print("Server Version:", self.client.server_version())

        self.collections = self.client.list_collections()

    def create_collection(self, collection_name, fields, partition_tag=None, overwrite=True):
        """

        :param collection_name:
        :param fields:
            collection_param = {
                "fields": [
                    #  Milvus doesn't support string type now, but we are considering supporting it soon.
                    #  {"name": "title", "type": DataType.STRING},
                    {"name": "category_", "type": DataType.INT32},
                    {"name": "vector", "type": DataType.FLOAT_VECTOR, "params": {"dim": 768}},
                ],
                "segment_row_limit": 4096,
                "auto_id": False
            }

        :param overwrite:
        :return:
        """
        if self.client.has_collection(collection_name) and overwrite:
            self.client.drop_collection(collection_name)
            self.client.create_collection(collection_name, fields)
        elif self.client.has_collection(collection_name):
            print(f"{collection_name} already exist !!!")
        else:
            self.client.create_collection(collection_name, fields)

        if partition_tag is not None:
            self.client.create_partition(collection_name, partition_tag=partition_tag)

    def create_index(self, collection_name, field_name, index_type='IVF_FLAT', metric_type='IP', index_params=None):
        """
        MetricType:
            INVALID = 0
            L2 = 1
            IP = 2
            # Only supported for byte vectors
            HAMMING = 3
            JACCARD = 4
            TANIMOTO = 5
            #
            SUBSTRUCTURE = 6
            SUPERSTRUCTURE = 7
        IndexType:
            INVALID = 0
            FLAT = 1
            IVFLAT = 2
            IVF_SQ8 = 3
            RNSG = 4
            IVF_SQ8H = 5
            IVF_PQ = 6
            HNSW = 11
            ANNOY = 12

            # alternative name
            IVF_FLAT = IVFLAT
            IVF_SQ8_H = IVF_SQ8H

        class DataType(IntEnum):
            NULL = 0
            INT8 = 1
            INT16 = 2
            INT32 = 3
            INT64 = 4

            STRING = 20

            BOOL = 30

            FLOAT = 40
            DOUBLE = 41

            VECTOR = 100
            UNKNOWN = 9999

        class RangeType(IntEnum):
            LT = 0   # less than
            LTE = 1  # less than or equal
            EQ = 2   # equal
            GT = 3   # greater than
            GTE = 4  # greater than or equal
            NE = 5   # not equal
        :return:
        """
        if index_params is None:
            index_params = {'nlist': 1024}

        params = {
            'index_type': index_type,
            # 'index_file_size': 1024,
            'params': index_params,

            'metric_type': metric_type,
        }
        self.client.create_index(collection_name, field_name, params) # field_name='embedding'

    def insert(self):

        self.client.flush()
        pass

    def search(self):
        pass

    def drop_collection(self, collection_name):
        if self.client.has_collection(collection_name):
            self.client.drop_collection(collection_name)

    def drop_partition(self, collection_name, partition_tag):
        if self.client.has_partition(collection_name, partition_tag):
            self.client.drop_partition(collection_name, partition_tag, timeout=30)

    def noramlize(self, x):
        if len(x.shape) > 1:
            return x / np.clip(x ** 2, 1e-12, None).sum(axis=1).reshape((-1, 1) + x.shape[2:]) ** 0.5
        else:
            return x / np.clip(x ** 2, 1e-12, None).sum() ** 0.5
