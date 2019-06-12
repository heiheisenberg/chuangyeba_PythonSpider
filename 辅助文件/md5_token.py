from selenium import webdriver
import time

md5_url = 'http://md5.com/?secretKey=111&userid=222&exId=333'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # 无头模式
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('chrome://settins')
driver.get(md5_url)
js='window.open("{0}")'.format(md5_url)
driver.execute_script(js)
time.sleep(2)
driver.close()
