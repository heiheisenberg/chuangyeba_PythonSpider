import logging

# 日志级别
# 将信息打印到控制台上
# logging.debug(u"苍井空")
# logging.info(u"麻生希")
# logging.warning(u"小泽玛利亚")
# logging.error(u"桃谷绘里香")
# logging.critical(u"泷泽萝拉")

# 设置日志级别
# logging.basicConfig(level=logging.NOTSET)

# 部分名词解释
# Logging.Formatter：这个类配置了日志的格式，在里面自定义设置日期和时间，输出日志的时候将会按照设置的格式显示内容。
# Logging.Logger：Logger是Logging模块的主体，进行以下三项工作：
# 1. 为程序提供记录日志的接口
# 2. 判断日志所处级别，并判断是否要过滤
# 3. 根据其日志级别将该条日志分发给不同handler
# 常用函数有：
# Logger.setLevel() 设置日志级别
# Logger.addHandler() 和 Logger.removeHandler() 添加和删除一个Handler
# Logger.addFilter() 添加一个Filter,过滤作用
# Logging.Handler：Handler基于日志级别对日志进行分发，如设置为WARNING级别的Handler只会处理WARNING及以上级别的日志。
# 常用函数有：
# setLevel() 设置级别
# setFormatter() 设置Formatter

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置
# 由于日志基本配置中级别设置为DEBUG，所以一下打印信息将会全部显示在控制台上
logging.info('this is a loggging info message')
logging.debug('this is a loggging debug message')
logging.warning('this is loggging a warning message')
logging.error('this is an loggging error message')
logging.critical('this is a loggging critical message')

# 日志输出-文件
import logging  # 引入logging模块
import os.path
import time
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/Logs/'
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
# 日志
logger.debug('this is a logger debug message')
logger.info('this is a logger info message')
logger.warning('this is a logger warning message')
logger.error('this is a logger error message')
logger.critical('this is a logger critical message')

