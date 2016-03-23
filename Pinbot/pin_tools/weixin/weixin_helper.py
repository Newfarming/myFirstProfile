# coding: utf-8
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")).replace('\\', '/')

sys.path.append(project_path)

from app.weixin.runtime.weixin_utils import (
    WeixinService
)


def create_menu():
    return WeixinService.create_menu()

def get_access_token():
    return WeixinService.get_base_access_token()


if __name__ == '__main__':

    argv = sys.argv[1]
    if argv == 'create_menu':
        print create_menu()
    if argv == 'get_access_token':
        print get_access_token()