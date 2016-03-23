var notHasCard = function(){
    var html = $('#JS_no_card').html();
    $.LayerOut({
        html: html,
        dialogCss: 'width:540px;'
    });
};

var markResume = function(){
    var html = $('#JS_to_mark').html();
    $.LayerOut({
        html: html,
        closeByShadow: false,
        dialogCss: 'height:250px;'
    });
};

var isHasCompanyInfo = function( callback ){
  var url = '/companycard/get/json/?' + Math.random();
    $.get( url , {} , function( res ){
      var msg = {
            8: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>恭喜，简历购买成功！</p>',
            9: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>您好！正在为您准备简历。请稍后在简历中心查收！</p>',
            1: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请先购买简历套餐，便能购买您喜欢的简历了。</p>',
            2: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>您已购买过此简历，请到简历中心查查看！</p>',
            3: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>抱歉，您的点数不足！</p>',
            4: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>抱歉，操作失败了，请刷新重试一下？</p>'
        };

        if( res && res.status ){
            if( res.has_mark ){
                markResume();
                return;
            };
            window.infos = res;
            if( typeof callback == 'function' ){
                callback();
            };
        }else if( res && res.data ){
            //购买成功
            if(res.data==8){
              $('#js-nav-meet').addClass('nav-red');
              $('#js-nav-qusetion').removeClass('nav-blue');
              $('#js-faq-click').addClass('faq-robot-meet').removeClass('faq-robot-qusetion').find('span').text('约面话术');
              $('#js-meet-content').show();
              $('#js-qusetion-content').hide();
            }
            $.alert( msg[ res.data ] );
        }else{
            $.alert('请求失败，请刷新重试！');
        };

    }, 'json' );
};

var chooseCard = function(){
    var html = $('#JS_choose_cards').html(),
        jobs = infos.jobs || [],
        width = 925;

    if( !jobs.length ){
        notHasCard();
        return;
    };

    if( jobs.length == 1 ){
        width = 490;
    };

    $.LayerOut({
        html: html,
        closeByShadow: false,
        dialogCss: 'width:' + width + 'px; height:610px;'
    });

    $.intentionCard({
        list: jobs,
        allowSend: true,
        contentDom: '#JS_jobs_ajax_content',
        callback: cardScroll
    });

};

var directDownload = function( obj ){
    //Popup.pending();
    var $this = $( obj ),
        feed_id = $( 'body' ).attr( 'data-feed_id' ),
        resume_id = $this.attr( 'data-resumeid' ),
        sendid = $this.attr( 'data-sendid' ),
        job_id = $this.attr('data-job_id'),
        data = {
            feed_id: feed_id,
            resume_id: resume_id,
            sendid: sendid,
            job_id: job_id
        },
        msg = {
            8: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>恭喜，简历购买成功！</p>',
            9: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>您好！正在为您准备简历。请稍后在简历中心查收！</p>',
            1: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请先购买简历套餐，便能购买您喜欢的简历了。</p>',
            2: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>您已购买过此简历，请到简历中心查查看！</p>',
            3: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>抱歉，您的点数不足，请先购买点数！</p>',
            4: '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>抱歉，操作失败了，请刷新重试一下？</p>'
        };
    if( $this.attr('disabled') ) return false;
    $this.attr('disabled', true);
    var req = $.get('/transaction/buy', data, function(ret) {
        $this.attr('disabled', false);
        if (payTimer) {
          clearTimeout(payTimer);
        };
        if (ret && ret.status) {
          if (ret.data == 8) {
            $.alert( msg[ ret.data ] , function(){
                location.reload();
            });
          } else if (ret.data == 9) {
            $.alert( msg[ ret.data ] , function(){
                location.reload();
            });
          };
        } else {
          if (/^[1234]$/.test(ret.data)) {
            $.alert( msg[ ret.data ] );
          };
        };
    }).fail(function(ret) {
        $.alert( msg[ 4 ] );
    });

    payTimer = setTimeout(function() {
        req.abort();
        $.alert( msg[ 4 ] );
    }, 20000);
};

