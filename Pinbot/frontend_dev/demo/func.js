/**
 * 渲染展示列表
 * @param  {string} target [HTML id/class]
 * @param  {object} arr    [列表对象]
 * @return  {null}    [没有返回]
 */
var render = function(target, arr) {
    var objLen = function(obj) {
        var len = 0;
        for (var i in obj) {
            if (obj.hasOwnProperty(i)) {
                len++;
            }
        }
        return len;
    };
    if ($(target).length) {
        if(typeof arr == 'string'){
            $(target).html(arr);
        }else{
            var html = '';
            var style = '';
            var xh = 0;
            var length = objLen(arr);

            style += "<style>\n";
            html += ' <table border="1" cellpadding="10" cellspacing="2" width="100%"> ';

            var initType = function(type) {
                if (type == 'img') {
                    return '<span class="type" title="纯图片">纯图片</span>';
                } else if (type == 'clearPos') {
                    return '<span class="type" title="清除定位">清除定位</span>';
                } else {
                    return '<span class="type">' + type + '</span>';
                }
            };

            for (var i in arr) {
                var item = arr[i];

                style += "/* start " + item.title + " */\n";
                style += item.style + " \n";
                style += "/* end " + item.title + " */\n";

                if (xh % 3 == 0) html += '    <tr>';

                var type = (item.type && item.type != '') ? initType(item.type) : '';
                html += '        <td class="f-width-33">';
                html += '            <div class="title">［' + item.title + '］' + type + '</div>';
                html += '            <div class="show">';
                html += item.source;
                html += '            </div>';
                html += '            <textarea class="style">' + item.style + '</textarea>';
                html += '            <textarea class="source">' + item.source.replace(/(clearPos)/ig, '') + '</textarea>';
                html += '        </td>';

                if (xh % 3 == 2) html += '    </tr>';
                if (xh == length - 1) html += '    </tr>';
                xh++;
            }

            style += "</style>\n";
            html += '</table>';

            $(target).html(style + html);
        }
    }
};

/**
 * 返回页头HTML
 * @param  {string} target [HTML id/class]
 * @return  {null}    [没有返回]
 */
var header = function(target) {
    if ($(target).length) {
        var html = '<div class="inner-wrap clearfix">' +
            '<h1 class="logo-menu-bg-fix"><a href="http://www.pinbot.me/" title="聘宝，专业人才推荐" style="overflow:hidden;text-indent: -9999px;"><img class="logo pinbot-logo" src="/static/b_index/img/logo_121x75.png" border="0"></a></h1>' +
            '<div class="nav-wrap">' +
            '<ul class="main-nav clearfix">' +
            '<li class="curr"> <a href="/special_feed/page/"><i class="ic ic-nav ic-nav-feed"></i>职位定制</a></li>' +
            '<li class="" > <a href="/transaction/bought/"><i class="ic ic-nav ic-nav-resume"></i>简历中心</a></li>' +
            '<li class="" > <a href="/payment/my_account/"><i class="ic ic-nav ic-nav-pay"></i>我的钱包</a></li>' +
            '<li class=""><a href="/companycard/get/"><i class="ic ic-nav ic-nav-setting"></i>企业名片</a></li>' +
            '<li class=""><a href="/partner/home/"><i class="i-new i-new-hide"></i>互助招聘</a></li>' +
            '<li class=""><a href="/promotion_point/link/" class="invite-reward-icon"><i class="ic ic-nav ic-nav-setting"></i>邀请有奖</a></li>' +
            '</ul>' +
            '<div class="main-user-control">' +
            '<a class="main-user-control-icon "></a>' +
            '<ul class="main-user-control-dropdown-menu">' +
            '<li><a href="/users/profile/">个人设置</a></li>' +
            '<li><a href="/chat/" class="">我的会话</a></li>' +
            '<li><a href="/notify/">我的通知</a></li>' +
            '<li class="menu-exit"><a href="/signout">退出</a></li>' +
            '</ul>' +
            '</div>' +
            '<div class="main-notice">' +
            '<a class="notice-handle selected" href="javascript:void(0)" id="JS_toggle_notice">通知</a>' +
            '<ul class="notice-list">' +
            '<li class="no-notice" id="JS_no_notice">暂无新的通知</li>' +
            '<li class="last-child clearfix">' +
            '<a href="javascript:void(0)" id="JS_view_notice" class="left">查看全部通知</a>' +
            '<a href="javascript:void(0)" id="JS_hide_notice" class="right">收起</a>' +
            '</li>' +
            '</ul>' +
            '</div>' +
            '</div>' +
            '</div>';
        $(target).html(html);
    }
};

/**
 * 返回菜单HTML
 * @param  {string} target [HTML id/class]
 * @return  {null}    [没有返回]
 */
var menu = function(target, currentName) {
    if ($(target).length) {
        var html = '<div id="resume-list-header">' +
            '<ul class="main-subnav-list">' +
            '<li class="first-child ">' +
            '<a href="http://localhost:3000/index.html">聘宝常用组件库</a>' +
            '</li>' +
            '<li class="' + ((currentName == 'Button按钮') ? 'on' : '') + '">' +
            '<a href="http://localhost:3000/button.html">Button按钮</a>' +
            '</li>' +
            '<li class="' + ((currentName == 'Icon图标') ? 'on' : '') + '">' +
            '<a href="http://localhost:3000/icon.html">Icon图标</a>' +
            '</li>' +
            '<li class="' + ((currentName == 'Modal弹窗') ? 'on' : '') + '">' +
            '<a >Modal弹窗</a>' +
            '</li>' +
            '<li class="' + ((currentName == 'Form表单') ? 'on' : '') + '">' +
            '<a >Form表单</a>' +
            '</li>' +
            '</ul>' +
            '</div>';
        $(target).html(html);
    }
};

/**
 * 返回正文HTML容器
 * @param  {string} target   [HTML id/class]
 * @param  {string} descName [正文描述]
 * @param  {string} Title    [正文标题]
 * @param  {string} info     [描述]
 * @return {null}          [没有返回]
 */
var container = function(target, descName, Title, info) {
    if ($(target).length) {
        var html = '<form name="uploadForm" novalidate="" autocomplete="off">' +
            '<div class="edit-form">' +
            '<div class="step-title">' +
            '<p class="text-center cf46c62 t-info">' + descName + '</p>' +
            '<h1 class="text-center h-step1">' +
            Title +
            '<i class="sprite i-toggle" id="h_step1"></i>' +
            '</h1>' +
            '<p class="text-center cf46c62 t-ps">' + info + '</p>' +
            '</div>' +
            '<section id="JS_resume">' +
            '<div class="form-panel list-component">' +
            '</div>' +
            '</section>' +
            '<!-- <div class="form-handle">' +
            '<a href="javascript:void(0)" class="btn btn-blue-240">下一页</a>' +
            '</div> -->' +
            '</div>' +
            '</form>';
        $(target).html(html);
    }
};