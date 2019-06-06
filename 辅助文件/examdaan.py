##//*[@id="A0"]
import re

def get_exam_list(filename):
    with open(filename, 'r') as f:
        examdata = f.read()
        f.close()
        
    examcompile = re.compile('<p class="answer">答案：\[(\w)\]</p>', re.S)
    examlists   = re.findall(examcompile, examdata)
    examlist = []
    
    for i, item in enumerate(examlists):
        item = item + str(i)
        yield '//*[@id="{0}"]'.format(item)
        
if __name__ == '__main__':
    for i in get_exam_list('exam.txt'):
        print(i)
        