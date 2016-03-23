# coding: utf-8


class DailyReportAdmin(object):

    list_display = (
        'report_date',
        'code_count',
        'register_user_count',
        'total_user_count',
        'login_user_count',
        'login_percent',
        'reco_job_count',
        'check_job_count',
        'favour_job_count',
        'send_job_count',
        'dislike_job_count',
        'refresh_job_count',
        'favour_company_count',
    )
    list_filter = (
        'report_date',
    )


class WeekReportAdmin(object):

    list_display = (
        'start_date',
        'end_date',
        'code_count',
        'code_chain',
        'register_user_count',
        'register_user_chain',
        'total_user_count',
        'total_user_chain',
        'login_user_count',
        'login_user_chain',
        'login_percent',
        'remain_user_percent',
        'reco_job_count',
        'reco_job_chain',
        'check_job_count',
        'check_job_chain',
        'favour_job_count',
        'favour_job_chain',
        'send_job_count',
        'send_job_chain',
        'dislike_job_count',
        'dislike_job_chain',
        'refresh_job_count',
        'refresh_job_chain',
        'favour_company_count',
        'favour_company_chain',
    )
    list_filter = (
        'start_date',
        'end_date',
    )
