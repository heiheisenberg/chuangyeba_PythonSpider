import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('setting.ini')
sections = config.sections()  # 返回所有配置块标题
options = config.options(sections[0])
HM_LVT = config.get(sections[0], options[0])
JLXCKID = config.get(sections[0], options[1])
cookie = HM_LVT + '; ' + JLXCKID
print(cookie)

url = 'http://hnust.hunbys.com/web/examination/examSubmit'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '554',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': cookie,
    'Host': 'hnust.hunbys.com',
    'Origin': 'http://hnust.hunbys.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_request_url():
    with open("课后作业url.txt", encoding='utg-8') as f:
        for line in f:
            yield line.strip('\n')
        

def get_hidden_info(url):
    url = get_reqeust_url()
    response = requests.get(url=url, headers=headers)
    