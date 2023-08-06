#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : mimongo
# @Time         : 2020-03-20 11:26
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
# https://www.jb51.net/article/159652.htm
# https://www.cnblogs.com/kaituorensheng/p/5181410.html

import pymongo
from pymongo import MongoClient

from tqdm.auto import tqdm
from ..utils import isMac


class Mongo(object):
    """插入速度200维向量 20w/min
    tag2vec = m.db.word2vec.tag2vec
    tag2vec.delete_many({})
    tag2vec.count_documents({})
    docs = get_docs(dff.w, dff.v)
    tag2vec.insert_many(docs, False)
    tag2vec.find_one()
    tag2vec.count_documents({})

    # https://www.cnblogs.com/wangyuxing/p/9879504.html
    news_word2vec.find_one({'id': 0}, projection={'v': 0}) # 指定返回键值
    tag2vec.find({'w': {'$in': ['娱乐', '体育']}}) # $in $nin

    l = [{'w': 1, 'v': 2}, {'w': 3, 'v': 4}]
    dic = dict([i.values() for i in l])
    [{'w': k, 'v': v} for k, v in dic.items()]

    """

    def __init__(self, db='mig3_algo_push', print_info=False):
        """
        10.162.39.41:28026
        mig3_algo_push
        :param db:
        :param print_info:
        """
        database = 'mig3_algo_push'
        user = 'mig3_algo_push_wr'
        passwd = 'zxBy84SkD3G4ce9424S4IB5HzYZ29uGX'
        iplist = '10.162.39.41:28026,10.162.52.42:28026,10.132.57.49:28026'
        replicaSet = 'mig_algo_push'

        url = "mongodb://localhost:27017" if isMac else f"mongodb://{user}:{passwd}@{iplist}/{database}?replicaSet={replicaSet}&authSource=admin"
        self.client = MongoClient(url)
        self.db = self.client[db]
        self.collection_names = self.db.collection_names()

        # Info
        if print_info:
            print({
                "主节点": self.client.is_primary,
                "最大连接数": self.client.max_pool_size
            })
            print(self.client.admin.command('ismaster'))

    def insert(self, collection: pymongo.collection.Collection, docs):
        if isinstance(docs, dict):
            docs = [docs]
        print("插入前documents:", collection.count_documents({}))
        collection.insert_many(docs, False)
        print("插入后documents:", collection.count_documents({}))

    def get_docs(self, keys, values):
        return [{'id': i, 'w': k, 'v': v} for i, (k, v) in tqdm(enumerate(zip(keys, values)))]

    def drop_collection(self, name_or_collection):
        self.db.drop_collection(name_or_collection)

    def __starter(self):
        """
        # info
        collection.count_documents({})

        # 增
        collection.insert_one({'x': 1})
        collection.insert_one({'xx': 2})
        ids = collection.insert_many([{'xxx': 3}, {'xxx': 4}])

        from bson.objectid import ObjectId

        collection.find_one({'x': 1})
        collection.find_one({'_id': ObjectId('5e743cea06be472ac7298def')})

        # 复杂的查询
        list(collection.find({})) # collection.find().count()
        list(collection.find({'xx': {'$gt': 1}}))

        condition = {'s': 1}
        # update_one update_many
        # result = collection.replace_one(condition, {'s': 1, 'ss': 2}) # 完全替换 # upsert=True强拆
        result = collection.replace_one(condition, {'$set': {'s':1, 'sss': 3}}) # {**d1, **d2}
        """
        pass
