import requests
import json
import configparser
import re
import time
from selenium import webdriver

config = configparser.ConfigParser()
config.read('setting.ini')
sections = config.sections()  # 返回所有配置块标题
options = config.options(sections[0])
cookie_All = config.get(sections[0], options[2])
print(cookie_All)

url_sub = 'http://hnust.hunbys.com/web/examination/examSubmit'


headers_post = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    #'Content-Length': '554',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': cookie_All,
    'Host': 'hnust.hunbys.com',
    'Origin': 'http://hnust.hunbys.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

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


def get_reqeust_url():
    with open("homeworklist.txt", encoding='utf-8') as f:
        for line in f:
            yield line.strip('\n')
        

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

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless') # 无头模式
            driver = webdriver.Chrome(chrome_options=chrome_options)
            md5_url = 'http://md5.com/?secretKey={0}&userid={1}&exId={2}'.format(secretKey, userid, exId)
            driver.get(md5_url)
            time.sleep(0.5)
            input = driver.find_element_by_xpath('//*[@id="out"]')
            token = input.text
            driver.quit()
            print(token)
            
            payload = {
            'courseId': "6493",
            'type': "1",
            'exId': exId,                     
            'ccId': chapterId,
            'knoId': ccId,                  # 当前视频id
            "answers":[                         # 选择题
                {"qid":"0","value":["A"]},
                {"qid":"1","value":["A"]},
                {"qid":"2","value":["B"]},
                {"qid":"3","value":["B"]},
                {"qid":"4","value":["A", "B"]},
                {"qid":"5","value":["B", "A"]},
                {"qid":"9","value":["1"]},
                {"qid":"10","value":["1"]},
                {"qid":"11","value":["创业吧"]}],# 最后一个简答题
            "blankAnswers":[                    # 填空题
                {"qid":"6","value":{"0":"创业"}},
                {"qid":"7","value":{"0":"创业"}},
                {"qid":"8","value":{"0":"创业"}}],
            'total': 12,
            'unanswered': 0,
            'examination':"",
            'token': token
            }
            
            if exId == '235124'
                payload = {
                'courseId': "6493",
                'type': "1",
                'exId': exId,                     
                'ccId': chapterId,
                'knoId': ccId,                  # 当前视频id
                "answers":[                         # 选择题
                    {"qid":"0","value":["A"]},
                    {"qid":"1","value":["A"]},
                    {"qid":"2","value":["B"]},
                    {"qid":"3","value":["B"]},
                    {"qid":"4","value":["A", "B"]},
                    {"qid":"5","value":["B", "A"]},
                    {"qid":"6","value":["1"]},
                    {"qid":"7","value":["1"]},
                    {"qid":"11","value":["创业吧"]}],# 最后一个简答题
                "blankAnswers":[                    # 填空题
                    {"qid":"8","value":{"0":"创业","1":""}},
                    {"qid":"9","value":{"0":"创业","1":""}},
                    {"qid":"10","value":{"0":"创业"}}],
                'total': 12,
                'unanswered': 0,
                'examination':"",
                'token': token
                }
            
            submit = requests.post(url=url_sub, data=json.dumps(payload), headers=headers_post)
            print(submit.status_code)
            # 687985 2.10提交失败
            #time.sleep(2)

if __name__ == "__main__":
    print("请确保当前cookie值正确，在这里请复制完整cookie值：")
    print("2.10请手动完成")
    input("请输入任何键开始提交作业...")
    
    get_hidden_info()
    
    