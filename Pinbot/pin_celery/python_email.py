# coding:utf-8
'''
发送html文本邮件
'''
import smtplib  
from email.mime.text import MIMEText
import time
from django.template.loader import render_to_string
from models import MarketEmailSendDetail
from datetime import datetime
   
EMAILS_CONFIG = {               
               'hello@hopperclouds.com':{'USER':'hello@hopperclouds.com',
                         'PASSWORD':'asd123123',
                         'HOST':'smtp.qq.com',
                         'FORM_EMAIL':'hello@hopperclouds.com',
                         'TLS':False,
                         'PORT':25},
               'hr@hopperclouds.com':{'USER':'hr@hopperclouds.com',
                         'PASSWORD':'asd123123',
                         'HOST':'smtp.qq.com',
                         'FORM_EMAIL':'hr@hopperclouds.com',
                         'TLS':False,
                         'PORT':25},
               }
EMAILS = ['hello@hopperclouds.com','hr@hopperclouds.com']
  
def get_connection(host,username,password):
    """
    @summary:服务器连接
    """
    connection = smtplib.SMTP()  
    connection.connect(host)  #连接smtp服务器
    connection.login(username,password)  #登陆服务器
    return connection
  
def send_email(connection,subject, message, from_email, to_email):
    msg = MIMEText(message,_subtype='html',_charset='gb2312')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = subject    #设置主题
    msg['From'] = from_email
    msg['To'] = to_email
    try:  
        result = connection.sendmail(from_email, to_email, msg.as_string())  #发送邮件
        return True,''
    except Exception, e:  
        return False,str(e)
 
def send_mass_email(to_list,subject,message,from_email='pinbot@hopperclouds.com'):
    i = 0
    connection1 = None
    connection2 = None
    connection = None
    from_email = ''
    for email in to_list:
        if i == 0:
            connection1 = get_connection(host="smtp.qq.com",username="hello@hopperclouds.com",password="asd123123")
            from_email = 'hello@hopperclouds.com'
            connection = connection1
        elif i == 491:
            connection.close()
            connection2 = get_connection(host="smtp.qq.com",username="hr@hopperclouds.com",password="asd123123")
            connection = connection2
            from_email = 'hr@hopperclouds.com'
        
        details = MarketEmailSendDetail()
        details.send_time = datetime.now()
        details.from_email = from_email
        details.subject = subject
        details.to_email = email
        details.save()
        
        token = str(details.id)
        message = message.replace("pinbot_token",token)
         
        result,info = send_email(connection,subject, message, from_email, email)
        details.status = result
        details.error_info = info
        details.save()
        
        i += 1
        time.sleep(8)
        
    connection.close()
