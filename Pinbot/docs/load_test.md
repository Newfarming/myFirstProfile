<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 对www.pinbot.me压力测试</a>
<ul>
<li><a href="#sec-1-1">1.1. 服务器配置</a></li>
<li><a href="#sec-1-2">1.2. 用户最常访问的几个接口</a>
<ul>
<li><a href="#sec-1-2-1">1.2.1. 用户定制推荐简历列表(查询接口，数据存在Mongo中, 需要登录)</a></li>
<li><a href="#sec-1-2-2">1.2.2. 简历详情页展示(查询接口，不需要登录，简历数据存于Mongo业务数据是MySQL)</a></li>
<li><a href="#sec-1-2-3">1.2.3. 简历中心(查询接口，需要登录，简历数据存于Mongo业务数据是MySQL)</a></li>
<li><a href="#sec-1-2-4">1.2.4. 对推荐结果不感兴趣(更新接口，需要登录，更新Mongo数据)</a></li>
</ul>
</li>
<li><a href="#sec-1-3">1.3. 历史504原因总结</a>
<ul>
<li><a href="#sec-1-3-1">1.3.1. RabbitMQ 由于异步任务过多挂掉</a></li>
<li><a href="#sec-1-3-2">1.3.2. Mongo慢查询导致集群锁住</a></li>
<li><a href="#sec-1-3-3">1.3.3. MySQL慢查询导致MySQL负载过高</a></li>
<li><a href="#sec-1-3-4">1.3.4. 总结：</a></li>
</ul>
</li>
<li><a href="#sec-1-4">1.4. 预计有瓶颈的地方</a>
<ul>
<li><a href="#sec-1-4-1">1.4.1. MySQL单机</a></li>
</ul>
</li>
<li><a href="#sec-1-5">1.5. 之前用过的压力测试工具</a></li>
</ul>
</li>
</ul>
</div>
</div>


# 对www.pinbot.me压力测试

author: runforever

## 服务器配置

www.pinbot.me的服务是使用阿里云的服务器，配置如下:
-   4核CPU
-   8G内存
-   5M的带宽

