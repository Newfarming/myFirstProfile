# 帐号接口API

## 注册登录

### 注册

URL: `/users/account_register/`
-   Method: POST
-   Params: 使用json格式提交
    -   user\_email: 企业邮箱
    -   company\_name: 企业名称
    -   password: 密码
    -   phone: 联系电话
    -   name: 真实姓名
    -   qq: 联络qq
    -   code: 短信验证码
    -   select_fields: 领域列表

-   Return:
    -   status: 状态 ok 注册成功， form\_error 表单错误
    -   msg: message 信息
    -   errors: 表单错误具体信息
    -   username: 用户名
    -   redirect_url: 自动跳转链接

### 登陆

URL: `/users/account_login/`
-   Method: POST
-   Params: 使用json格式提交
    -   username: 用户账号/手机或邮箱
    -   password: 密码

-   Return:
    -   status: 状态 ok 登陆成功， form\_error 表单错误
    -   msg: message 信息
    -   errors: 表单错误具体信息
    -   username: 用户名
    -   redirect_url: 自动跳转链接
    -   user\_industry: 用户所属行业

## 短信验证

### 申请短信验证

URL: `/users/send_sms_code/`
-   Method: POST
-   Params: 使用json格式提交
    -   action_name: 业务类型(AccountReg/ChangePwd/ChangeMobile)
    -   mobile: 手机号

-   Return:
    -   status: 状态 ok 验证码请求成功， error 表单错误
    -   msg: message 信息

### 短信验证码验证
URL: `/users/vaild_sms_code/`
-   Method: POST
-   Params: 使用json格式提交
    -   action_name: 业务类型(AccountReg/ChangePwd/ChangeMobile)
    -   code: 手机上收到的短信验证码
    -   mobile: 手机号

-   Return:
    -   status: 状态 ok 验证码请求成功， error 表单错误
    -   msg: message 信息

## 账号绑定

### 修改手机号
URL: `/users/change_mobile/`
-   Method: POST
-   Params: 使用json格式提交
    -   password: 用户密码
    -   code: 短信验证码
    -   mobile: 手机号

-   Return:
    -   status: 状态 ok 验证码请求成功， error 表单错误
    -   msg: message 信息

### 判断接收邮箱是否绑定
URL: `/users/notify_email_is_bind/`
-   Method: GET
-   Return:
    -   status: 状态 ok 请求成功， error 请求失败
    -   is_bind: true 已绑定, false 未绑定
    -   msg: message 信息
    -   notify_email: 接收邮箱地址


### 判断微信账号是否绑定
URL: `/users/weixin_is_bind/`
-   Method: GET
-   Return:
    -   status: 状态 ok 请求成功， error 请求失败
    -   is_bind: true 已绑定, false 未绑定
    -   msg: message 信息


### 发送邮箱验证码
URL: `/users/send_email_code/`
-   Method: POST
-   Params: 使用json格式提交
    -   password: 用户密码
    -   email: 新的接收邮箱


-   Return:
    -   status: 状态 ok 验证码请求成功， error 表单错误
    -   msg: message 信息


### 修改接收邮箱
URL: `/users/change_notify_email/`
-   Method: POST
-   Params: 使用json格式提交
    -   password: 用户密码
    -   code: 邮箱验证码
    -   email: 新的接收邮箱


-   Return:
    -   status: 状态 ok 验证码请求成功， error 表单错误
    -   msg: message 信息

### 重新发送绑定接收邮箱链接
URL : `/users/resend_bind_email/`
-   Method: GET
-   Return:
    -   status: 状态 ok 请求成功， error 请求失败
    -   msg: message 信息

## 密码服务
### 根据手机号找回密码
URL: `/users/change_pwd_by_mobile/`
-   Method: POST
-   Params: 使用json格式提交
    -   mobile: 手机号
    -   code: 短信验证码
    -   password: 新用户密码
    -   re_password: 新用户密码_重复


-   Return:
    -   status: 状态 ok 验证码请求成功， error 表单错误
    -   msg: message 信息

### 根据旧密码修改新密码
URL: `/users/change_my_pwd/`
-   Method: POST
-   Params: 使用json格式提交
    -   old_password: 旧密码
    -   new_password: 新密码
    -   confirm_password: 新密码_重复


-   Return:
    -   status: 状态 ok 修改密码成功， error 表单错误
    -   msg: message 信息

## 个人信息
### 修改个人信息
URL: `/users/change_my_info/`
-   Method: POST
-   Params: 使用json格式提交
    -   realname: 姓名
    -   qq: qq号码


-   Return:
    -   status: 状态 ok 修改成功， error 表单错误
    -   msg: message 信息

### 修改企业信息
URL: `/users/change_company_info/`
-   Method: POST
-   Params: 使用json格式提交
    -   company_name: 公司名称
    -   company_url: 公司主页


-   Return:
    -   status: 状态 ok 修改成功， error 表单错误
    -   msg: message 信息

### 修改收货信息
URL: `/users/change_my_recv_info/`
-   Method: POST
-   Params: 使用json格式提交
    -   province: 省份
    -   city: 城市
    -   area: 区县
    -   street: 街道门牌号
    -   recv_name: 收货人姓名
    -   recv_phone: 收货人电话

-   Return:
    -   status: 状态 ok 修改成功， error 表单错误
    -   msg: message 信息


## 活动报名

### 申请新行业活动报名

URL: `/users/new_industry_bookin/`
-   Method: POST
-   Params: 使用json格式提交
    -   bookin_type: "1" 为4月16日北京场, "2" 为4月16日成都场

-   Return:
    -   status: 状态 ok 报名成功， error 报名失败
    -   msg: message 信息