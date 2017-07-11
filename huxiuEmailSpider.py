import urllib
from urllib import request
from bs4 import BeautifulSoup
import ssl
import threading
import smtplib
from email.mime.text import MIMEText


def huxiu(content):
    context=ssl._create_unverified_context()

    url="https://www.huxiu.com/story/index"
    request=urllib.request.Request(url)
    respone=urllib.request.urlopen(request,context=context)
    Soup=BeautifulSoup(respone,"html.parser")
    names=Soup.select("body > div.story-container > div > ul > li > p")
    times=Soup.select("body > div.story-container > div > ul > li > div.story-list-author > p")
    sketchs=Soup.select("body > div.story-container > div > ul > li > div.story-list-detail > p")
    urls=Soup.select("body > div.story-container > div > ul > li > div.story-list-detail > p > a")
    for name,time,sketch,url in zip(names,times,sketchs,urls):
        date={
            '简述':sketch.get_text(),
            '短文名':name.get_text(),
            '链接':url['href'],        
            '距离现在时间':time.get_text()                 
            }
        temp="短文名：%(短文名)s\n简述：%(简述)s\n距离现在时间：%(距离现在时间)s\n链接：%(链接)s\n"
        a=temp%date+"\n"
        content+=a
    return content

def mail(content):
    _user ="beckysimpson@163.com"
    _pwd ="a939194640"
    _to ="939194640@qq.com"

    msg=MIMEText(content)
    msg["Subject"]="虎嗅短文每日推送"
    msg["From"]=_user
    msg["To"]=_to

    try:
        s=smtplib.SMTP_SSL("smtp.163.com",465)
        s.login(_user,_pwd)
        s.sendmail(_user,_to,msg.as_string())
        s.quit()
        print("成功")
    except smtplib.SMTPException:
        print("Error:无法发送邮件")

def fun_timer():
    b=''
    c=huxiu(b)
    mail(c)
    global timer
    timer=threading.Timer(43200,fun_timer)
    timer.start()
timer=threading.Timer(35520,fun_timer)
timer.start()