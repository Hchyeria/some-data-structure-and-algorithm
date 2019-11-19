from Shopping import Shopping

# 读取测试文件
def read_test():
    shop = Shopping()
    with open('test1.txt', 'r') as f:
        data = f.readline().strip()
        # 添加商品
        while len(data) != 1:
            data = data.split(' ')
            name, price = data
            price = float(price)
            shop.add_good((name, price))
            data = f.readline().strip()
        case = int(data)
        while case > 0:
            # 重置一下
            shop.reset()
            count = case
            # 添加优惠券
            while count:
                coupon = f.readline().strip().split(' ')
                total = float(coupon[-1])
                del coupon[0], coupon[-1]

                def foo(x):
                    temp = x.split('*')
                    return temp[0], int(temp[1])

                temp = list(map(foo, coupon))
                shop.add_coupon(temp, total)
                count -= 1
            # 添加购买的商品
            purchase_case = int(f.readline().strip())
            while purchase_case:
                purchase_good = f.readline().strip().split(' ')
                name, num = purchase_good
                num = int(num)
                shop.add_purchase((name, num))
                purchase_case -= 1
            print("%0.2f" % shop.find_minimum_cost())
            case = int(f.readline().strip())
    return

read_test()