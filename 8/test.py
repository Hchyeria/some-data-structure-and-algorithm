from LoveStory import Graph


# 读取测试文件
def read_test(*args, **kwargs):
    with open('test1.txt', 'r') as f:
        # 读取测试次数 当为 0 时停止
        n = int(f.readline().strip())
        while n:
            count = n - 1
            # 实例化 Graph
            graph = Graph(n)
            while count:
                # 读取边信息 并添加两个节点
                u, v = map(int, f.readline().strip().split(' '))
                graph.add(u, v)
                count -= 1
            # 广度优先设定深度值
            graph.bfs()
            # 设定入栈和出栈的时间
            graph.set_stack_time()
            case = int(f.readline().strip())
            while case:
                a, b, c = map(int, f.readline().strip().split(' '))
                if graph.judge_same(a, b, c):
                    print("Yes")
                else:
                    print("No")
                case -= 1
            n = int(f.readline().strip())


read_test()