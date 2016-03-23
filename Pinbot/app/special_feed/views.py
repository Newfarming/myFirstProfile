# coding: utf-8

import json
import datetime
import logging
import itertools
from bson import json_util

from django.shortcuts import render
from django.views.generic import View
from django.db.models import F
from django.db import transaction

from .feed_utils import (
    CheckRestFeed,
    CheckFeedExpire,
)
from .view_mixin import AdvanceQueryMixin

from app.vip.vip_utils import VipRoleUtils
from feed.views import feed_group_search_ajax
from feed.models import (
    Feed,
    Feed2,
    FeedResult,
    UserReadResume,
    UserFeed2,
    PubFeedData,
    EmailFeedData,
    UserFeed,
)
from resumes.models import (
    ResumeTag,
    UserWatchResume,
    ContactInfoData,
    Comment,
)
from transaction.models import (
    UserChargePackage,
    ResumeBuyRecord,
    DownloadResumeMark,
)
from resumes.helper import mongo_to_dict
from feed_utils import FeedCacheUtils
from pin_utils.django_utils import (
    JsonResponse,
    get_oid,
    get_int,
    str2datetime,
    get_tomommow,
    get_today,
    after7day,
    get_object_or_none,
    update_document,
)
from pin_utils.mixin_utils import (
    LoginRequiredMixin,
    CSRFExemptMixin,
    StaffRequiredMixin,
)
from pin_utils.parse_utils import (
    ParseUtils,
)

from app.task_system.task_finished_judge import look_up_extention

from FeedCelery.celery_utils import CeleryUtils

django_log = logging.getLogger('django')


class SpecialFeedPage(LoginRequiredMixin, View, CheckFeedExpire, CheckRestFeed):
    template_name = 'feed_list.html'

    def get_mysql_userfeed(self, feed):
        str_obj_id = str(feed.id)
        try:
            self.mysql_feed = UserFeed.objects.select_related(
                'user_charge_pkg',
            ).get(
                feed__feed_obj_id=str_obj_id,
                is_deleted=False,
            )
        except UserFeed.DoesNotExist:
            django_log.error('mysql user feed not exists %s' % str_obj_id)
            self.mysql_feed = None
        return self.mysql_feed

    def get_start_time(self, feed):
        if not self.mysql_feed:
            return None

        mysql_feed = self.mysql_feed
        return mysql_feed.user_charge_pkg.start_time if mysql_feed.user_charge_pkg else False

    def get_partner_feed(self):
        if not self.mysql_feed or not self.mysql_feed.user_charge_pkg or not self.mysql_feed.user_charge_pkg.feed_package:
            return False

        if self.mysql_feed.user_charge_pkg.feed_package.name == '人才伙伴订阅':
            return True
        else:
            return False

    def add_unread_count(self, all_feed):
        feed_list = []

        for feed in all_feed:
            if not feed.feed.display:
                continue
            feed_sid = str(feed.feed.id)
            feed.feed.unread_count = len(
                FeedCacheUtils.get_today_cache(feed_sid)
            )
            feed.feed.expire_status = self.feed_expire_status(feed.feed)
            feed.feed.has_expire = self.feed_has_expire(feed.feed)

            self.get_mysql_userfeed(feed.feed)
            feed.feed.start_time = self.get_start_time(feed.feed)
            feed.feed.partner_feed = self.get_partner_feed()
            feed_list.append(feed)
        return feed_list

    def get_all_feed(self):
        user = self.request.user
        all_feed = UserFeed2.objects.filter(
            username=user.username,
            is_deleted=False,
        ).order_by('-add_time').select_related()
        all_feed = self.add_unread_count(all_feed)

        return all_feed

    def get(self, request):
        '''
        兼容接口请求和页面请求
        '''
        ajax_request = request.is_ajax()
        all_feed = self.get_all_feed()
        has_rest_feed = self.has_rest_feed()

        if not all_feed:
            if ajax_request:
                return JsonResponse({
                    'status': 'no_feed',
                    'msg': '没有定制',
                })

            return render(
                request,
                'feed_home_page.html',
                {},
            )

        all_feed_dict = [
            {
                'feed': {
                    'id': str(f.feed.id),
                    'keywords': f.feed.keywords,
                    'salary_min': f.feed.salary_min,
                    'salary_max': f.feed.salary_max,
                    'expect_area': f.feed.expect_area,
                    'talent_level': f.feed.talent_level,
                    'feed_type': f.feed.feed_type,
                    'unread_count': f.feed.unread_count,
                    'expire_status': f.feed.expire_status,
                    'has_expire': f.feed.has_expire,
                    'start_time': f.feed.start_time,
                    'partner_feed': f.feed.partner_feed,
                    'job_type': f.feed.job_type,
                    'title': f.feed.title,
                    'last_click_time': f.feed.last_click_time,
                    'calced': f.feed.calced,
                },
            }
            for f in all_feed
        ]
        current_vip = VipRoleUtils.get_current_vip(request.user)

        data = {
            'all_feed': all_feed_dict,
            'has_rest_feed': has_rest_feed,
            'vip_user': True if current_vip else False,
        }

        if ajax_request:
            return JsonResponse({
                'status': 'ok',
                'data': data,
                'msg': 'ok',
            })

        data_json = json.dumps(data, default=json_util.default)

        return render(
            request,
            self.template_name,
            {
                'data': data_json,
                'all_feed': all_feed,
                'has_rest_feed': has_rest_feed,
            },
        )


