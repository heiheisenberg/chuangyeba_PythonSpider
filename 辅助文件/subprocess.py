import sys
import time
import os


def print_hello():
    print("hello world")
    time.sleep(4)
    restart_program()


def restart_program():
    print('restart')
    python = sys.executable # 获取当前执行python
    os.execl(python, python, *sys.argv) #执行命令


if __name__ == '__main__':
    print_hello()