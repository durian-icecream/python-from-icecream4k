# 面向对象 C++  java   python
#     给钱  加辣椒  不要香菜，放香菜杀了你
#     函数 -> 吕大妈
#     烧饼
#     用    做
#
# 面向过程 C  汇编
#     准备钱 面粉  擀面杖  香菜   酱料
#     揉面  醒面  擀面   烧制.....
#     烧饼


# a = input('请输入:') # 1
# b = a + a # 11
#
# print(b * 5)


# a = input("请输入性别:")
# if a == 'boy':
#     print("大大泡泡糖")
# elif a == 'girl':
#     print("xxx")
# elif a == 's':
#     print("xxx")
# else:
#     print('美少女')

# list01 = [1,2,3,4,5,6]
# print(list01[3]) # 查
# list01.append(7) # 增
# print(list01)
# list01[3] = 'aaaa'  # 改
# print('更改之后的结果:',list01)
# list01.pop(3)       # 删
# print('删除后的结果:',list01)
# from selenium import webdriver
# import time
# import random
# list01 = ['https://baike.baidu.com/item/%E5%BD%AD%E4%BA%8E%E6%99%8F/305410?fr=aladdin','https://www.bilibili.com/','https://www.csdn.net/']
# def do(list01):
#     d.get(list01[i])
# def wait():
#     time.sleep(3)
#     d.quit()
# for i in range(0,len(list01)):
#     d = webdriver.Chrome()
#     if list01[0] == list01[i]:
#         do(list01)
#         # d.find_element_by_id('kw').send_keys('彭于晏')
#         target = d.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[1]/div/div[30]')
#         d.execute_script("arguments[0].scrollIntoView();", target)
#         wait()
#     elif list01[1] == list01[i]:
#         # d.get((list01[]))
#         do(list01)
#         d.find_element_by_class_name('nav-search-keyword').send_keys('彭于晏')
#         wait()
#     elif list01[2] == list01[i]:
#         do(list01)
#         d.find_element_by_class_name('input_search').send_keys('测试')
#         wait()
#     else:
#         print('error')
