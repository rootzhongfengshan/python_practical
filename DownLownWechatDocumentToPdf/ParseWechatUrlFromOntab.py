# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:58:57 2019

@author: zhongfs
"""

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

def returnurlfromhtml(originalurl):
    result = requests.get(originalurl,headers)
    data = result.content
    select_encode = re.findall('charset=(.*?)">',result.text, re.S)
    result_text = str(data, str(select_encode[0]))
    outputurl = re.findall('text-decoration: none;" href="(.*?)">',result_text, re.S)
    return outputurl

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
    
def write2html(dirpath,title,article):
    ## 创建转换器
    ## 转换文档
    ## 写入文件
    htmldirpath=dirpath+ '/html/'
    pdfdirpath=dirpath+ '/pdf/'
    if not os.path.exists(htmldirpath):# 判断目录是否存在，不存在则创建新的目录
        os.makedirs(htmldirpath)
    if not os.path.exists(pdfdirpath):# 判断目录是否存在，不存在则创建新的目录
        os.makedirs(pdfdirpath)
    # 创建md文件
    #title=title.replace('/', '').replace('*', '').replace('*', '')
    title = re.sub('[\\\\/:*?\"<>|]', '', title)
    try:
        fp = open(htmldirpath+title+'.html', 'ab')
        fp.write(article.encode())
        fp.close()
        transfer_html_2_pdf(htmldirpath+title+'.html', pdfdirpath+title)
        print(title+"下载完成....")
    except:
        #print(title+"异常....")
        errresult.append(title+"异常....")
        

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
    #url='https://juejin.im/entry/5aa4f1506fb9a028e52d7624'
    #url='https://juejin.im/user/57b3c6ac2e958a0056224b2c/collections'
    #original
    #url='https://mp.weixin.qq.com/s?__biz=MzU0NjEyNDc0OQ==&mid=2247485295&idx=1&sn=68ca25212f8a65aa34f38c7d7e6962dd&chksm=fb6321cdcc14a8db059f3f31b4a9f1105867c72911ddef4820817b502312774a94c5092a90bc&mpshare=1&scene=24&srcid=0607cA2axYMxBF5ZwNZZpLr9&key=52682f658a9059336e8b4d15da0cd67f7e589ee72eaa2ce47404229047cf5fe50f6415375544be6ab46fbe6bd784fac6366bf070af3794e97c3e515c660adce8fccfc98efa753ac9adaf1c54e27cf0e5&ascene=14&uin=MjAxMDg2NDk0NA%3D%3D&devicetype=Windows+7&version=62060728&lang=zh_CN&pass_ticket=s%2ByFUllGTnmgwRzNEU1GDLHIwpP95vdomZhkgYs3zULfsUys%2FkTGA%2BIuj%2FPwVF93'
    urls = ['https://www.one-tab.com/page/VagCCtZiSbqYwfQDl-DZgQ'
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

        with open('WechatArticleUrlList'+date+'.md','w') as fw:
            fw.write('%s'%'\n'.join(result))
            
        with open('ErrorList'+date+'.md','w') as fw:
            fw.write('%s'%'\n'.join(errresult))