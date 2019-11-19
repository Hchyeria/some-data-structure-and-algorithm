# -*- coding:utf-8 -*-
"""
    The love story of mysterious country
    Question 8
    Author: Hchyeria
"""
import queue
from collections import deque

import math

# 定义节点类
# 节点有 入栈 in_stack 和出栈 out_stack 的时间信息
# next 数组 记录邻接节点
# val 记录村落编号
class Node:
    def __init__(self, val):
        self.in_stack = 0
        self.out_stack = 0
        self.next = []
        self.val = val

    def __repr__(self):
        return repr((self.val, self.in_stack, self.out_stack))


# 定义一个图类
# 村落之间任意两个都有一条路可以连通
# 实际上就是一颗树 特殊的图
class Graph:
    def __init__(self, n):
        self.root = Node
        # 储存所有节点信息
        self.node = [None for i in range(n)]

        # 储存深度信息
        # 便于能够过滤一些邻接节点
        self.deep = [0] * n

    # 添加节点的函数
    def add(self, u: int, v: int):
        # 如果不存在 则创建一个
        if not self.node[u]:
            self.node[u] = Node(u)
        if not self.node[v]:
            self.node[v] = Node(v)
        # 添加相应节点的邻接节点
        if self.node[v] not in self.node[u].next:
            self.node[u].next.append(self.node[v])
        if self.node[u] not in self.node[v].next:
            self.node[v].next.append(self.node[u])

    # 广度优先设置深度信息
    def bfs(self):
        # 利用队列的先进先出的特点 方便实现广度优先遍历
        q = queue.Queue()
        # 起点深度为 1
        self.deep[self.node[0].val] = 1
        q.put(0)
        while not q.empty():
            ptr = q.get()
            front = self.node[ptr]
            first = self.node[ptr].next
            # 将还没有深度值的子节点的深度值更新
            for item in first:
                if not self.deep[item.val]:
                    self.deep[item.val] = self.deep[front.val] + 1
                    q.put(item.val)

    # 设置 出入栈 的时间
    def set_stack_time(self):
        # 利用 deque 实现
        my_stack = deque()
        set_stack_time(0, my_stack, 1, self.deep, self.node)

    # 判断 c 是否在 a b 路径上
    def judge_same(self, a, b, c):
        # 如果等于其中一个 返回 True
        if c == a or c == b:
            return True
        # 取出 a b c 的入栈出栈时间值
        a_in = self.node[a].in_stack
        a_out = self.node[a].out_stack
        b_in = self.node[b].in_stack
        b_out = self.node[b].out_stack
        c_in = self.node[c].in_stack
        c_out = self.node[c].out_stack
        c_deep = self.deep[self.node[c].val]
        # 保证 a 始终在左边
        if a_in > b_in:
            b_out, a_out = a_out, b_out
            b_in, a_in = a_in, b_in
        # 考虑边缘情况 如果 a b 紧邻 那么 c 肯定不在 ab 路径上 返回 False
        if a_in == b_in - 1:
            return False
        # 如果  c 是 a 的祖先节点 并且不是 b 的祖先节点 返回 True
        if c_in < a_in and c_out < b_in:
            return True
        # 如果  c 是 b 的祖先节点 并且不是 a 的祖先节点 返回 True
        if c_in > a_out and c_out > b_out:
            return True
        # 如果 c 是 a b 的共同祖先节点
        # 那么 c 必须是最近的共同祖先节点 才能返回 True
        # 我们只需证明 c 的子节点里面 没有 ab 的共同祖先节点 即可
        elif c_in < a_in and c_out > b_out:
            # 过滤掉深度值不够的节点 即不是 c 的子节点的节点
            array = list(filter(
                lambda x: self.deep[x.val] > c_deep,
                self.node[c].next
            ))
            # 因为子节点入栈出栈时间区间也是呈递增的 可以使用二分查找
            return True if binary_search(a_in, b_out, array) else False
        # 考虑边缘情况 当 b 是 a 的祖先的时候 即 a b c 呈一条直线
        elif c_in > a_in and c_in < b_in:
            return True
        else:
            return False


# 递归调用 深度优先 返回 count 值为下一个节点所用
# count 是用来递增的记录节点的出栈和入栈值
def set_stack_time(index, my_stack, count, deep, node_array):
    # 获取当前节点 如果是空直接返回 count
    node = node_array[index]
    if not node:
        return count
    # 更新当前节点的入栈值 并且 count + 1
    node.in_stack = count
    count += 1
    # 压入栈中
    my_stack.append(node)
    front = node.next
    parent_deep = deep[node.val]
    # 循环取出邻接节点
    for item in front:
        # 当邻接节点的深度值更大才进行递归
        if deep[item.val] > parent_deep:
            # 递归调用 邻接节点
            count = set_stack_time(item.val, my_stack, count, deep, node_array)
    # 出栈
    temp = my_stack.pop()
    # 更新出栈时间值 并且 count + 1
    temp.out_stack = count
    count += 1
    # 返回 count 值
    return count


# 二分查找 每次搜索范围减半
def binary_search(a_in, b_out, array):
    left = 0
    right = len(array) - 1
    mid = left + ((right - left) // 2)
    while left <= right:
        mid_node = array[mid]
        m_in = mid_node.in_stack
        m_out = mid_node.out_stack
        # 如果存在 ab的共同祖先节点 返回 False
        if m_in < a_in and m_out > b_out:
            return False
        elif m_out < a_in:
            left = mid + 1
        else:
            right = mid - 1
    # 没有找到 返回 True
    return True
