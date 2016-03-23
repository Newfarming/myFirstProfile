# coding: utf-8
'''
Created on 2014-2-20

@author: root
@summary:  提供邮件服务的接口
'''
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import get_connection
from models import *
import datetime


ADMINS_EMAILS = {'pinbot@hopperclouds.com':{'USER':'pinbot@hopperclouds.com',
                           'PASSWORD':'hopper2013',
                           'HOST':'smtp.qq.com',
                           'FORM_EMAIL':'pinbot@hopperclouds.com',
                           'TLS':False,
                           'PORT':25},
                 
                 'hello@hopperclouds.com':{'USER':'hello@hopperclouds.com',
                           'PASSWORD':'asd123123',
                           'HOST':'smtp.qq.com',
                           'FORM_EMAIL':'hello@hopperclouds.com',
                           'TLS':False,
                           'PORT':25},
                 
                 'pinbot_xiaoyi@hopperclouds.com':{'USER':'pinbot_xiaoyi@hopperclouds.com',
                           'PASSWORD':'asd123123',
                           'HOST':'smtp.qq.com',
                           'FORM_EMAIL':'pinbot_xiaoyi@hopperclouds.com',
                           'TLS':False,
                           'PORT':25},
                 }

def email_connect(email):
    if not email in ADMINS_EMAILS:
        return False,'from_email is not in admins'
    else:
        auth_password = ADMINS_EMAILS[email]['PASSWORD']
        fail_silently = False
        return True,get_connection(username=email,
                                    password=auth_password,
                                    fail_silently=fail_silently)

def load_template(subject_file,message_file,subject_dict=None,message_dict=None):
    subject = render_to_string(subject_file,subject_dict)  
    message = render_to_string(message_file,message_dict)
    subject = ''.join(subject.splitlines())
    return subject,message

def send_one_email(subject, message, from_email, email,
               connection=None,type="html"):
    if not from_email in ADMINS_EMAILS:
        return False,'from_email is not in admins'
    if not isinstance(email, list) and not isinstance(email,tuple):
        recipient_list = list()
        recipient_list.append(email)
    else:
        recipient_list = recipient_list
    try:
        ret = send_mail(subject=subject,message=message,from_email=from_email,\
                  fail_silently=recipient_list,auth_user=ADMINS_EMAILS[from_email]['USER'],\
                  auth_password=ADMINS_EMAILS[from_email]['PASSWORD'],connection=connection,type=type)
        
        email_log = EmailSendLog()
        email_log.from_email = from_email
        email_log.send_time = datetime.datetime.now()
        email_log.subject = subject
        to_emails = ''
        for to_email in recipient_list:
            to_emails += to_email 
        email_log.to_email = to_emails
        email_log.status = 'success'
        email_log.save()
    except Exception , IntegrityError:
        email_log = EmailSendLog()
        email_log.from_email = from_email
        email_log.send_time = datetime.datetime.now()
        email_log.subject = subject
        to_emails = ''
        for to_email in recipient_list:
            to_emails += to_email 
        email_log.to_email = to_emails
        email_log.status = 'fail'
        email_log.error_info = str(IntegrityError)
        email_log.save()
        
        return False, str(IntegrityError)
        
    return True, ''



def send_mail(subject=None, message=None, from_email=None, recipient_list=None,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None,type="html"):
    """
    发送单封邮件
    """
    connection = connection or get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    msg = EmailMessage(subject, message, from_email, recipient_list,
                        connection=connection)
    msg.content_subtype = type
    return msg.send()


def send_mass_mail(datatuple, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):
    """
    发送大量邮件,每封邮件的具体信息存放在datatuple中
    """
    connection = connection or get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    messages = [EmailMessage(subject, message, sender, recipient,
                             connection=connection)
                for subject, message, sender, recipient in datatuple]
    return connection.send_messages(messages)

# connect = email_connect('hello@hopperclouds.com')
# send_one_email(connection=connect,subject='test',message='test',from_email='hello@hopperclouds.com',email='liyao@hopperclouds.com')