class FeedListMixin(object):
    only_fields = []

    def get_query_cond(self):
        return {}

    def get_sort_cond(self):
        return ['-id']

    def get_feed_list(self, feed_id):
        feed_id = get_oid(feed_id)

        if not feed_id:
            return []

        page = get_int(self.request.GET.get('start', '0'))
        if page < 0:
            page = 0

        query_cond = self.get_query_cond()
        query_cond.update({'feed': feed_id})

        feed_result_list = FeedResult.objects(
            resume_source__ne='talent_partner',
            **query_cond
        ).only(*self.only_fields).skip(
            self.page_count * page
        ).limit(
            self.page_count
        ).order_by(
            *self.get_sort_cond()
        ).select_related()

        feed_result_dict_list = []
        for f in feed_result_list:
            try:
                work_years = f.resume.get_work_years()
                feed_dict = mongo_to_dict(f, [])
                feed_result_dict_list.append(feed_dict)
                feed_dict['resume']['work_years'] = work_years
            except AttributeError:
                # 处理由于删除重复简历,导致的推荐结果缺失问题
                django_log.error('resume not exists %s' % f.resume.id)
                continue

        feed_query_count = FeedResult.objects(**query_cond).count()

        tomorrow = get_tomommow()
        total_count = 13 * FeedResult.objects(feed=feed_id).count()
        total_recommend_count = FeedResult.objects(
            feed=feed_id,
            published=True,
            is_recommended=True,
            display_time__lt=tomorrow,
        ).count()

        newest_recommend_count = FeedResult.objects(
            feed=feed_id,
            user_read_status__ne='read',
            published=True,
        ).count()

        return {
            'start': page,
            'next_start': page + 1 if feed_result_dict_list else -1,
            'data': feed_result_dict_list,
            'total_recommend_count': total_recommend_count,
            'total_count': total_count,
            'newest_recommend_count': newest_recommend_count,
            'feed_query_count': feed_query_count,
        }

    def get_latest_edu(self, resume):
        edus = resume.get('educations', [{}])
        sort_edus = sorted([i for i in edus if i], key=lambda x: str2datetime(x.get('start_time')), reverse=True)
        return sort_edus[:1]

    def filter_resume(self, resume):
        filter_resume = {
            'id': resume.get('id', ''),
            'works': resume.get('works', [{}])[:1],
            'gender': resume.get('gender', ''),
            'age': resume.get('age', ''),
            'job_target': resume.get('job_target', {}),
            'address': resume.get('address', ''),
            'work_years': resume.get('work_years', 0),
            'educations': self.get_latest_edu(resume),
            'self_evaluation': resume.get('self_evaluation', ''),
            'is_secret': resume.get('is_secret', False),
            'last_contact': resume.get('last_contact', ''),
            'hr_evaluate': resume.get('hr_evaluate', ''),
            'current_salary': resume.get('current_salary', ''),
            'latest_salary': resume.get('latest_salary', ''),
        }
        return filter_resume


