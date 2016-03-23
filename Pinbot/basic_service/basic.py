# coding:utf-8
'''
Created on 2013-10-21

@author: likaiguo.happy@163.com
'''
import re
import codecs
import datetime
from Pinbot.settings import PROJECT_ROOT

filename = PROJECT_ROOT + '/resource/job_keyword_exclude_tech_keywords-2013-10-21-1.2.txt'
lines = codecs.open(filename, 'r', 'utf-8').read()
s = u'】'
lines = lines.split(s)
lines = lines[1:-1]
s = u'：'
tmp = u'/'
JOB_RELEATED_WT = 8

def job_keywords_exclude_keywords(job_word=''):


    job_exclude_words_dict = {}
    for line in lines:

        line = line.split()
        job, exclude_words = line[0], line[1]

        if job_word in job:
            jobs = job.split(s)[1].split(tmp)
            try:
                exclude_words = exclude_words.split(s)[1].split(tmp)
            except:
                pass
            for job in jobs:
                job_exclude_words_dict[job] = exclude_words

    return job_exclude_words_dict

def keyword_related_job(job_word=''):

    job_exclude_words_dict = {}
    for line in lines:

        line = line.split()
        job, exclude_words = line[0], line[1]

        if job_word in job:
            jobs = job.split(s)[1].split(tmp)
            try:
                exclude_words = exclude_words.split(s)[1].split(tmp)
            except:
                pass
            for job in jobs:
                job_exclude_words_dict[job] = JOB_RELEATED_WT

    return job_exclude_words_dict


def get_month(start_time, end_time):

    regex = re.compile("\d{1,10}")
    today = datetime.date.today()
    if u'今' in start_time:
        total_month = 0
    elif start_time != '':
        try:
            start_year, start_month = regex.findall(start_time)
        except:
            start_year, start_month = today.year, today.month

        if(u'今' in end_time):
            end_year, end_month = today.year, today.month
        else:
            try:
                end_year, end_month = regex.findall(end_time)
            except:
                end_year, end_month = today.year, today.month
        total_month = (int(end_year) - int(start_year)) * 12 + int(end_month) - int(start_month)
    else:
        total_month = 0
    return total_month


def compare_time(first_time, second_time):
    # 1 behand , 0 equal  -1 before
    """
    @summary: liyao写的一段程序,比较两个时间区间是否重叠,
    @todo: 需要重新修改

    """
    # TODO:2013-12-2 19:21:23

    if not first_time or not second_time:
        return -1

    first_year = 0
    first_month = 0

    second_year = 0
    second_month = 0
    regex = re.compile("\d{1,10}")
    today = datetime.date.today()

    if(u'今' in first_time):
        first_year, first_month = today.year, today.month
    else:
        try:
            first_year, first_month = regex.findall(first_time)
        except:
            first_year, first_month = today.year, today.month


    if(u'今' in second_time  or not second_time):
        second_year , second_month = today.year, today.month
    elif(second_time):
        try:
            second_year , second_month = regex.findall(second_time)
        except:
            second_year , second_month = today.year, today.month

    if int(first_year) > int(second_year):
        return 1
    if int(first_year) == int(second_year):
        if int(first_month) > int(second_month):
            return 1
        else:
            if int(first_month) == int(second_month):
                return 0
            if int(first_month) < int(second_month):
                return -1
    if int(first_year) < int(second_year):
            return -1


def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
                return True
        else:
                return False





if __name__ == '__main__':
    job_keywords_exclude_keywords(job_word='')
