import re,time
import os
#import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#import pyautogui      # 这里是用于保存图片
#import pyperclip
#from yanzhengma import *  # 验证码接口
from setting import *     #这里保存了所有用户参数


class Hunst(object):
    """
    实现无人值守24小时刷网课
    """
    cookie_lvt = {
        'name':'Hm_lvt_e3d5c180b9eb27e8dd46713b446fd944',
        'value':HM_LVT,   
        'domain':'.hnust.hunbys.com'
    }
    cookie_JL = {
        'name':'JLXCKID',
        'value':JLXCKID,
        'domain':'.hunbys.com'
    }
    
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')       # 无界面运行
        #chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized') # 最大化
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        
    def visit_index(self):
        # 使用cookie登陆后直接进入主页
        self.driver.get("http://hnust.hunbys.com/")
        self.driver.add_cookie(self.cookie_lvt)
        self.driver.add_cookie(self.cookie_JL)
        time.sleep(2)
        self.driver.get("http://hnust.hunbys.com/web/student/course/list")
        
        # 现在开始进入刷课环节，先会弹出签到表
        # 在这里签到完成
        str = time.ctime(time.time())
        str = str[0:10] + ' 00:00:00 CST 2019'
        if str[8] == ' ':
            str = str[0:8] + '0' + str[9:]
        qiandao = '//*[@id="{0}"]/p[2]/i'.format(str)
        try:
            # 如果出现了签到表，进行签到
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="hasnotSign"]')))
            self.driver.find_element_by_xpath(qiandao).click()
            time.sleep(2)
        except TimeoutException:
            # 超时时表示今天签到完成
            pass
        
        
        # 进入学习
        WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inProgressCourseData"]/div/div[2]/p[2]/span/a')))
        self.driver.find_element_by_xpath('//*[@id="inProgressCourseData"]/div/div[2]/p[2]/span/a').click()
        
        # 继续上一次进度
        video_element = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="video"]')))
        ActionChains(self.driver).move_to_element(video_element).perform()
        print("start play...")
        self.driver.execute_script("return arguments[0].play()",video_element)  # 开始播放
        #time.sleep(10)
        
        ## 单独测试视频定位
        ##滚动测试
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        #self.driver.find_element_by_xpath('//*[@id="688104"]').click()
        #self.driver.execute_script("return arguments[0].play()",video_element)  # 开始播放   
        # # 这里进行正则匹配，得到视频播放列表
        # #主循环
        flag = 1
        current_id = 0
        next_id = 0
        while True:
            try:
                WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="layui-layer-title"]')))
                print('题目弹出...')
                # 保存当前页面，提取原题与答案
                with open('exam.txt', 'w') as f:
                    f.write(self.driver.page_source)
                    f.close()

                for item in get_exam_list('exam.txt'):
                    try:
                        self.driver.find_element_by_xpath(item).click()
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                        pass

                # 当一切都没问题时，提交答案
                print('做题完毕')
                self.driver.find_element_by_xpath('//*[@class="layui-layer-btn0"]').click()
                time.sleep(2)   
            except TimeoutException:
                pass
                
            ##如果视频播放完毕，切换下一个，先要判断当前视频是否播放结束
            # 爬取播放列表
            with open('playlist.txt','w') as f:
                f.write(self.driver.page_source)
                f.close()
            # 送入解析函数，得到当前视频id 和播放状态class, 下一个视频id
            
            #get_play_list('playlist.txt')
            # print('current_id:%s     next_id:%s' %(current_id, next_id))
            # if (current_id == '' ) and (next_id != ''):
                # # 当前视频播放完毕
                # # 切换到下一个视频 //*[@id="687967"]
                # time.sleep(10)      #等待当前视频片尾结束
                # next_id_xpath = '//*[@id="{0}"]'.format(int(next_id))
                # self.driver.find_element_by_xpath(next_id_xpath).click()
            # elif next_id == '':
                # print('所有视频都播放完毕，程序退出，感谢使用') 
            #这里代码在视频生命周期只执行一次
            if flag:
                current_id, next_id = get_play_list('playlist.txt')
                current_id_xpath = '//*[@id="{0}"]'.format(int(current_id))
                self.driver.find_element_by_xpath(current_id_xpath).click()
                time.sleep(1)
                flag = 0
                continue
            else:
                now_id, later_id = get_play_list('playlist.txt')
                if now_id == next_id:
                    # 跳转到下一个视频
                    now_id_xpath = '//*[@id="{0}"]'.format(int(now_id))
                    self.driver.find_element_by_xpath(now_id_xpath).click()
                    time.sleep(1)
                    flag = 1
                

                      
def get_exam_list(filename):
    with open(filename, 'r') as f:
        examdata = f.read()
        f.close()
        
    examcompile = re.compile('<p class="answer">答案：\[(\w)\]</p>', re.S)
    examlists   = re.findall(examcompile, examdata)
    
    for i, item in enumerate(examlists):
        item = item + str(i)
        yield '//*[@id="{0}"]'.format(item)


def get_play_list(filename):

    current_id = ''
    next_id = ''
    
    with open(filename, 'r') as f:
        sourcedata = f.read()
        f.close()
   
    playcompile = re.compile('<a href="javascript:void\(0\)" id="(\d+)" title="(.*?)" canbelearn="(.*?)" currentknowledge="(\d)".*?>', re.S)
    playlist    = re.findall(playcompile, sourcedata)

    for item in playlist:
        if item[2] == 'true':
            current_id = item[0]
        elif item[2] == 'false':
            next_id = item[0]
            break
    
    return current_id, next_id


if __name__ == '__main__':
    hnust = Hunst()
    hnust.visit_index()
        
        