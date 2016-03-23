// 导航栏通知列表
$(function() {
    var $title = $('#JS_toggle_notice'),
        $notice_list = $('.notice-list'),
        hour = 1,
        exp = new Date(),
        domain = document.domain,
        cookName = 'notice_list';
    exp.setTime(exp.getTime() + hour * 60 * 60 * 1000);

    // 无通知，通知列表默认收起
    if ($('#JS_no_notice').length != 0) {
        $notice_list.hide();
        document.cookie = cookName + '=hidden' + ";path=/;domain=" + domain + ";expires=" + exp.toGMTString();
        $title.removeClass('selected');
    }

    // 通过cookie判断导航通知列表状态
    if (document.cookie.indexOf('notice_list=hidden') != -1) {
        $notice_list.hide();
        $title.removeClass('selected');
    } else {
        $notice_list.show();
        $title.addClass('selected');
    }

    // 展开通知
    $title.on('click', function(e) {
        var $this = $(this);
        $notice_list.toggle();
        if ($this.hasClass('selected')) {
            document.cookie = cookName + '=hidden' + ";path=/;domain=" + domain + ";expires=" + exp.toGMTString();
            $this.removeClass('selected');
        } else {
            document.cookie = cookName + '=show' + ";path=/;domain=" + domain + ";expires=" + exp.toGMTString();
            $this.addClass('selected');
        }
    });

    // 查看全部通知
    $('#JS_view_notice').on('click', function() {
        $notice_list.hide();
        document.cookie = cookName + '=hidden' + ";path=/;domain=" + domain + ";expires=" + exp.toGMTString();
        $title.removeClass('selected');
        window.location.href = '/notify/';
    });

    // 收起
    $('#JS_hide_notice').on('click', function() {
        $notice_list.hide();
        document.cookie = cookName + '=hidden' + ";path=/;domain=" + domain + ";expires=" + exp.toGMTString();
        $title.removeClass('selected');
    });

    var onload_queue = [];
    var dom_loaded = false;

    function loadScriptAsync(src, callback) {
        var script = document.createElement('script');
        script.type = "text/javascript";
        script.async = true;
        script.src = src;
        script.onload = script.onreadystatechange = function() {
            if (dom_loaded)
                callback();
            else
                onload_queue.push(callback);
            // clean up for IE and Opera
            script.onload = null;
            script.onreadystatechange = null;
        };
        var head = document.getElementsByTagName('head')[0];
        head.appendChild(script);
    }

    function domLoaded() {
        dom_loaded = true;
        var len = onload_queue.length;
        for (var i = 0; i < len; i++) {
            onload_queue[i]();
        }
        onload_queue = null;
    };
    // Dean's dom:loaded code goes here
    // do stuff
    domLoaded();

    var styles = document.getElementsByTagName('link');
    var reg = /index\.css/;
    if (styles && styles.length) {
        for (var i = 0; i < styles.length; ++i) {
            if (reg.test(styles[i].href)) return false;
        }
        var popup = document.createElement('div');
        popup.innerHTML = '<a href="javascript:void(0);" id="admin_qq" class="online-service" title="客服热线"><span class="i-service">客服热线</span><div class="service-style"><p><i class="i-tele"></i>028-83330727</p><p><i class="i-qq"></i>800031490</p></div></a>';
        window.onload = function() {
            loadScriptAsync(
                "http://wpa.b.qq.com/cgi/wpa.php",
                function() {
                    //document.body.appendChild(popup);
                    BizQQWPA.addCustom({
                        aty: '0',
                        nameAccount: '800031490',
                        selector: 'admin_qq'
                    });

                    var yinxiao_qqs = document.getElementsByClassName('yingxiao_qq');
                    for (var i = 0; i < yinxiao_qqs.length; ++i) {
                        BizQQWPA.addCustom({
                            aty: '0',
                            nameAccount: '800031490',
                            selector: yinxiao_qqs[i].id
                        });
                    }

                }
            );
        }
    }


})