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
from time import sleep 


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
#originalurl='https://blog.51cto.com/wgkgood/p3'
def returnurlfromhtml(originalurl):
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection' : 'keep-alive',
        'User-Agent': random.choice(useragents)
    } 
    result = requests.get(originalurl,headers)
    data = result.content
    select_encode = re.findall('charset=(.*?)">',result.text, re.S)
    result_text = str(data, str(select_encode[0]))
    outputurl = re.findall('<a class="tit" href="(.*?)">',result_text, re.S)
    return outputurl
    
#originalurl='https://juejin.im/user/5aa558886fb9a028c8127d23/collections'    
def returnsuburlfromcollections(originalurl):
    result = requests.get(originalurl,headers)
    data = result.content
    select_encode = re.findall('<head><meta charset=(.*?)><meta',result.text, re.S) 
    result_text = str(data, str(select_encode[0]))
    suburls=re.findall('data-v-2431a1b8><a href="(.*?)" target="_blank"',result_text, re.S)
    outputurl=[]
    for suburl in suburls:
        tmpsuburl = 'https://juejin.im'+suburl
        outputurl.append(tmpsuburl)
    return outputurl
#originalurl='https://juejin.im/collection/5cb13c686fb9a0747e1dc6a6'
def returnJunJinArticleUrlfromsuburl(originalurl):
    result = requests.get(originalurl,headers)
    data = result.content
    select_encode = re.findall('<head><meta charset=(.*?)><meta',result.text, re.S) 
    result_text = str(data, str(select_encode[0]))
    suburls=re.findall('<!----><!----><a href="(.*?)" target="_blank"',result_text, re.S)
    outputurl=[]
    for suburl in suburls:
        tmpsuburl = 'https://juejin.im'+suburl
        outputurl.append(tmpsuburl)
    return outputurl

    
#originalurl='https://blog.51cto.com/wgkgood/1531694'
def returnhtmlarticle(originalurl):
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection' : 'keep-alive',
        'User-Agent': random.choice(useragents)
    } 
    result = requests.get(originalurl,headers)
    data = result.content
    #select_encode = re.findall('charset=(.*?)/><meta',result.text, re.S)
    select_encode =['utf-8','']
    title=re.findall('<title>(.*?)</title>',result.text, re.S)
    result_text = str(data, str(select_encode[0]))
    soup = BeautifulSoup(result_text,'html.parser')
    title = soup.find('title').text
    #title2=soup.find_all('h2', class_=['rich_media_title'])
    #savetitlename = re.findall('id="activity-name">(.*?)</h2>',str(title2[0]), re.S)
    savetitlename = title
    if savetitlename :
        savetitlename = re.sub('[\n\\\\/:*?\ "<>|]', '', savetitlename)
    else :
        savetitlename = "Error";
    articleall=str(soup.find_all('div'))
    #artstdtxt=soup.find_all('div',id_='juejin')
    #artstdsoup=BeautifulSoup(str(arttxt[0]),'html5lib')
    #artstdtxt=artstdsoup.find_all('div',class_='rich_media_content')
    artstdtxt=soup.find(name='div',attrs={"class":"artical-content-bak main-content editor-side-new"})
    if artstdtxt:
        artbody=str(artstdtxt)
        artbody = re.sub('data-src="','src="',artbody)
    else:
        artbody="error"
#        artbody = re.sub('data-src="','src="',artbody)
    #    if originalurl.find('post') != -1:
#        dataid=re.findall('</h1><div class="article-content" data-id="(.*?)" data-v-', articleall, re.S)
#        articlebody=re.findall('</h1><div class="article-content" data-id="'+str(dataid[0])+'" data-v-e09a79f2="" itemprop="articleBody">(.*?)</div>', articleall, re.S)
#        artbody=str(articlebody[0])
#        artbody = re.sub('data-src="','src="',artbody)
#    else:
#        articlebody=re.findall('<!----><div class="entry-content article-content" data-v-41d33d72="" itemprop="articleBody"> <a id="more"></a>(.*?)</div>', articleall, re.S)
#        artbody=str(articlebody[0])
#        artbody = re.sub('data-src="','src="',artbody)    
    
    return savetitlename,artbody
    
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
        

