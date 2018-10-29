# -*- coding:utf-8 -*-
import re
import requests
import random
import time
import multiprocessing
useragents = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
    ]


def getsubxfplayurl(htmlurl):
    subheaders = {
        "User-Agent": random.choice(useragents)
        }
    try:
        subresult = requests.get(htmlurl,subheaders)
        subdata=subresult.content
        subresult_text=str(subdata,'utf-8')
        title=re.findall('<strong>影片名称：</strong><font color="#000">(.*?)</font>', subresult_text, re.S)
        xfurl = re.findall('<input name="copy_sel" type="checkbox" value="(.*?)"><a href=', subresult_text, re.S)
        if xfurl:
            retrunstr=title[0]+'\n'+str(xfurl[0])
        else:
            retrunstr='errline'
    except requests.exceptions.ConnectionError:
        print(htmlurl+'【错误】当前连接无法访问')
        retrunstr='err with'+str(htmlurl)
    return retrunstr
def savefile(astring,count):
    ISOTIMEFORMAT='%Y%m%d'
    dir ='xfbyredraintime-cao'+str(time.strftime(ISOTIMEFORMAT, time.localtime()))+'--'+str(count)+'.txt' 
    fp = open(dir, 'ab')
    fp.write((astring+'\n').encode())
    fp.close()

if __name__ == '__main__': 
    #url='http://www.bibizyz5.com/?r=785'
    pages=range(654,655)
    #pool = multiprocessing.Pool(processes=8)
    print("---------------------1---------------")
    for count in pages:
        #url =  input("Input key url: ")
        url ='http://www.bibizyz6.com/index-'+str(count)+'.html'
        headers = {
        "User-Agent": random.choice(useragents)
        }
        time.sleep(random.randint(1,2))
        try:
            result = requests.get(url,headers=headers)
        except requests.exceptions.ConnectionError:
            print(url+'【错误】当前连接无法访问')
            continue
        if result.status_code==200:
            data = result.content
            result_text = str(data, 'utf-8')
            suburls = re.findall('width="459"><a href="(.*?)" target="_blank"', result_text, re.S)
            for suburl in suburls:   
                realsuburl='http://www.bibizyz6.com'+suburl
                time.sleep(random.randint(1,5))
                savestr=getsubxfplayurl(realsuburl)
                savefile(savestr,count)
                #pool.apply_async(getsubxfplayurl,args=(realsuburl,count))
    #pool.close()
    #pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    