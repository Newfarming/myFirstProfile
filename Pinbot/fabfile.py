# coding: utf-8

'''
automation your task
author: runforever

description:
    ubuntu 14.04

function:
    linit: init pinbot runtime env
    runserver: run django local server
    lflake8: add flake8 hook in git
    linstall_lib: install pinbot depend python lib

usage:
   no param:
      fab runserver
   has param
      fab runserver:8080
'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Pinbot.settings'

from fabric.api import (
    local,
    hosts,
    cd,
    run,
    with_settings,
    prefix,
    prompt,
)

from contextlib import contextmanager as _contextmanager

BASE_DIR = os.path.dirname(__file__)

PRODUCT_ENV = 'www.pinbot.me'
PRODUCT_USER = 'deploy'
PRO_PROJECT_DIR = '/home/deploy/Pinbot'

TEST_ENV = 'b.pinbot.me'
TEST_USER = 'deploy'
PROJECT_DIR = '/home/deploy/Pinbot'
PRE_PROJECT_DIR = '/home/deploy/PrePinbot'

PROJECT_VENV_DIR = os.path.join(PROJECT_DIR, 'pin_venv')
PROJECT_VENV_PYTHON = os.path.join(PROJECT_DIR, 'pin_venv/bin/python')
PROJECT_VENV_PIP = os.path.join(PROJECT_DIR, 'pin_venv/bin/pip')

CURRENT_DIR = os.getcwd()
VENV_DIR = os.path.join(CURRENT_DIR, 'pin_venv')
VENV_PYTHON = os.path.join(CURRENT_DIR, 'pin_venv/bin/python')
VENV_PIP = os.path.join(CURRENT_DIR, 'pin_venv/bin/pip')

PIP_IMAGE_SRC = 'http://pypi.douban.com/simple/ --trusted-host pypi.douban.com'
SRC_PRE_COMMIT_FILE = os.path.join(CURRENT_DIR, 'git_hooks/pre-commit')
DEST_PRE_COMMIT_FILE = os.path.join(CURRENT_DIR, '.git/hooks/pre-commit')

SUPERVISORD_CONF = os.path.join(PROJECT_DIR, 'deploy_conf/supervisor/supervisord.conf')
PRO_SUPERVISORD_CONF = os.path.join(PRO_PROJECT_DIR, 'deploy_conf/supervisor/supervisord.conf')

WEIXIN_TOOLS_CONF = os.path.join(PRO_PROJECT_DIR, 'pin_tools/weixin/weixin_helper.py')

RENV_ACTIVATE = os.path.join(PROJECT_DIR, 'pin_venv/bin/activate')
DB_TOOLS_DIR = os.path.join(PROJECT_DIR, 'pin_tools/db_tools')


@_contextmanager
def rvenv():
    with prefix('source %s && export LC_ALL="en_US.utf8"' % RENV_ACTIVATE):
        yield


def runserver(port=8000):
    '''
    run pinbot server
    param:
        port
    '''
    local('%s manage.py runserver %s --insecure' % (VENV_PYTHON, port))


def run_celery():
    '''
    run pinbot celery
    '''
    python = os.path.join(BASE_DIR, 'pin_venv/bin/python')
    local('export PYTHONPATH={0} && {1} pin_celery/celery_app.py worker -l info -n web_worker'.format(BASE_DIR, python))


def linit():
    '''
    init development server
    '''
    print 'start init virtualenv pinbot venv'
    if not os.path.isdir(VENV_DIR):
        local('virtualenv pin_venv')

    print 'start install python lib'
    local('export PATH=$PATH:/usr/local/mysql/bin && %s install -r requirements.txt -i %s' % (VENV_PIP, PIP_IMAGE_SRC))
    local('%s install git+https://github.com/djsutho/django-debug-toolbar-request-history.git' % VENV_PIP)
    local('%s install git+https://github.com/runforever/django-notifications.git' % VENV_PIP)
    print 'pinbot env init success'


def lflake8():
    '''
    add flake8 hook in git pre-commit
    '''
    print 'add flake8 hook'
    if os.path.isdir(VENV_DIR):
        local('%s install flake8 -i %s' % (VENV_PIP, PIP_IMAGE_SRC))
    else:
        local('sudo pip install flake8 -i %s' % (VENV_PIP, PIP_IMAGE_SRC))
    local('cp %s %s' % (SRC_PRE_COMMIT_FILE, DEST_PRE_COMMIT_FILE))
    local('chmod +x %s' % DEST_PRE_COMMIT_FILE)
    print 'install falke8 hook success'


@hosts(TEST_ENV)
@with_settings(user=TEST_USER)
def reload_weixin_menu():
    '''
    reload weixin menu
    '''
    with cd(PROJECT_DIR):
        with rvenv():
            run('python %s create_menu' % (WEIXIN_TOOLS_CONF))


@hosts(PRODUCT_ENV)
@with_settings(user=PRODUCT_USER)
def fix_userprofile(username):
    '''
    修复没有userprofile的数据
    '''
    fix_user_profile_script = os.path.join(PROJECT_DIR, 'pin_tools/db_tools/fix_add_userprofile.py')
    with cd(DB_TOOLS_DIR):
        with rvenv():
            run('python %s %s' % (fix_user_profile_script, username))


@hosts(PRODUCT_ENV)
@with_settings(user=PRODUCT_USER)
def fix_send_weixin_redpack(users_file):
    '''
    微信补发红包
    '''
    fix_send_weixin_redpack_script = os.path.join(PROJECT_DIR, 'pin_tools/db_tools/fix_send_weixin_redpack.py')
    with cd(DB_TOOLS_DIR):
        with rvenv():
            run('python %s %s' % (fix_send_weixin_redpack_script, users_file))


@hosts(TEST_ENV)
@with_settings(user=TEST_USER)
def pre_deploy_test(remote='origin', branch='test'):
    '''
    测试环境版本预发布，安装python lib，数据库migrate
    '''
    with cd(PRE_PROJECT_DIR):
        with rvenv():
            run('git stash')
            run('git checkout %s' % branch)
            run('git pull --rebase %s %s' % (remote, branch))
            run('git stash pop')
            run('%s install -r requirements.txt ' % PROJECT_VENV_PIP)
            run('python manage.py migrate')


@hosts(TEST_ENV)
@with_settings(user=TEST_USER)
def deploy_test(remote='origin', branch='test'):
    pre_deploy_test()
    with cd(PROJECT_DIR):
        with rvenv():
            run('git stash')
            run('git checkout %s' % branch)
            run('git pull --rebase %s %s' % (remote, branch))
            run('git stash pop')
            run('python manage.py collectstatic --noinput')
            run('supervisorctl -c %s restart web' % SUPERVISORD_CONF)
            run('python manage.py compress --force')


@hosts(TEST_ENV)
@with_settings(user=TEST_USER)
def test_service():
    with cd(PROJECT_DIR):
        with rvenv():
            run('supervisorctl -c %s status' % PRO_SUPERVISORD_CONF)
            service = prompt(
                'restart service  *c_worker *c_beat default option is restart *all service',
                default='c_worker c_beat',
            )
            run('supervisorctl -c %s restart %s' % (PRO_SUPERVISORD_CONF, service))


@hosts(TEST_ENV)
@with_settings(user=TEST_USER)
def fetch_test(remote='origin', branch='master'):
    with cd(PROJECT_DIR):
        with rvenv():
            run('git checkout -- .')
            run('git fetch %s %s' % (remote, branch))
            run('git checkout %s' % branch)
            run('%s install -r requirements.txt -i %s' % (PROJECT_VENV_PIP, PIP_IMAGE_SRC))
            run('python manage.py collectstatic --noinput')
            run('python manage.py compress --force')
            run('supervisorctl -c %s restart web' % SUPERVISORD_CONF)


@hosts(PRODUCT_ENV)
@with_settings(user=PRODUCT_USER)
def pro_service():
    with cd(PROJECT_DIR):
        with rvenv():
            run('supervisorctl -c %s status' % PRO_SUPERVISORD_CONF)
            service = prompt(
                'restart service  *c_worker *c_beat default option is restart *all service',
                default='c_worker c_beat',
            )
            run('supervisorctl -c %s restart %s' % (PRO_SUPERVISORD_CONF, service))


@hosts(PRODUCT_ENV)
@with_settings(user=PRODUCT_USER)
def reload_pro_service():
    with cd(PROJECT_DIR):
        with rvenv():
            run('supervisorctl -c %s status' % PRO_SUPERVISORD_CONF)
            confirm = prompt(
                'Confirm to reload supervisor, y/n',
            )
            if confirm.lower() == 'y':
                run('supervisorctl -c %s reload' % PRO_SUPERVISORD_CONF)


@hosts(PRODUCT_ENV)
@with_settings(user=PRODUCT_USER)
def pre_pro_deploy(remote='origin', branch='master'):
    '''
    生产环境版本预发布，安装python lib，数据库migrate
    '''
    with cd(PRE_PROJECT_DIR):
        with rvenv():
            run('git checkout %s' % branch)
            run('git pull --rebase %s %s' % (remote, branch))
            run('%s install -r requirements.txt ' % PROJECT_VENV_PIP)
            run('python manage.py migrate')


@hosts(PRODUCT_ENV)
@with_settings(user=PRODUCT_USER)
def pro_deploy(remote='origin', branch='master'):
    '''
    发布生产环境
    '''
    pre_pro_deploy()
    with cd(PROJECT_DIR):
        with rvenv():
            run('git checkout -- .')
            run('git checkout %s' % branch)
            run('git pull --rebase %s %s' % (remote, branch))
            run('python manage.py collectstatic --noinput')
            run('supervisorctl -c %s restart web' % SUPERVISORD_CONF)
            run('supervisorctl -c %s restart c_beat c_worker' % SUPERVISORD_CONF)
            run('sh -c "((nohup python manage.py compress --force > /dev/null 2> /dev/null) & )"', pty=False)
