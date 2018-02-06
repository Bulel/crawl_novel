#-*- encoding: utf-8 -*-
# @function: download novel
# @author:   Bulel
'''
download(993,994,url_end): 993 is the start num of novel, 994 is the end num
of novel, do not change url_end, it's the list of all urls

'''

import requests
import random
import time
import os
import re


class Repeat(Exception):
    print("Repeat download\r\n")
    

header={'Host':'www.qishu.tw',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Referer':'http://www.qishu.tw/book_13860/',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'Cache-Control':'max-age=0'
        }


def novel_write(num,content):
    
    novel_path='C:\\Users\\Administrator\\Desktop\\novel\\'
    if os.path.exists(novel_path) is False:
        os.mkdir(novel_path)
    
    with open(novel_path+'novel_%d.txt'%num,'a') as f:
        f.write(content)
        f.close


def parse_url():
    
    try:
        url_web = 'http://www.qishu.tw/book_13860/'
        url0 = requests.get(url_web,stream = True,headers=header,timeout=50)    
        url = re.findall(r'<dd><a href=.(.*?).>',url0.text)

        return url
    except:
        time.sleep(30)
        parse_url()


def download(start,num,url_end):

    for c in range(start,num):
        
        url='http://www.qishu.tw/book_13860/'+url_end[c]

        try:
            add = requests.get(url,stream = True,headers=header,timeout=50)

        except Repeat as e:

            add = requests.get(url,stream = True,headers=header,timeout=50)
        except:
            print("Exception: maybe lost conneceton with server,will try again after 60s")
            time.sleep(60)
            add = requests.get(url,stream = True,headers=header,timeout=50)
            
        add.encoding = 'gbk' # window default encode method mbcs also can work

        try:
            raw0 = re.sub(r'&nbsp;',' ',add.text) # replace blank space chr to ' '
            raw0 = re.sub(r'<br>','\r',raw0)      # in web source, there are two <br>
            raw1 = raw0.encode('utf-8').decode('utf-8')
		    
            title = re.search(r'<h1>(.*?)</h1>',raw1) # get the title of the novel chapter
            novel_write(c,str(title.group(1))+"\r\n") # write() argument must be str, not _sre.SRE_Match
		    
		    
            
            sli = raw1.split("<br />")                #parse all body in <br />
            length = len(sli)
		    
            chapter = ''
            
            first_word = sli[0].split('"content">')
            chapter = chapter + str(first_word[-1])
            print("The first word of novel_%d is: "%c,first_word[-1])
            
            for i in range(1,length-1):
                 chapter = chapter+str(sli[i])+"\n"  #all the paragraphs except the first and last

            last_word = sli[length-1].split("</div>")
            '''because the last word of the chapter is mixed in the last html code, so need to split it from
               html code
            '''
		    
            chapter = chapter + str(last_word[0])
            novel_write(c,chapter)
            
            print("\r\nThe last word of novel_%d is: "%c,last_word[0])
            time.sleep(random.randint(1,5)) 

        except:
            download(c,num,url_end) #In testing, fail to parse title too many times,so repeat download

def main():

    url_end = parse_url()
    num = len(url_end)
    print("The novels num is: %d \r\n"%num)
    download(3500,num,url_end)
    

if __name__ == '__main__':
    main()
