<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 聘宝的C端产品Web端</a>
<ul>
<li><a href="#sec-1-1">1.1. 业务需求</a></li>
<li><a href="#sec-1-2">1.2. 目录结构</a></li>
<li><a href="#sec-1-3">1.3. 项目技术</a></li>
<li><a href="#sec-1-4">1.4. 初始化项目</a></li>
<li><a href="#sec-1-5">1.5. 测试环境账户</a>
<ul>
<li><a href="#sec-1-5-1">1.5.1. 用户</a></li>
<li><a href="#sec-1-5-2">1.5.2. 数据库</a></li>
</ul>
</li>
</ul>
</li>
</ul>
</div>
</div>

# 聘宝的C端产品Web端

## 业务需求

1.  Brick需要读取Pinbot的Feed作为职位卡片展示
2.  Brick需要和Pinbot的互动，简历投递和会话
3.  Pinbot下载简历等行为需要和Brick互动

## 目录结构

Brick项目在Pinbot的项目中，目的是因为两者相互依赖，使用同一套数据库，
但是依赖关系不是那么紧密，需要单独部署，所以将项目的settings做区分，
需要维护两套settings，跟数据库表结构相关的app需要同时加入到Pinbot和Brick
项目各自的settings中。

## 项目技术

1.  Django负责Web，使用的版本为1.6.5
2.  MySql做为数据库，与Pinbot使用同一套数据库
3.  使用South作为数据库的版本控制管理

## 初始化项目

1.  初始化Brick的virturalenv
2.  运行pip install -r requirements.txt来安装Python的依赖
3.  开发时复制settings/settings\_dev.py.example 到settings/settings\_dev.py做为开发时使用的配置（必须）

## 测试环境账户

### 用户

测试环境已经关闭密码登录，只能使用公钥登录，要使用测试环境请把公钥发我（runforever）

    ssh test@218.244.150.173

    # root密码4ZHtw8v8
    # test密码POIlkj,mn

### 数据库

测试环境使用MySql作为数据库

    # 使用test_product，用户名是admin, 密码是root

Mongo数据库账号密码

    # 管理账户root, root, recruiting数据库账户admin, root

Flower管理账户密码

    # 管理账户admin, Hopperclouds2014


后台admin的Nginx管理账户密码

    # 管理账户pinbot, Hopperclouds2014
