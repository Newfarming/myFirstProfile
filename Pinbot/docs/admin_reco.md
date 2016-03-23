<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 管理员推荐相关接口</a>
<ul>
<li><a href="#sec-1-1">1.1. 管理员发送实时推荐任务</a></li>
</ul>
</li>
</ul>
</div>
</div>


# 管理员推荐相关接口

## 管理员发送实时推荐任务

`/special_feed/admin/send_reco_task/<feed_id:str>/`
-   Method: GET
-   Params:
    -   无
-   Return:
    -   status: 状态 ok， form\_error定制id有问题
    -   msg: ok
    -   task\_id: 任务ID
-   Example:
    -   <http://127.0.0.1:8080/special_feed/admin/send_reco_task/56c539c58230db59138ddb29/>
