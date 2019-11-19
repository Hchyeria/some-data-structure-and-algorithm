import random
import numpy as np
import re


# 随机生成商品名
def generate_name():
    obj_name = ''.join(np.random.choice(list("abcdefghijklmnopqrstuvwxyz"), random.randint(2, 10)))
    obj_name = re.sub(r'^', "[", obj_name)
    obj_name = re.sub(r'$', "]", obj_name)
    return obj_name


# 生成测试文件代码
def write_test(count=3):
    with open('test.txt', 'w') as f:
        # 生成 10000 种不同商品
        goods = ['[flower]', '[vase]']
        prices = [2.00, 5.00]
        f.write(str('[flower]') + ' ' + str(2.00) + '\n')
        f.write(str('[vase]') + ' ' + str(5.00) + '\n')
        # 随机生成 1000-2 个商品 其中为了便于测试 其中两个商品 已经定为 [flower] 和 [vase]
        N = 1000-2
        while N:
            obj_name = generate_name()
            # 避免重复
            if obj_name not in goods:
                goods.append(obj_name)
            else:
                while obj_name not in goods:
                    obj_name = generate_name()
            # 随机生成价格
            obj_price = np.round(random.random() * random.randint(2, 200), 2)
            prices.append(obj_price)
            f.write(str(obj_name) + ' ' + str(obj_price) + '\n')
            N -= 1

        while count:
            n = random.randint(2, 5)
            f.write(str(n) + '\n')
            coupon = 1
            # 选出 6 个商品再在这里面选 为了不超过 6 个
            choose_coupon_good = np.random.choice(goods, 6, replace=False)
            while n:
                coupon_good = np.random.choice(choose_coupon_good, random.randint(1, 6), replace=False)

                # 随机生成数量 计算总价 并且格式化
                class Foo:
                    def __init__(self):
                        self.less_price = 0.0

                    def bar(self, x):
                        num = random.randint(2, 6)
                        self.less_price += (prices[goods.index(x)] * num)
                        return str(x) + '*' + str(num)

                    def get_price(self):
                        return self.less_price

                foo = Foo()
                temp = list(map(foo.bar, coupon_good))
                # 随机使价格比总价小
                temp.append(str(round(foo.get_price() - len(coupon_good)*random.random(), 2)))
                temp.insert(0, str(coupon))
                # 专程字符串写入文件
                string = ' '.join(temp)
                f.write(string + '\n')
                coupon += 1
                n -= 1
            # 生成客户购买的商品
            total = random.randint(2, 4)
            choose_shop_good = np.random.choice(goods, total, replace=False)
            temp = list(map(lambda x: ' '.join([x, str(random.randint(1, 10))]) + '\n', choose_shop_good))
            temp.insert(0, str(total) + '\n')
            f.writelines(temp)
            count -= 1
        f.write('-1')
        f.write('\n')
        f.close()


write_test()