class SpecialFeedList(
        LoginRequiredMixin,
        View,
        AdvanceQueryMixin,
        FeedListMixin,
        CheckFeedExpire):

    page_count = 5
    only_fields = [
        'feed',
        'resume',
        'calc_time',
        'user_read_status',
        'display_time',
        'pub_time',
        'feed_source',
        'tags',
    ]

    def get_query_read_status(self, query_cond):
        read_status = self.request.GET.get('latest', '1')
        if read_status == '1':
            query_cond.update({
                'user_read_status': {'$ne': 'read'},
            })
        return query_cond

    def get_query_send(self, query_cond):
        send = self.request.GET.get('send', '0')
        partner = self.request.GET.get('partner', '0')

        if send == '1':
            query_cond.update({
                'feed_source': 'brick',
            })

        if partner == '1':
            query_cond.update({
                'feed_source': 'talent_partner',
            })

        if partner == '1' and send == '1':
            query_cond.update({
                'feed_source__in': ['talent_partner', 'brick'],
            })

        return query_cond

    def get_query_advance(self, query_cond):
        work_years = self.get_advance_work_years()
        degree = self.get_advance_degree()
        gender = self.get_advance_gender()
        age = self.get_advance_age()
        current_area = self.get_current_area()
        salary = self.get_advance_salary()

        not_query_advance = (
            not work_years
            and not degree
            and not gender
            and not age
            and not current_area
            and not salary
        )
        if not_query_advance:
            return query_cond

        feed_oid = get_oid(self.kwargs.get('feed_id'))
        feed_resumes = list(FeedResult.objects.filter(
            feed=feed_oid,
            published=True,
            is_recommended=True,
        ).order_by('-display_time').limit(500).only('resume').as_pymongo())
        ids_list = [str(i['resume']) for i in feed_resumes]

        search_params = {
            'work_years': work_years,
            'degree': degree,
            'gender': gender,
            'age': age,
            'current_area': current_area,
            'salary': salary,
            'size': 100,
            'ids_list': ','.join(ids_list),
        }
        result = ParseUtils.search_resume(search_params)
        resume_data = result.get('data', {}).get('results', [])

        if result.get('status') != 'ok':
            return query_cond

        query_cond.update({
            'resume__in': [get_oid(i['id']) for i in resume_data if i.get('id')]
        })

        return query_cond

    def query_title_match(self, query_cond):
        title_match = get_int(self.request.GET.get('title_match', 0))
        if not title_match:
            return query_cond
        query_cond.update({'score__cls_score__gte': 50})
        return query_cond

    def query_extend_match(self, query_cond):
        extend_match = get_int(self.request.GET.get('extend_match', 0))
        if not extend_match:
            return query_cond
        query_cond.update({'score__cls_score__lt': 50})
        return query_cond

    def query_reco_time(self, query_cond):
        title_match = get_int(self.request.GET.get('title_match', 0))
        if title_match:
            return query_cond

        reco_time = abs(get_int(self.request.GET.get('reco_time', 0)))
        if not reco_time or reco_time < 0:
            return query_cond

        if reco_time > 30:
            reco_time = 30

        today = get_today()
        start_date = today + datetime.timedelta(days=-reco_time)
        query_cond.update({'display_time__gte': start_date})
        return query_cond

    def get_query_cond(self):
        tomorrow = get_tomommow()
        default_query_cond = {
            'display_time__lt': tomorrow,
            'published': True,
            'is_recommended': True,
        }
        query_cond = self.get_query_read_status(default_query_cond)
        query_cond = self.get_query_send(query_cond)
        query_cond = self.get_query_advance(query_cond)
        query_cond = self.query_extend_match(query_cond)
        query_cond = self.query_title_match(query_cond)
        query_cond = self.query_reco_time(query_cond)
        return query_cond

    def get_sort_cond(self):
        extend_match = get_int(self.request.GET.get('extend_match', 0))
        if extend_match:
            return ['-job_related', '-display_time']
        return ['-display_time', '-job_related']

    def filter_feed(self, feed):
        filter_feed = {
            'id': feed.get('id', ''),
            'keywords': feed.get('keywords', '').replace(u'，', ',').split(','),
        }
        return filter_feed

    def get_resume_watch_list(self, feed_results):
        user = self.request.user
        resume_id_list = [str(i['resume']['id']) for i in feed_results if i.get('resume')]
        resume_watch_list = list(UserWatchResume.objects.filter(
            user=user,
            resume_id__in=resume_id_list,
            type=1,
        ).values_list(
            'resume_id',
            flat=True,
        ))
        return resume_watch_list

    def get_contact_info_mapper(self, feed_results):
        user = self.request.user
        resume_id_list = [str(i['resume']['id']) for i in feed_results if i.get('resume')]
        buy_resume_id_list = list(ResumeBuyRecord.objects.filter(
            resume_id__in=resume_id_list,
            status='LookUp',
            user=user,
        ).values_list('resume_id', flat=True))
        contact_infos = ContactInfoData.objects.filter(
            resume_id__in=buy_resume_id_list,
        ).values(
            'resume_id',
            'name',
            'phone',
            'email',
            'qq',
        )
        contact_mapper = {
            i['resume_id']: i
            for i in contact_infos
        }
        return contact_mapper

    def get_mark_log_mapper(self, feed_results):
        user = self.request.user
        resume_id_list = [str(i['resume']['id']) for i in feed_results if i.get('resume')]

        buy_resume_query = DownloadResumeMark.objects.select_related(
            'buy_record'
        ).prefetch_related(
            'mark_logs',
            'mark_logs__mark',
        ).filter(
            buy_record__resume_id__in=resume_id_list,
            buy_record__user=user,
        )

        mark_log = {
            buy_resume.buy_record.resume_id: [
                {
                    'mark_name': log.mark.name,
                    'mark_time': log.mark_time,
                    'good_result': log.mark.good_result,
                }
                for log in list(buy_resume.mark_logs.all())[::-1][:1]
            ]
            for buy_resume in buy_resume_query
        }
        return mark_log

    def get_comment_info_mapper(self, feed_results):
        user = self.request.user
        resume_id_list = [str(i['resume']['id']) for i in feed_results if i.get('resume')]
        comment_query = list(Comment.objects.filter(
            user=user,
            resume_id__in=resume_id_list,
        ).values(
            'resume_id',
            'content',
            'comment_time',
        ).order_by('-id'))
        comment_info_mapper = {
            key: list(group)[:1]
            for key, group in itertools.groupby(comment_query, lambda x: x['resume_id'])
        }
        return comment_info_mapper

    def filter_feed_result(self, feed_result):
        '''
        过滤定制结果数据，只返回前端需要的字段
        已经保密的简历也需要过滤
        '''
        filter_feed_list = []
        feed_list = feed_result['data']

        resume_watch_list = self.get_resume_watch_list(feed_list)
        contact_info_mapper = self.get_contact_info_mapper(feed_list)
        mark_log_mapper = self.get_mark_log_mapper(feed_list)
        comment_info_mapper = self.get_comment_info_mapper(feed_list)

        for fr in feed_list:
            fr['resume'] = self.filter_resume(fr['resume'])

            # 过滤已经保密的简历
            if fr['resume']['is_secret']:
                continue

            resume_id = fr['resume'].get('id', '')
            fr['feed'] = self.filter_feed(fr['feed'])
            fr['favStatus'] = True if resume_id in resume_watch_list else False
            fr['contact_info'] = contact_info_mapper.get(resume_id, {})
            fr['mark_log'] = mark_log_mapper.get(resume_id, [])
            fr['comment_log'] = comment_info_mapper.get(resume_id, [])

            if (fr.get('tags', {}) or {}).get('keywords', []):
                fr['tags']['keywords'] = list(set([i.lower() for i in fr['tags']['keywords']]))
            filter_feed_list.append(fr)

        feed_result['data'] = filter_feed_list
        return feed_result

    def check_feed_display(self, feed_id):
        username = self.request.user.username
        feed_oid = get_oid(feed_id)

        if not feed_oid:
            return False

        user_feed = UserFeed2.objects(
            username=username,
            feed=feed_oid,
        ).first()
        return user_feed

    def set_feed_time(self, feed_id):
        now = datetime.datetime.now()
        feed_oid = get_oid(feed_id)
        feed_expire_time = after7day()

        Feed2.objects(id=feed_oid).update(
            set__last_click_time=now,
            set__feed_expire_time=feed_expire_time,
        )
        Feed.objects.filter(feed_obj_id=str(feed_id)).update(
            last_click_time=now,
            feed_expire_time=feed_expire_time,
        )
        return True

    def set_display_count(self, feed_result):
        feed_list = feed_result['data']
        feed_result_oid_list = [get_oid(fr['id']) for fr in feed_list if get_oid(fr.get('id'))]
        result = FeedResult.objects(
            id__in=feed_result_oid_list
        ).update(
            inc__display_count=1
        )
        return result

    @look_up_extention
    def get(self, request, feed_id):
        if not self.check_feed_display(feed_id):
            feed_result = {
                'start': 1,
                'next_start': -1,
                'data': [],
                'total_recommend_count': 0,
                'total_count': 0,
                'newest_recommend_count': 0,
            }
            update_cache = []
        else:
            feed_result = self.get_feed_list(feed_id)
            update_cache = FeedCacheUtils.set_cache_expire(feed_id)
            self.set_feed_time(feed_id)
            self.set_display_count(feed_result)

        filter_feed_result = self.filter_feed_result(feed_result)
        result = {
            'status': 'ok',
            'count': 10,
            'update_cache': update_cache,
        }
        result.update(filter_feed_result)
        return JsonResponse(result)


