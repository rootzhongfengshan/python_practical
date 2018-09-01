# -*- coding:utf-8 -*-
import re
import requests
import os
def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False
def dowmloadPic(html,keyword):
    pic_url = re.findall('data-src=\'(.*?)\'', html, re.S)
    i = 1
    savedir=keyword+'/'
    mkdir(savedir)
    for each in pic_url:
        print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
        try:
            pic = requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载')
            continue
        dir = savedir + keyword + '_' + str(i) + '.jpg'
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1

if __name__ == '__main__':
    #word = input("Input key word: ")
    url =  input("Input key url: ")
    result = requests.get(url)
    data = result.content
    result_text = str(data, 'gbk')
    savename = re.findall('<title>(.*?)</title>', result_text, re.S)
    dowmloadPic(result_text,str(savename[0]))

    