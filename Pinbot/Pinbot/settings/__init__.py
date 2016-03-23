# coding: utf-8

'''
separate dev settings and production settings
'''
from mongoengine import connect
from mongoengine import register_connection
from settings import *

try:
    from settings_dev import *
except:
    pass

host = OTHER_DATABASE.get('mongo').get('host')
username = OTHER_DATABASE.get('mongo').get('user')
password = OTHER_DATABASE.get('mongo').get('password')
port = OTHER_DATABASE.get('mongo').get('port')
replicaset = OTHER_DATABASE.get('mongo').get('replicaset')
tag_sets = OTHER_DATABASE.get('mongo').get('tag_sets')

if replicaset:
    from pymongo import ReadPreference
    mongo_conn = connect(
        'recruiting',
        host=host,
        replicaSet=replicaset,
        read_preference=ReadPreference.SECONDARY_PREFERRED,
        connectTimeoutMS=30000,
        tag_sets=tag_sets,
    )
else:
    connect('recruiting', host=host, username=username, password=password, port=int(port))

register_connection(**SPIDERS_MONGO)
