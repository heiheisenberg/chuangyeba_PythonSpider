## 1.环境搭建和开发环境
	1.环境搭建
	pip install -U selenium pyautogui pyperclip requests json -i https://pypi.doubanio.com/simple/
	注意：如果还有其他库报错，请自行下载pip install 
	参数：
		-U 如果以安装，升级为最新版本
		-i 使用镜像源，提高下载速度
		
	2.下载Chromedriver, 并加入环境变量，便于python调用，建议放在python 安装目录script下
	http://npm.taobao.org/mirrors/chromedriver/
	根据浏览器版本下载对应的webdriver,否则会运行异常
	
	3.开发环境
	python3				下载地址:https://www.python.org/getit/
	window10 X64
	chrome x64    		下载地址：https://www.google.cn/intl/zh-CN/chrome/
	
## 2.关于验证码和登陆参数
	这里使用了云打码来过图片验证，如果有自己的账号，可以填入
	
	
## 3.文件介绍
	1.chuangyeba.py		## 主文件
	2.chuangyeba_beta.py##测试版本，添加了最新的改动
	3.yanzhengma.py		## 云打码平台接口文件，不需更改
	4.setting.py		## 用户参数设置都在这里，必须自己设置好参数！！！！！
	5.辅助文件是开发中的测试文档，并不参与 chuangyeba.py 的运行，是必要参考文件
	
	其他文件
	1.playlist.html		## 经过渲染后传回来的源码，用于正则匹配
	2.playitem.txt		## 经过初步正则匹配的视频列表
	3.videoplay.py		## html5 视频控制测试，这里是用bilibli测试
	4.exam.txt			## 包含了随堂测试的网页源码


## 4.如何使用
	设置好必要参数后，在当前文件下调用cmd
	>python chuangyeba.py