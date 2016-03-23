# coding:utf-8
from django.conf.urls import patterns

urlpatterns = patterns('statistics.views',
    (r'^data', 'statistic_data'),
    (r'^access', 'view_user_op'),
    (r'^user_feeds', 'view_user_feeds'),
    (r'^feed_result', 'user_feed_result'),
    (r'^get_all_keywords', 'get_all_keywords'),
    (r'^feedback', 'feedback'),
    (r'^manual_reco', 'manual_reco_statis'),
    (r'^get_report','statistic_report'),
    (r'^resume_click','get_recommand_detail'),
)
