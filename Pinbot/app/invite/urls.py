# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (
    ApplyInviteCode,
    ApplyOperation,
    CheckApplyEmail,
    RedirectApplyCode,
)

from pin_utils.xadmin_utils import XAdminOperationForm


urlpatterns = patterns(
    '',
    url(
        '^$',
        ApplyInviteCode.as_view(),
        name='invite-apply-code',
    ),
    url(
        '^apply_code/$',
        RedirectApplyCode.as_view(),
        name='invite-apply-code-bak',
    ),
    url(
        '^check_apply_email/$',
        CheckApplyEmail.as_view(),
        name='invite-check-apply-email',
    ),
    url(
        '^apply_verify_form/(?P<op_id>\d+)/$',
        XAdminOperationForm.as_view(
            template='xadmin_verify_operation.html'
        ),
        name='invite-apply-verify-form',
    ),
    url(
        '^apply_operation/(?P<apply_id>\d+)/$',
        ApplyOperation.as_view(),
        name='invite-apply-operation',
    ),
    url(
        '^apply_fail_email/$',
        TemplateView.as_view(template_name='apply_fail_email.html'),
    ),
    url(
        '^apply_success_email/$',
        TemplateView.as_view(template_name='apply_success_email.html'),
    ),
    url(
        '^apply_beta_success_email/$',
        TemplateView.as_view(template_name='apply_beta_success_email.html'),
    ),
)
