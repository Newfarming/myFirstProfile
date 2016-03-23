# coding: utf-8

from django.conf.urls import patterns, url
from views.template import (
    AddEmailTemplate,
    AddEmailTemplateCategory,
    EditEmailTemplateCategory,
    EditEmailTemplate,
    GetEmailTemplate
)
from views.email import (
    SendEmail,
    SendSms
)

from views.tags import (
    AddTag,
    EditTag,
    DeleteTag
)

urlpatterns = patterns(
    '',
    url(
        '^add_tpl/$',
        AddEmailTemplate.as_view(),
        name='sendemail-add-template',
    ),
    url(
        '^add_tpl_category/$',
        AddEmailTemplateCategory.as_view(),
        name='sendemail-add-template-category'
    ),
    url(
        '^edit_tpl_category/(?P<cid>.+)/$',
        EditEmailTemplateCategory.as_view(),
        name='sendemail-edit_template-category'
    ),
    url(
        '^edit_tpl/(?P<tpl_id>.+)/$',
        EditEmailTemplate.as_view(),
        name='sendemail-edit-template'
    ),
    url(
        '^send/$',
        SendEmail.as_view(),
        name='sendemail-send_email'
    ),
    url(
        '^get_tpl/(?P<tpl_id>.+)/$',
        GetEmailTemplate.as_view(),
        name='sendemail-get-tpl'
    ),
    url(
        '^add_tag/$',
        AddTag.as_view(),
        name='sendemail-add-tag'
    ),
    url(
        '^edit_tag/(?P<tag_id>.+)/$',
        EditTag.as_view(),
        name='sendemail-edit-tag'
    ),
    url(
        '^del_tag/$',
        DeleteTag.as_view(),
        name='sendemail-del-tag'
    ),
    url(
        '^send_sms/$',
        SendSms.as_view(),
        name='sendemail-sms'
    ),
)
