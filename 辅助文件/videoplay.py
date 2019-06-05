'''
自动播放bilibili视频
'''
# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from  selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

drive=webdriver.Chrome()

drive.get("https://www.bilibili.com/video/av16041375/")                    
video=WebDriverWait(drive,30,0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="bilibiliPlayer"]/div[1]/div[1]/div[8]/video')))  # 找到视频
url=drive.execute_script("return arguments[0].currentSrc;",video)  # 打印视频地址
print(url)

print("start")
drive.execute_script("return arguments[0].play()",video)  # 开始播放
time.sleep(15)

print("stop")
drive.execute_script("return arguments[0].pause()",video) # 暂停
