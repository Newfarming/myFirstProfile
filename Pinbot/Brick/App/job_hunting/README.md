<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 推荐职位设计</a>
<ul>
<li><a href="#sec-1-1">1.1. 表设计</a></li>
<li><a href="#sec-1-2">1.2. 接口设计</a></li>
</ul>
</li>
</ul>
</div>
</div>

# 推荐职位设计

## 表设计

    class RecommendJob(models.Model):
        '''
        用户推荐职位列表
        给用户推荐的职位列表

        字段：
            user： C端的注册用户
            job： 对应B端的Feed
            resume： 对应C端的简历
            action： C端用户对该推荐职位的操作(收藏，屏蔽，投递)
        '''
        READ_META = (
            ('read', '已读'),
            ('unread', '未读'),
        )
        ACTION_META = (
            ('favorite', '收藏'),
            ('send', '投递'),
            ('dislike', '不感兴趣'),
        )
        user = models.ForeignKey(
            User,
            verbose_name='推荐用户',
        )
        job = models.ForeignKey(
            Job,
            verbose_name='推荐职位',
        )
        resume = models.ForeignKey(
            Resume,
            verbose_name='简历',
        )
        reco_time = models.DateTimeField(
            auto_now_add=True,
            verbose_name='推荐时间',
        )
        read_status = models.CharField(
            max_length=10,
            choices=READ_META,
            verbose_name='阅读状态',
            default='unread',
        )
        action = models.CharField(
            max_length=30,
            choices=ACTION_META,
            verbose_name='用户动作'
        )

        def __unicode__(self):
            return u'推荐%s给用户%s' % (
                self.job.company_name,
                self.user.username,
            )

        def __str__(self):
            return self.__unicode__()

        class Meta:
            verbose_name = '职位推荐列表'
            verbose_name_plural = verbose_name

## 接口设计

    class JobUtils(object):

        @classmethod
        def add_recommend_job(cls, resume_id, feed_id):
            '''
            根据resume_id和feed_id将推荐职位添加到推荐职位列表中
            '''
            pass
