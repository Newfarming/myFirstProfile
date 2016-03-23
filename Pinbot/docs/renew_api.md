<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 自助服务续期接口</a>
<ul>
<li><a href="#sec-1-1">1.1. 获取自助服务信息</a></li>
<li><a href="#sec-1-2">1.2. 生成续期订单</a></li>
<li><a href="#sec-1-3">1.3. 自助套餐列表</a></li>
</ul>
</li>
</ul>
</div>
</div>


# 自助服务续期接口

## 获取自助服务信息

`/vip/renew/info/<vip_info_id:int>/`
-   Method: GET
-   Params:
    -   无
-   Return:
    -   status: 状态 ok
    -   msg: message 信息
    -   data:
        -   active\_time: 生效时间
        -   expire\_time: 过期时间
        -   vip\_name: 套餐名字
        -   feed\_count: 定制数量
        -   pinbot\_point: 每周聘点
        -   id: 记录的数据库ID
        -   month\_price: 每月价格

## 生成续期订单

`/vip/renew/create/<vip_info_id:int>/`
-   Method: POST 使用application/json方式提交
-   Params:
    -   renew\_month 续期的时间长度
-   Return:
    -   status: 状态 ok 创建成功 valid\_month 月份不在3～12里
    -   msg: message 信息
    -   pay\_url: 支付链接
    -   order\_id: 订单号
    -   payment\_terms: 支付方式

## 自助套餐列表

`/vip/self_service/list/`
-   Method: GET
-   Params:
    -   无
-   Return:
    -   id: 记录ID
    -   name: 套餐名称
    -   pinbot\_point: 每周聘点数
    -   feed\_count: 定制数
    -   active\_time: 生效时间
    -   expire\_time: 过期时间
    -   is\_active: 是否生效
