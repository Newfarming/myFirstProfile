# coding: utf-8

import codecs
from basic_service.judge_unicode import is_all_number
# user operate a resume

DEFAULT = 0
WATCH_RESUME = 1
DISCARD_RESUME = 2
NEED_ANALYSIS = 9
KEYWORDS_LIST = []

from Pinbot.settings import PROJECT_ROOT

def import_manual_keywords(filename):
    hr_watch_words = []
    hr_watch_lines = codecs.open(filename, 'r', 'utf-8').readlines()

    s = u"""
        央视国际,cctv,斗地主,51wan,5173,7z,突发性,汉龙,阿拉丁,火星时代,yawan,cls168,认真负责,1号店,京东,旗舰店,劲舞团,zhy,奇侠传,图库,jpg,可乐吧,悠贝网,舞侠,9you,9u,wx,taobao,画师,侠客行,王者,技术难题,导购网,go,his,win2000,05,08,用人,tongxue8,风林火山,央视,誓魂,战旗,隔离带,03,布置,网上商城,06,05,08,展会,VIP,PDF,xntywnjg0otk2,xntywnda5mza0,xntywnjgzmdy0,umzuymjmyntey,vampire,参讨,review,2.0,tel,11e0,2002,九天,tips,dl380,专员,米斯,四川省,such,real,03,
    """
    exclude_words = s.split(',')
    
    for line in hr_watch_lines:
        if '.' not in line:
            line = line.strip()
            line = line.lower()
            line = line.split(',')
            
            for word in line:
                # 过滤数字,和除中文,英文的词
                if is_all_number(word)  or (word in exclude_words):
                    line.remove(word)
            hr_watch_words.extend(line)
            
    return  hr_watch_words


KEYWORDS_LIST = import_manual_keywords(PROJECT_ROOT + '/resource/cluster_game_1.4_yuan_yue.txt')
KEYWORDS_SET = set(KEYWORDS_LIST)


DEGREE_LIST = [u'博士', u'硕士', u'研究生', u'双学士', u'学士', u'本科', u'大专', u'专科' u'高中']
SOURCE_DICT = {'zhilian':u"智联", '51job':'51job', 'liepin':u'猎聘', 'headin':u'海丁', 'dajie':u'大街'}




































