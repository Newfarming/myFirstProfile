#任务系统接口文档

-   请求接口：
    -   url: `/task/`
    -   method: GET
    -   param: 无
    -   返回数据：获取所有的任务列表
    -   数据格式：json

例如:

    {
        'status': 'ok',
        'task_count': 17,任务总数
        'data': [ 所有任务的详情
            {
                'task_code': task_code, 任务代码
                'task_name': task_name, 任务名
                'description': task_descript, 任务描述
                'task_type': task_type, 任务类型 1.新手任务，2。成长任务 ，3.隐藏任务
                'reward_type': reward_type, 奖励类型
                'task_reward': task_reward, 任务奖励
                'task_count': task_count, 任务完成所需的条件达成次数
                'current_process': current_process, 任务进度
                'finished_status': finished_status, 完成情况：1未完成，2完成未领奖，3完成已经领奖
                'task_url': reak_url, 前往任务的url
            },
        ]
        'recent_reward_detail':[
                这是里“谁在什么时候得到多少个什么”这样的格式
                ]
    }

-   请求个人完成情况接口:
    -   url: /task/task_status/
    -   method: GET
    -   param: 无
    -   返回数据: 个人任务完成情况状态码
    -   数据格式: json

数据格式：

        {
            'status': 'ok',
            'msg': 'task_to_do', task_to_do,有任务可以做 reward_to_receive,有奖励可以领取, all_finished,全部完成
        }

-   请求任务完成详情接口:
    -   url: /task/finished/
    -   method: GET
    -   param: 无
    -   返回数据: 个人完成任务的详细状态
    -   数据格式: json

数据格式：

        {
            'status': 'ok',
            'data': [
                {
                    'task_name': task_name,
                    'task_code': task_code,
                    'description': description, 描述
                    'task_reawrd': 任务奖励
                    'reard_time': 奖励时间
                    'reward_due_time': reward_due_time, 奖励领取的过期时间
                    'coupon_used_time': coupon_used_time,抵用券的使用时间
                },
            ],
            'task_finished_count': 2
            ]
        }

-   请求任务奖励领取接口：
    -   url: /task/finished/
    -   method: POST
    -   param: task_code,task_times 任务代码和任务完成所需的条件达成次数
    -   返回数据: 领取情况
    -   数据格式: json

数据格式：

        {
            'status': 'ok',
            'msg': 'sucess'

-   请求地址接口：
    -   url: /task/address/
    -   method: POST GET
    -   param: name, province, city, street
    -   返回数据:  get,返回以上信息，post，提交以上信息
    -   数据格式: json

数据格式：

        get 返回的数据：
        {
            'name': 收件人名字,
            'province': 省
            'city': 市
            'street': 街道
        }

        post 提交的数据和上面一样
        返回：

        {
            'status': 'ok',
            'msg': 'sucess'
        }

-   领奖接口出错的信息：
    -   任务代码出错：这个是指前端传过来的任务代码task_code有误，'error task_code'
    -   微信绑定需求：这个是指奖励是微信红包的任务在领奖的时候，会判断是否用户绑定来微信，没有绑定就是 'weixin bind required'
    -   地址填写要求：这个是指，奖励是实物的任务，在领奖时会判断是否填写来邮寄地址，没有就是 'address required'
    -   其它错误：'task_code error or reward_status is due'


#问卷调查
-   获取问题数据：
    -   数据格式：json
    -   请求方法： get
    -   请求地址：/activity/questions/

数据内容例子:

    {
        'question': 这是一个问题,
        'question_id': 问题的id，提交数据时需要传给后台,
            'question_type': 问题类型,
            'anwser_type': 答案类型,
            'order': 问题顺序,
            'anwser_options': ['答案1', '答案2', '答案3', '答案4']，如果是空，那么就是非选择,
            'anwsers_count'：选项个数,
            'is_other_option': true,
    }
    这里的问题类型，是指是属于什么分类，如："用户基本信息","公司基本信息"，或者是"关于聘宝"
        (1, '用户信息' )
        (2, '公司信息' )
        (3, '关于聘宝' )
    这里的答案类型，是指答案的提交的格式，如："文本"，"单选"
        ('single_choies', '单选类型'),
        ('multi_choies', '复选类型'),
        ('single_choies_or_text', '单选或文本类型'),
        ('multi_choies_or_text', '复选或文本类型'),
        ('short_text', '短文本'),
        ('long_text', '长文本'),
        ('address', '地址'),
    问题顺序，是指问题的序号，这里暂时先不管这个，我估计后面我会在后端排序后传给你
    答案选项，这个是不定选项数的，可能会有多的，有少的
    允许其他答案，是指选项不能满足答案时，填写其他的东西

-   提交调查数据：
    -   数据格式：json
    -   请求方法： post
    -   请求地址：/activity/questionnaire_feedback/

请求数据格式：

    {
        'anwser':[
            {'question_id': 1, 'anwser': 答案},
            {'question_id': 2, 'anwser': 答案},
            {'question_id': 3, 'anwser': 答案},
        ]
    }
返回的数据格式:

    {
        'status': 'ok'/'error',
        'msg': '提交成功'/'提交的数据格式有误'
    }
