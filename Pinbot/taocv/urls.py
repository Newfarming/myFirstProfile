'''
Created on 2013-11-25

@author: dell
'''
from django.conf.urls import patterns


urlpatterns = patterns('taocv.views',
    (r'^nopermission','taocv_nopermission'),
    (r'^add_feedback','add_feedback_ajax'),
    (r'^notify_read/(?P<resume_id>\w+)', 'notify_read_ajax'),
    (r'city=(?P<city>.*)','index'),
    (r'^$','index'),
)
