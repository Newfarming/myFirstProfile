# coding:utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'
from resumes.models import ContactInfoData
def find_dup_contactinfo():
    existed_ids = set()
    contacts = ContactInfoData.objects.filter(resume_id=None).values('resume_id')
    for contact in contacts:
        if contact['resume_id'] in existed_ids:
            print contact['resume_id']
        else:
            existed_ids.add(contact['resume_id'])

def find_not_related_job():
    from Brick.App.job_hunting.models import RecommendJob
    from feed.models import Feed,UserFeed,Feed2,UserFeed2
    from bson import ObjectId
    jobs_set = set()
    not_related_jobs = Feed.objects.filter(is_related=False).values('id')
    for job in not_related_jobs:
        jobs_set.add(job['id'])
    
    can_not_delete = RecommendJob.objects.filter(read_status='read',action__in=['favorite','send','dislike'],job_id__in=jobs_set).values('job_id').distinct()
    
    can_not_delete_jobid = set()
    for job in can_not_delete:
        can_not_delete_jobid.add(job['job_id'])
    
    need_to_delete = jobs_set - can_not_delete_jobid
    print len(need_to_delete)
    print len(can_not_delete_jobid)
    i = 0
    for job_id in need_to_delete:
        print i
        i += 1
        recommends = RecommendJob.objects.filter(job_id=job_id)
        for to_recommend in recommends:
            to_recommend.delete()
#         try:
        feed_mysql = Feed.objects.get(id=job_id)
        feed_mysql_id = feed_mysql.id
        
        feed_obj_id = feed_mysql.feed_obj_id
        user_feeds = UserFeed.objects.filter(feed_id=feed_mysql_id)
        for user_feed in user_feeds:
            user_feed.delete()
            
        feed_mongo = Feed2.objects.filter(id=ObjectId(feed_obj_id))
        if feed_mongo.count() == 0:
            print feed_obj_id 
            feed_mysql.delete()
        else:
            feed_mongo = feed_mongo[0]
            feed_mongo_id = feed_mongo.id
            user_feeds2 = UserFeed2.objects.filter(feed=feed_mongo_id)
            for user_feed in user_feeds2:
                user_feed.delete()
            feed_mongo.delete()
            feed_mysql.delete()
#             
#         except:
#             pass

def find_no_user_feed():
    from Brick.App.job_hunting.models import RecommendJob
    from feed.models import Feed,Feed2,UserFeed,UserFeed2
    feed_ids = set()
    user_feed_ids = set()
    feeds = Feed2.objects.filter(feed_type=2).only('id')
    i = 0
    for feed in feeds:
        print i
        i += 1
        feed_ids.add(feed.id)
    
    user_feeds = UserFeed2.objects.all().only('feed')
    i = 0
    for user_feed in user_feeds:
        print i
        i += 1
        user_feed_ids.add(user_feed.feed)
    
    print len(feed_ids-user_feed_ids)
#     add_set = feed_ids-user_feed_ids
#     i = 0
#     j = 0
#     for feed_id in add_set:
#         print i
#         i += 1
#         feed_mysql = Feed.objects.get(id=feed_id)
#         if UserFeed.objects.filter(feed=feed_mysql).count() == 0:
#             print j
#             j += 1
#             UserFeed(user=feed_mysql.user, add_time=feed_mysql.add_time).save()

def mongo_not_in_mysql():
    from feed.models import Feed,Feed2,UserFeed,UserFeed2
    feed_ids = set()
    user_feed_ids = set()
    feeds = Feed2.objects.filter(feed_type=2).only('id')
    i = 0
    for feed in feeds:
        print i
        i += 1
        feed_ids.add(str(feed.id))
    
    user_feeds = Feed.objects.filter(feed_type=2).values('feed_obj_id')
    i = 0
    for user_feed in user_feeds:
        print i
        i += 1
        user_feed_ids.add(user_feed['feed_obj_id'])
    
    delete_feed = feed_ids - user_feed_ids
    print len(delete_feed)
    from bson import ObjectId
    i = 0
    for feed_id in delete_feed:
        print i
        i += 1
        feed_mongo = Feed2.objects.get(id=ObjectId(feed_id))
        user_feeds = UserFeed2.objects.filter(feed=feed_mongo)
        for user_feed in user_feeds:
            user_feed.delete()
        feed_mongo.delete()
#     
    print len(feed_ids - user_feed_ids)
    
def process_nashangban():
    from feed.models import Feed,Feed2,UserFeed,UserFeed2
    from bson import ObjectId
    feeds = Feed.objects.filter(job_url__contains='地点')
    for feed in feeds:
        print feed
        feed.expect_area = feed.expect_area.replace('地点','').strip()
        feed_mongo = Feed2.objects.get(id=ObjectId(feed.feed_obj_id))
        feed_mongo.expect_area = feed_mongo.expect_area.replace('地点','').strip()
        feed_mongo.save()                               
        feed.save()
        
    

# mongo_not_in_mysql()
# find_no_user_feed()
# process_nashangban()