class VerifyFeedList(StaffRequiredMixin, View, FeedListMixin):
    page_count = 10

    def get_query_read_status(self, query_cond):
        read_status = self.request.GET.get('latest', '1')
        if read_status == '1':
            query_cond.update({
                'user_read_status': {'$ne': 'read'},
            })
        return query_cond

    def get_query_manual(self, query_cond):
        manual = self.request.GET.get('is_manual')
        if manual == 'yes':
            query_cond.update({
                "admin": {"$regex": "@"}
            })
        return query_cond

    def get_query_calc_time(self, query_cond):
        if not query_cond.get('calc_time__gt'):
            return query_cond

        calc_time_str = self.request.GET.get('calc_time')
        if not calc_time_str:
            return query_cond

        calc_time = str2datetime(calc_time_str)
        invalid_time = datetime.datetime(1990, 01, 01)

        tomorrow = get_tomommow()
        min_calc_time = tomorrow + datetime.timedelta(days=-15)

        if calc_time == invalid_time:
            calc_time = min_calc_time
        query_cond['calc_time__gt'] = calc_time
        return query_cond

    def get_query_cond(self):
        tomorrow = get_tomommow()
        min_calc_time = tomorrow + datetime.timedelta(days=-30)
        query_meta = {
            'cached': {
                'is_recommended': True,
                'published': {'$ne': True},
                'calc_time__gt': min_calc_time,
            },
            'user': {
                'published': True,
                'display_time__lt': tomorrow,
                'is_recommended': True,
            },
            'tomorrow': {
                'display_time__gte': tomorrow,
                'published': True,
                'is_recommended': True,
            },
            'shield': {
                'is_recommended': False,
                'calc_time__gt': min_calc_time,
            },
            'search_result': {
            },
        }

        view = self.request.GET.get('view', 'cached')
        query_cond = query_meta.get(view, {})
        query_cond = self.get_query_read_status(query_cond)
        query_cond = self.get_query_manual(query_cond)
        query_cond = self.get_query_calc_time(query_cond)
        return query_cond

    def get_sort_cond(self):
        view = self.request.GET.get('view', 'cached')

        if view == 'user':
            return ['-display_time', '-job_related']

        order_job_related = self.request.GET.get('order_by_job', '')
        return ['-calc_time'] if order_job_related != '-job_related' else ['-job_related']

    def search_result(self, feed_id):
        request = self.request
        start = get_int(self.request.GET.get('start', 0))
        read_id_list = UserReadResume.objects.filter(
            user=request.user,
            feed_id=str(feed_id)
        ).values_list('resume_id')
        read_id_list = set([get_oid(res[0]) for res in read_id_list if res])
        return feed_group_search_ajax(start, feed_id, read_id_list)

    def add_tag_feed_result(self, feed_result):
        feed_list = feed_result['data']

        for fr in feed_list:
            resume_tags = ResumeTag.objects.filter(
                resume_id=fr['resume']['id'],
                status='new',
            )
            fr['fr_tags'] = fr['tags']
            fr['tags'] = [
                {'tag_id': tag.tag_id, 'tag': tag.tag_content}
                for tag in resume_tags
            ]
        return feed_result

    def filter_feed(self, feed_results):
        feed_list = feed_results['data']

        show_feed = []
        for fr in feed_list:
            fr['feed']['keywords'] = fr['feed'].get('keywords', '').replace(u'，', ',').split(',')
            if fr['resume']['is_secret'] and not fr['published']:
                continue
            show_feed.append(fr)

        feed_results['data'] = show_feed
        return feed_results

    def get_page_count(self):
        limit = get_int(self.request.GET.get('limit', 0))
        self.page_count = limit if limit else self.page_count
        return self.page_count

    def get(self, request, feed_id):
        view = self.request.GET.get('view', 'cached')
        if view == 'search_result':
            return self.search_result(feed_id)

        self.get_page_count()
        feed_result = self.get_feed_list(feed_id)
        feed_result = self.filter_feed(feed_result)
        feed_result = self.add_tag_feed_result(feed_result)

        result = {
            'status': 'ok',
            'count': 10,
            'feed_result_count': 80,
            'newest_recommend_count': 0,
            'unread_resumes_all_count': 10,
        }
        result.update(feed_result)
        return JsonResponse(result)


