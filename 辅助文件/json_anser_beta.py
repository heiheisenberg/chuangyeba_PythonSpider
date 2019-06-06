import requests
import re

url = 'http://hnust.hunbys.com/web/students/getClassWork'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '27',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'Hm_lvt_e3d5c180b9eb27e8dd46713b446fd944=1559533371,1559701410,1559787551,1559829778; JLXCKID=00eabfbf-be4d-4cb6-8a94-ebda0721a77b',
    'Host': 'hnust.hunbys.com',
    'Origin': 'http://hnust.hunbys.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_cataid():
    with open('playitem.txt','r', encoding='utf-8') as f:
        cataidlist = f.read()
        f.close()
    
    idcompile = re.compile('\{"id": "(.*?)".*?\}', re.S)
    idlist = re.findall(idcompile, cataidlist)
    for item in idlist:
        print(item)
        yield item
        

def download_json():
    for cataId in get_cataid():
        response = requests.post(url=url, data = {'courseId':'6493','cataId':cataId}, headers = headers)
        response.encoding = 'utf-8'
        with open('json_anser.txt', 'a') as f:
            f.write(response.text + '\n')
            f.close()
            
            
if __name__ == '__main__':
    download_json()