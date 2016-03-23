<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 简历详情页接口</a>
<ul>
<li><a href="#sec-1-1">1.1. 安排面试接口</a></li>
<li><a href="#sec-1-2">1.2. 修改面试时间接口</a></li>
<li><a href="#sec-1-3">1.3. 简历购买记录接口</a></li>
<li><a href="#sec-1-4">1.4. 简历购买记录侧边栏数据</a></li>
<li><a href="#sec-1-5">1.5. 企业名片发送记录接口</a></li>
<li><a href="#sec-1-6">1.6. 创建自定义文件夹（提交数据用JSON格式）</a></li>
<li><a href="#sec-1-7">1.7. 更新自定义文件夹名（提交数据用JSON格式）</a></li>
<li><a href="#sec-1-8">1.8. 删除自定义文件夹</a></li>
<li><a href="#sec-1-9">1.9. 添加简历到自定义文件夹(提交数据用JSON)</a></li>
<li><a href="#sec-1-10">1.10. 自定义文件夹移除简历(提交数据用JSON)</a></li>
</ul>
</li>
</ul>
</div>
</div>


# 简历详情页接口

## 安排面试接口

`/resume/interview/send/<buy_record_id:int>/`
-   Method: POST
-   Content-Type: multipart/form-data
-   Params:
    -   interview\_time: 面试时间eg:(2015-12-26 12:02)
    -   code\_name: 标记状态 invite\_interview(安排面试), next\_interview(安排下一轮面试)
-   Return:
    -   status: 状态 ok, form\_error 表单错误
    -   msg: ok

## 修改面试时间接口

`/resume/interview_time/change/<interview_record_id:int>/`
-   Method: POST
-   Content-Type: multipart/form-data
-   Params:
    -   interview\_time: 面试时间eg:(2015-12-26 12:02)
-   Return:
    -   status: 状态 ok, form\_error 表单错误
    -   msg: ok

## 简历购买记录接口

`/resume/buy_record/list/`
-   Method: GET
-   Content-Type: multipart/form-data
-   Params:
    -   page: 页数
    -   mark: 简历类型
        -   no\_will: 无求职意愿
        -   send\_offer: 发送offer
        -   entry: 入职
        -   eliminate: 淘汰
        -   pending: 进一步跟进
        -   unmark: 未标记
        -   interview\_stage: 面试阶段
        -   next\_interview: 下一轮面试
        -   invite\_interview: 安排面试
        -   unconfirm: 待定
        -   break\_invite: 爽约
        -   entry\_stage: 入职阶段
    -   category: 自定义文件夹名字
    -   search\_fields: 搜索类型(position\_title职位名 company\_name公司名 name姓名 school学校 all简历全文)
    -   keywords: 搜索关键词
-   Return:
    -   status: 状态 ok
    -   msg: ok
    -   count: 数据总数
    -   current: 当前页数
    -   is\_paginated: 是否分页
    -   pages: 总页数
    -   data: 购买记录
        -   id: 记录ID
        -   status: 简历购买状态 LookUp 可以查看，secret 保密，Start购买中
        -   current\_mark: 当前标记状态
        -   current\_mark\_display: 当前标记状态展示
        -   mark\_time: 标记时间
        -   resume\_id: 简历ID
        -   feed\_id: 用户定制ID
        -   status\_display: 简历购买状态展示
        -   op\_time: 操作时间
        -   interview:
            -   id: 记录ID
            -   interview\_count: 面试次数
            -   interview\_time: 面试时间
        -   contact\_info: 联系信息
            -   qq: QQ号
            -   phone: 电话
            -   name: 姓名
            -   email: 邮箱
            -   status: 简历联系信息状态 public 公开, secret 保密
        -   comment\_info: 评价信息
            -   content: 备注信息
            -   comment\_time: 备注时间
            -   resume\_id: 简历ID
        -   resume: 简历信息
            -   job\_target: 期望职位信息
                -   job\_career: 职业生涯
                -   salary: 期望薪资范围
                -   job\_category: 职位类型 e.g: 全职 实习
                -   job\_hunting\_state: 求职状态
                -   job\_industry: 职位领域
                -   enroll\_time: 注册时间
                -   expectation\_area: 期望工作城市
            -   education: 教育经历
                -   school: 学校
                -   start\_time: 开始时间
                -   end\_time: 结束时间
                -   degree: 学位
                -   major: 专业
            -   address: 现居地
            -   id: 简历的ID
            -   gender: 性别
            -   age: 年龄
            -   works: 工作经历
                -   salary: 薪资
                -   company\_category: 公司类型
                -   start\_time: 开始时间
                -   position\_category: 职位类别
                -   company\_scale: 公司规模
                -   compnay\_name: 公司名称
                -   industry\_category: 公司类别
                -   position\_title: 职位名称
                -   job\_desc: 职位描述
                -   duration: 持续时间
                -   end\_time: 结束时间
            -   work\_years: 工作年限

## 简历购买记录侧边栏数据

