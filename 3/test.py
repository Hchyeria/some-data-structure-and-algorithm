import time
from functools import wraps

from Dinik import Dinik


# 计算时间的装饰器
def fn_timer(times):
    def decorator(func):
        @wraps(func)
        def function_timer(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            t1 = time.time()
            print("Time running %s: %s seconds %d" %
                  (kwargs['name'], str((t1 - t0)), times)
                  )
            return result
        return function_timer
    return decorator


@fn_timer(1)
def read_test(*args, **kwargs):
    # 读入测试文件
    with open('test.txt', 'r') as f:
        data = f.readline()
        while data:
            # 定义映射表
            hash_map = {}
            count = 0
            # 取出每组测试的 第一组数据
            test_data = list(data.strip().split(' '))
            # 考虑边缘数据情况
            s, t, n = test_data
            n = int(n)
            if not n:
                break
            hash_map[s] = count
            count += 1
            hash_map[t] = count
            count += 1
            # 初始化 Dinik 类
            dinik = Dinik(0, 1, n)
            while n:
                temp_list = list(f.readline().strip().split(' '))
                u, v, w = temp_list
                if u not in hash_map:
                    hash_map[u] = count
                    count += 1
                if v not in hash_map:
                    hash_map[v] = count
                    count += 1

                # 加入边的信息到图
                dinik.add(hash_map[u], hash_map[v], int(w))
                n -= 1
            res = dinik.find_max_flow()
            print(res)
            data = f.readline()
    return


read_test(name='Dinik')
