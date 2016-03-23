<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. Pinbot Web服务</a>
<ul>
<li><a href="#sec-1-1">1.1. 技术</a></li>
<li><a href="#sec-1-2">1.2. 初始化环境</a></li>
<li><a href="#sec-1-3">1.3. 版本发布</a></li>
<li><a href="#sec-1-4">1.4. 本地开发环境</a>
<ul>
<li><a href="#sec-1-4-1">1.4.1. 使用Docker部署开发环境服务</a></li>
<li><a href="#sec-1-4-2">1.4.2. 安装Docker</a></li>
<li><a href="#sec-1-4-3">1.4.3. 启动服务</a></li>
</ul>
</li>
<li><a href="#sec-1-6">1.6. 监控服务</a>
<ul>
<li><a href="#sec-1-6-1">1.6.1. sentry</a></li>
<li><a href="#sec-1-6-2">1.6.2. flower(celery监控服务)</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</div>


# Pinbot Web服务

## 服务
B端，Pinbot

C端，Brick

## 技术

Django, Mysql, Mongo, Redis, RabbitMQ

## 初始化环境

    # 安装 fabric 和 virtualenv，和fig（管理Docker）
    sudo pip install fabric virtualenv fig

    # 进入到Pinbot项目安装python 依赖
    # linux 需要安装Mysql相关的依赖，Mac需要安装Mysql
    fab linit

    # 运行服务准备
    # 使用B端开发环境的settings
    cd Pinbot/Pinbot/settings/ && cp settings_dev.py.example settings_dev.py

    # 使用C端开发环境的settings
    cd Pinbot/Brick/settings/ && cp settings_dev.py.example settings_dev.py

    # 启动B端
    python manage.py runserver 8000

    # 启动C端
    python manage_brick.py runserver 8001

## 版本发布

    # 发布测试环境
    # 1. push 要发布的分支到upstream test
    git push -f upstream feature-xxx:test
    # 2. 发布测试环境
    fab deploy_test

    # 发布B端生产环境
    fab pro_deploy

    # 如果数据库model有改动，需要在版本发布前执行数据库的migrate
    python manage.py migrate

    # 然后再执行发布命令 fab pro_deploy

    # B端重启supervisor服务
    fab pro_service

    # B端重新加载supervisor服务
    fab reload_pro_service

    # 发布C端生产环境
    fab -f brick_fab.py pro_deploy

## 本地开发环境

### 使用Docker部署开发环境服务

Pinbot项目需要服务有如下
1.  Mysql

2.  Mongo

3.  Redis

4.  RabbitMQ

### 安装Docker

安装Docker Toolbox 安装方法[<https://www.docker.com/toolbox>](https://www.docker.com/toolbox)

新版本Docker使用Docker Machine来启动Docker Server
### 使用

    # 查看存在的Docker Machine
    docker-machine ls

    # 启动 default 环境
    docker-machine start default

    # 使用default 环境
    docker-machine env default

    # 关联到docker 虚拟环境
    eval "$(docker-machine env default)"

    # 关闭
    docker-machine stop default

    # 查看IP
    docker-machine ip

    # 帮助
    docker-machine help

新版本Docker使用Docker compose 来管理container
### 使用

    # 初始化聘宝开发环境
    cd Pinbot
    docker-compose up

    # 初始化聘宝Web开发所需要的服务
    docker-compose -f pinbot-service.yml -p service up

    # 查看帮助
    docker-compose help

    # 常用命令
    docker ps 查看正在运行的docker container
    docker ps -a 查看所有运行过的container
    docker exec -it <container_id or container name> /bin/bash 进入正在运行的container
    docker stop <container_id> 关闭container
    docker start <container_id> 打开container

导入测试环境所需要的数据
### 使用

    # 导入Mysql测试数据，使用sequel pro等工具导入，新建一个名未pinbot的数据库，然后将测试数据导入

    # 导入Mongo数据
    # 1. 复制测试数据到mongo 的docker container
    docker cp data_bak service_mongo_1:/root

    # 2. 进入mongo 的docker container
    docker exec -it service_mongo_1 /bin/bash

    # 3. 执行导入命令
    cd /root/data_bak && mongorestore -d recruiting --drop mongo/recruiting/

将setting_dev配置改成docker machine的配置

注意事项

1. mongo 无用户名密码
2. redis 密码是root
3. rabbitmq 用户密码是 guest guest
4. mysql 用户密码是 admin root

参考资料[<http://docs.docker.com/>](http://docs.docker.com/)

## 监控服务

### sentry

异常监控服务, sentry.pinbot.me

### flower(celery监控服务)

地址pinflo.pinbot.me

### 邮件服务

sendcloud http://sendcloud.sohu.com/login.html

mailgun http://www.mailgun.com/

submail(目前正在使用) http://submail.cn/chs
