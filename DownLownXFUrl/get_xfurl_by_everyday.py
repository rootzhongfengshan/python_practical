# -*- coding:utf-8 -*-
import re
import requests
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from email.header import Heade
useragents = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
    ]
headers = {
        "User-Agent": random.choice(useragents)
        }
ISOTIMEFORMAT='%Y%m%d'
def getsubxfplayurl(htmlurl):
    subresult = requests.get(htmlurl,headers)  
    subdata=subresult.content
    subresult_text=str(subdata,'utf-8')
    title=re.findall('<strong>影片名称：</strong><font color="#000">(.*?)</font>', subresult_text, re.S)
    #print(title)
    xfurl = re.findall('<input name="copy_sel" type="checkbox" value="(.*?)"><a href=', subresult_text, re.S)
    #print(xfurl)
    #print(title[0]+'\n'+str(xfurl[0]))
    return title[0]+'\n'+str(xfurl[0])
def savefile(astring):
    dir ='xfurlwett-'+str(time.strftime(ISOTIMEFORMAT, time.localtime()))+'.txt'
    #print(dir)
    fp = open(dir, 'ab')
    fp.write((astring+'\n').encode())
    fp.close()
    
def sentemail():
    caodate=str(time.strftime(ISOTIMEFORMAT, time.localtime()))
    host = 'smtp.163.com'  # 设置发件服务器地址
    port = 465  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
    sender = 'a419914150@163.com'  # 设置发件邮箱，一定要自己注册的邮箱
    pwd = 'B8b322927'  # 设置发件邮箱的密码，等会登陆会用到
    receiver0 = '419914150@qq.com' # 设置邮件接收人，可以是扣扣邮箱
    receiver1 = '1879230382@qq.com'
    body = '<h1>'+caodate+'</h1><p>zhongfs</p>' # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html') # 设置正文为符合邮件格式的HTML内容
    message = MIMEMultipart() 
    message['subject'] = caodate+'下载附件通知' # 设置邮件标题
    message['from'] = sender  # 设置发送人
    message['to'] = receiver0  # 设置接收人 
    #message['From'] = Header("菜鸟教程", 'utf-8')
    #message['To'] =  Header("测试", 'utf-8')
    #subject = 'Python SMTP 邮件测试'
    #message['Subject'] = Header(subject, 'utf-8')
    #邮件正文内容
    message.attach(msg)
    filename='xfurlwett-'+caodate+'.txt'
    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="'+filename+'"'
    message.attach(att1)
 
    # 构造附件2，传送当前目录下的 runoob.txt 文件
    #att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')
    #att2["Content-Type"] = 'application/octet-stream'
    #att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
    #message.attach(att2)
    try:
	    s = smtplib.SMTP_SSL(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
	    s.login(sender, pwd)  # 登陆邮箱
	    s.sendmail(sender, receiver0, message.as_string())# 发送邮件！
	    #s.sendmail(sender, receiver1, msg.as_string())
	    print ('Done.sent email success')
    except smtplib.SMTPException:
	    print ('Error.sent email fail')
if __name__ == '__main__': 
    url='http://www.bibizyz6.com/?r=785'
    time.sleep(random.randint(2,5))
    result = requests.get(url,headers)
    #print(result.status_code)
    if result.status_code==200:
        data = result.content
        #print(data)
        result_text = str(data, 'utf-8')
        #print(result_text)
        suburls = re.findall('width="459"><a href="(.*?)" target="_blank"', result_text, re.S)
        #print(suburls)
        for suburl in suburls:
            #time.sleep(random.randint(2,5))
            realsuburl='http://www.bibizyz6.com'+suburl
            #print(realsuburl)
            savefile(getsubxfplayurl(realsuburl))
        sentemail()
    