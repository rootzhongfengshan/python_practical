需要从微信公众号的文章下载下来，保存成pdf，以便以后的学习和阅读。
前期准备工作
```python
import os
import sys
import getopt
import requests
import time
import random
import re
import html2text
from bs4 import BeautifulSoup
import pdfkit

useragents = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET CLR 1.1.4322)'
    
]
ISOTIMEFORMAT='%Y%m%d%H%M%S'
date=str(time.strftime(ISOTIMEFORMAT, time.localtime()))
```

从一个url链接中提取文章名，和文章具体的内容

```python
def returnhtmlarticle(originalurl):
    result = requests.get(originalurl,headers)
    data = result.content
    select_encode = re.findall('charset=(.*?)">',result.text, re.S)
    result_text = str(data, str(select_encode[0]))
    soup = BeautifulSoup(result_text,'html5lib')
    title2=soup.find_all('h2', class_=['rich_media_title'])
    savetitlename = re.findall('id="activity-name">(.*?)</h2>',str(title2[0]), re.S)
    if savetitlename :
        savetitlename = re.sub('[\n\\\\/:*?\ "<>|]', '', savetitlename[0])
    else :
        savetitlename = "Error";
    articleall=str(soup.find_all('div'))
    arttxt=soup.find_all('div',class_='rich_media_area_primary_inner')
    artstdsoup=BeautifulSoup(str(arttxt[0]),'html5lib')
    artstdtxt=artstdsoup.find_all('div',class_='rich_media_content')
    if artstdtxt:
        article = str(artstdtxt[0])
        artbody = re.sub('data-src="','src="',article)
    else:
        article = str(articleall)
        artbody = re.sub('data-src="','src="',article)
    
    return savetitlename,artbody
```

转换为html

```python
def write2html(dirpath,title,article):
    ## 创建转换器
    ## 转换文档
    ## 写入文件
    if not os.path.exists(dirpath):# 判断目录是否存在，不存在则创建新的目录
        os.makedirs(dirpath)
    # 创建md文件
    #title=title.replace('/', '').replace('*', '').replace('*', '')
    title = re.sub('[\\\\/:*?\"<>|]', '', title)
    try:
        fp = open(dirpath+title+'.html', 'ab')
        fp.write(article.encode())
        fp.close()
        transfer_html_2_pdf(dirpath+title+'.html', dirpath+title)
        print(title+"下载完成....")
    except:
        print(title+"异常....")
        errresult.append(title+"异常....")
```



转换为pdf

```python

def transfer_html_2_pdf(htmls, bookname):
        '''
        把所有html文件转换成pdf文件
        参数配置查看https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
        '''
        
        options = {
                'page-size': 'A4',
                'margin-top': '0.2in',
                'margin-right': '0.2in',
                'margin-bottom': '0.2in',
                'margin-left': '0.2in',
                'minimum-font-size': 15,
                'encoding': "UTF-8"
                }
        print ("*** Transfer_html_2_pdf begin ***")
        #config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        pdfname = str(bookname) + '.pdf'
        pdfkit.from_file(htmls, pdfname, options=options)
        print ("*** Transfer_html_2_pdf end ***")
```

从tab中获取链接

```python

def returnurlfromhtml(originalurl):
    result = requests.get(originalurl,headers)
    data = result.content
    select_encode = re.findall('charset=(.*?)">',result.text, re.S)
    result_text = str(data, str(select_encode[0]))
    outputurl = re.findall('text-decoration: none;" href="(.*?)">',result_text, re.S)
    return outputurl
```

日记，记录下载了多少文章，以及哪些文章下载异常

```python
  with open('WechatArticleUrlList'+date+'.md','w') as fw:
            fw.write('%s'%'\n'.join(result))
            
        with open('ErrorList'+date+'.md','w') as fw:
            fw.write('%s'%'\n'.join(errresult))
```

主调度程序：

```python

if __name__ == "__main__":
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection' : 'keep-alive',
        'Host':  'mmbiz.qpic.cn',
        'Origin'	: 'https://mp.weixin.qq.com',
        'Referer'	: 'https://mp.weixin.qq.com/s?__b…479003243499e0f930be79&scene=0',
        'User-Agent': random.choice(useragents)
    } 
    head="<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>"
    urls = ['https://www.one-tab.com/page/nJ6aPLClSg-_4daEiX1Gvw'
            ]
    result=[]
    errresult=[]
    for url in urls:
        outputurls=returnurlfromhtml(url)
        #dealurl=str(outputurls[1])
        for dealurl in outputurls:
            #dealurl=dealurl+'#wechat_redirect'
            print(dealurl)
            savetitlename,artbody=returnhtmlarticle(dealurl)
            pwd = os.getcwd() # 获取当前的文件路径
            dirpath = pwd + '/WechatDownloadArticle'+date+'/'
            write2html(dirpath,savetitlename,head+'\n'+artbody)
            savetomd="["+savetitlename+"]("+dealurl+")"+"\n";
            result.append(savetomd)
```

