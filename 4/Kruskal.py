# -*- coding:utf-8 -*-
"""
    Minimum spanning tree: set up wires
    Question 4
    Author: Hchyeria
"""


# 定义边的类
class Edge:
    def __init__(self, u: int, v: int, w: int):
        self.u = u
        self.v = v
        self.w = w

    def __repr__(self):
        return repr((self.u, self.v, self.w))


# 并查集算法
class DisjointSet:
    def __init__(self, n: int):
        self.disjoint_set = [-1] * n

    # 找寻该节点的根节点
    def find_root(self, x):
        # 如果值小于 0 返回下标
        # 否则继续寻找 知道小于 0 为止
        if self.disjoint_set[x] < 0:
            return x
        next_x = x
        while self.disjoint_set[next_x] >= 0:
            next_x = self.disjoint_set[next_x]
        return next_x

    # 合并
    def union(self, root1, root2):
        # 如果root2 的集合数目更多
        # 将 root1 指向 root2 即可
        if self.disjoint_set[root2] < self.disjoint_set[root1]:
            self.disjoint_set[root1] = root2
        else:
            # 否则 如果相同 self.disjoint_set[root1] -1
            if self.disjoint_set[root2] == self.disjoint_set[root1]:
                self.disjoint_set[root1] -= 1
            # 将 root2 指向 root2 即可
            self.disjoint_set[root2] = root1

    # 为了第 7 题 新增的方法
    # 熊猫病毒感染合并的时候 不需要比较哪个集合的数目多
    # 之间强制合并 指向病毒 即可
    def force_union(self, root1, root2):
        self.disjoint_set[root2] = root1


# Kruskal 算法寻找最小生成树
class Kruskal:
    def __init__(self):
        # 储存边的信息
        self.edge = []

    # 添加边
    def add(self, u, v, w):
        self.edge.append(Edge(u, v, w))

    # 寻找最小生成树
    def get_minimum_spanning_tree(self):
        new_edge = []
        # 将所有边按照权值从小到大排序
        edge_list = sorted(self.edge, key=lambda x: x.w)
        n = len(edge_list)
        disjoint_set = DisjointSet(n)
        # 最小的权重和
        wt = 0
        # 循环取出
        for i in range(n):
            # 如果已经满足条件 所有节点都加入了 则退出
            if len(new_edge) == n-1:
                break
            temp_edge = edge_list[i]
            root1 = disjoint_set.find_root(temp_edge.u)
            root2 = disjoint_set.find_root(temp_edge.v)
            # 边的两个点 如果不在同一个集合 则合并
            if root1 != root2:
                disjoint_set.union(root1, root2)
                new_edge.append(temp_edge)
                wt += temp_edge.w
        # 返回权重值
        return wt