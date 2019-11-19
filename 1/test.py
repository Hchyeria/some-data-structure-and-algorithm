from BinarySearchTree import BinarySearchTree
from AVLTree import AVLTree
from SplayTree import SplayTree

import random
import time
from functools import wraps
import sys
sys.setrecursionlimit(10000)


# 计算时间的装饰器
def fn_timer(times):
    def decorator(func):
        @wraps(func)
        def function_timer(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            t1 = time.time()
            print("Time running %s: %.2f ms %d" %
                  (args[-1], (t1 - t0) * 1000, times)
                  )
            return result
        return function_timer
    return decorator


b_tree = BinarySearchTree()
a_tree = AVLTree()
s_tree = SplayTree()

repeat_count = 1


@fn_timer(repeat_count)
def repeat_fuc(fuc, number, timess,  **kwargs):
    for i in range(timess):
        fuc(number)


@fn_timer(repeat_count)
def time_all(nums, tree, type, *args):
    for num in nums:
        tree.__getattribute__(type)(num)


def test(tree):
    for num in nums:
        repeat_fuc(tree.insert, num, repeat_count, name='Insert')

    for num in nums:
        repeat_fuc(tree.delete, num, repeat_count, name='Delete')

    for num in nums:
        repeat_fuc(tree.insert, num, repeat_count, name='Insert')

    for num in list(reversed(nums)):
        repeat_fuc(tree.delete, num, repeat_count, name='Delete')

    for num in shuffle_nums:
        repeat_fuc(tree.insert, num, repeat_count, name='Insert')

    for num in shuffle_nums:
        repeat_fuc(tree.delete, num, repeat_count, name='Delete')


def get_time(count=6):
    for i in range(count):
        n = (1000 + 500 * i)
        nums = list(range(n))
        reverse_num = reversed(nums)
        print(n)
        print('asc insert asc delete')
        time_all(nums, b_tree, 'insert', 'b_tree insert ' + str(n))
        time_all(nums, b_tree, 'delete', 'b_tree delete ' + str(n))
        time_all(nums, a_tree, 'insert', 'a_tree insert ' + str(n))
        time_all(nums, a_tree, 'delete', 'a_tree delete ' + str(n))
        time_all(nums, s_tree, 'insert', 's_tree insert ' + str(n))
        time_all(nums, s_tree, 'delete', 's_tree delete ' + str(n))
        print('asc insert desc delete')
        time_all(nums, b_tree, 'insert', 'b_tree insert ' + str(n))
        time_all(reverse_num, b_tree, 'delete', 'b_tree delete ' + str(n))
        time_all(nums, a_tree, 'insert', 'a_tree insert ' + str(n))
        time_all(reverse_num, a_tree, 'delete', 'a_tree delete ' + str(n))
        time_all(nums, s_tree, 'insert', 's_tree insert ' + str(n))
        time_all(reverse_num, s_tree, 'delete', 's_tree delete ' + str(n))
        print('random insert random delete')
        time_all(sorted(nums, key=lambda k: random.random()), b_tree, 'insert', 'b_tree insert ' + str(n))
        time_all(sorted(nums, key=lambda k: random.random()), b_tree, 'delete', 'b_tree delete ' + str(n))
        time_all(sorted(nums, key=lambda k: random.random()), a_tree, 'insert', 'a_tree insert ' + str(n))
        time_all(sorted(nums, key=lambda k: random.random()), a_tree, 'delete', 'a_tree delete ' + str(n))
        time_all(sorted(nums, key=lambda k: random.random()), s_tree, 'insert', 's_tree insert ' + str(n))
        time_all(sorted(nums, key=lambda k: random.random()), s_tree, 'delete', 's_tree delete ' + str(n))


get_time(6)