# coding=utf-8
from selenium import webdriver
import random
import smtplib
from email.mime.text import MIMEText  # 引入smtplib和MIMEText
from time import sleep 
import time
import json

sleep(random.randint(6, 10))

driver = webdriver.Firefox()
driver.get("http://10.161.10.72:10007/login.html")

#usernames=['zhongfs','songwy','guowei','guoxj']
#passwds=['7094','9195','6163','6731']
usernames=[]
passwds=[]
def getuserinfo():
    f = open("userinfo.json",encoding='utf-8')
    setting = json.load(f)
    useraccount=setting['useraccount']
    for i in range(len(useraccount)):
        usernames.append(useraccount[i]['username'])
        passwds.append(useraccount[i]['passwd'])
    print(usernames)
    print(passwds)

def login(username,passwd):  
    #为了for循环，每个用户退出后，重新获得页面  
    now_handle = driver.current_window_handle
    driver.switch_to_window(now_handle)
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("pass").clear()
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("pass").send_keys(passwd)
	#登陆
    driver.find_element_by_css_selector("button.btn.btn-primary.btn-sm.btn-block.btn-extra").click()
    #获取登录之后的页面
    now_handle = driver.current_window_handle
    driver.switch_to_window(now_handle)
    #点击运维用户管理
    driver.find_element_by_css_selector("a.first-menu.collapsed").click()
	#点击员工正常签到
    driver.find_element_by_id("sign").click()
    
    now_handle = driver.current_window_handle
    print(now_handle)
    driver.switch_to_window(now_handle)
	#点击确定
    driver.find_element_by_id("userNormalSignNoticeBtn").click()
    sleep(2)
    now_handle = driver.current_window_handle
    driver.switch_to_window(now_handle)
    #driver.find_element_by_css_selector("div.just-qiandao.qiandao-sprits.actived").click()
    #driver.find_element_by_css_selector("div.just-qiandao.qiandao-sprits").click()
    #sleep(5)
    driver.find_element_by_xpath(".//*[@id='js-just-qiandao']").click()
    sleep(3)
    now_handle = driver.current_window_handle
    driver.switch_to_window(now_handle)
    driver.find_element_by_xpath(".//*[@id='commonModal']/div/div/div[3]/button").click()
    sleep(3)
    now_handle = driver.current_window_handle
    driver.switch_to_window(now_handle)
    #driver.find_element_by_xpath(".//*[@id='container']/div[1]/div/div[2]/ul/li[3]/a").click()
    #/html/body/div[1]/div[1]/div/div[2]/ul/li[3]/a
    sleep(3)
    now_handle = driver.current_window_handle
    driver.switch_to_window(now_handle)
    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/ul/li[7]/a").click()
    sleep(3)
    now_handle = driver.current_window_handle
    driver.switch_to_window(now_handle)
    driver.find_element_by_xpath(".//*[@id='logout']").click()    
    #driver.close()
    #now_handle = driver.current_window_handle
    #driver.switch_to_window(now_handle)
    #driver.find_element_by_partial_link_text("退出").click()
    #sleep(2)
    #driver.find_element_by_css_selector("i.fa.fa-sign-out").click()

    #driver.find_element_by_css_selector("button.btn.btn-sm.btn-default").click()
    #now_handle = driver.current_window_handle
    #driver.switch_to_window(now_handle)
    #driver.find_element_by_css_selector("btn.btn-sm.btn-primary").click()
    #driver.find_element_by_id("logout").click()
    
def sentemail():
    host = 'smtp.163.com'  # 设置发件服务器地址
    port = 465  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
    sender = 'a419914150@163.com'  # 设置发件邮箱，一定要自己注册的邮箱
    pwd = 'B8b322927'  # 设置发件邮箱的密码，等会登陆会用到
    receiver = '419914150@qq.com' # 设置邮件接收人，可以是扣扣邮箱
    receiver1 = '1879230382@qq.com'
    body = '<h1>你已成功打卡</h1><p>zhongfs</p>' # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html') # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = '打卡通知' # 设置邮件标题
    msg['from'] = sender  # 设置发送人
    msg['to'] = receiver  # 设置接收人
    try:
	    s = smtplib.SMTP_SSL(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
	    s.login(sender, pwd)  # 登陆邮箱
	    s.sendmail(sender, receiver, msg.as_string())# 发送邮件！
	    s.sendmail(sender, receiver1, msg.as_string())
	    print ('Done.sent email success')
    except smtplib.SMTPException:
	    print ('Error.sent email fail')

if __name__ == '__main__':
    getuserinfo()
    for i in range(len(usernames)):
        login(usernames[i],passwds[i])
        print(random.randint(1, 10))
        sleep(random.randint(2, 10))
    driver.close()
    sentemail()



