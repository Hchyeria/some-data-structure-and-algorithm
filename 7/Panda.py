# -*- coding:utf-8 -*-
"""
    Nimaya: union find set
    Question 7
    Author: Hchyeria
"""
import sys
sys.path.append('../4')
from Kruskal import DisjointSet


# 定义表示每台计算机类
class Entry:
    def __init__(self, m, n, val):
        self.m = m
        self.n = n
        self.val = val
        self.next = None

    def __repr__(self):
        return repr((self.m, self.n, self.val))


class Nimaya:
    def __init__(self, m, n):
        # 使用矩阵存储图
        self.graph = [[0 for clo in range(n)] for row in range(m)]
        # 图的行数和列数
        self.m = m
        self.n = n
        # 引用第四题写好的 并查集 类
        self.union_find_set = DisjointSet(m * n)
        # 病毒最多的天数感染全部
        self.max_day = -99999
        # 储存病毒信息
        self.virus = []

    # 添加函数
    def add(self, m, n, val):
        self.graph[m][n] = val
        # 如果是病毒 添加到数组
        if val > 0:
            for i in range(len(self.virus)):
                if val == self.virus[i].val:
                    root1 = self.union_find_set.find_root(self.virus[i].m * self.n +self.virus[i]. n)
                    root2 = self.union_find_set.find_root(m * self.n + n)
                    self.union_find_set.union(root1, root2)
                    return
            self.virus.append(Entry(m, n, val))
        else:
            # 根据计算机的防御级别 找出最大的防御级别即是最多需要的天数
            self.max_day = max(self.max_day, abs(val))

    # 获取某一台电脑或者病毒 附近没有被病毒感染的函数
    def get_adjacent(self, m, n):
        # 注意四边的边界情况即可
        res = []
        if m != 0:
            if not self.is_virused(m - 1, n):
                res.append((m - 1, n))
        if n != 0:
            if not self.is_virused(m, n - 1):
                res.append((m, n - 1))
        if m != (self.m - 1):
            if not self.is_virused(m + 1, n):
                res.append((m + 1, n))
        if n != self.n - 1:
            if not self.is_virused(m, n + 1):
                res.append((m, n + 1))
        return res

    # 分组 防御级别相同的为一组 并为这个组选择一个虚拟根节点
    def group(self, m, n, visited):
        # 递归结束条件 所有的节点都已经访问过
        if 0 not in visited:
            return
        visited[m * self.n + n] = 1
        adjacent = self.get_adjacent(m, n)
        root1 = self.union_find_set.find_root(m * self.n + n)
        # 循环附近的节点
        for item in adjacent:
            x, y = item
            root2 = self.union_find_set.find_root(x * self.n + y)
            # 如果虚拟根节点不相等
            if root1 != root2:
                # 如果防御能力相同并且 是电脑 则合并
                if self.graph[x][y] == self.graph[m][n] and self.graph[m][m] < 0:
                    self.union_find_set.union(root1, root2)
            # 如果节点没有被访问过 递归该节点
            if not visited[x * self.n + y]:
                self.group(x, y, visited)

    # 判断是否被病毒感染的函数
    # 比较该节点的虚拟根节点是否指向其中一种病毒即可
    def is_virused(self, m, n):
        root2 = self.union_find_set.find_root(m * self.n + n)
        for virus in self.virus:
            root1 = self.union_find_set.find_root(virus.m * self.n + virus.n)
            if root1 == root2:
                return True
        return False

    # 感染函数
    def infect(self):
        # 按照病毒的种类排序 小的先开始感染
        temp = sorted(self.virus, key=lambda x: x.val)
        self.virus = temp
        # 从第一天开始 最多不超过 最大防御级别的天数
        for day in range(1, self.max_day+1):
            for virus in self.virus:
                ptr = virus
                val = virus.val
                # 找出该病毒感染过的所有节点
                temp = list(
                    filter(
                        lambda item: self.union_find_set.find_root(item[0]) == (virus.m * self.n + virus.n),
                        enumerate(self.union_find_set.disjoint_set)
                    ))
                # 挨个开始感染
                for index, p in temp:
                    t_n = index % self.n
                    t_m = (index - t_n)//self.n
                    root1 = self.union_find_set.find_root(t_m * self.n + t_n)
                    adjacent = self.get_adjacent(t_m, t_n)
                    for item in adjacent:
                        x, y = item
                        root2 = self.union_find_set.find_root(x * self.n + y)
                        # 如果还没有被感染
                        if not self.is_virused(x, y):
                            # 并且防御级别小于天数 则该电脑可以被感染
                            if abs(self.graph[x][y]) <= day:
                                self.union_find_set.force_union(root1, root2)
                                self.graph[x][y] = val
                                # 加入到感染数组
                                temp.append((x * self.n + y, val))

    # 获取指定哪种病毒种类的个数
    def get_virus_res(self, type_name):
        # 自需要找出 并查集里面根节点指向该病毒的节点 即可
        for virus in self.virus:
            val = virus.val
            if val == type_name:
                x, y = virus.m, virus.n
                break
        temp = list(
            filter(
                lambda item: self.union_find_set.find_root(item[0]) == (x*self.n + y),
                enumerate(self.union_find_set.disjoint_set)
            ))
        # 返回长度
        return len(temp)