`/resume/side/`
-   Method: GET
-   Content-Type: multipart/form-data
-   Params:
    -   无
-   Return:
    -   status: 状态 ok
    -   msg: ok
    -   data: 购买记录
        -   mark\_count: 侧边数据统计
            -   total: 总数
            -   no\_will: 无求职意愿数量
            -   next\_interview: 下一轮面试数量
            -   invite\_interview: 安排面试数量
            -   job\_interview: 参加面试数量
            -   send\_offer: 发送offer数量
            -   entry: 入职数量
            -   eliminate: 淘汰数量
            -   pending: 进一步跟进
            -   unmark: 未标记
            -   unconfirm: 待定数量
            -   break\_invite: 爽约数量
        -   categories: 自定义文件夹
            -   id: 记录ID
            -   category\_name: 分类名
            -   resume\_num: 简历数量
        -   watch\_count: 收藏数量
        -   send\_card\_count: 企业名片数量

## 企业名片发送记录接口

`/resume/send_record/list/`
-   Method: GET
-   Content-Type: multipart/form-data
-   Params:
    -   page: 页数
    -   search\_fields: 搜索类型(position\_title职位名 company\_name公司名 name姓名 school学校 all简历全文)
    -   keywords: 搜索关键词
-   Return:
    -   status: 状态 ok
    -   msg: ok
    -   count: 数据总数
    -   current: 当前页数
    -   is\_paginated: 是否分页
    -   pages: 总页数
    -   data: 购买记录
        -   id: 记录ID
        -   send\_status: 发送情况 0 发送失败  1 发送成功  2 待发送
        -   send\_status\_display: 发送状态展示
        -   send\_time: 发送时间
        -   resume\_id: 简历ID
        -   feed\_id: 定制ID
        -   has\_download: 是否下载
        -   download\_status: 下载状态
        -   feedback\_time: 求职者反馈时间
        -   feedback\_status: 反馈状态 0 等待确认 1 感兴趣 2 不感兴趣 3 无回复
        -   feedback\_status\_display: 反馈状态展示
        -   contact\_info: 联系信息
            -   qq: QQ号
            -   phone: 电话
            -   name: 姓名
            -   email: 邮箱
            -   status: 简历联系信息状态 public 公开, secret 保密
        -   comment\_info: 评价信息
            -   content: 备注信息
            -   comment\_time: 备注时间
            -   resume\_id: 简历ID
        -   resume\_info: 简历信息
            -   job\_target: 期望职位信息
                -   job\_career: 职业生涯
                -   salary: 期望薪资范围
                -   job\_category: 职位类型 e.g: 全职 实习
                -   job\_hunting\_state: 求职状态
                -   job\_industry: 职位领域
                -   enroll\_time: 注册时间
                -   expectation\_area: 期望工作城市
            -   education: 教育经历
                -   school: 学校
                -   start\_time: 开始时间
                -   end\_time: 结束时间
                -   degree: 学位
                -   major: 专业
            -   address: 现居地
            -   id: 简历的ID
            -   gender: 性别
            -   age: 年龄
            -   works: 工作经历
                -   salary: 薪资
                -   company\_category: 公司类型
                -   start\_time: 开始时间
                -   position\_category: 职位类别
                -   company\_scale: 公司规模
                -   compnay\_name: 公司名称
                -   industry\_category: 公司类别
                -   position\_title: 职位名称
                -   job\_desc: 职位描述
                -   duration: 持续时间
                -   end\_time: 结束时间
            -   work\_years: 工作年限

## 创建自定义文件夹（提交数据用JSON格式）

`/resume/category/create/`
-   Method: POST
-   Content-Type: JSON
-   Params:
    -   category\_name: 文件夹名称
-   Return:
    -   status: 状态 ok, form\_error 表单错误
    -   msg: ok
    -   data:
        -   id: 数据库ID

## 更新自定义文件夹名（提交数据用JSON格式）

`/resume/category/update/<category_id:int>/`
-   Method: POST
-   Content-Type: JSON
-   Params:
    -   category\_name: 文件夹名称
-   Return:
    -   status: 状态 ok, form\_error 表单错误
    -   msg: ok
    -   data:
        -   id: 数据库ID

## 删除自定义文件夹

`/resume/category/delete/<category_id:int>/`
-   Method: GET
-   Content-Type: www-form
-   Params:
    -   无
-   Return:
    -   status: 状态 ok
    -   msg: ok

## 添加简历到自定义文件夹(提交数据用JSON)

`/resume/category_resume/<category_id:int>/`
-   Method: POST
-   Content-Type: JSON
-   Params:
    -   record\_id: [1123, 1124] 简历的ID，使用Array
-   Return:
    -   status: 状态 ok
    -   msg: ok

## 自定义文件夹移除简历(提交数据用JSON)

`/resume/category_resume/remove/<category_id:int>/`
-   Method: POST
-   Content-Type: JSON
-   Params:
    -   record\_id: [1123, 1124] 简历的ID，使用Array
-   Return:
    -   status: 状态 ok
    -   msg: ok
