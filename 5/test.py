import random

from MinimumCircle import MinimumCircle
from MinimumCircle import Point


def write_test():
    count = random.randint(1000, 10000)
    exit_position = []
    with open('test2.txt', 'w') as f:
        f.write(str(count) + '\n')
        while count:
            # 默认 500
            x = random.randint(1, count)
            y = random.randint(1, count)
            while (x, y) in exit_position:
                x = random.randint(1, count)
                y = random.randint(1, count)
            exit_position.append((x, y))
            f.write(' '.join(list(map(str, [x, y]))) + '\n')
            count -= 1
        f.write(str(0) + '\n')
        f.close()

# write_test()


def read_test(*args, **kwargs):
    # 读入测试文件
    with open('test2.txt', 'r') as f:
        data = f.readline().strip()
        while data:
            minimum_circle = MinimumCircle()
            n = int(data)
            if not n:
                break
            while n:
                test_data = f.readline().strip()
                x, y = list(map(lambda item: float(item), test_data.split(' ')))
                # 添加点
                minimum_circle.add(Point(x, y))
                n -= 1
            print('%.2f' % (minimum_circle.find_minimum()/2))
            data = f.readline().strip()
    return


read_test()