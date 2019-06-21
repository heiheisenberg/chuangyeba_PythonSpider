import threading
import time

number_list = []
for i in range(100):
    number_list.append(i)
        
class DoWork(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        
    def run(self):
        while len(number_list) != 0:
            self.lock.acquire()
            item = number_list.pop(0)
            self.lock.release()
            print(item)
            time.sleep(1)
            
if __name__ == '__main__':
    for i in range(5):
        home = DoWork()
        home.start()
        time.sleep(1)
    
    while True:
        pass