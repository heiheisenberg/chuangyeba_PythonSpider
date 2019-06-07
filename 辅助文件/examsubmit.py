import requests
import json

url = 'http://hnust.hunbys.com/web/examination/examSubmit'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '554',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': 'Hm_lvt_e3d5c180b9eb27e8dd46713b446fd944=1559533371,1559701410,1559787551,1559829778; JLXCKID=dbd81154-d529-42ae-b572-88ca62c70fb1',
    'Host': 'hnust.hunbys.com',
    'Origin': 'http://hnust.hunbys.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

payload = {
    'courseId': "6493",
    'type': "1",
    'exId': 235113,                     # 每次递增1？
    'ccId':"687966",
    'knoId': "687973",                  # 当前视频id
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
        {"qid":"6","value":{"0":"创业","1":"创业"}},
        {"qid":"7","value":{"0":"创业","1":"创业"}},
        {"qid":"8","value":{"0":"创业"}}],
    'total': 12,
    'unanswered': 0,
    'examination':"",
    'token': "1a388013315953171fd6d04c310220c1" #文档d20cfa0d5be10f6f33d14298d8062a57
}

response = requests.post(url=url, data=json.dumps(payload), headers=headers)
print(response.status_code)
