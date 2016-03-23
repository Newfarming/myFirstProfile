# encoding: utf-8

from Pinbot.settings import PROJECT_ROOT
import re
# import Config
import jieba
from multiprocessing.pool import job_counter

jieba.load_userdict(PROJECT_ROOT + "/resource/userdict.txt")

from basic import job_keywords_exclude_keywords
from judge_unicode import is_other


SEARCH_KEYWORDS_WEIGHT = 3
SEARCH_JOB_EXTEND_WT = 1
EXTEND_WORDS_WT = 0.5
JOB_RELEATED_WT = 8

from jobs.models import JobKeywords

class input_data:
    """
    @change:  优化
    """
    # 搜索关键词
    key_words = ''
    extend_words = []
    
    def get_extend_words_dict(self, key_words):
        # 根据输入关键词,扩展出相应关键词
        keywords_dict = dict()
        # 最为相关职位
        jobs_dict = {}
        
        search_keywords_list = jieba.cut(key_words.lower())
        
        # 排除的职位
        jobs_exclude_words_dict = {}
        
        
        for i, keyword in enumerate(search_keywords_list):
            keyword = keyword.strip()
            if  keyword == u'游戏' or is_other(keyword) :
#             if is_other(keyword) :
                continue
            
            keyword = keyword.lower()
            keywords_dict[keyword] = SEARCH_KEYWORDS_WEIGHT
            
#             keyword = keyword.replace('+', '\+')
#             keyword = re.escape(keyword) 
#             s = ".*%s.*" % keyword
#             regex = re.compile(s)
            
            
            # 判断是否为一个职位词
            keyword_related_job_dict = job_keywords_exclude_keywords(job_word=keyword)
            # 添加排除掉的职位
            jobs_exclude_words_dict.update(keyword_related_job_dict)

          
            
            
            if keyword_related_job_dict:
                # 如果是职位词则---按照职位词进行处理
                # 职位近义词  -- 权重稍低
                for keyword_job in keyword_related_job_dict:
                    jobs_dict[keyword_job] = JOB_RELEATED_WT - 4
                # 本身是职位,权重较高    
                jobs_dict[keyword] = JOB_RELEATED_WT
            else:
                # 如果不是职位词则用  技能匹配职位--权重稍高
                jobs = JobKeywords.objects.filter(cluster_id__gte=4000,job_category__contains=keyword).order_by("-cluster_id").limit(10) 
                
                for job in  jobs:
                    tags = job.tags.strip()
                    extend_keywords_list = tags.split(',')
                    for extend_keyword in extend_keywords_list:
                        if not keywords_dict.has_key(extend_keyword):
                            keywords_dict[extend_keyword] = SEARCH_JOB_EXTEND_WT
                    job_category = job.job_category.strip()
                    if not jobs_dict.get(job_category):
                        jobs_dict[job_category] = JOB_RELEATED_WT

            # 扩展词
            jobs = JobKeywords.objects.filter(cluster_id__gte=4000,tags__contains=keyword).order_by("-cluster_id").limit(10)
            for job in jobs:
                tags = job.tags.strip()
                extend_keywords_list = tags.split(',')
                for extend_keyword in extend_keywords_list:
                    if not keywords_dict.has_key(extend_keyword):
                        keywords_dict[extend_keyword] = EXTEND_WORDS_WT
                
                job_category = job.job_category.strip()
                
                if not jobs_dict.get(job_category):
                    jobs_dict[job_category] = JOB_RELEATED_WT - 4
        
        # 过滤排除词的job和关键词
        jobs_exclude_words_list = []
        
        

        
        for exclude_words in jobs_exclude_words_dict.values():
            jobs_exclude_words_list.extend(exclude_words)

        # 获取所有职位相关的词
        all_job_dict = job_keywords_exclude_keywords()
        all_jobs_list = all_job_dict.keys()
        jobs_list = jobs_dict.keys()
        jobs_keywords_list = jieba.cut("".join(jobs_list))
        
        jobs_keywords_list = list(jobs_keywords_list)
        jobs_keywords_dict = {}.fromkeys(jobs_keywords_list, JOB_RELEATED_WT - 4)
        jobs_dict.update(jobs_keywords_dict)
        other_exclude_jobs_list = list(set(all_jobs_list) - set(jobs_keywords_list))        
        jobs_exclude_words_list.extend(other_exclude_jobs_list)
        
        # 删除排除词相关的关键词
        keywords_list = keywords_dict.keys()
        for keyword in keywords_dict.keys():
            for exclude_word in jobs_exclude_words_list:
                if exclude_word:
                    if exclude_word in keyword and keywords_dict.get(keyword):
                        try:
                            keywords_dict.pop(keyword)
                        except Exception, e:
                            pass
                else:
                    jobs_exclude_words_list.remove(exclude_word)

                
        # 删除排除词相关的工作
        for keyword in jobs_dict.keys():
            for exclude_word in jobs_exclude_words_list:
                if  exclude_word and jobs_dict.get(exclude_word) and (exclude_word in keyword or keyword in exclude_word):
                    try:
                        jobs_dict.pop(keyword)
                    except Exception, e:
                        pass
        return keywords_dict, jobs_dict     

class input_resume:
    
    def get_resume_dict(self):
        resume_dict = dict()
        return resume_dict
    
if __name__ == "__main__":                    
    input_data().get_extend_words_dict('游戏运营')                