内核调优配置:

    vm.swappiness = 0
    net.ipv4.neigh.default.gc_stale_time=120
    net.ipv4.conf.all.rp_filter=0
    net.ipv4.conf.default.rp_filter=0
    net.ipv4.conf.default.arp_announce = 2
    net.ipv4.conf.all.arp_announce=2
    net.ipv4.tcp_max_tw_buckets = 5000
    net.ipv4.tcp_syncookies = 1
    net.ipv4.tcp_max_syn_backlog = 1024
    net.ipv4.tcp_synack_retries = 2
    net.ipv6.conf.all.disable_ipv6 = 1
    net.ipv6.conf.default.disable_ipv6 = 1
    net.ipv6.conf.lo.disable_ipv6 = 1
    net.ipv4.conf.lo.arp_announce=2

    net.core.netdev_max_backlog = 400000
    #该参数决定了，网络设备接收数据包的速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目。

    net.core.optmem_max = 10000000
    #该参数指定了每个套接字所允许的最大缓冲区的大小

    net.core.rmem_default = 10000000
    #指定了接收套接字缓冲区大小的缺省值（以字节为单位）。

    net.core.rmem_max = 10000000
    #指定了接收套接字缓冲区大小的最大值（以字节为单位）。

    net.core.somaxconn = 65535
    #Linux kernel参数，表示socket监听的backlog(监听队列)上限

    net.core.wmem_default = 11059200
    #定义默认的发送窗口大小；对于更大的 BDP 来说，这个大小也应该更大。

    net.core.wmem_max = 11059200
    #定义发送窗口的最大大小；对于更大的 BDP 来说，这个大小也应该更大。

    net.ipv4.conf.all.rp_filter = 1
    net.ipv4.conf.default.rp_filter = 1
    #严谨模式 1 (推荐)
    #松散模式 0

    net.ipv4.tcp_congestion_control = bic
    #默认推荐设置是 htcp

    net.ipv4.tcp_window_scaling = 0
    #关闭tcp_window_scaling
    #启用 RFC 1323 定义的 window scaling；要支持超过 64KB 的窗口，必须启用该值。

    net.ipv4.tcp_ecn = 0
    #把TCP的直接拥塞通告(tcp_ecn)关掉

    net.ipv4.tcp_sack = 1
    #关闭tcp_sack
    #启用有选择的应答（Selective Acknowledgment），
    #这可以通过有选择地应答乱序接收到的报文来提高性能（这样可以让发送者只发送丢失的报文段）；
    #（对于广域网通信来说）这个选项应该启用，但是这会增加对 CPU 的占用。

    net.ipv4.tcp_max_tw_buckets = 10000
    #表示系统同时保持TIME_WAIT套接字的最大数量

    net.ipv4.tcp_max_syn_backlog = 8192
    #表示SYN队列长度，默认1024，改成8192，可以容纳更多等待连接的网络连接数。

    net.ipv4.tcp_syncookies = 1
    #表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0，表示关闭；

    net.ipv4.tcp_timestamps = 1
    #开启TCP时间戳
    #以一种比重发超时更精确的方法（请参阅 RFC 1323）来启用对 RTT 的计算；为了实现更好的性能应该启用这个选项。

    net.ipv4.tcp_tw_reuse = 1
    #表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭；

    net.ipv4.tcp_tw_recycle = 1
    #表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭。

    net.ipv4.tcp_fin_timeout = 10
    #表示如果套接字由本端要求关闭，这个参数决定了它保持在FIN-WAIT-2状态的时间。

    net.ipv4.tcp_keepalive_time = 1800
    #表示当keepalive起用的时候，TCP发送keepalive消息的频度。缺省是2小时，改为30分钟。

    net.ipv4.tcp_keepalive_probes = 3
    #如果对方不予应答，探测包的发送次数

    net.ipv4.tcp_keepalive_intvl = 15
    #keepalive探测包的发送间隔

    #net.ipv4.tcp_mem
    #确定 TCP 栈应该如何反映内存使用；每个值的单位都是内存页（通常是 4KB）。
    #第一个值是内存使用的下限。
    #第二个值是内存压力模式开始对缓冲区使用应用压力的上限。
    #第三个值是内存上限。在这个层次上可以将报文丢弃，从而减少对内存的使用。对于较大的 BDP 可以增大这些值（但是要记住，其单位是内存页，而不是字节）。

    net.ipv4.tcp_rmem = 32768 131072 16777216
    #与 tcp_wmem 类似，不过它表示的是为自动调优所使用的接收缓冲区的值。

    net.ipv4.tcp_wmem = 30000000 30000000 30000000
    #为自动调优定义每个 socket 使用的内存。
    #第一个值是为 socket 的发送缓冲区分配的最少字节数。
    #第二个值是默认值（该值会被 wmem_default 覆盖），缓冲区在系统负载不重的情况下可以增长到这个值。
    #第三个值是发送缓冲区空间的最大字节数（该值会被 wmem_max 覆盖）。

    net.ipv4.ip_local_port_range = 1024 65000
    #表示用于向外连接的端口范围。缺省情况下很小：32768到61000，改为1024到65000。

    #net.ipv4.netfilter.ip_conntrack_max=65535
    #设置系统对最大跟踪的TCP连接数的限制

    net.ipv4.tcp_slow_start_after_idle = 0
    #关闭tcp的连接传输的慢启动，即先休止一段时间，再初始化拥塞窗口。

    net.ipv4.route.gc_timeout = 100
    #路由缓存刷新频率，当一个路由失败后多长时间跳到另一个路由，默认是300。

    net.ipv4.tcp_syn_retries = 1
    #在内核放弃建立连接之前发送SYN包的数量。

    net.ipv4.icmp_echo_ignore_broadcasts = 1
    # 避免放大攻击

    net.ipv4.icmp_ignore_bogus_error_responses = 1
    # 开启恶意icmp错误消息保护

    #net.inet.udp.checksum=1
    #防止不正确的udp包的攻击

    net.ipv4.conf.default.accept_source_route = 0
    #是否接受含有源路由信息的ip包。参数值为布尔值，1表示接受，0表示不接受。
    #在充当网关的linux主机上缺省值为1，在一般的linux主机上缺省值为0。
    #从安全性角度出发，建议你关闭该功能。

