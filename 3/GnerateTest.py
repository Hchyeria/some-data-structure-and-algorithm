import random

import numpy as np


# 随机生成地点名
def generate_name():
    obj_name = ''.join(np.random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), 3))
    return obj_name

# 随机生成起点和终点名称
# exit_place 代表已经存在的边的信息
def generate_place(destination, source, exit_place):
    length = len(exit_place)
    # 当已经生成很多地点之后 为了使生成的图能够连通连通性 应该在已经生成的地点中随机选取 建立连通关系
    # 这里阈值是250
    if length > 250:
        # 从已经生成的地点中随机选取一个地点 作为起点
        one = exit_place[random.randint(0, length-1)][0]
        # 起点不能是 目的终点
        while one == destination:
            one = exit_place[random.randint(0, length-1)][0]
        # 从已经生成的地点中随机选取一个地点 作为终点
        two = exit_place[random.randint(0, length-1)][1]
        # 终点不能是目的起点 也不能等于起点
        while two == source and two == one:
            two = exit_place[random.randint(0, length-1)][1]
    else:
        # 随机概率生成不同的地点名 或者 source 作为起点
        one = generate_name() if random.randint(1, 500) < 400 else source
        # 起点不能是 目的终点
        while one == destination:
            one = generate_name()
        # 随机概率生成不同的地点名 或者 destination 作为终点
        two = generate_name() if random.randint(1, 500) < 400 else destination
        # 终点不能是目的起点 也不能等于起点
        while two == source and two == one:
            two = generate_name()
    # 不能已经存在的组合重复
    while (one, two) in exit_place:
        one, two = generate_place(destination, source, exit_place)
    return one, two


# 生成测试文件代码
def write_test(n=500, count=10):
    with open('test2.txt', 'w') as f:
        while count:
            # 默认 500
            num = n or random.randint(1, 500)
            source = generate_name()
            destination = generate_name()
            # 终点不能等于起点
            while destination == source:
                destination = generate_name()
            temp = [source, destination, str(num)]
            f.write(' '.join(temp) + '\n')
            # exit_place 代表已经存在的边的信息
            # 达到去重的目的
            exit_place = []
            while num:
                one, two = generate_place(destination, source, exit_place)
                exit_place.append((one, two))
                three = random.randint(1, num)
                f.write(' '.join(list(map(str, [one, two, three]))) + '\n')
                num -= 1
            count -= 1
        f.write(' '.join([generate_name(), generate_name(), str(0)]) + '\n')
        f.close()


write_test()