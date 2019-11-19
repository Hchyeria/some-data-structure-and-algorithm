# -*- coding:utf-8 -*-
"""
    Union find set: check the network
    Question 2
    Author: Hchyeria
"""

import random
import re
import sys
sys.path.append('../1')
from SplayTree import SplayTree
from SplayTree import TreeNode


# 生成测试文件代码
def write_test(n=0, count=5):
    with open('test1.txt', 'w') as f:
        while count:
            num = n or random.randint(1, 10000)
            f.write(str(num) + '\n')
            while num:
                one = random.choice('CI')
                two = random.randint(1, num)
                three = random.randint(1, num)
                if not num == 1:
                    while three == two:
                        three = random.randint(1, num)
                list_write = [one, two, three]
                for var in list_write:
                    f.write(str(var))
                    f.write(' ')
                f.write('\n')
                num -= 1
            f.write('S')
            f.write('\n')
            count -= 1
        f.write('0')
        f.write('\n')
        f.close()


# write_test(1)

# 读入测试文件 进行处理输出
# 此算法时间复杂度为 O(I * N) I为数据以 I 开头出现的次数 N为数据量
# 空间复杂度为 O(N)
def read_test():
    # 读入测试文件
    with open('test2.txt', 'r') as f:
        # 按行分割
        test_data = f.read().split('\n')
        for line in test_data:
            # 如果第一个字符是数字
            if line.isdigit():
                n = int(line)
                # 是 0 则结束
                if not n:
                    break
                # 建立 n 长度的 data 数组用来保存集合信息
                # 这里用到了第一题 的伸展树来表示集合
                data = list(map(lambda x: SplayTree(TreeNode(x)), range(n + 1)))
                data[0] = None
            else:
                # 如果 遇到 S 则表示一组数据结束
                if line == 'S':
                    # 过滤到不重要的第一个 和重复的元素
                    data = list(set(data))[1:]
                    # 如果只剩一棵树了 说明所有节点都可以连通
                    if len(data) == 1:
                        print('The network is connected.\n')
                    else:
                        # 否则 输出集合的个数
                        print('There are %d components.\n' % len(data))
                else:
                    # 数组以空格分隔
                    temp_list = list(line.strip().split(' '))

                    one, two, three = temp_list
                    two, three = int(two), int(three)
                    # 如果以 I 开头
                    if one == 'I':
                        # 如果两个节点不是属于同一个树 说明它们没有联通
                        if not data[two] == data[three]:
                            # 合并两个树 然后更新相应节点属于的集合
                            if data[two]:
                                temp = data[two].merge(data[three])
                                data = list(map(lambda x: temp if x == data[three] else x, data))

                            else:
                                temp = data[three].merge(data[two])
                                data = list(map(lambda x: temp if x == data[two] else x, data))
                    else:
                        # 如果遇到 C
                        # 判断两个节点是不是属于同一个树 不是输出 no 是输出 yes
                        if data[two]:
                            if data[two] == data[three]:
                                print('yes')
                            else:
                                print('no')
                        else:
                            if data[two] == data[three]:
                                print('yes')
                            else:
                                print('no')

        return


read_test()
