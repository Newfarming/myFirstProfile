<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 移动端微信接口API</a>
<ul>
<li><a href="#sec-1-1">1.1. 注册登录</a>
<ul>
<li><a href="#sec-1-1-1">1.1.1. 注册</a></li>
<li><a href="#sec-1-1-2">1.1.2. 登陆</a></li>
<li><a href="#sec-1-1-3">1.1.3. 检查token是否有效</a></li>
</ul>
</li>
<li><a href="#sec-1-2">1.2. 定制相关</a>
<ul>
<li><a href="#sec-1-2-1">1.2.1. 新增（编辑）定制（获取表单填写信息）</a></li>
<li><a href="#sec-1-2-2">1.2.2. 提交（更新）定制</a></li>
<li><a href="#sec-1-2-3">1.2.3. 用户定制列表</a></li>
<li><a href="#sec-1-2-4">1.2.4. 用户定制推荐简历的列表</a></li>
<li><a href="#sec-1-2-5">1.2.5. 删除定制</a></li>
<li><a href="#sec-1-2-6">1.2.6. 删除推荐结果</a></li>
<li><a href="#sec-1-2-7">1.2.7. 添加收藏</a></li>
<li><a href="#sec-1-2-8">1.2.8. 删除收藏</a></li>
<li><a href="#sec-1-2-9">1.2.9. 收藏列表详情</a></li>
<li><a href="#sec-1-2-10">1.2.10. 查看定制</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</div>


# 移动端微信接口API

## 注册登录

### 注册

URL: `/hr/register/`
-   Method: POST
-   Params: 使用x-www-form-urlencoded的提交方式
    -   user\_email: 用户邮箱
    -   password: 密码
    -   company\_name: 公司名称
    -   phone: 联系电话
-   Return:
    -   status: 状态 ok 注册成功， form\_error 表单错误
    -   msg: message 信息
    -   errors: 表单错误具体信息
    -   username: 用户名

### 登陆

URL: `/hr/login/`
-   Method: POST
-   Params: 使用x-www-form-urlencoded的提交方式
    -   username: 用户邮箱
    -   password: 密码
-   Return:
    -   status: 状态 ok 登陆成功， form\_error 表单错误， not\_active 未激活, not\_hr 不是hr用户
    -   msg: message 信息
    -   errors: 表单错误具体信息
    -   username: 用户名
    -   user\_industry: 用户所属行业
    -   auth\_info: 认证信息
        -   user: 用户数据库ID
        -   token: 认证的token
    -   注意：token认证需要在header里添加Authorization 值是Basic user:token的base64编码Basic OTA3OjQ1ZC1mNWIxNTUzMDA1ZDFhNjcyYWM4Yw==

### 检查token是否有效

URL: `/hr/valid_token/<:user>/<:token>/`
-   Method: GET
-   Params:
    -   无
-   Return:
    -   status: 状态 ok 可以使用, token\_error 无效token
    -   msg: message 信息

## 定制相关

### 新增（编辑）定制（获取表单填写信息）

URL: `/special_feed/edit_feed/<feed_id>/` 编辑定制的话需要加上feed\_id
-   Method: GET
-   Params:
    -   无
-   Return:
    -   status:
        -   ok: 成功
        -   feed\_error: 定制错误
        -   no\_rest\_feed: 没有剩余定制可以使用
    -   msg: message 信息
    -   data: 数据信息
        -   feed: 用户定制数据
            -   skill\_required: 技能要求
            -   keywords: 关键词信息 e.g: ['python', 'nodejs']
            -   job\_desc: 职位描述
            -   salary\_min: 最低薪资
            -   salary\_max: 最高薪资
            -   talent\_level: 人才级别 e.g: ['中级', '高级']
            -   expect\_area: 期望工作城市
            -   title: 职位名称
            -   company\_prefer: 人才偏好 e.g: [{'id': 1, 'name': '一线互联网人才'}]
            -   job\_welfare: 工作福利 e.g: ['不加班', '364天都放假']
            -   job\_domain: 职位领域 e.g: [{id: 1: category: "O2O"}]
            -   company: 公司信息
                -   categroys: 公司领域 e.g: [{id: 1, category: "医疗健康"}]
                -   url: 公司网址
                -   product\_url: 产品地址（聘宝用的是这个地址）
                -   company\_stage: 公司发展阶段 e.g A轮
                -   company\_name: 公司名称
                -   key\_points: 公司亮点
                -   desc: 公司描述
        -   company\_prefer: 人才偏好选项
        -   expect\_area: 期望城市选项
        -   job\_welfare: 公司福利选项
        -   calced: 是否计算过

