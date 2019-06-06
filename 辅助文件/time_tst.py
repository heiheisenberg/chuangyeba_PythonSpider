##生成格式 Wed Jun 05 00:00:00 CST 2019

import time

d = time.time()     # 显示当前的时间

ud = time.gtime(d)       # 把时间戳转换为含9个元素的元组，转换为UTC 时间
ld = time.localtime(d)   # 当地时间

#time.strftime()

#time.ctime(time.time())
time.asctime(ld)

str = time.ctime(time.time())
str = str[0:10] + ' 00:00:00 CST 2019'
if str[8] == ' ':
    str = str[0:8] + '0' + str[9:]