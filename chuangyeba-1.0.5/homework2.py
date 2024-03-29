import requests
import json
import configparser
import re
import time
from selenium import webdriver
from payload2 import *
import sys

# 读取配置文件，获取cookie
config = configparser.ConfigParser()
config.read('setting.ini')
sections = config.sections()  # 返回所有配置块标题
options = config.options(sections[0])
cookie_All = config.get(sections[0], options[2])
print(cookie_All)

# 答案提交页面
url_sub = 'http://hnust.hunbys.com/web/examination/examSubmit'

# post请求头
headers_post = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    #'Content-Length': '995',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': cookie_All,
    'Host': 'hnust.hunbys.com',
    'Origin': 'http://hnust.hunbys.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# get请求头
headers_get = {
    'Host': 'hnust.hunbys.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': cookie_All
}

# 获得每章节测试的请求页面
def get_reqeust_url():
    with open("homeworklist2.txt", encoding='utf-8') as f:
        for line in f:
            yield line.strip('\n')


# 获得正确试卷答案
def get_payload(exId, token):
    for item in payloadlist:
        if item.get('exId') == int(exId):
            item['token'] = token
            return item
    print("exId 索引错误！！")
    sys.exit(1)
        
     

def get_hidden_info():
    for url in get_reqeust_url():
        if url != '':
            response = requests.get(url=url, headers=headers_get)
            response.encoding = 'utf-8'
            ccId = re.search('<input type="hidden" id="ccId" value="(\d+)".*?>', response.text, re.S).group(1)
            print(ccId)
            userid = re.search('<input type="hidden" id="userid" value="(\d+)".*?>', response.text, re.S).group(1)
            secretKey = re.search('<input type="hidden" id="secretKey" value="(.*?)".*?>', response.text, re.S).group(1)
            exId = re.search('<input type="hidden" id="exId" value="(\d+)".*?>', response.text, re.S).group(1)
            chapterId = re.search('<input type="hidden" id="chapterId" value="(\d+)".*?>', response.text, re.S).group(1)
            
            params = {
                'secretKey':secretKey,
                'exId':exId,
                'userid':userid
            }


            md5_url = 'http://120.79.174.63/?secretKey={0}&userid={1}&exId={2}'.format(secretKey, userid, exId)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless') # 无头模式
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(md5_url)
            time.sleep(0.5)
            input = driver.find_element_by_xpath('//*[@id="out"]')
            token = input.text
            driver.quit()
            print(token)
            
            ## 传参获得正确载荷数据
            payload = get_payload(exId, token)
            
            submit = requests.post(url=url_sub, data=json.dumps(payload), headers=headers_post)
            print(submit.status_code)
            time.sleep(2)


if __name__ == "__main__":
    print("请确保当前cookie值正确，在这里请复制完整cookie值：")
    input("请输入任何键开始提交作业...")
    get_hidden_info()