class PublishFeedResult(StaffRequiredMixin, CSRFExemptMixin, View):

    def convert_display_time(self, display_time_str):
        display_time = str2datetime(display_time_str)

        if not display_time:
            default_display_time = get_tomommow()
            return default_display_time

        # 展示时间只需要精确到天
        # 同一天的推荐结果需要按job_related排序
        display_time = datetime.datetime(
            display_time.year,
            display_time.month,
            display_time.day,
        )
        return display_time

    def add_pub_data(self, feed_oid, resume_oids, display_time):
        if not resume_oids:
            return False

        today = get_today()
        tomorrow = get_tomommow()

        feed = Feed2.objects(id=feed_oid)[0]
        email = feed.username
        pub_admin = self.request.user.username

        pub_feed = PubFeedData.objects(
            feed=feed_oid,
            pub_time__gte=today,
            pub_time__lt=tomorrow,
        ).first()
        if pub_feed:
            if display_time == tomorrow:
                update_kwargs = {
                    'set__display_time': tomorrow,
                }
            else:
                update_kwargs = {}

            PubFeedData.objects(
                feed=feed_oid,
                pub_time__gte=today,
                pub_time__lt=tomorrow,
            ).update(
                set__pub_admin=pub_admin,
                add_to_set__resumes=resume_oids,
                **update_kwargs
            )
        else:
            pub_feed = PubFeedData(
                email=email,
                pub_admin=pub_admin,
                feed=feed_oid,
                resumes=resume_oids,
                pub_time=datetime.datetime.now(),
                display_time=display_time,
            )
        pub_feed.save()
        return True

    def add_email_data(self, feed_oid, resume_oids):
        if not resume_oids:
            return False

        feed = Feed2.objects(id=feed_oid)[0]
        email = feed.username
        pub_admin = self.request.user.username

        email_feed = EmailFeedData.objects(
            feed=feed_oid,
            is_send=False,
        ).first()

        if email_feed:
            EmailFeedData.objects(
                feed=feed_oid,
                is_send=False,
            ).update(
                set__pub_admin=pub_admin,
                add_to_set__resumes=resume_oids,
            )
        else:
            email_feed = EmailFeedData(
                email=email,
                pub_admin=pub_admin,
                feed=feed_oid,
                resumes=resume_oids,
            )
        email_feed.save()
        return True

    def publish_all(self, request):
        username = request.POST.get('username')
        display_time_str = request.POST.get('pub_time', '')

        user_feeds = UserFeed2.objects(
            username=username,
            is_deleted=False,
        ).select_related()

        if not user_feeds:
            return JsonResponse({
                'status': 'error',
                'msg': u'没有查到用户%s的相关订阅' % username,
            })

        now = datetime.datetime.now()
        display_time = self.convert_display_time(display_time_str)
        total_count = 0

        for user_feed in user_feeds:
            feed_id = user_feed.feed.id
            feed_results = FeedResult.objects(
                feed=feed_id,
                is_recommended=True,
                published=False,
            ).select_related()
            resume_oids = [fr.resume.id for fr in feed_results]

            # 添加cls_score，如果没有这个字段设置为100
            FeedResult.objects(
                feed=feed_id,
                is_recommended=True,
                published=False,
                score__cls_score=None,
            ).update(
                set__score__cls_score=100
            )

            # 发布推荐结果
            FeedResult.objects(
                feed=feed_id,
                is_recommended=True,
                published=False,
            ).update(
                set__published=True,
                set__display_time=display_time,
                set__pub_time=now,
            )

            self.add_pub_data(feed_id, resume_oids, display_time)
            self.add_email_data(feed_id, resume_oids)
            FeedCacheUtils.add_feed_id_update_cache(feed_id)

            total_count += len(resume_oids)

        return JsonResponse({
            'status': 'ok',
            'msg': u'已成功发布%s条订阅' % total_count,
        })

    def post(self, request):
        publish_all = request.POST.get('publish_all')
        if publish_all:
            return self.publish_all(request)

        feed_sid = request.POST.get('feed_id', '')
        resume_sids = request.POST.getlist('resume_ids[]', [])
        display_time_str = request.POST.get('pub_time', '')

        feed_id = get_oid(feed_sid)

        if not feed_id:
            return JsonResponse({
                'status': 'error',
                'msg': u'没有订阅',
            })

        if not resume_sids:
            return JsonResponse({
                'status': 'error',
                'msg': u'请选择要发布的简历',
            })

        now = datetime.datetime.now()
        display_time = self.convert_display_time(display_time_str)
        resume_oids = [get_oid(resume_id) for resume_id in resume_sids]
        admin = request.user

        # 发布数据
        FeedResult.objects(
            feed=feed_id,
            resume__in=resume_oids,
        ).update(
            set__published=True,
            set__display_time=display_time,
            set__pub_time=now,
            set__publisher=admin.username,
        )

        # 添加cls_score，如果没有这个字段设置为100
        FeedResult.objects(
            feed=feed_id,
            resume__in=resume_oids,
            score__cls_score=None,
        ).update(
            set__score__cls_score=100,
        )

        self.add_pub_data(feed_id, resume_oids, display_time)
        self.add_email_data(feed_id, resume_oids)
        FeedCacheUtils.add_feed_id_update_cache(feed_sid)

        return JsonResponse({
            'status': 'ok',
            'msg': u'已成功发布%s条订阅' % len(resume_oids),
        })


