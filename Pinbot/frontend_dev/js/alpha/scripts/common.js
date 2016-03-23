/*
    author: 516758517@qq.com
    date:  2014-07-30
    description: 公共JS
 */


$.LayerOut = function( setting ){
    return new $.LayerOut.prototype.init(setting);
};
$.LayerOut.prototype = {
    constructor: $.LayerOut,
    version: '1.0',
    init: function( setting ){
        if( $._LayerOut ) delete $._LayerOut;
        $('.modal-backdrop,.modal').remove();
        this.setting = setting = $.extend({
            title: '', //提示标题
            html: '',
            dialogCss: '',
            closeByShadow: true,
            confirmByShadow: false,
            handlers: [],
            callback: null
        }, setting);
        $._LayerOut = this;
        $._LayerOut.getHtml();
        if( typeof $._LayerOut.setting.callback == 'function' ) $._LayerOut.setting.callback();
    },
    getHtml: function(){
        setting = this.setting;
        var html = '<div class="modal-backdrop fade in"></div>' +
                    '<div class="modal" id="myModal" tabindex="-1" style="display: block;">' +
                        '<div class="modal-dialog" style="' + this.setting.dialogCss + '">' +
                            '<div class="modal-content" id="JS_modal_content">' +
                                ( this.setting.title ? '<div class="modal-header clearfix"><h4 class="modal-title Left" id="myModalLabel">' + this.setting.title + '</h4><span class="Right">' + ( this.setting.date ? this.setting.date : '' ) + '</span></div>' : '' ) +
                                '<div class="modal-body">' + this.setting.html + '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>';

        $('body').append( html );

        if( setting.handlers.length ){
            var handleContent = $( '<div class="modal-handle"></div>' );
            for( var i = 0 , l = setting.handlers.length ; i < l ; i++){
                var hand = setting.handlers[i],
                    btn = $( '<a class="' + hand.className + '">' + hand.title + '</a>' );
                btn.on( hand.eventType , hand.event );
                handleContent.append( btn );
            };
        };

        $('#JS_modal_content').append( handleContent );

        var _content = $('.modal-dialog'),
            height = _content.height(),
            wHieght = $(window).height();
        _content.css( 'marginTop' , ( wHieght - height ) / 2 + 'px' );

        $('.JS_close_layerout').on('click',this.close);

        var that = this;
        $('#myModal').on('click',function(e){
            e = e || window.event;
            var target = e.target || e.srcElement;
            if( e.target != this ) return;
            if( setting.handlers.length && setting.confirmByShadow ){
                setting.handlers[0].event();
            }else if( setting.closeByShadow ){
                that.close();
            };
        });
    },
    close: function(){
        $('.modal-backdrop,.modal').remove();
        delete $._LayerOut;
    }
};
$.LayerOut.prototype.init.prototype = $.LayerOut.prototype;

$.alert = function( html , onOk , title , setting){
    var setting = $.extend({
        title: title || '提示',
        html: html || '请确认！',
        handlers: [{
            title: '确定',
            eventType: 'click',
            confirmByShadow: false,
            className: 'layer-button blue-button',
            event: function(){
                if( typeof onOk == 'function' ){
                    onOk();
                };
                $._LayerOut.close(); //需要点击背景层执行和确认一样的操作的时候，confirmByShadow=true,并重写这个function
            }
        }]
    },setting);

    $.LayerOut( setting );
};

$.confirm = function( html , onOk , onCancel , title , setting ){
    var setting = $.extend({
        title: title || '提示',
        html: html || '请确认！',
        handlers: [
            {
                title: '确定',
                eventType: 'click',
                className: 'layer-button blue-button',
                event: function(){
                    if( typeof onOk == 'function' ){
                        onOk();
                    };
                    $._LayerOut.close();
                }
            },
            {
                title: '取消',
                eventType: 'click',
                className: 'layer-button grey-button',
                event: function(){
                    if( typeof onCancel == 'function' ){
                        onCancel();
                    };
                    $._LayerOut.close();
                }
            }
        ]
    },setting);

    $.LayerOut( setting );
};

// 扩展jquery
jQuery.prototype.serializeObject=function(){
    var obj = new Object();
    $.each(this.serializeArray(),function(index,param){
        if(!(param.name in obj)){
            obj[param.name]=param.value;
        };
    });
    return obj;
};

//通用的Click事件
$.Click = (function( $ , undefined ){

    var click = function( setting ){
        return new click.prototype.init( setting );
    };
    click.prototype = {
        constructor: click,
        init: function( setting ){
            this.setting = $.extend({
                dom: '',                //操作dom
                before: null,           //执行函数，返回true|false;
                isOk: true,             //提交状态
                lock: true,             //锁定点击
                unlock: function(){     //解锁按钮
                    $( this.setting.dom ).removeClass('locked-click');
                },
                callback: null          //回调函数
            },setting);
            if( this.setting.lock ){
                $( this.setting.dom ).addClass('locked-click');
            };
            if( typeof this.setting.before == 'function' ){
                this.setting.isOk = this.setting.before();
            };
            if( this.setting.isOk ){
                this.setting.callback.call( this );
            }else{
                this.setting.unlock.call( this );
            };
        }
    };
    click.prototype.init.prototype = click.prototype;

    return function( setting ){
        if( !setting || !setting.dom || $(setting.dom).hasClass('locked-click') ) return;
        return click( setting );
    };

})(jQuery);

