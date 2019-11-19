# -*- coding:utf-8 -*-
"""
    Dynamic Programming: Shopping
    Question 6
    Author: Hchyeria
"""
from functools import reduce
import numpy as np

# 定义链表的节点类
class Entry:
    def __init__(self, name, total):
        self.name = name
        self.total = total
        self.next = None

    def __repr__(self):
        return repr((self.name, self.total))


class Shopping:
    def __init__(self):
        # 储存所有商品的信息 用 hash表来进行商品名与下标的转换
        self.goods = {}
        # 储存所有商品的价格
        self.prices = []
        # 储存客户购买的商品的信息
        self.purchase = []
        # 储存优惠券的信息
        # 每个元素是一个链表 链表头的元素 代表该优惠方案的总价钱
        self.coupon = []
        # 储存优惠券涉及到的商品
        self.coupon_goods = []

    # 添加商品信息
    def add_good(self, goods):
        self.prices.append(goods[1])
        self.goods[goods[0]] = len(self.prices) - 1

    # 添加客户购买商品的信息
    def add_purchase(self, goods):
        self.purchase.append((self.goods[goods[0]], goods[1]))

    # 添加优惠券的信息
    def add_coupon(self, coupon, total):
        temp = list(map(lambda x: Entry(self.goods[x[0]], x[1]), coupon))
        # 链表头 储存该优惠方案的总价
        first = Entry(-1, total)
        first.next = temp[0]
        for i in range(len(temp)):
            item = temp[i]
            # 添加优惠券信息的同时 计算出优惠方案涉及到的商品信息
            # 如果没有在数组里面则添加上去
            if item.name not in self.coupon_goods:
                self.coupon_goods.append(item.name)
            # 最后一个商品的 next 为 None
            if i != (len(temp) - 1):
                item.next = temp[i+1]

        self.coupon.append(first)

    # 重置优惠方案 和 接下来客户购买的信息
    def reset(self):
        self.purchase = []
        self.coupon = []
        self.coupon_goods = []

    # 计算不用优惠券 商品本该付的价钱
    def calculate_price(self, array):
        return reduce(lambda aac, val: aac + (self.prices[val[0]] * val[1]), array, 0)

    # 获取商品的价格
    def get_price(self, index):
        return self.prices[self.coupon_goods[index]] if self.coupon_goods[index] >= 0 else 0

    def find_minimum_cost(self):
        # 初始化 动态规划 的数组
        dp = [[[[[[0 for i in range(10)] for i in range(10)] for i in range(10)] for i in range(10)] for i in range(10)] for i in range(10)]
        # 没在优惠券涉及商品里的商品 直接计算本来该付的价钱
        vanilla = self.calculate_price(filter(lambda x: x[0] not in self.coupon_goods, self.purchase))
        # 需要计算何种优惠便宜的商品
        discount = filter(lambda x: x[0] in self.coupon_goods, self.purchase)
        # 如果优惠涉及的商品种类小于 6 用 -1 填满
        while len(self.coupon_goods) < 6:
            self.coupon_goods.append(-1)
        # 客户最多有 6 件商品
        dis_goods = [0] * 6
        # 初始化每种商品需要的数量
        for x, y in discount:
            dis_goods[self.coupon_goods.index(x)] = y
        # 每种商品需要的数量
        need1, need2, need3, need4, need5, need6 = dis_goods
        # 嵌套循环
        for i in range(need1+1):
            for j in range(need2+1):
                for k in range(need3+1):
                    for n in range(need4+1):
                        for m in range(need5+1):
                            for h in range(need6+1):
                                # 假设最小的价钱就是 商品数量乘以价钱的和
                                min_price = i*self.get_price(0) + j*self.get_price(1)\
                                            + k*self.get_price(2) + n*self.get_price(3)\
                                            + m*self.get_price(4) + h*self.get_price(5)
                                # 循环试试每种优惠方案
                                for v in self.coupon:
                                    total = v.total
                                    first = v.next
                                    elements = [0] * 6
                                    # 初始化该优惠方案需要的每种商品的数量
                                    while first:
                                        elements[self.coupon_goods.index(first.name)] = first.total
                                        first = first.next
                                    k1, k2, k3, k4, k5, k6 = elements
                                    # 如果购买的数量达到可以使用该优惠方案的要求
                                    if i >= k1 and j >= k2 and k >= k3 and n >= k4 and m >= k5 and h >= k6:
                                        # 动态规划 比较出最小的 不用优惠和用了优化哪个钱少
                                        min_price = min(dp[i-k1][j-k2][k-k3][n-k4][m-k5][h-k6] + total, min_price)
                                # 更新信息
                                dp[i][j][k][n][m][h] = min_price
        return dp[need1][need2][need3][need4][need5][need6] + vanilla
