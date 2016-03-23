# coding: utf-8

import requests

PINBOT_HOST = 'http://192.168.99.100:8888/'

BACKEND_LOGIN_URL = '{0}hr/backend_login/'.format(PINBOT_HOST)
PINBOT_LOGIN_URL = '{0}signin/'.format(PINBOT_HOST)
LOGOUT_URL = '{0}signout'.format(PINBOT_HOST)
ACCOUNT_PAGE = '{0}payment/my_account/'.format(PINBOT_HOST)

user_str = '''
    runforever@163.com,
    kkk@kkk.com,
'''


def login(user):
    with requests.Session() as s:
        s.post(
            PINBOT_LOGIN_URL,
            data={
                'email': 'likaiguo.happy@163.com',
                'password': '19870716',
            }
        )
        ret = s.get(BACKEND_LOGIN_URL, params={'username': user})
        json_content = ret.json()
        if json_content['status'] == 'ok':
            print 'user {0} login success'.format(user)

            s.get(ACCOUNT_PAGE)
            s.get(LOGOUT_URL)


def main():

    user_list = [i.strip() for i in user_str.split(',') if i.strip()]
    for user in user_list:
        username = user.strip()

        if username:
            login(username)


if __name__ == '__main__':
    main()