Web服务使用Nginx和uWSGI搭建
Nginx关键配置:

    user www-data;
    worker_processes 4;
    pid /run/nginx.pid;
    worker_cpu_affinity 0001 0010 0100 1000;
    worker_rlimit_nofile 65535;

    events {
        use epoll;
        worker_connections 51200;
        # multi_accept on;
    }

uWSGI关键配置:

    # 8个web worker 每个web worker最大监听20000个请求
    master = true
    processes = 8
    thread = 100
    thread-stacksize = 512
    stats = 127.0.0.1:9194
    buffer-size = 65535
    enable-threads = true
    http-timeout = 60
    socket-timeout = 60
    pp = /home/deploy/Pinbot
    module = Pinbot.wsgi
    chmod-socket = 666
    harakiri = 60
    max-requests = 20000
    listen = 20000
    no-orphans

根据服务器配置期望的测试结果：至少能扛住2w并发

## 用户最常访问的几个接口

### 用户定制推荐简历列表(查询接口，数据存在Mongo中, 需要登录)

URL: `/special_feed/feed_list/5301d989fb6dec344c92b4fe`
-   Method: GET
-   Params:
    -   start: 开始页数
    -   latest: 是否未读 0 或者1
    -   send: 是否投递 0 或者 1
    -   partner: 是否人才伙伴推荐 0或者1
-   Return:
    -   status:
        -   ok: 成功
        -   no\_feed: 没有新增任何定制
    -   total\_recommend\_count: 总推荐数
    -   total\_count: 显示总数
    -   newest\_recommend\_count: 新推荐数
    -   feed\_query\_count: 查询总数
    -   next\_start: 下一页
    -   data: 用户推荐数据 [{feed: {}, pub\_time: 'xxx'}, {feed: {}}]
        -   feed:
            -   keywords: 推荐关键词 ['数据挖掘', '爬虫']
            -   id: 定制的数据库ID
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
            -   last\_contact: 最后联系
            -   hr\_evaluate: HR评价
            -   gender: 性别
            -   age: 年龄
            -   self\_evaluation: 自我评价
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
        -   favStatus: 是否关注， true false
        -   user\_read\_status: 用户阅读状态
        -   pub\_time: 展示时间
        -   calc\_time: 计算时间
        -   id: feed\_result推荐结果数据的ID
        -   tags: 标签, 包含关键词，学校类别等信息

### 简历详情页展示(查询接口，不需要登录，简历数据存于Mongo业务数据是MySQL)

接口地址：<http://www.pinbot.me/resumes/display/53042d2ffb6dec2fc8a44093/>

### 简历中心(查询接口，需要登录，简历数据存于Mongo业务数据是MySQL)

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

### 对推荐结果不感兴趣(更新接口，需要登录，更新Mongo数据)

URL: `/feed/modify_feed_result`
-   Method: GET
-   Params:
    -   feed\_id: 定制objectid
    -   resume\_id: 简历objectid
    -   reco\_index: -150 删除  150恢复
-   Return:
    -   status: 状态 ok
    -   msg: ok

## 历史504原因总结

### RabbitMQ 由于异步任务过多挂掉

系统访问日志用异步的方式写入导致RabbitMQ队列满了直接挂掉
解决方案：同步写日志，不使用RabbitMQ

### Mongo慢查询导致集群锁住

解决方案：重启Mongo主节点或者kill掉慢查询，开启慢查询日志，定期优化查询，使用查询前用explain来看查询命中索引情况

### MySQL慢查询导致MySQL负载过高

解决方案: kill掉慢查询，开启慢查询日志，定期优化查询，不用的数据定期清理掉

### 总结：

504基本都是由于数据库等服务慢导致uWSGI响应慢，不是uWSGI的处理能力不够

## 预计有瓶颈的地方

### MySQL单机

MySQL单机的性能目前并不是很清楚，用户的业务数据都是存在MySQL里面，
预计这里是性能瓶颈

## 之前用过的压力测试工具

测试机器Mac air 4核 4G 内存，2000个并发测试主页没有问题。没有测过更高的并发因为测试机器内存不够
