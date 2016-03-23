# coding:utf-8

from django.conf.urls import patterns, url

from views import (
    DownloadResume,
)

from app.resume.views.follow_views import (
    ResumeDetail,
)

urlpatterns = patterns(
    'resumes.views',
    (r'^$', 'resume_watch'),
    (r'^all/(?P<page>\d*)', 'index'),
    (r'^watch/(?P<page>\d*)', 'resume_watch'),
    (r'^discard/(?P<page>\d*)', 'resume_discard'),

    (r'^add_watch/(?P<resume_id>\w+)', 'add_watch'),
    (r'^remove_watch/(?P<resume_id>\w+)', 'remove_watch'),
    (r'^discard_resume/(?P<resume_id>\w+)', 'discard_resume'),

    (r'^add_comment/(?P<resume_id>\w+)', 'add_comment'),
    (r'^get_comments/(?P<resume_id>\w+)/', 'get_comments'),
    (r'^delete_comment/(?P<resume_id>\w+)/(?P<comment_id>\w+)/', 'delete_comment'),

    (r'^get_resumes_state/$', 'get_resumes_state'),
    (r'^addResume$', 'collect_resume'),
    (r'^add_resume', 'collect_resume'),

    (r'^save_to_pinbot', 'save_to_pinbot'),

    (r'^get_parsed_resume', 'get_parsed_resume'),
    url(
        r'^display/(?P<resume_id>\w+)/(?P<resume_score>\d*)',
        ResumeDetail.as_view(),
        name='resume-display-resume'
    ),
    (r'^analyse_resumes', 'analyse_resumes'),
    (r'^get_analyse_data', 'get_analyse_data'),
    (r'^get_processed_count', 'get_processed_count'),

    (r'^add_tag_resume', 'add_resume_tag'),
    (r'^del_tag_resume', 'del_resume_tag'),
    (r'^all_tags', 'get_all_tags'),
    (r'^add_tag_search', 'add_search_tag'),
    (r'^delete_fail_resume', 'delete_fail_resume'),
    (r'^delete_collect_resume', 'delete_collect_resume'),
    (r'^notexistedresume', 'notexistedresume'),

    url(
        r'^download_resume/(?P<download_type>(pdf|html))/(?P<resume_id>.+)/$',
        DownloadResume.as_view(),
        name='resume-download-resume',
    )
)
