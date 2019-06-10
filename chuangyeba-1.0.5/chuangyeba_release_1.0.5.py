import re,time
import os
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,ElementNotVisibleException,ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import configparser
import threading                    # 1.0.4 新增，超时自动重启
from goto import with_goto          # 对层嵌套跳出

refresh_signal = 0
config = configparser.ConfigParser()
config.read('setting.ini')
sections = config.sections()  # 返回所有配置块标题
options = config.options(sections[1])
timecount = int(config.get(sections[1], options[0]))
timecopy = timecount            # 备份超时时间



class Timeout(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        print("看门狗线程启动...")
        global timecount
        while True:
            if timecount == 0:
                global refresh_signal
                refresh_signal = 1
                print("看门狗超时，触发重启进程")
                break
            else:
                timecount -= 1
            time.sleep(1)
            #print("timecount:%d" %(self.timecount))


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
    
    
    # 程序异常重启函数
    def restart_program(self):
        print('restart')
        self.driver.quit()
        python = sys.executable # 获取当前执行python
        os.execl(python, python, *sys.argv) #执行命令
        
    def do_homework(self):
        print('题目弹出...')
        print('[INFO]正在重置看门狗')
        global timecount
        global timecopy
        timecount = timecopy
        print("看门狗重置成功：%d" %(timecount))
        # 保存当前页面，提取原题与答案
        with open('exam.txt', 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)
            f.close()

        for item in get_exam_list('exam.txt'):
            try:
                button_element = self.driver.find_element_by_xpath(item)
                button_element.click()
                time.sleep(1)
            except:
                print("做题出现未知错误，请修复")
                pass

        # 当一切都没问题时，提交答案
        print('做题完毕,正在提交')
        self.driver.find_element_by_xpath('//*[@class="layui-layer-btn0"]').click()
        print('提交成功')
        time.sleep(1)   
        
        
        
    # 特殊视频id处理函数
    def special_deal(self, next_id):
        for index, id in enumerate(self.special_id, start=3):
            if id == next_id:
                try:
                    xpath = '//*[@id="hostBody"]/div[2]/div[2]/div[1]/div[2]/ul/li[{0}]/p/span'.format(index)
                    target = self.driver.find_element_by_xpath(xpath)
                    self.driver.execute_script("arguments[0].scrollIntoView();", target)
                    target.click()
                except ElementClickInterceptedException as e:
                    print("[ERROR]视频列表展开无效，即将重启")
                    print(e)
                    time.sleep(2)
                    self.restart_program()
                

    @with_goto
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
            print('[WARING]当前cookie已失效，请重新设置cookie值')
            input('请按任意键结束...')
            sys.exit(1)
   
        # 主循环
        flag = 1
        current_id = 0
        next_id = 0
        while True:
            label .start
            # 判断是否弹窗
            try:
                WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="doclasswork"]')))
                self.do_homework()
            except TimeoutException:
                pass
            
            # # 避免视频中断,在弹窗判断之后
            # try:
                # video_element = WebDriverWait(self.driver, 5, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="video"]')))
                # ActionChains(self.driver).move_to_element(video_element).perform()
                # self.driver.execute_script("return arguments[0].play()",video_element)
                # print("视频播放中...")
            # except:
                # print('防视频中断出错')
                # pass
            
            # 如果视频播放完毕，切换下一个，先要判断当前视频是否播放结束
            # 爬取播放列表
            with open('playlist.txt','w', encoding='utf-8') as f:
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
                            # 出现异常，可能是当前元素不可见,可能是遭遇弹窗
                            # 如果遭遇弹窗，回到弹窗检测
                            print('[WARING]当前id与测量id不同')
                            self.special_deal(current_id)
                flag = 0
                continue
            else:
                now_id, later_id = get_play_list('playlist.txt')
                if now_id == next_id:
                    # 跳转到下一个视频
                    try:
                        now_id_xpath = '//*[@id="{0}"]'.format(int(now_id))
                        flag = 1
                        target = self.driver.find_element_by_xpath(now_id_xpath)
                        self.driver.execute_script("arguments[0].scrollIntoView();", target)
                        target.click()
                    except ElementNotVisibleException:
                        print('[ERROR]元素定位失败，可能是遭遇弹窗')
                        goto .start
                    except ElementClickInterceptedException:
                        print("[ERROR]元素点击冲突")
                        goto .start
                    # 视频切换可以放心刷新
                    self.driver.refresh()
                    video_element = WebDriverWait(self.driver, 5, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="video"]')))
                    time.sleep(2)       # 这里确认视频加载成功，可能出现网络延时
                    video_element.click()
                    # ActionChains(self.driver).move_to_element(video_element).perform()
                    # self.driver.execute_script("return arguments[0].play()",video_element)
                    print('[INFO]切换视频成功')    
            # 在这里检测重启标志位是否被触发
            global refresh_signal
            if refresh_signal == 1:
                # 当长时间没响应时，将重启程序
                print('[INFO]time is up')
                refresh_signal = 0
                self.restart_program()
                
                

                      
def get_exam_list(filename):
    with open(filename, 'r',encoding='utf-8') as f:
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
    
    with open(filename, 'r',encoding='utf-8') as f:
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
    timethread = Timeout()
    timethread.start()
    
    hnust = Hunst()
    hnust.visit_index() 
        