class ResetFeedExpireTime(LoginRequiredMixin, View, CheckFeedExpire):

    def is_malice_user(self, feed_id):
        username = self.request.user.username
        feed_oid = get_oid(feed_id)

        user_feed = UserFeed2.objects(
            username=username,
            feed=feed_oid,
            is_deleted=False,
        )
        return False if user_feed else True

    def get(self, request, feed_id):
        if self.is_malice_user(feed_id):
            return JsonResponse({
                'status': 'error',
                'msg': u'你的请求有误，查询失败',
            })

        feed_oid = get_oid(feed_id)
        user_feed = UserFeed2.objects(
            feed=feed_oid,
            is_deleted=False,
        ).first()

        if not (user_feed and self.feed_expire_status(user_feed.feed)):
            return JsonResponse({
                'status': 'ok',
                'msg': u'订阅未过期，不需要重置'
            })
        feed_expire_time = after7day()
        Feed2.objects(id=feed_oid).update(
            set__feed_expire_time=feed_expire_time
        )
        Feed.objects.filter(feed_obj_id=feed_id).update(
            feed_expire_time=feed_expire_time
        )
        CeleryUtils.user_feed_task(feed_id)

        return JsonResponse({
            'status': 'ok',
            'msg': u'设置成功',
        })


class GetRestFeed(LoginRequiredMixin, View, CheckRestFeed):

    def get(self, request):
        has_rest_feed = self.has_rest_feed()

        return JsonResponse({
            'status': 'ok' if has_rest_feed else 'error',
            'has_rest_feed': has_rest_feed,
        })