$(function(){

    var alertUpgrade=function(point){
        var alertModal=function(title, annotation, msg, btnTitle, btnFunc) {
            var cssStar = (annotation == '') ? '' : 'annotation-star';
            return '<div class="mission-success pay-mission-success">' +
                '<h3 class="text-center"><i class="i-ms"></i>' + title + '</h3>' +
                //'<span class="annotation ' + cssStar + '">' + annotation + '</span>' +
                '<p class="c607d8b f14 text-center pd-bottom-20">' + msg + '</p>' +
                '<p class="mt20 text-center">' +
                '<a class="btn btn-blue btn-click-ok" href="javascript:void(0);">' + btnTitle + '</a>' +
                '</p>' +
                '</div>';
        };
        $.LayerOut({
            html: alertModal(
                '<span class="pay-alert"></span><span class="pay-title">简历下载失败！您的聘点不足！</span>',
                '',
                '您的聘点数量：<span class="cf46c62">'+point+'</span>个，请升级成为聘宝会员，或者<a href="/payment/point_recharge/" class="c63c2ec">购买聘点</a>。<br><a href="javascript:void(0);"  id="JS_service_btn" class="c63c2ec">有疑问请联系我们</a>',
                '升级聘宝会员',
                null
            ),
            afterClose: function() {
                //$._LayerOut.close();
            }
        });
        $(".modal").undelegate(".btn-click-ok").delegate(".btn-click-ok", "click", function(e) {
            $._LayerOut.close();
            document.location.href='/vip/role_info/';
        });
        $.Menu();

    };

    //未发送企业名片直接下载
    $('.buy-status-1 a').on('click', function(e) {
        e.preventDefault();

        //检查是否是聘宝会员
        $.ajax({
            type: 'get',
            url: '/vip/get_user_info/',
            success: function(data){
                //console.log(data);
                if(data.status!=undefined && data.status=='ok'){
                    //非会员
                    if(parseInt(data.pinbot_point)<=0){
                        alertUpgrade(data.pinbot_point);
                    }else{
                        var hasCompanyCard = function(){
                            var html = $('#JS_has_card_html').html();
                            $.LayerOut({
                              html: html,
                              dialogCss: 'width:540px;'
                            });
                        };
                        isHasCompanyInfo( hasCompanyCard );
                    }
                }else{
                    alertUpgrade(data.pinbot_point);//data.pinbot_point
                    //$.alert('<p class="alert-notice">获取用户状态失败，请刷新再试！</p>');
                }
            },
            error:function(){
                //alertUpgrade(0);
                $.alert('<p class="alert-notice-center"><span>获取用户状态失败，请刷新再试！</span></p>');
            }
        });

    });

    //选择需要发送的企业名片
    $( document ).on( 'click' , '#JS_send_card_btn' , chooseCard );

    //直接点击发送企业名片
    $('.send-company-card .has-layer').on( 'click' , function(){
        isHasCompanyInfo( chooseCard );
    });

    //未发送企业名片直接下载
    $( document ).on( 'click' , '.JS_buy_not_sendcard' , function(){
        directDownload( this );
    });

    //发送了企业名片后直接下载
    $( '.JS_buy_after_sendcard' ).on( 'click' , function(){
        var that = this;
        $.confirm( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>您已发送了企业名片进行意向确认，还要再直接下载该简历吗？</p><p style="text-align:center;font-size:16px;">提醒：确认下载会在已扣3个点的基础上再扣除您10个点数</p>' , function(){
            directDownload( that );
        });
        return false;
    });

    //不合适点击
    $('.fit-btn').on('click', function(){
        var $this = $(this);
        var url = $this.attr('data-unfit_url');
        $.ajax({
            type: 'get',
            url: url,
            success: function(data){
                if(data && data.status == 'ok'){
                    location.reload();
                }
            }
        });
    });

});

