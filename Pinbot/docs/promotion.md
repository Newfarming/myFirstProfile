<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 推广伙伴相关接口</a>
<ul>
<li><a href="#sec-1-1">1.1. 推广记录接口</a></li>
</ul>
</li>
</ul>
</div>
</div>


# 推广伙伴相关接口

## 推广记录接口

`/promotion_point/record/list/`
-   Method: GET
-   Params:
    -   page: 页数
-   Return:
    -   status: 状态 ok
    -   msg: ok
    -   data: 推广记录
        -   id: 记录ID
        -   register\_username: 推广的注册用户
        -   register\_company\_name: 推广注册用户的公司
        -   point: 推广获得的点数
        -   coin: 推广获得的金币
        -   promotion\_date: 推广的日期
