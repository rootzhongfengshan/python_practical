import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
ISOTIMEFORMAT='%Y%m%d'
def sentemail():
    caodate=str(time.strftime(ISOTIMEFORMAT, time.localtime()))
    host = 'smtp.163.com'  
    # 设置发件服务器地址
    port = 465  
    # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
    sender = 'a419914150@163.com'  
    # 设置发件邮箱，一定要自己注册的邮箱
    pwd = 'B8b322927'  
    # 设置发件邮箱的密码，等会登陆会用到
    receiver0 = '419914150@qq.com' 
    # 设置邮件接收人，可以是扣扣邮箱
    receiver1 = '1879230382@qq.com'
    body = '<h1>'+caodate+'</h1><p>zhongfs</p>' 
    # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html') 
    # 设置正文为符合邮件格式的HTML内容
    message = MIMEMultipart() 
    message['subject'] = caodate+'下载附件通知' 
    # 设置邮件标题
    message['from'] = sender  
    # 设置发送人
    message['to'] = receiver0  
    # 设置接收人 
    message.attach(msg)
    filename='xfurlwett-'+caodate+'.txt'
    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="'+filename+'"'
    message.attach(att1)
    try:
	    s = smtplib.SMTP_SSL(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
	    s.login(sender, pwd)  # 登陆邮箱
	    s.sendmail(sender, receiver0, message.as_string())# 发送邮件！
	    #s.sendmail(sender, receiver1, msg.as_string())
	    print ('Done.sent email success')
    except smtplib.SMTPException:
	    print ('Error.sent email fail')
if __name__ == '__main__':
    sentemail()