class RenewalFeed(LoginRequiredMixin, View, CheckRestFeed):

    def feed_not_expire(self, feed_oid):
        now = datetime.datetime.now()
        feed = Feed2.objects(
            id=feed_oid,
            username=self.request.user.username,
            expire_time__gt=now,
        )
        return True if feed else False

    def renewal_feed(self, feed_oid):
        feed_id = str(feed_oid)
        user = self.request.user
        now = datetime.datetime.now()

        user_charge_pkg = UserChargePackage.objects.filter(
            user=user,
            feed_end_time__gte=now,
            pay_status='finished',
            rest_feed__gt=0,
            pkg_source=1,
        )[0]
        mongo_feed = Feed2.objects(
            id=feed_oid
        ).first()
        mysql_feed = get_object_or_none(
            Feed,
            feed_obj_id=feed_id,
        )
        old_mongo_user_feed = UserFeed2.objects(
            feed=mongo_feed,
            username=user.username,
            is_deleted=False,
        ).first()

        expire_time = user_charge_pkg.feed_end_time

        mongo_feed.expire_time = expire_time
        mysql_feed.expire_time = expire_time

        mysql_user_feed = UserFeed(
            feed=mysql_feed,
            user=user,
            user_charge_pkg=user_charge_pkg,
            add_time=now,
            expire_time=expire_time,
        )

        mongo_user_feed = UserFeed2(
            username=user.username,
            feed=mongo_feed,
            expire_time=expire_time,
            read_id_list=old_mongo_user_feed.read_id_list,
            read_count=old_mongo_user_feed.read_count,
        )

        with transaction.atomic():
            result = UserChargePackage.objects.filter(
                id=user_charge_pkg.id,
                rest_feed__gt=0,
            ).update(rest_feed=F('rest_feed') - 1)

            if result:
                UserFeed2.objects(
                    feed=mongo_feed,
                    is_deleted=False,
                    username=user.username,
                ).update(set__is_deleted=True)

                mongo_feed.save()
                mongo_user_feed.save()

                UserFeed.objects.filter(
                    feed=mysql_feed,
                    is_deleted=False,
                    user=user,
                ).update(is_deleted=True)

                mysql_feed.save()
                mysql_user_feed.save()

        return True

    def get(self, request, feed_id):
        feed_oid = get_oid(feed_id)
        if not feed_oid:
            return JsonResponse({
                'status': 'data_error',
                'msg': u'没有找到相关数据',
            })

        if self.feed_not_expire(feed_oid):
            return JsonResponse({
                'status': 'not_expire',
                'msg': '订阅未过期，不需要续期'
            })

        has_rest_feed = self.has_rest_feed()
        if not has_rest_feed:
            return JsonResponse({
                'status': 'no_rest_feed',
                'msg': u'没有剩余订阅，请先购买',
            })

        self.renewal_feed(feed_oid)

        return JsonResponse({
            'status': 'ok',
            'msg': u'续期已成功',
        })


class EditFeedRemark(StaffRequiredMixin, View):

    def post(self, request, feed_id):
        feed_id = get_oid(feed_id)
        username = request.user.username
        now = datetime.datetime.now()

        update_data = json_util.loads(request.body)

        for r in update_data.get('remarks', []):
            if not r.get('username'):
                r['username'] = username
            if not r.get('op_time'):
                r['op_time'] = now
            r['necessary_keywords'] = r.get('necessary_keywords', '').split() if r.get('necessary_keywords', '') else []
            r['exclude_job_keywords'] = r.get('exclude_job_keywords', '').split() if r.get('exclude_job_keywords', '') else []
            r['latent_semantic_keywords'] = r.get('latent_semantic_keywords', '').split() if r.get('latent_semantic_keywords', '') else []

        feed_query = Feed2.objects.filter(
            id=feed_id,
        )
        if feed_query:
            feed = feed_query[0]
            update_feed = update_document(
                feed,
                ignored=update_data.get('ignored', False),
                remarks=update_data.get('remarks'),
            )
            update_feed.save()

        return JsonResponse({
            'status': 'ok',
            'msg': '保存成功',
        })
