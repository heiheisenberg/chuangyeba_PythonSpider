import re
import json

def get_play_list():
    with open('playlist.txt', 'r') as f:
        sourcedata = f.read()
        f.close()
   
    playcompile = re.compile('<a href="javascript:void\(0\)" id="(\d+)" title="(.*?)".*?class="(.*?)".*?>', re.S)
    playlist    = re.findall(playcompile, sourcedata)

    for item in playlist:
        print(item)
        yield{
            'id':item[0],
            'title':item[1],
            'class':item[2].strip()
        }
        
        
def write_to_file(content):
	with open('playitem.txt','a',encoding = 'utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False)+'\n')
		f.close()
        
def main():
    for item in get_play_list():
        write_to_file(item)
    
    
if __name__ == '__main__':
    main()