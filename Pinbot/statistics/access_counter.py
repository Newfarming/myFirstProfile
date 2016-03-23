# coding:utf-8
'''
Created on 2013-11-8

@author: likaiguo.happy@gmail.com 2013-11-8 13:08:26
每个页面访问量的统计装饰器
'''
import json
from datetime import datetime
import time
from statistics.models import StatisticsModel, PINBOT_ANALYSE, \
    PINBOT_ANALYSE_REFRESH, GET_ANALYSE_DATA, GET_ANALYSE_DATA_REFRESH



def page_access_counter_dec(page_type_id=0):
    """
    @summary: 页面访问计数器
    @author: likaiguo.happy@gmail.com 2013-11-8 15:51:50
    """
    def _page_access_counter_dec(function):
        
        def __inner_deco(request, page_type_id=page_type_id, *arg, **kw):
            keywords = ''
            url = ''
            if request.method == 'GET':
                p = request.GET.copy()
                if  page_type_id in [PINBOT_ANALYSE, PINBOT_ANALYSE_REFRESH, GET_ANALYSE_DATA, GET_ANALYSE_DATA_REFRESH]:
                    data = request.session.get('data')
                    if request.session.get('is_refresh'):
                        if page_type_id == PINBOT_ANALYSE:
                            page_type_id = PINBOT_ANALYSE_REFRESH
                        elif page_type_id == GET_ANALYSE_DATA:
                            page_type_id = GET_ANALYSE_DATA_REFRESH
                    if data:
                        data = json.loads(data)
                        keywords = data.get('keywords', '')
                        urls = data.get('urls', [])
                        url = ','.join(urls)
                else:
                    keywords = p.get('keywords', '')
                    url = p.get('url', '')
            elif request.method == 'POST':
                p = request.POST.copy()
                if page_type_id == PINBOT_ANALYSE:
                    data = p.get('data')
                    if data:
                        data = json.loads(data)
                        keywords = data.get('keywords', '')
                        urls = data.get('urls', [])
                        url = ','.join(urls)
                else:    
                    keywords = p.get('keywords', '')
                    url = p.get('url', '')
            username = request.user.username
            time_now = time.time()
            statistic_data = StatisticsModel(username=username, page_id=page_type_id, access_time=datetime.now())
            statistic_data.search_keywords = keywords
            statistic_data.url = url
            
            statistic_data.access_url = request.path
            statistic_data.refer_url = request.META.get('HTTP_REFERER', '')
            
            
#             statistic_data.user_agent = request.META.get('HTTP_USER_AGENT ', '')
            
            res = function(request, *arg, **kw)
            
            
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')    
            statistic_data.ip = ip
            statistic_data.cost_time = time.time() - time_now         
            statistic_data.save()
            return res
        return __inner_deco
    
    return  _page_access_counter_dec

if __name__ == '__main__':
    pass