### 提交（更新）定制

URL: `/special_feed/submit_feed/`
-   Method: POST
-   Params: 使用json格式提交

    // 提交数据格式
    {
     'analyze_job_domain': [],
     'categorys': [{'category': 'O2O', 'id': 7},
                    {'category': '移动互联网',
                     'id': 14}],
     'company_prefer': [2],
     'expect_area': '北京,上海',
     'feed_id': '55cbfe688230db3518998292',
     'job_desc': 'Python\nHtml\nJS',
     'job_domain': [7],
     'job_welfare': '不加班,不打卡',
     'keywords': 'python',
     'salary_max': 5000,
     'salary_min': 3000,
     'skill_required': '',
     'talent_level': '中级,高级',
     'title': 'Python开发'
    }
-   Return:
    -   status:
        -   ok: 成功
        -   form\_error: 表单错误
        -   feed\_error: 定制错误
        -   no\_feed: 没有剩余定制可以使用
    -   errors: 表单错误信息
    -   msg: message 信息
    -   redirect\_url: 重定向URL
    -   username: 用户名
    -   mission\_time: 新手任务开始时间
    -   show\_mission: 是否展示新手任务

### 用户定制列表

URL: `/special_feed/page/`
-   Method: GET
-   Params:
    -   无
-   Return:
    -   status:
        -   ok: 成功
        -   no\_feed: 没有新增任何定制
    -   msg: message 信息
    -   data: 数据信息
        -   all\_feed: 用户定制数据 [{feed: {}}, {feed: {}}]
            -   feed:
                -   last\_click\_time: 最后点击时间 时间戳
                -   start\_time: 服务开始时间 时间戳
                -   job\_type: 职位类型
                -   feed\_type: 定制类型
                -   partner\_feed: 人才伙伴定制
                -   job\_desc: 职位描述
                -   keywords: 职位关键词
                -   has\_expire: 是否定制过期
                -   expire\_status: 是否7天过期 7天未点击
                -   id: 定制的数据库ID
                -   salary\_min: 最低薪资
                -   salary\_max: 最高薪资
                -   talent\_level: 人才级别 e.g: '中级, 高级'
                -   expect\_area: 期望工作城市 e.g: "广州,成都,北京"
                -   title: 职位名称
                -   unread\_count: 未读数量
        -   has\_rest\_feed: 是否有剩余定制数
        -   vip\_user: 是否是vip用户

### 用户定制推荐简历的列表

URL: `/special_feed/feed_list/5301d989fb6dec344c92b4fe`
-   Method: GET
-   Params:
    -   start: 开始页数
    -   latest: 是否未读 0 或者1
    -   send: 是否投递 0 或者 1
    -   partner: 是否人才伙伴推荐 0或者1
    -   title_match: 职位匹配 0或者1
    -   extend_match: 扩展匹配 0或者1
    -   reco_time: 推荐时间7,15,30(代表7天，15天，30天)
    -   current_area: 现居地 e.g: 成都
    -   salary_min: 最低薪资 e.g: 2000
    -   salary_max: 最高薪资 e.g: 20000
