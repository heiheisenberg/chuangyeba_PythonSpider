import re,time
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui      # 这里是用于保存图片
import pyperclip
from yanzhengma import *  # 验证码接口
from setting import *     #这里保存了所有用户参数


class Hunst(object):
    """
    实现无人值守24小时刷网课
    """
 
    
    def __init__(self):

        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')       # 无界面运行
        #chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized') # 最大化
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        
    def visit_index(self):
        self.driver.get("http://hnust.hunbys.com/")
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="showLogin"]')))
        reg_element = self.driver.find_element_by_xpath('//a[@id="showLogin"]')
        reg_element.click()
        time.sleep(0.5)
        
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//img[@id="verifycodeImg"]')))
        login_element = self.driver.find_element_by_xpath('//img[@id="verifycodeImg"]')
        # 保存图片,保存图片前先删除原来验证码
        if os.path.exists(pic_dir):
            os.remove(pic_dir)
        action = ActionChains(self.driver).move_to_element(login_element)
        action.context_click(login_element)
        action.perform()
        pyautogui.typewrite(['v'])
        time.sleep(0.5)
        
        #将地址以及文件名复制
        pyperclip.copy(pic_dir)
        # 粘贴
        pyautogui.hotkey('ctrlleft','V')
        pyautogui.typewrite(['enter'])
        
        # 接入云打码平台输入验证码
        # 初始化
        time.sleep(2)
        yundama = YDMHttp(username, password, appid, appkey)
        # 登陆云打码
        uid = yundama.login();
        print('uid: %s' % uid)
        # 查询余额
        balance = yundama.balance();
        print('balance: %s' % balance)
        
        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, codetype, timeout);
        print('cid: %s, result: %s' % (cid, result))
        
        # 填入验证码，学号，密码
        self.driver.find_element_by_xpath('//*[@id="verifcode"]').send_keys(result)
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(login_number)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(login_password)
        self.driver.find_element_by_xpath('//*[@id="login_btn"]').click()
        time.sleep(1)
        
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
        WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="inProgressCourseData"]/div/div[2]/p[2]/span/a')))
        self.driver.find_element_by_xpath('//*[@id="inProgressCourseData"]/div/div[2]/p[2]/span/a').click()
        
        # 继续上一次进度
        video_element = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="video"]')))
        ActionChains(self.driver).move_to_element(video_element).perform()
        print("start play...")
        self.driver.execute_script("return arguments[0].play()",video_element)  # 开始播放
        #time.sleep(10)
        
        # 爬取播放列表
        with open('playlist.txt','w') as f:
            f.write(self.driver.page_source)
            f.close()
            
        # 这里进行正则匹配，得到视频播放列表
        #     
        while True:
            try:
                WebDriverWait(self.driver, 10, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="layui-layer-title"]')))
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
                ##如果视频播放完毕，切换下一个 
            except TimeoutException:
                pass
                

def get_exam_list(filename):
    with open(filename, 'r') as f:
        examdata = f.read()
        f.close()
        
    examcompile = re.compile('<p class="answer">答案：\[(\w)\]</p>', re.S)
    examlists   = re.findall(examcompile, examdata)
    
    for i, item in enumerate(examlists):
        item = item + str(i)
        yield '//*[@id="{0}"]'.format(item)


if __name__ == '__main__':
    hnust = Hunst()
    hnust.visit_index()
        
        