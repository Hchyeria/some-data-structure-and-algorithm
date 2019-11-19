from Panda import Nimaya


# 读取测试文件
def read_test(*args, **kwargs):
    with open('test1.txt', 'r') as f:
        m, n = map(int, f.readline().strip().split(' '))
        # 都为 0 停止测试
        while m != 0 and n != 0:
            nimaya = Nimaya(m, n)
            temp_m = 0
            while m:
                line_data = list(map(int, f.readline().strip().split(' ')))
                for clo in range(n):
                    nimaya.add(temp_m, clo, line_data[clo])
                temp_m += 1
                m -= 1
            # 用来储存是否访问过的信息的数组
            visited = [0] * (temp_m * n)
            # 分组
            nimaya.group(0, 0, visited)
            # 感染
            nimaya.infect()
            case = int(f.readline().strip())
            while case:
                type_name = int(f.readline().strip())
                print(nimaya.get_virus_res(type_name))
                case -= 1
            m, n = map(int, f.readline().strip().split(' '))


read_test()