import math

from Kruskal import Kruskal
import numpy as np
import re


# 定义表示三维位置的节点的类
class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return repr((self.x, self.y, self.z))


# 定义门的类
class Door:
    def __init__(self, one, two, three, four):
        # 门有四个顶点的位置
        self.one = one
        self.two = two
        self.three = three
        self.four = four

    # 获取门的高度
    def get_height(self):
        if self.one.z > 0:
            return self.one.z
        elif self.two.z > 0:
            return self.two.z
        else:
            return self.three.z

    # 获取门在 x 或 y 上的范围
    def get_range(self, type):
        if abs(self.one.__getattribute__(type) - self.two.__getattribute__(type)) > 0:
            return (min(self.one.__getattribute__(type), self.two.__getattribute__(type)),
                    max(self.one.__getattribute__(type), self.two.__getattribute__(type)))
        else:
            return (min(self.one.__getattribute__(type), self.three.__getattribute__(type)),
                    max(self.one.__getattribute__(type), self.three.__getattribute__(type)))


# 定义房间的类
class Room:
    def __init__(self, l, w, h, n):
        self.n = n
        # 储存插座
        self.outlet = []
        # 储存门
        self.door = None
        # 表示插座和门处于哪面墙
        # top 0 bottom 1 left 2 right 3 front 4 rear 5
        self.wall = []
        # 房间的长宽高
        self.l = l
        self.w = w
        self.h = h

    # 根据方位判断处在哪面墙上
    def set_wall(self, obj):
        if isinstance(obj, Door):
            if math.isclose(obj.one.y, 0):
                self.wall.append(5)
            elif math.isclose(obj.one.x, 0):
                self.wall.append(2)
            elif math.isclose(obj.one.x, obj.two.x):
                self.wall.append(3)
            else:
                self.wall.append(4)
        else:
            if math.isclose(obj.x, 0):
                self.wall.append(2)
            elif math.isclose(obj.y, 0):
                self.wall.append(5)
            elif math.isclose(obj.z, 0):
                self.wall.append(1)
            elif math.isclose(obj.y, self.w):
                self.wall.append(4)
            else:
                self.wall.append(3)

    # 添加门
    def set_door(self, door):
        self.door = door
        self.set_wall(door)

    # 添加插座
    def add_outlet(self, outlet):
        self.outlet.append(outlet)
        self.set_wall(outlet)

    # 是否在同一面墙
    def is_together(self, o1: int, o2: int):
        return self.wall[o1] == self.wall[o2]

    # 是否相对
    def is_across(self, o1: int, o2: int):
        # 用到了异或 1 的技巧
        return self.wall[o1] == (self.wall[o2] ^ 1)

    # 是否相邻
    def is_beside(self, o1: int, o2: int):
        return not self.is_together(o1, o2) and not self.is_across(o1, o2)

    # 是否和门在同一墙上
    def is_same_wall_with_door(self, o: int):
        return self.wall[o] == self.wall[self.n]

    # 两个位置的连线 是否穿过了门 已经判定了和门在同一堵墙上才调用
    def is_cross_door(self, o: Position, temp: Position):
        type = 'y'
        if re.match(r'[5|4]', str(self.wall[self.n])):
            type = 'x'
        # 在左右墙上返回 y 上的范围
        # 在前后墙上则返回 x 上的范围
        u, v = self.door.get_range(type)
        # 两个位置都不在地板上
        if not math.isclose(o.z, 0) and not math.isclose(temp.z, 0):
            # 两个位置的高度 其中一个比门高 则肯定不会穿门
            # 否则比较一下范围
            if o.z - self.door.get_height() < 0 and temp.z - self.door.get_height() < 0:
                return True if temp.__getattribute__(type) - u >= 0 and temp.__getattribute__(type) - v <= 0 \
                               and o.__getattribute__(type) - u >= 0 and o.__getattribute__(type) - v <= 0 else False
            return False
        # 如果两个都在地板 那么肯定不会穿门
        elif math.isclose(o.z, 0) and math.isclose(temp.z, 0):
            return False
        else:
            # 其中一个在地板 另一个在四周
            # 如果最高的那个 比门矮 那么肯定不会穿门
            # 否则比较在不在范围里
            if max(o.z, temp.z) - self.door.get_height() < 0:
                return False
            return True if temp.__getattribute__(type) - u >= 0 and temp.__getattribute__(type) - v <= 0 and \
                           o.__getattribute__(type) - u >= 0 and o.__getattribute__(type) - v <= 0 else False

    # 找出在同一面墙上 cost
    def find_cost_together(self, o1: Position, o2: Position, is_same):
        # 假定结果就是 不考虑穿门的情况
        res = abs(o1.x - o2.x) + abs(o1.y - o2.y) + abs(o1.z - o2.z)
        if not is_same:
            return res
        type = 'y'
        # 在左右墙上返回 y 上的范围
        # 在前后墙上则返回 x 上的范围
        if re.match(r'[5|4]', str(self.wall[self.n])):
            type = 'x'
        # 两个位置都不在地板上
        if not math.isclose(o1.z, 0) and not math.isclose(o2.z, 0):
            # 如果穿门了
            # 则 多出来两截 从门上面或者上面  穿过 需要比较谁最小
            if self.is_cross_door(o1, o2):
                return res + 2 * min(self.door.get_height() - max(o1.z, o2.z), min(o1.z, o2.z))
            else:
                return res
        # 如果两个都在地板 那么肯定不会穿门
        elif math.isclose(o1.z, 0) and math.isclose(o2.z, 0):
            return res
        else:
            # 如果穿门了
            # 则 多出来两截 从门左边或者右边  穿过 需要比较谁最小
            if self.is_cross_door(o1, o2):
                u, v = self.door.get_range(type)
                return res + 2 * min(v - max(o1.__getattribute__(type), o2.__getattribute__(type)),
                                     min(o1.__getattribute__(type), o2.__getattribute__(type)) - u)
            else:
                return res

    # 当不在同一面墙上 需要在两个之间的  边界处 假定一个 temp
    # 获取 插座1 到 temp 的距离 加上 插座2 到 temp 的距离 便是答案
    # 此函数是获取 temp 需要在哪个边界上
    def witch_border(self, p1, p2):
        w1 = self.wall[p1]
        w2 = self.wall[p2]
        if re.match(r'[2|4]', str(w1)) and re.match(r'[2|4]', str(w2)):
            return 0, self.w
        if re.match(r'[2|5]', str(w1)) and re.match(r'[2|5]', str(w2)):
            return 0, 0
        if re.match(r'[3|4]', str(w1)) and re.match(r'[3|4]', str(w2)):
            return self.l, self.w
        if re.match(r'[3|5]', str(w1)) and re.match(r'[3|5]', str(w2)):
            return self.l, 0
        if re.match(r'[2|1]', str(w1)) and re.match(r'[2|1]', str(w2)):
            temp = p1.y if math.isclose(p1.z, 0) else p1.z
            return 0, temp
        if re.match(r'[3|1]', str(w1)) and re.match(r'[3|1]', str(w2)):
            temp = p1.y if math.isclose(p1.z, 0) else p1.z
            return self.l, temp
        if re.match(r'[5|4]', str(w1)) and re.match(r'[5|4]', str(w2)):
            temp = p1.x if math.isclose(p1.z, 0) else p1.x
            return temp, 0
        if re.match(r'[1|4]', str(w1)) and  re.match(r'[1|4]', str(w2)):
            temp = p1.x if math.isclose(p1.z, 0) else p1.x
            return temp, self.w

    # 找出相邻插座的 cost
    # 在两面墙相交处 取一点 temp
    # temp 垂直于较高的那点
    # 变成 插座1 到 temp 的距离 加上 插座2 到 temp 的距离
    # 相当于求解两次 find_cost_together
    def find_cost_beside(self, o1: Position, o2: Position, is_same, border):
        x, y = border
        # 两个位置都不在地板上
        if not math.isclose(o1.z, 0) and not math.isclose(o2.z, 0):
            # temp 垂直较高的那点
            if o1.z - o2.z > 0:
                t_z = o1.z
                temp = Position(x, y, t_z)
                res = self.find_cost_together(o1, temp, is_same[0]) + self.find_cost_together(o2, temp, is_same[1])
                if not is_same[0] and not is_same[1]:
                    return res
                # 如果穿门了
                # 则 多出来两截 从门上面或者从地板 穿过 需要比较谁最小
                if self.is_cross_door(o1, temp):
                    res = self.find_cost_together(o1, temp, is_same[0]) +\
                          self.find_cost_together(o2, temp, is_same[1]) + 2 * min(self.door.get_height() - t_z, o2.z)
            else:
                t_z = o2.z
                temp = Position(x, y, t_z)
                # 如果穿门了
                # 则 多出来两截 从门上面或者从地板 穿过 需要比较谁最小
                if not self.is_cross_door(o2, temp):
                    res = self.find_cost_together(o1, temp, is_same[0]) + self.find_cost_together(o2, temp, is_same[1])
                else:
                    res = self.find_cost_together(o1, temp, is_same[0]) +\
                          self.find_cost_together(o2, temp, is_same[1]) + 2 * min(self.door.get_height() - t_z, o1.z)
        else:
            temp = Position(x, y, 0)
            res = self.find_cost_together(o1, temp, is_same[0]) + self.find_cost_together(o2, temp, is_same[1])
        return res

    # 找出相对插座的 cost
    # 在两面墙两个相交处 取二点 temp1 temp2
    # temp1 temp2 垂直较高的那点
    # 变成 插座1 到 temp2 的距离 加上 插座2 到 temp2 的距离
    # 求解 find_cost_together 和 find_cost_beside 各一次
    def find_cost_across(self, o1: Position, o2: Position, is_same, is_front_rear):
        # 相对的情况 连线的可能有三种
        # 顺时针 逆时针 从地板穿
        # 三种情况都需要计算出来进行比较
        t_z = max(o1.z, o2.z)
        # 根据所在墙的不同 找出不同的 temp
        temp1, temp3 = Position(0, self.w, t_z), Position(self.l, o1.y, 0)
        temp2, temp4 = Position(self.l, self.w, t_z), Position(self.l, 0, t_z)
        temp5 = Position(o1.x, self.w, 0)
        # 分成前后相对 和 左右相对情况
        if not is_front_rear:
            if math.isclose(o1.x, 0):
                # 顺时针 逆时针 从地板穿 三种情况
                res1 = self.find_cost_beside(o1, temp2, is_same[:2], (0, self.w)) + self.find_cost_together(temp2, o2, is_same[2])
                res2 = self.find_cost_beside(o1, temp4, is_same[::3], (0, 0)) + self.find_cost_together(temp4, o2, is_same[2])
                res3 = self.find_cost_beside(o1, temp3, [is_same[0], False], (0, o1.y)) + self.find_cost_together(temp3, o2, is_same[2])
            else:
                res1 = self.find_cost_beside(o2, temp2, is_same[2:], (0, self.w)) + self.find_cost_together(temp2, o1, is_same[0])
                res2 = self.find_cost_beside(o2, temp4, is_same[::3], (0, 0)) + self.find_cost_together(temp4, o1, is_same[0])
                res3 = self.find_cost_beside(o2, temp3, [is_same[2], False], (0, o2.y)) + self.find_cost_together(temp3, o1, is_same[0])
        else:
            if math.isclose(o1.y, 0):
                res1 = self.find_cost_beside(o1, temp2, is_same[:2], (self.l, 0)) + self.find_cost_together(temp2, o2, is_same[2])
                res2 = self.find_cost_beside(o1, temp1, is_same[::3], (0, 0)) + self.find_cost_together(temp1, o2, is_same[2])
                res3 = self.find_cost_beside(o1, temp5, [is_same[0], False], (o1.x, 0)) + self.find_cost_together(temp5, o2, is_same[2])
            else:
                res1 = self.find_cost_beside(o2, temp2, is_same[2:], (self.l, 0)) + self.find_cost_together(temp2, o1, is_same[0])
                res2 = self.find_cost_beside(o2, temp1, is_same[::3], (0, 0)) + self.find_cost_together(temp1, o1, is_same[0])
                res3 = self.find_cost_beside(o2, temp5, [is_same[2], False], (o2.x, 0)) + self.find_cost_together(temp5, o1, is_same[0])

        return min(res1, res2, res3)

    # 求出两个插座间最小的 cost
    def get_wire(self):
        kruskal = Kruskal()
        for i, value in enumerate(self.outlet):
            for j in range(i+1, self.n):
                o1 = self.outlet[i]
                o2 = self.outlet[j]
                f1 = self.is_same_wall_with_door(i)
                f2 = self.is_same_wall_with_door(j)
                # 是否 和门在同一墙
                # 相邻 相同 还是 在同一堵墙
                if self.is_together(i, j):
                    res = self.find_cost_together(o1, o2, f1)
                elif self.is_beside(i, j):
                    res = self.find_cost_beside(o1, o2, [f1, f2], self.witch_border(i, j))
                else:
                    # 是否在前后墙标志
                    # 计算相对墙情况是 需要分情况
                    is_front_rear = False if re.match(r'[2|3]', str(self.wall[i])) else True
                    if is_front_rear:
                        res = self.find_cost_across(o1, o2, [f1, self.wall[self.n] == 3, f2, self.wall[self.n] == 2],
                                                    is_front_rear)
                    else:
                        res = self.find_cost_across(o1, o2, [f1, self.wall[self.n] == 4, f2, self.wall[self.n] == 5],
                                                    is_front_rear)
                kruskal.add(i, j, res)
        # 返回最小生成树的权值和
        min_wire = math.ceil(kruskal.get_minimum_spanning_tree())
        return min_wire


def read_test(*args, **kwargs):
    # 读入测试文件
    with open('test1.txt', 'r') as f:
        data = f.readline().strip()
        while data:
            data = data.split(' ')
            # 取出每组测试的 第一组数据
            if len(data) == 4:
                # 获取长宽高 和 插座个数
                l, w, h, n = list(map(lambda x: int(x), data))
                if not l and not w and not h and not n:
                    break
                room = Room(l, w, h, n)
                while n:
                    test_data = f.readline().strip().split(' ')
                    x, y, z = list(map(float, test_data))
                    # 设置插座
                    room.add_outlet(Position(x, y, z))
                    n -= 1
                test_data = f.readline().strip().split(' ')
                # 设置门的四个点
                x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4 = list(map(lambda item: np.float(item), test_data))
                room.set_door(Door(Position(x1, y1, z1), Position(x2, y2, z2), Position(x3, y3, z3), Position(x4, y4, z4)))
                print(room.get_wire())
            data = f.readline().strip()
    return


read_test()

