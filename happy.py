# 编程语言 - 面向对象

# name = input('请输入您所选择的英雄名>>>')#亚瑟
# print('欢迎来到王者峡谷,',name)
# print(name,"使用的是长剑")
# name = input('请输入您所选的英雄名>>>')#王昭君
# print(name)

# 容器
# 列表

# 增删改查
# 增加 - append
# list01.append(1)
# list01.append('大王叫我来巡山')
# list01.append(True)
# 删除
# print(list01)
# list01.pop(-1)
# print(list01)


# 你去买可乐，身上只有50块，一个可乐5块钱，你能买多少可乐啊？
# money = 50
# colo = 5
# c = 0 # 循环次数！！！！！！
# while money >= colo:
#     money = money - colo
#     c = c + 1
#     print('你买了,',c,'次可乐')

# 面试题:for 循环的运行机制
# for循环当中的变量依次绑定可迭代对象的所有元素，当绑定结束
# 循环则结束

# while True:
#     list01.pop(-1)
#     if list01 == []:
#         break
# print(list01)
# 查


# 登录注册
# 注册
list01 = []
uid = input("请输入账号[注册]:")
upwd = input("请输入密码[注册]:")
list01.append(uid)
list01.append(upwd)
# 登录
# 登录,如果3次账号输入错误，程序退出的这个需求怎么办
c_0 = 0 # 账号的循环次数!!!!!!!!
c_1 = 0 # 密码的循环次数!!!!!!!!
while c_0 < 3:
    id = input('请输入您的账号[登录]:')
    if id == list01[0]:
        print("账号输入正确!")
        while c_1 < 3:
            pwd = input('请输入您的密码[登录]:')
            if pwd == list01[1]:
                print("登录成功!!")
                break
            else:
                if c_1 == 2:
                    print("密码输入错误过多，程序已退出")
                    break
                else:
                    print("密码错误,还剩下%d次机会" % (2 - c_1))
                    c_1 += 1
        break
    else:
        if c_0 == 2:
            print("您的账号输入错误次数太多，程序已退出")
            break
        else:
            print("您输入的账号不存在,还剩下%d次机会" % (2 - c_0))
            c_0 += 1

