from selenium import webdriver
import time 
browse = webdriver.Chrome()
browse.get('http://www.tmooc.cn/')
time.sleep(3)
browse.quit()
