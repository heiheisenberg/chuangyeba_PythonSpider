import re,time
import os
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import configparser

class Hunst(object):
    """
    实现无人值守24小时刷网课
    """
    HM_LVT = ''
    JLXCKID = ''
    
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
    
    special_id = ['687977','688001','688019','688036','688056','688087','688098']
    
    def __init__(self):
        ## 配置信息初始化
        self.config = configparser.ConfigParser()
        self.config.read('setting.ini')
        sections = self.config.sections()  # 返回所有配置块标题
        options = self.config.options(sections[0])
        self.HM_LVT = self.config.get(sections[0], options[0])
        self.JLXCKID = self.config.get(sections[0], options[1])
        self.cookie_lvt['value'] = self.HM_LVT
        self.cookie_JL['value'] = self.JLXCKID
        
        print(self.cookie_lvt)
        print(self.cookie_JL)
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized') # 最大化
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
    
    
    # 特殊视频id处理函数
    def special_deal(self, next_id):
        for index, id in enumerate(self.special_id, start=3):
            if id == next_id:
                xpath = '//*[@id="hostBody"]/div[2]/div[2]/div[1]/div[2]/ul/li[{0}]/p/span'.format(index)
                target = self.driver.find_element_by_xpath(xpath)
                self.driver.execute_script("arguments[0].scrollIntoView();", target)
                target.click()
    
    
    # 程序异常重启函数
    def restart_program(self):
        print('restart')
        self.driver.quit()
        python = sys.executable # 获取当前执行python
        os.execl(python, python, *sys.argv) #执行命令
    
    
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
            WebDriverWait(self.driver, 2, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="hasnotSign"]')))
            self.driver.find_element_by_xpath(qiandao).click()
            time.sleep(2)
        except TimeoutException:
            # 超时时表示今天签到完成
            pass
        
        # 点击学习，进入学习
        try:
            WebDriverWait(self.driver, 2, 0.5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inProgressCourseData"]/div/div[2]/p[2]/span/a')))
            self.driver.find_element_by_xpath('//*[@id="inProgressCourseData"]/div/div[2]/p[2]/span/a').click()
        except TimeoutException:
            self.driver.quit()
            print('当前cookie已失效，请重新设置cookie值')
            input('请按任意键结束...')
            sys.exit(1)
        
        # 继续上一次进度
        video_element = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="video"]')))
        ActionChains(self.driver).move_to_element(video_element).perform()
        print("start play...")
        self.driver.execute_script("return arguments[0].play()",video_element)  # 开始播放,默认播放
        
        # 主循环
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
                
            # 如果视频播放完毕，切换下一个，先要判断当前视频是否播放结束
            # 爬取播放列表
            with open('playlist.txt','w') as f:
                f.write(self.driver.page_source)
                f.close()
         
            #这里代码在视频生命周期只执行一次
            if flag:
                current_id, next_id = get_play_list('playlist.txt')
                # 如果下个视频是下一章的视频则展开下一章的视频列表
                if next_id in self.special_id:
                    self.special_deal(next_id)
                else:
                    # 在这里确保当前视频是可以正常播放的
                    while True:
                        try:
                            current_id_xpath = '//*[@id="{0}"]'.format(int(current_id))
                            self.driver.find_element_by_xpath(current_id_xpath).click()
                            break
                        except ElementNotVisibleException:
                            # 出现异常，可能是当前元素不可见
                            self.special_deal(current_id)
                time.sleep(1)
                flag = 0
                continue
            else:
                now_id, later_id = get_play_list('playlist.txt')
                if now_id == next_id:
                    # 跳转到下一个视频
                    try:
                        now_id_xpath = '//*[@id="{0}"]'.format(int(now_id))
                        time.sleep(1)
                        flag = 1
                        target = self.driver.find_element_by_xpath(now_id_xpath)
                        self.driver.execute_script("arguments[0].scrollIntoView();", target)
                        target.click()
                    except ElementNotVisibleException:
                        print('元素定位失败，程序即将重启')
                        time.sleep(2)
                        self.restart_program()

                      
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
        
        