# coding: utf-8
from django.conf import settings

WEIXIN_HOST = settings.WEIXIN_HOST

LOGIN_URL = "http://{0}/?from=weixin".format(WEIXIN_HOST)
REG_URL = "http://{0}/#/signup/?from=weixin".format(WEIXIN_HOST)
RECOMMAND_URL = "http://{0}/#/recommand/list/?from=weixin".format(WEIXIN_HOST)
FAVOURS_URL = "http://{0}/#/favours/list/?from=weixin".format(WEIXIN_HOST)
CUSTOMIZE_URL = "http://{0}/#/customize/list/?from=weixin".format(WEIXIN_HOST)
CUSTOMIZE_NEW_URL = "http://{0}/#/customize/new/?from=weixin".format(WEIXIN_HOST)

REDIRECT_LOGIN_URL = "http://{0}/".format(WEIXIN_HOST)
REDIRECT_REG_URL = "http://{0}/#/signup/".format(WEIXIN_HOST)

TEXT_DICT = {
}

CHAT_MAP = {
    u'人才':
        {
            'type': 'show_text',
            'welcome_str': '聘小宝给你准备了一顿大餐 <a href="{0}">立即查看推荐</a>'.format(RECOMMAND_URL),
        },
    u'收藏':
        {
            'type': 'show_text',
            'welcome_str': '优秀人才傲娇的很，要么再主动联系，要么就挑别人剩下的咯... <a href="{0}">我的收藏</a>'.format(FAVOURS_URL),
        },
    u'职位':
        {
            'type': 'show_text',
            'welcome_str': '完善职位需求，推荐会更准哦~ <a href="{0}">我的职位</a>'.format(CUSTOMIZE_URL),
        },
    'subscribe':
        {
            'welcome_str': '欢迎加入聘宝大家庭，聘小宝在此，绑定账号才可以玩哦\n\n' \
            '1、老用户请点击<a href="{0}">立即绑定</a>\n\n' \
            '2、新用户请点击<a href="{1}">注册绑定</a>\n\n' \
            '成功绑定后提交首个定制，即可获得聘小宝慰问红包一枚！\n'.format(LOGIN_URL, REG_URL),

            'success_str': '您已经绑定聘宝账号：%s, 如需解除绑定，请登录网页版并在“个人设置”中操作',
            'has_bind': '该账号已经绑定,请先解绑!',
            'fail_str': '您无法绑定聘宝账号,可能是您并未在pinbot.me注册账号!<a href="{1}">注册绑定</a>'.format(LOGIN_URL, REG_URL)
        },
    'get_red_pack':
        {
            'success_str': '您已成功领取红包',
            'fail_str': '领取红包失败,没有领取资格或账号不存在!'
        }
}

EVENT_KEY_MAP = {
    'KEY_BIND_ACCOUNT': {
        'fun_name': 'click_bind_account',
        'welcome_str': '聘小宝提示，绑定账号才可以玩哦！\n\n1、老用户请点击<a href="{0}">立即绑定</a> \n\n2、新用户请点击<a href="{1}">注册绑定</a>'.format(LOGIN_URL, REG_URL),
        'success_str': '您已经绑定聘宝账号：%s, 如需解除绑定，请登录网页版并在“个人设置”中操作'
    },

    'KEY_CONTACT_US': {
        'fun_name': 'click_contact_us',
        'welcome_str': '如有疑问请拨打028-83330727, 等待你的可能是浑厚播音嗓，抑或清甜软妹音...也可以直接给小宝留言，贴心小宝随时恭候~ 对了，登陆网页版(www.pinbot.me)也能找到我们哦！',
    },

    'KEY_HELP': {
        'fun_name': 'click_help',
        'welcome_str': '按以下提示操作，快速get聘宝新技能~ \n 1、直接回复“人才”，查看简历推荐\n 2、直接回复“收藏”，查看已经收藏的简历\n 3、直接回复"职位”，查看已经提交的职位需求',
    },

    'KEY_VIEW_JOB': {
        'fun_name': 'click_view_job',
        'welcome_str': '聘小宝提示，绑定账号才可以玩哦！\n\n1、老用户请点击<a href="{0}">立即绑定</a> \n\n2、新用户请点击<a href="{1}">注册绑定</a>'.format(LOGIN_URL, REG_URL),
        'success_str': '以下是您已经提交的职位，点击职位名称可查看详细推荐：\n\n %s',
        'no_data': '您还没有提交职位，优秀人才不能等，赶快 <a href="{0}">新增定制</a> 吧！'.format(CUSTOMIZE_NEW_URL)
    },
}

FEED_NOTIFY_MSG_TEMPLATE = {
    "first": {
        "value": "",
        "color": "#000000"
    },
    "keyword1": {
        "value": "",
        "color": "#173177"
    },
    "keyword2": {
        "value": "",
        "color": "#173177"
    },
    "keyword3": {
        "value": "",
        "color": "#173177"
    },
    "remark": {
        "value": "",
        "color": "#000000"
    },
}