//通用的ajax请求方法
$.Ajax = (function( $ , undefined ){
    var ajax = function( setting ){
        return new ajax.prototype.init( setting );
    };
    ajax.prototype = {
        constructor: ajax,
        init: function( setting ){
            this.setting = setting = $.extend({
                url: '',
                form: '',
                callDom: '',
                method: 'post',
                isOk: true,
                data: '',
                failed: function(){
                    $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请求失败了，刷新再试一下吧！</p>');
                },
                successed: function( res ){
                    if( res && res.status == 'ok' ){
                        if( this.setting.callback && typeof this.setting.callback == 'function' ){
                            this.setting.callback( res );
                        }else{
                            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>操作成功！</p>');
                        };
                    }else{
                        if( this.setting.errorCallback && typeof this.setting.errorCallback == 'function' ){
                            this.setting.errorCallback( res );
                        }else{
                            if( res && res.msg ){
                                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + res.msg + '</p>');
                            }else{
                                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请求失败了，刷新再试一下吧！</p>');
                            };
                        };
                    };
                },
                verify: null,           //验证数据
                callback: null,         //请求成功回调
                errorCallback: null     //请求失败回调
            }, setting);
            var form = $( this.setting.form ),
                that = this;
            if( this.setting.verify ){  //自定义验证
                this.setting.isOk = this.setting.verify();
            };
            if( form && !this.setting.data ){
                this.setting.data = $( this.setting.form ).serializeObject();
            };
            if( this.setting.isOk ){
                window._commonAjax = $[this.setting.method]( this.setting.url , this.setting.data , function( res ){
                    that.setting.successed.call( that , res );
                    that.unlock();
                    window._commonAjax = null;
                }).fail( function(){
                    that.setting.failed.call( that );
                    that.unlock();
                });
            }else{
                that.unlock();
            };
        },
        unlock: function(){
            if( this.setting.callDom ){
                $( this.setting.callDom ).removeClass( 'locked-click' );
            };
        }
    };
    ajax.prototype.init.prototype = ajax.prototype;
    return function( setting ){
        return ajax( setting );
    };
})(jQuery);

//通用的请求
$.commonAjax = function(){

    if( $( this ).hasClass('locked-click' ) ) return false;

    if( window._commonAjax ){
        window._commonAjax.abort();
        window._commonAjax = null;
    };

    var that = this,
        $this = $( this ),
        before = $this.attr('data-before'),
        type = $this.attr('data-ajax_common_type'), //获取通用类型
        verify = $this.attr('data-ajax_verify'),    //此处是数据验证函数
        func = $this.attr('data-callback'),         //请求完成回调函数
        errorCallback = $this.attr('data-errorCallback'),         //请求失败回调函数
        method = $this.attr('data-method'),         //请求方式
        form = '',
        url = '',
        data = {
            callDom: that
        };

    if( type == 'normal' ){
        url = $this.attr('data-ajax_url');
        method = method || 'get';
        data.data = $.extend( true , {} , $this.data() );
        delete data.data.ajax_url;
        delete data.data.before;
        delete data.data.ajax_common_type;
        delete data.data.ajax_verify;
        delete data.data.callback;
        delete data.data.errorCallback;
        delete data.data.method;
    }else{
        form = $this.attr('data-form') ? $( $this.attr('data-form') ) : $this.closest('form');
        url = form.attr('data-ajax_url') || form.attr('action');
        method = method || 'post';
        data.form = form;
    };

    if( verify && typeof window[verify] == 'function' ){
        data.verify = function(){
            return window[verify]( form );
        };
    };

    if( func && typeof window[func] == 'function' ){
        data.callback = window[func];
    };

    if( errorCallback && typeof window[errorCallback] == 'function' ){
        data.errorCallback = window[errorCallback];
    };

    data.url = url;
    data.method = method;

    $.Click({
        dom: that,
        before: window[before],
        callback: function(){
            $.Ajax( data );
        }
    });
};

//通用的过滤xss
filterXss = function( str ){
    var reg = /<script>|<\/script>/igm,
        func = function( val , index ){
            val = val.replace(/</g , '&lt;' );
            val = val.replace(/>/g , '&gt;' );
            return val;
        };
    str = str.replace( reg , func );
    return str;
};

/**
 * [DOMContentLoaded]
 * @return {[type]} [description]
 */
$(function(){

    $('body').on('click', function() {
        var menu = $('.main-user-control-dropdown-menu');
        if( menu.is(':visible') ) menu.hide();
    });

    $('body').on('click', '.main-user-control-icon', function(e) {
        e.stopPropagation();
        $('.tao-money-tips').hide();
        $(this).parent().find('.main-user-control-dropdown-menu').toggle();
    });

    $('body').on('click', '.tao-money-tips>p', function(e) {
        var url = $(this).data('memo-url');
        $.post(url, function() {});
        $(this).parent().fadeOut();
    });
});