def transfer_html_2_pdf(htmls, bookname):
        '''
        把所有html文件转换成pdf文件
        参数配置查看https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
        '''
        
        options = {
                'page-size': 'A4',
                'margin-top': '0.3in',
                'margin-right': '0.3in',
                'margin-bottom': '0.3in',
                'margin-left': '0.3in',
                'minimum-font-size': 13,
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
        'User-Agent': random.choice(useragents)
    } 
    head="<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>"
    #url='https://juejin.im/entry/5aa4f1506fb9a028e52d7624'
    #url='https://juejin.im/user/57b3c6ac2e958a0056224b2c/collections'
    #original
    #url='https://mp.weixin.qq.com/s?__biz=MzU0NjEyNDc0OQ==&mid=2247485295&idx=1&sn=68ca25212f8a65aa34f38c7d7e6962dd&chksm=fb6321cdcc14a8db059f3f31b4a9f1105867c72911ddef4820817b502312774a94c5092a90bc&mpshare=1&scene=24&srcid=0607cA2axYMxBF5ZwNZZpLr9&key=52682f658a9059336e8b4d15da0cd67f7e589ee72eaa2ce47404229047cf5fe50f6415375544be6ab46fbe6bd784fac6366bf070af3794e97c3e515c660adce8fccfc98efa753ac9adaf1c54e27cf0e5&ascene=14&uin=MjAxMDg2NDk0NA%3D%3D&devicetype=Windows+7&version=62060728&lang=zh_CN&pass_ticket=s%2ByFUllGTnmgwRzNEU1GDLHIwpP95vdomZhkgYs3zULfsUys%2FkTGA%2BIuj%2FPwVF93'
    urls = ['https://www.one-tab.com/page/rMWy3Hq3T1KBzil3U8vuDg'
            ]
    result=[]
    errresult=[]

    # url='https://juejin.im/user/5aa558886fb9a028c8127d23/collections'
    # #url='https://juejin.im/user/57b3c6ac2e958a0056224b2c/collections'
    # #result = requests.get(originalurl,headers)
    # suburls=returnsuburlfromcollections(url)
    # for suburl in suburls:
        # subcollecturls=returnJunJinArticleUrlfromsuburl(suburl)
        # for subcollecturl in subcollecturls:
            # savetitlename,artbody=returnhtmlarticle(subcollecturl)
            # pwd = os.getcwd() # 获取当前的文件路径
            # dirpath = pwd + '/WechatDownloadArticle'+date+'/'
            # write2html(dirpath,savetitlename,head+'\n'+artbody)
            # savetomd="["+savetitlename+"]("+subcollecturl+")"+"\n";
            # result.append(savetomd)
    pages=range(1,2)
    originalurl='https://blog.51cto.com/13527416/p'
    for i in pages:
        dealurl=originalurl+str(i)
        outputurls=returnurlfromhtml(dealurl)
        for outputurl in outputurls:
            sleep(random.randint(3, 7))
            savetitlename,artbody=returnhtmlarticle(outputurl)
            pwd = os.getcwd() # 获取当前的文件路径
            dirpath = pwd + '/52CTODownloadArticle'+date+'/'        
            write2html(dirpath,savetitlename,artbody)

        with open('JuejinArticleUrlList'+date+'.md','w') as fw:
            fw.write('%s'%'\n'.join(result))
            
        with open('JuejinErrorList'+date+'.md','w') as fw:
            fw.write('%s'%'\n'.join(errresult))
            
    
    # for url in urls:
        # outputurls=returnurlfromhtml(url)
        # #dealurl=str(outputurls[1])
        # for dealurl in outputurls: 
            # print(dealurl)
            # savetitlename,artbody=returnhtmlarticle(dealurl)
            # pwd = os.getcwd() # 获取当前的文件路径
            # dirpath = pwd + '/juejinDownloadArticle'+date+'/'
            # write2html(dirpath,savetitlename,head+'\n'+artbody)
            # savetomd="["+savetitlename+"]("+url+")"+"\n";
            # result.append(savetomd)

        # with open('SFArticleUrlList'+date+'.md','w') as fw:
            # fw.write('%s'%'\n'.join(result))
            
        # with open('ErrorList'+date+'.md','w') as fw:
            # fw.write('%s'%'\n'.join(errresult))