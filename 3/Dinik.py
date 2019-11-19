# -*- coding:utf-8 -*-
"""
    Network flows: the universal tour
    Question 3
    Author: Hchyeria
"""
import queue


# 定义图的边的类
class Edge:
    def __init__(self, u: int, v: int, w: int):
        self.u = u
        self.v = v
        self.w = w


# 运用 Dinik 网络流算法解决
# 比起传统的 Ff 算法 Dinik 算法能够利用 图的deep的概念 选择增广路径的时候只能选择 deep 递增的一条
# 优化了寻找增广路径的算法
# 该算法理论时间复杂度可以达到 O(n*2)
# 但本题经过了一些性能优化 实际上运行的效果不错 速度也快
# 具体优化的细节:
# 1：当前弧优化; 对于一些已经找过的节点 它的前面几条路径已经访问过了 那么我们再次访问到这个节点
#     的时候可以从没有访问过的路径开始 减少每次循环的次数
# 2: 多路增广优化; 利用递归 将相对节点的所有路径的流相加之后 再让该节点的流减去相加后的流 避免一条一条的减 浪费时间
# 3: 炸点优化; 当这个节点可流的流量已经为 0 了 直接让其对应 deep 变为 -2 让广度优先寻找增广路径的时候不可能再访问到它
#     相当于把这个节点隔绝掉一样
class Dinik:
    def __init__(self, s: int, t: int, n: int):
        # 起点
        self.s = s
        # 终点
        self.t = t
        # 节点总数
        self.n = n
        # 最大流
        self.max_flow = 0
        # 存储边数据
        self.edge_array = []
        # 图的信息 用 graph[u][v] 可以访问到对应边的数组下标 edge_array[graph[u][v]]
        # graph[u][v] ^ 1  可以访问到对应边的临边的数组下标edge_array[graph[u][v] ^ 1]
        self.graph = [[]]*n
        # 储存深度信息
        self.deep = []

    # 添加节点的函数
    def add(self, u: int, v: int, w: int):
        # edge_array存储所有边的信息 临边的权重为0
        # 边必须以偶数开始 临边存储在相邻位置 才能用 异或1 取到临边信息
        self.edge_array.append(Edge(u, v, w))
        self.edge_array.append(Edge(v, u, 0))
        size = len(self.edge_array)
        # grapg保存下标信息
        if self.graph[u]:
            self.graph[u].append(size-2)
        else:
            self.graph[u] = [size - 2]

        if self.graph[v]:
            self.graph[v].append(size - 1)
        else:
            self.graph[v] = [size - 1]

    # 广度优先遍历图 更新 deep 信息
    # 并返回能否找到增广路径
    # 也就是有没有路到从起点到终点
    def bfs(self):
        # 每次都需要重新设置 deep
        self.deep = [0] * self.n
        # 利用队列的先进先出的特点 方便实现广度优先遍历
        q = queue.Queue()
        # 起点深度为 1
        self.deep[self.s] = 1
        q.put(self.s)
        while not q.empty():
            ptr = q.get()
            size = len(self.graph[ptr])
            for i in range(size):
                edg = self.edge_array[self.graph[ptr][i]]
                if not self.deep[edg.v] and edg.w > 0:
                    # 将相邻的节点深度加1
                    self.deep[edg.v] = self.deep[edg.u] + 1
                    q.put(edg.v)
        # 返回能否找到增广路径
        return self.deep[self.t] > 0

    # Dinik 算法核心
    # min_flow 代表当前路径的最小容量
    def dfs(self, x, min_flow, cur):
        # 如果找到终点 或者 当前最小流量已经为 0 了 直接返回 min_flow
        if x == self.t or min_flow == 0:
            return min_flow
        # 保存流量值
        fl = 0
        # 遍历节点分支的路径
        for i in range(cur[x], len(self.graph[x])):
            # 当前弧优化 记录下次从没有访问过的开始遍历
            cur[x] = i
            if not min_flow:
                break
            edg = self.edge_array[self.graph[x][i]]
            # Dinik 算法 路径必须是深度递增的
            if self.deep[edg.v] == self.deep[edg.u] + 1 and edg.w:
                # 多路增广优化
                child_flow = self.dfs(edg.v, min(min_flow, edg.w), cur)
                # 当前边权重- 反边+
                self.edge_array[self.graph[x][i]].w -= child_flow
                self.edge_array[self.graph[x][i] ^ 1].w += child_flow
                min_flow -= child_flow
                fl += child_flow
        # 炸点优化
        if not fl:
            self.deep[x] = -2
        return fl

    # 找出最大流函数
    def find_max_flow(self):
        res = 0
        # 当还有增广路径 说明还可以增流 继续找
        while self.bfs():
            cur = [0]*len(self.edge_array)
            res += self.dfs(self.s, float("inf"), cur)
        return res


