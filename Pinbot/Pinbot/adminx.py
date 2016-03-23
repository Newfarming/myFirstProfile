# coding:utf-8

import xadmin
from xadmin.layout import *

from xadmin import views


class UserSettingsAdmin(object):
    model_icon = 'cog'


class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "欢迎使用Pinbot后台管理系统!",
                "content": "<h3> 欢迎使用Pinbot后台管理系统! </h3>"},
            {"type": "chart", "model": "app.accessrecord", 'chart': 'user_count', 'params': {
                '_p_date__gte': '2013-01-08', 'p': 1, '_p_date__lt': '2013-01-29'}},
            {"type": "list", "model": "app.host", 'params': {
                'o': '-guarantee_date'}},
        ],
    ]

# Pinbot后台首页
pinbot_index_view = views.website.IndexView
pinbot_index_view.site_title = "Pinbot Admin"
xadmin.site.register(pinbot_index_view, MainDashboard)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)


class MailboxAdmin(object):
    list_display = ('name', 'company_name', 'phone')
    model_icon = 'cog'




from transaction.models import *
from pinbot_package.models import *
xadmin.site.register(FeedService, FeedServiceAdmin)

xadmin.site.register(ResumePackge, ResumePackgeAdmin)
xadmin.site.register(UserChargePackage, UserChargePackageAdmin)

from transaction.models import *

from taocv.models import *
xadmin.site.register(UserResumeFeedback, UserResumeFeedbackAdmin)
xadmin.site.register(TaocvConfig, TaocvConfigAdmin)

from basic_service.models import EmailSendLog, EmailSendLogAdmin
xadmin.site.register(EmailSendLog, EmailSendLogAdmin)

from jobs.models import Company, Job, HunterInterest, JobAdmin, HunterInterestAdmin
xadmin.site.register(Job, JobAdmin)
xadmin.site.register(HunterInterest, HunterInterestAdmin)
