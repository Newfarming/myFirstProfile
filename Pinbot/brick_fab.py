# coding: utf -8

'''
automation your task
author: runforever
'''

import os

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


ENV = 'brick'
PIP_IMAGE_SRC = 'http://pypi.douban.com/simple/'

DEPLOY_USER = 'deploy'

TEST_ENV = 'test.pinbot.me'
TEST_USER = 'test'
DIR = '/home/deploy/Pinbot'

PRO_USER = 'deploy'
PRO_ENV = '121.40.106.215'

RENV_ACTIVATE = os.path.join(DIR, 'pin_venv/bin/activate')


@_contextmanager
def rvenv():
    with prefix('source %s && export LC_ALL="en_US.utf8"' % RENV_ACTIVATE):
        yield


def runserver(ip='127.0.0.1', port=8000):
    '''
    run pinbot server
    param:
        ip
        port
    '''
    local('python manage.py runserver %s:%s --insecure --settings=Brick.settings' % (ip, port))


@hosts(TEST_ENV)
@with_settings(user=DEPLOY_USER)
def install_test_pkg():
    with cd(DIR):
        with rvenv():
            run('pip install -r requirements.txt')


@hosts(TEST_ENV)
@with_settings(user=DEPLOY_USER)
def pull_test(remote='origin', branch='master'):
    with cd(DIR):
        run('git checkout %s' % branch)
        run('git pull --rebase %s %s' % (remote, branch))


@hosts(TEST_ENV)
@with_settings(user=DEPLOY_USER)
def restart_service():
    with cd(DIR):
        with rvenv():
            service = prompt(
                'restart service *brick *c_worker *websocket default option is restart *all service',
                default='brick',
            )
            run('supervisorctl -c Brick/Deploy/supervisor/supervisor.conf restart %s' % service)


@hosts(TEST_ENV)
@with_settings(user=DEPLOY_USER)
def reload_service():
    with cd(DIR):
        with rvenv():
            run('supervisorctl -c Brick/Deploy/supervisor/supervisor.conf reload')


@hosts(TEST_ENV)
@with_settings(user=DEPLOY_USER)
def service_status():
    with cd(DIR):
        with rvenv():
            run('supervisorctl -c Brick/Deploy/supervisor/supervisor.conf status')


@hosts(TEST_ENV)
@with_settings(user=DEPLOY_USER)
def deploy_env():
    with cd(DIR):
        with rvenv():
            run('pip install -r requirements.txt')
            run('python manage.py collectstatic --noinput --settings=Brick.settings')
            run('python manage.py compress --force --settings=Brick.settings')


@hosts(TEST_ENV)
@with_settings(user=DEPLOY_USER)
def deploy_test(remote='origin', branch='master'):
    pull_test(remote, branch)
    deploy_env()
    restart_service()


@hosts(PRO_ENV)
@with_settings(user=PRO_USER)
def pro_install_pkg():
    with cd(DIR):
        with rvenv():
            run('pip install -r requirements.txt')


@hosts(PRO_ENV)
@with_settings(user=PRO_USER)
def pro_pull(remote='origin', branch='master'):
    with cd(DIR):
        run('git checkout -- .')
        run('git checkout %s' % branch)
        run('git pull --rebase %s %s' % (remote, branch))


@hosts(PRO_ENV)
@with_settings(user=PRO_USER)
def pro_restart_service():
    with cd(DIR):
        with rvenv():
            service = prompt(
                'restart service *brick *c_worker *websocket default option is restart *all service',
                default='brick',
            )
            run('supervisorctl -c Brick/Deploy/supervisor/supervisor.conf restart %s' % service)


@hosts(PRO_ENV)
@with_settings(user=PRO_USER)
def pro_reload_service():
    with cd(DIR):
        with rvenv():
            run('supervisorctl -c Brick/Deploy/supervisor/supervisor.conf reload')


@hosts(PRO_ENV)
@with_settings(user=PRO_USER)
def pro_service_status():
    with cd(DIR):
        with rvenv():
            run('supervisorctl -c Brick/Deploy/supervisor/supervisor.conf status')


@hosts(PRO_ENV)
@with_settings(user=PRO_USER)
def pro_deploy_env():
    with cd(DIR):
        with rvenv():
            run('pip install -r requirements.txt')
            run('python manage.py collectstatic --noinput --settings=Brick.settings')
            run('python manage.py compress --force --settings=Brick.settings')


@hosts(PRO_ENV)
@with_settings(user=PRO_USER)
def pro_deploy(remote='origin', branch='master'):
    pro_pull(remote, branch)
    deploy_env()
    restart_service()


@hosts(PRO_ENV)
@with_settings(user=PRO_USER)
def send_email(subject='', tpl='', send_type='test', filename=''):
    with cd(DIR):
        with rvenv():
            run('export PYTHONPATH=%s && python Brick/Utils/email/send_mail.py %s %s %s %s' % (DIR, subject, tpl, send_type, filename))
