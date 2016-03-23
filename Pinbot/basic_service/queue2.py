# coding:utf-8
import thread
import pika
import sys
import json
from Pinbot.settings import OTHER_DATABASE
import threading

credentials = pika.PlainCredentials(OTHER_DATABASE.get('rabbitmq').get('user'), OTHER_DATABASE.get('rabbitmq').get('password'))
connection = pika.BlockingConnection(pika.ConnectionParameters(credentials=credentials, host=OTHER_DATABASE.get('rabbitmq').get('host')))

channel = connection.channel()
channel.queue_declare(queue=OTHER_DATABASE.get('rabbitmq').get('html_resume_queue'), durable=True)


buy_resume_channel = connection.channel()  # 购买简历的rabbitmq消息队列
buy_resume_channel.queue_declare(queue=OTHER_DATABASE.get('rabbitmq').get('buy_resume_queue'), durable=True)


mutex = threading.Lock()
