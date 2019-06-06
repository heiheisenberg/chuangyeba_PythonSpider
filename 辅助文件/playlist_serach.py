import re
import json

def get_play_list(filename):
    with open(filename, 'r') as f:
        sourcedata = f.read()
        f.close()
   
    playcompile = re.compile('<a href="javascript:void\(0\)" id="(\d+)" title="(.*?)" canbelearn="(.*?)".*?>', re.S)
    playlist    = re.findall(playcompile, sourcedata)

    for item in playlist:
        print(item)
        yield{
            'id':item[0],
            'title':item[1],
            'canbelearn':item[2].strip()
        }
        
        
def write_to_file(filename, content):
	with open(filename,'a',encoding = 'utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False)+'\n')
		f.close()
        
def main():
    for item in get_play_list('playlist.txt'):
        write_to_file('playitem.txt',item)
    
    
if __name__ == '__main__':
    main()