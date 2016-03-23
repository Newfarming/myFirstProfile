'''
Created on 2013-11-25

@author: dell
'''
from django.conf.urls import patterns, url

from .views import add_manual_feed_result
from .job_views import (
    ReceiveJobList,
    ResumeUnfit,
)
from app.special_feed.views import (
    SpecialFeedPage,
    EditFeedRemark,
)
from app.special_feed.edit_views import (
    EditFeed,
)

from pin_utils.django_utils import (
    require_staff,
)


urlpatterns = patterns(
    '',
    url(
        r'^receive_resume/$',
        ReceiveJobList.as_view(),
        name='feed-receive-resume',
    ),
    url(
        r'^resume_unfit/(?P<job_id>\d+)/$',
        ResumeUnfit.as_view(),
        name='feed-resume-unfit',
    ),
    url(
        r'^staff_add_resume/$',
        require_staff(add_manual_feed_result),
        name='feed-staff-add-resume',
    ),
    url(
        r'^edit_remarks/(?P<feed_id>\w+)/$',
        EditFeedRemark.as_view(),
        name='feed-edit-remarks',
    ),
    url(
        r'^new/$',
        EditFeed.as_view(),
        name='feed-add-new',
    ),
    url(
        r'^edit/(?P<feed_id>\w+)/$',
        EditFeed.as_view(),
        name='feed-edit-feed',
    ),
)

urlpatterns += patterns(
    'feed.views',
    (r'^group/all$', 'feed_group_ajax', {"feed_id": ""}),
    (r'^group/(?P<feed_id>\w+)', 'feed_group_ajax'),
    url(r'^delete/(?P<feed_id>\w+)', 'feed_delete', name='feed-delete'),
    (r'^get/(?P<feed_id>\w+)/(?P<resume_id>\w+)', 'feed_get'),
    (r'^add_resume', 'add_manual_feed_result'),
    (r'^modify_feed_result', 'modify_feed_result'),
    (r'^send_feed_email', 'send_feed_email'),
    (r'^feed_email/(?P<feed_str>.*)', 'record_feed_email'),
    (r'^modify_frequency', 'modify_send_frequency'),
    (r'feedFrequency','feed_frequency_set'),
    (r'^nopermission','feed_nopermission'),
    url(
        r'^$',
        SpecialFeedPage.as_view(template_name='re_feed_list.html'),
        name='old-feed-page'
    ),
)
