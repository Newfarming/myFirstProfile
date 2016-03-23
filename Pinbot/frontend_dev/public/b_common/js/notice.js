/*
    author: 516758517@qq.com
    date:  2015-05-04
    description: 全站标记通知(基于jquery)
 */

var Notice = ( function( $ , undefined ){
    if( !$ ) return;
    var notice = function( setting ){
        return new notice.prototype.init( setting );
    };
    notice.prototype = {
        constructor: notice,
        init: function( setting ){
            this.setting = $.extend({
                loop: false
            },setting);
            this.setting.cookName = 'pb_notice';
            this.getData();
        },
        getData: function(){
            var that = this;
            if( this.hasCookie() ) return;
            $.get( '/transaction/mark_notify/' , {
                ___: new Date().getTime()
            } , function( res ){
                if( !res || res.status != 'ok' || !res.has_mark || !res.redirect_url ) return;
                that.showMsg( res );
            } , 'json' );
        },
        hasCookie: function(){
            var cook = document.cookie;
            if( cook.length && cook.indexOf( this.setting.cookName + '=' ) > -1 ){
                return true;
            };
        },
        setCookie: function(){
            var hour = 1,
                exp  = new Date(),
                domain = document.domain;
            exp.setTime(exp.getTime() + hour*60*60*1000);
            document.cookie = this.setting.cookName + "=true" + ";path=/;domain=" + domain + ";expires=" + exp.toGMTString();
        },
        showMsg: function( res ){
            var url = res.redirect_url,
                html = '<div style="position:fixed;top:-74px;left:0;width:100%; background:#FFFFFF; padding: 25px 0; z-index: 98; text-align:center; font-size:15px;display:hide;border-bottom:solid 1px #eee;" id="JS_notice_tip_box">' +
                            '<span style="color:#444;display:inline-block;vertical-align:middle;">你还有简历未标记为完结状态！</span>' +
                            '<a style="color:#44b5e8;display:inline-block;vertical-align:middle;font-size:15px; text-decoration:underline;cursor:pointer;" data-href="' + url + '" class="JS_set_notice_cookie">现在去标记</a>' +
                            '<a style="display:inline-block;background:url(/static/b_common/img/ricon.png);width:23px; height:24px;vertical-align:middle;margin-left:40px;font-size:15px;cursor:pointer;" data-href="' + url + '" class="JS_set_notice_cookie"></a>' +
                            '<a href="javascript:;" style="display:inline-block; position:absolute; top: 50%; right: 20px; margin-top: -8px;background:url(/static/mark/img/close_tip.png); width: 16px; height:16px;font-size:15px;cursor:pointer;" id="JS_close_notice_btn_czc"></a>' +
                        '</div>';
            $('body').append( html );
            this.bindEvent();
        },
        bindEvent: function(){
            var that = this,
                top = $( window ).scrollTop();

            if( top > 60 ){
                $('#JS_notice_tip_box').show().animate( {top: 0} );
            }else{
                $('#JS_notice_tip_box').show().animate( {top: 60} );
            };

            $('#JS_close_notice_btn_czc').css({
                right: ( $( window ).width() - 1140 ) / 2 + 'px'
            }).on( 'click' , function(){
                $( this ).parent().remove();
                that.setCookie();
                $(window).off( 'scroll' , Notice.prototype.scroll );
            });

            $('.JS_set_notice_cookie').on( 'click' , function(){
                that.setCookie();
                location.href = $( this ).attr('data-href');
            });

            $(window).on( 'scroll' , window , Notice.prototype.scroll );
        },
        scroll: function(){
            var top = $( window ).scrollTop();
            if( top > 60 ){
                $('#JS_notice_tip_box').css( 'top' , 0 );
            }else{
                $('#JS_notice_tip_box').css( 'top' , '60px' );
            };
        }
    };
    notice.prototype.init.prototype = notice.prototype;
    return notice;
})( window.jQuery );

if( window.jQuery ){
    $(function(){
        Notice();
    });
};