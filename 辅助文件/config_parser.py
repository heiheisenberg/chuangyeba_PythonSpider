import configparser

config = configparser.ConfigParser()

config.read('setting.ini')

sections = config.sections()  # 返回所有配置块标题
options = config.options(sections[0])

HM_LVT = config.get(sections[0], options[0])
JLXCKID = config.get(sections[0], options[1])
print(HM_LVT)
print(JLXCKID)
