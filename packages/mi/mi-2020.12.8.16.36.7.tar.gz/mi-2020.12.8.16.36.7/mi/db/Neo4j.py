#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : Neo4j
# @Time         : 2020/9/18 11:26 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from tqdm.auto import tqdm
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

from py2neo import Graph, Node, Relationship


class Neo4j(object):

    def __init__(self, profile="bolt://10.241.141.162:7687", username='neo4j', password='mi'):
        self.graph = Graph(profile, username=username, password=password)
        # self.graph.delete_all()

    def create_nodes(self, df_nodes, label="Demo", max_workers=30):
        """

        :param label: Node Label 可以理解为一个集合
        :param node_list: [(k, v, r), ] 三元组
        :return:
        """
        df_nodes.columns = ['k', 'v', 'r']
        groups = df_nodes.groupby('k')
        print(f"Num Group: {len(groups)}")

        func = lambda group: [self._create_node(label, nodes) for nodes in tqdm(group[1].values)]

        with ThreadPoolExecutor(max_workers, thread_name_prefix=f"{label}__") as pool:
            _ = pool.map(func, tqdm(groups), chunksize=1)

    def _create_node(self, label, nodes):
        k, v, r = nodes

        node_key = self._create(label, k)
        node_value = self._create(label, v)

        if node_key != node_value:
            node_relation = Relationship(node_key, r, node_value)  # r也可以是节点
            self.graph.create(node_relation)

    @lru_cache(1024)
    def _create(self, label, name):
        subgraph = Node(label, name=name)
        self.graph.create(subgraph)
        return subgraph
