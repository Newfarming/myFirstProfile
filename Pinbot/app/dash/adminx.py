# coding: utf-8


class PinbotDailyReportAdmin(object):
    list_display = (
        'report_date',
        'register_user_count',
        'total_user_count',
        'login_user_count',
        'pay_user_count',
        'total_pay_count',
    )
    list_filter = (
        'report_date',
    )
