# -*- coding:utf-8 -*-
"""
    Divide and Conquer: find the minimum circle
    Question 5
    Author: Hchyeria
"""
import math


# 定义点的类
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # 获取两点之间距离的函数
    def get_distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def __repr__(self):
        return repr((self.x, self.y))


# 根据 x y 来进行排序
def sort_by_type(array, type_name):
    return sorted(array, key=lambda x: x.__getattribute__(type_name))


class MinimumCircle:
    def __init__(self):
        # 储存所有点的信息
        self.point = []

    # 添加点的函数
    def add(self, p):
        self.point.append(p)

    # 找出需要的套圈的最小半径的函数
    def find_minimum(self):
        # 预先以 x 和 y 排序好
        x_array = sort_by_type(self.point, 'x')
        y_array = sort_by_type(self.point, 'x')
        return find_minimum(x_array, y_array)


def find_minimum(x_array, y_array):
    length = len(x_array)
    # 考虑 长度为 1 或 2 的边缘情况
    if length == 1:
        return float('inf')
    elif length == 2:
        return x_array[0].get_distance(x_array[1])
    else:
        # 取以 x 排序的数组的中点划分为 左右两个子集
        mid = len(x_array) >> 1
        left_array = []
        right_array = []
        left_part = x_array[:mid]
        right_part = x_array[mid:]
        # 递归寻找 左右两子集的最小环值
        left = find_minimum(left_part, y_array)
        right = find_minimum(right_part, y_array)
        d = min(left, right)
        # 扫描一遍 让 左右两个子集以 y 排好序
        for item in y_array:
            if item in left_part:
                left_array.append(item)
            else:
                right_array.append(item)
        min_dis = d
        # 寻找中间处可能存在的最小值
        for i in left_array:
            for j in right_part:
                # 如果 x 或 y 之差已经大于 d 了 那么不必继续找了
                # 减少计算 最多有5次比较
                if abs(i.y - j.y) >= d or abs(i.x - j.x) >= d:
                    break
                # 否则计算取最小的
                min_dis = min(min_dis, i.get_distance(j))
        return min_dis