-   Return:
    -   status:
        -   ok: 成功
        -   no\_feed: 没有新增任何定制
    -   total\_recommend\_count: 总推荐数
    -   total\_count: 显示总数
    -   newest\_recommend\_count: 新推荐数
    -   feed\_query\_count: 查询总数
    -   next\_start: 下一页
    -   data: 用户推荐数据 [{feed: {}, pub\_time: 'xxx'}, {feed: {}}]
        -   feed:
            -   keywords: 推荐关键词 ['数据挖掘', '爬虫']
            -   id: 定制的数据库ID
        -   resume: 简历信息
            -   job\_target: 期望职位信息
                -   job\_career: 职业生涯
                -   salary: 期望薪资范围
                -   job\_category: 职位类型 e.g: 全职 实习
                -   job\_hunting\_state: 求职状态
                -   job\_industry: 职位领域
                -   enroll\_time: 注册时间
                -   expectation\_area: 期望工作城市
            -   education: 教育经历
                -   school: 学校
                -   start\_time: 开始时间
                -   end\_time: 结束时间
                -   degree: 学位
                -   major: 专业
            -   address: 现居地
            -   id: 简历的ID
            -   last\_contact: 最后联系
            -   hr\_evaluate: HR评价
            -   gender: 性别
            -   age: 年龄
            -   self\_evaluation: 自我评价
            -   works: 工作经历
                -   salary: 薪资
                -   company\_category: 公司类型
                -   start\_time: 开始时间
                -   position\_category: 职位类别
                -   company\_scale: 公司规模
                -   compnay\_name: 公司名称
                -   industry\_category: 公司类别
                -   position\_title: 职位名称
                -   job\_desc: 职位描述
                -   duration: 持续时间
                -   end\_time: 结束时间
            -   work\_years: 工作年限
        -   favStatus: 是否关注， true false
        -   user\_read\_status: 用户阅读状态
        -   pub\_time: 展示时间
        -   calc\_time: 计算时间
        -   id: feed\_result推荐结果数据的ID
        -   tags: 标签, 包含关键词，学校类别等信息
        -   contact_info: 已经下载简历联系信息, 没有下载信息为空{}
            -   qq: QQ号
            -   phone: 电话
            -   name: 姓名
            -   email: 邮箱
            -   resume_id: 简历ID
        -   mark_log: 标记列表, 没有标记为空[]
            -   mark_time: 标记时间, 时间戳格式
            -   good_result: 进展是否顺利true, false
            -   mark_name: 标记状态
        -   comment_log: 备注列表, 没有备注为空[]
            -   content: 备注信息
            -   comment_time: 备注时间
            -   resume_id: 简历ID
### 删除定制

URL: `/feed/delete/<feed_id:objectid>`
-   Method: GET
-   Params:
    -   无
-   Return:
    -   status: 状态 ok
    -   msg: ok

### 删除推荐结果

URL: `/feed/modify_feed_result`
-   Method: GET
-   Params:
    -   feed\_id: 定制objectid
    -   resume\_id: 简历objectid
    -   reco\_index: -150 删除  150恢复
-   Return:
    -   status: 状态 ok
    -   msg: ok

### 添加收藏

URL: `/resumes/add_watch/<resume_id:objectid>`
-   Method: GET
-   Params:
    -   feed\_id: 定制objectid
-   Return:
    -   status: 状态 ok
    -   msg: ok

### 删除收藏

URL: `/resumes/remove_watch/<resume_id:objectid>`
-   Method: GET
-   Params:
    -   feed\_id: 定制objectid
-   Return:
    -   status: 状态 ok
    -   msg: ok

### 收藏列表详情

URL: `/resume/follow/list/`
-   Method: GET
-   Params:
    -   无
    -   search_fields: 搜索类型(position_title职位名 company_name公司名 name姓名 school学校 all简历全文)
    -   keywords: 搜索关键词

-   Return:
    -   status: 状态 ok
    -   msg: ok
    -   data: 用户推荐数据 [{feed: {}, pub\_time: 'xxx'}, {feed: {}}]
        -   feed\_id: 定制的ID
        -   add\_time: 关注时间
        -   keywords: 关键词
        -   resume: 简历信息
            -   contact\_info: 联系信息
                -   qq: QQ号
                -   phone: 电话
                -   name: 姓名
                -   email: 邮箱
                -   status: 简历联系信息状态 public 公开, secret 保密
            -   job\_target: 期望职位信息
                -   job\_career: 职业生涯
                -   salary: 期望薪资范围
                -   job\_category: 职位类型 e.g: 全职 实习
                -   job\_hunting\_state: 求职状态
                -   job\_industry: 职位领域
                -   enroll\_time: 注册时间
                -   expectation\_area: 期望工作城市
            -   education: 教育经历
                -   school: 学校
                -   start\_time: 开始时间
                -   end\_time: 结束时间
                -   degree: 学位
                -   major: 专业
            -   address: 现居地
            -   id: 简历的ID
            -   last\_contact: 最后联系
            -   hr\_evaluate: HR评价
            -   gender: 性别
            -   age: 年龄
            -   self\_evaluation: 自我评价
            -   works: 工作经历
                -   salary: 薪资
                -   company\_category: 公司类型
                -   start\_time: 开始时间
                -   position\_category: 职位类别
                -   company\_scale: 公司规模
                -   compnay\_name: 公司名称
                -   industry\_category: 公司类别
                -   position\_title: 职位名称
                -   job\_desc: 职位描述
                -   duration: 持续时间
                -   end\_time: 结束时间
            -   work\_years: 工作年限

### 查看定制

URL: `/feed/get/<feed_id:objectid>/<resume_id:objectid>`
-   Method: GET
-   Params:
    -   无
-   Return:
    -   status: 状态 ok
    -   msg: ok
