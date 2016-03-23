<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 套餐改版接口</a>
<ul>
<li><a href="#sec-1-1">1.1. 我的钱包</a>
<ul>
<li><a href="#sec-1-1-1">1.1.1. 获取我的套餐接口</a></li>
<li><a href="#sec-1-1-2">1.1.2. 获取我的订单</a></li>
</ul>
</li>
<li><a href="#sec-1-2">1.2. 套餐改版版本发布注意事项</a></li>
</ul>
</li>
</ul>
</div>
</div>


# 套餐改版接口

## 我的钱包

### 获取我的套餐接口

-   url: `/payment/service_list/`
-   method: GET
-   请求参数:
    -   status: 套餐状态
        -   applying: 申请中
        -   success: 已开通
        -   refund: 退款中
        -   cancel\_refund: 取消退款
        -   refunded: 退款成功
        -   closed: 已关闭
        -   canceled: 已取消
        -   deleted: 已删除
        -   expired: 已过期
-   返回:
    -   data: 套餐数据
        -   service\_desc 套餐信息
        -   price 价格
        -   active\_time 生效时间
        -   create\_time 创建时间
        -   expire\_time 过期时间
        -   status 套餐状态
    -   is\_paginated: true 有分页， false 无分页
    -   pages: 总页数
    -   current: 当前页数
    -   count: 总记录数
    -   per\_page: 每页记录数

### 获取我的订单

-   url: `/payment/payment_record/`
-   method: GET
-   请求参数:
    -   record\_type: 订单类型
        -   1 充值
        -   2 提现
        -   3 支出
        -   4 收入
    -   order\_status: 订单状态
        -   unpay 进行中
        -   paid 交易成功
        -   fail 交易失败
        -   refund 退款
        -   cancel\_refund 取消退款
        -   refunded 退款成功
        -   closed 已关闭
        -   canceled 已取消
        -   deleted 已删除
-   返回:
    -   data: 订单数据
        -   actual\_price: 价格
        -   order\_type: 支出 提现 收入 充值
        -   order\_id: 订单ID
        -   create\_time: 创建时间
        -   pay\_time: 付款时间
        -   order\_status: 交易状态
    -   is\_paginated: true 有分页， false 无分页
    -   pages: 总页数
    -   current: 当前页数
    -   count: 总记录数
    -   per\_page: 每页记录数

## 套餐改版版本发布注意事项

1.  数据库执行migrate
2.  运行脚本python pin\_tools/db\_tools/old\_record\_item.py 将以前的vip数据添加到ItemRecord
3.  需要重启celery supervisorctl -c deploy\_conf/supervisor/supervisord.conf restart c\_worker c\_beat
