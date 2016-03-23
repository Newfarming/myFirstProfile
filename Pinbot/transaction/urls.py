# coding: utf-8

from django.conf.urls import patterns, url

from .mark_views import (
    MarkResume,
    MarkNotify,
    ResumeBuyRecordList,
    AdminVerifyRemark,
    RecordMarkChoice,
)
from app.resume.views import center_views

from pin_utils.xadmin_utils import (
    XAdminOperationForm
)


urlpatterns = patterns(
    'transaction.views',
    url(
        r'^bought/(?P<page_curr>\d*)',
        center_views.ResumeCenter.as_view(),
        name='transaction-bought',
    ),
    (r'^addcontactInfo', 'add_contactInfo'),
    (r'^return/secret/(?P<bought_id>\w+)/', 'return_secret_points'),
    (r'^return/(?P<op_type>\w+)/(?P<user_fd_back_id>\w+)/', 'return_points'),
    (r'^buy$', 'buy'),
)

urlpatterns += patterns(
    '',
    url(
        '^mark_resume/(?P<record_id>\d+)/$',
        MarkResume.as_view(),
        name='transaction-mark-resume',
    ),
    url(
        '^mark_notify/$',
        MarkNotify.as_view(),
        name='transaction-mark-notify',
    ),
    url(
        '^unmark_resume/$',
        ResumeBuyRecordList.as_view(
            query='unmark',
        ),
        name='transaction-buy-record',
    ),
    url(
        '^remark_form/(?P<op_id>\d+)/$',
        XAdminOperationForm.as_view(
            template='admin_remark_form.html'
        ),
        name='transaction-admin-remark-form',
    ),
    url(
        '^add_verify_remark/(?P<mark_id>\d+)/$',
        AdminVerifyRemark.as_view(),
        name='transaction-add-verify-remark',
    ),
    url(
        '^record_mark_choice/(?P<record_id>\d+)/$',
        RecordMarkChoice.as_view(),
        name='transaction-record-mark-choice',
    ),
)
