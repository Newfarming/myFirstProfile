<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 订单相关接口</a>
<ul>
<li><a href="#sec-1-1">1.1. 管理员创建订单</a></li>
</ul>
</li>
</ul>
</div>
</div>


# 订单相关接口

## 管理员创建订单

`/vip/order/admin_create/`
-   Method: POST
-   Content-Type: x-www-form-urlencoded
-   Params:
    -   username: 客户的用户名
    -   product\_type: 商品类型(manual\_service 人工服务)
    -   num: 数量
    -   pid: 商品的数据库ID
    -   payment\_terms: 付款方式(offline 线下，alipay支付宝)
    -   is\_insurance: 是否支付入职险 0 不支付 1 支付
-   Return:
    -   status: 状态 ok， form\_error定制id有问题
    -   order\_id: 订单id
    -   order\_price: 订单价格
    -   msg: 信息ok
    -   pay\_url: 支付URL
    -   payment\_terms: 支付方式
