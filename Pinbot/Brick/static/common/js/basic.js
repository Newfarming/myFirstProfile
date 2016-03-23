/*
    author: 516758517@qq.com
    date:  2015-01-09
    description: 聘宝basic js库
    update: 2015-08-18 LayerOut弹窗缺少关闭事件的回调，所以增加回调功能 by Adam
 */

$.LayerOut = function( setting ){
    return new $.LayerOut.prototype.init(setting);
};
$.LayerOut.prototype = {
    constructor: $.LayerOut,
    version: '1.1',
    init: function( setting ){
        if( $._LayerOut ) delete $._LayerOut;
        $('.modal-backdrop,.modal').remove();
        this.setting = setting = $.extend({
            title: '', //提示标题
            html: '',
            dialogCss: '',
            isShowCloseBtn: true,
            closeByShadow: true,
            confirmByShadow: false,
            handlers: [],
            callback: null,
            //关闭事件的回调
            afterClose: null
        }, setting);
        $._LayerOut = this;
        $._LayerOut.getHtml();
        if( $._LayerOut != undefined && $._LayerOut.setting!=undefined
            && typeof $._LayerOut.setting.callback == 'function' ) $._LayerOut.setting.callback();
    },
    getHtml: function(){
        setting = this.setting;
        var html = '<div class="modal-backdrop fade in"></div>' +
                    '<div class="modal" id="myModal" tabindex="-1" style="display: block;">' +
                        '<div class="modal-dialog" style="' + this.setting.dialogCss + '">' +
                            '<div class="modal-content" id="JS_modal_content">' +
                                ( this.setting.isShowCloseBtn ? '<p class="close-layer text-right"><a href="javascript:;" class="close-layerout-btn JS_close_layerout"></a></p>' : '' ) +
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
        if( typeof setting.afterClose == 'function' ){
            setting.afterClose();
        };
    }
};
$.LayerOut.prototype.init.prototype = $.LayerOut.prototype;

$.alert = function( html , onOk , title , setting){
    var setting = $.extend({
        title: title || '',
        html: html || '',
        handlers: [{
            title: '确定',
            eventType: 'click',
            className: 'button button-primary w158 f16',
            event: function(){
                if( typeof onOk == 'function' ){
                    onOk();
                };
                $._LayerOut.close(); //需要点击背景层执行和确认一样的操作的时候，setting里面的confirmByShadow=true
            }
        }]
    },setting);

    $.LayerOut( setting );
};

$.confirm = function( html , onOk , onCancel , title , setting ){
    var setting = $.extend({
        title: title || '',
        html: html || '',
        handlers: [
            {
                title: '确定',
                eventType: 'click',
                className: 'button button-primary w158 f16',
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
                className: 'button button-normal w158 f16',
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

            $.Click.handleCaches = $.Click.eventCaches || [];

            $.Click.handleCaches.push({
                dom: this.setting.dom,
                clicker: this
            });

            this.handle();
        },
        handle: function(){
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
        if( $.Click.handleCaches && $.Click.handleCaches.length ){
            for( var i = 0 , l = $.Click.handleCaches.length ; i < l ; i++ ){
                var cache = $.Click.handleCaches[ i ];
                if( cache.dom == setting.dom ){
                    cache.clicker.handle();
                    return;
                };
            };
        };
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
                callback: function( res ){
                    if( res && res.status == 'ok' ){
                        $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>操作成功！</p>' , function(){
                            if( res.redirect_url ){
                                location.href = res.redirect_url;
                            };
                        },'',{confirmByShadow:true});
                    }else{
                        if( res && res.msg ){
                            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + res.msg + '</p>');
                        }else{
                            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请求失败了，刷新再试一下吧！</p>');
                        };
                    };
                },
                verify: null,           //验证数据
                after: null         //请求成功回调
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
                this.setting.data.___ = new Date().getTime();
                window._commonAjax = $[this.setting.method]( this.setting.url , this.setting.data , function( res ){
                    that.setting.callback.call( that , res );
                    that.unlock();
                    window._commonAjax = null;
                }).fail( function(){
                    that.setting.failed.call( that );
                    that.unlock();
                });
            }else{
                that.unlock();
            };
            if( typeof this.setting.callback == 'function' ){
                this.setting.callback();
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
        after = $this.attr('data-after'),         //请求之后执行函数
        method = $this.attr('data-method'),         //请求方式
        isLock = $this.hasClass('locked-click' ),
        form = '',
        url = '',
        data = {
            callDom: that
        };
    if( isLock ) return false;

    if( type == 'normal' ){
        url = $this.attr('data-ajax_url');
        method = method || 'get';
        data.data = $.extend( true , {} , $this.data() );
        delete data.data.ajax_url;
        delete data.data.before;
        delete data.data.ajax_common_type;
        delete data.data.ajax_verify;
        delete data.data.callback;
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

    if( after && typeof window[after] == 'function' ){
        data.after = window[after];
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
    if( !str ) return;
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
    * [loadBgImg 背景图片按需加载]
    * @param  {[object]} setting [attr:存储背景路径的属性,loadImg:加载图片的方法,imgList:背景图片对象队列（需传）,callback:函数回调]
    * @return {[type]}         [description]
*/
$.loadBgImg = function(setting){

    setting = $.extend(
        {
            attr: 'data-bg',
            loadImg : function( img , bgUrl ){
                var newImg = new Image();
                newImg.onload = newImg.onerror = function(){
                    img.css( 'backgroundImage' , 'url(' + bgUrl + ')' ).removeAttr('data-bg');
                    newImg = null;
                };

                newImg.src = bgUrl;
            },
            imgList: [],
            callback: null
        },
        setting
    );

    if( !setting.imgList.length ){
        setting.imgList = $('[' + setting.attr + ']');
    };

    var list = setting.imgList;
    if( !list.length) return;

    for( var i = 0; i < list.length; i++ ){
        var $img = $( list[i] ),
            bgUrl = $img.attr( setting.attr );
        if( !bgUrl ) continue;
        setting.loadImg( $img , bgUrl );
    };

    if( typeof setting.callback == 'function' ){
        setting.callback();
    };
};

/**
    * [lazyImg 懒加载]
    * @param  {[object]} setting [description]
    * @return {[type]}         [description]
*/
$.lazyImg = function( setting ){
   return new $.lazyImg.prototype.init( setting );
};
$.lazyImg.prototype = {
    constructor : $.lazyImg, //构造函数
    imgList : [], //全部的图片队列
    loadingList: [], //加载中的图片队列
    init : function( setting ){
        this.setting = $.extend(
            {
                attr:'data-src', //存放图片的节点属性
                loadType: 1, //加载方式 2按照图片数量加载,1根据屏幕来加载(只针对Y轴)
                count : 30, //打开网页默认加载的图片数量
                scrollLimit: 30, //滚动时间限制，多少毫秒内滚动不计算
                isLock: false, //滚动加载是否锁定
                scrollTop: 0, //默认滚动的距离
                scrollBorder: 60, //计算图片数量的临界边距
                callback: null
            },
            setting
        );
        this.imgList = $('img[' +  this.setting.attr + ']');
        window._lazy = this;
        this.getPositionByBody();
        this.start();
        $(window).on('scroll', window, window._lazy.scroll);
    },
    start: function(){
        var list = _lazy.getList();
        for( var i = 0; i < list.length ; i++ ){
            var img = list[i],
                $img = $( img ),
                src = $img.attr( _lazy.setting.attr );
            _lazy.loadImg( $img , src);
            _lazy.loadingList.push( img );
        };
        _lazy.resetImgFromImgList();
    },
    getList: function(){
        var arr = [];
        if( _lazy.setting.loadType == 1 ){
            var sTop = $(window).scrollTop(),
                wHeight = $(window).height();
            for( var i = 0; i < _lazy.imgList.length ; i++ ){
                var iTop = $(_lazy.imgList[i]).offset().top;
                if( iTop < ( sTop + wHeight + _lazy.setting.scrollBorder ) ){
                    arr.push( _lazy.imgList[i] );
                    _lazy.filterImg(i);
                };
            };
        }else{
            var len = _lazy.imgList.length > this.setting.count ? this.setting.count :  _lazy.imgList.length;
            for(var i = 0 ; i < len.length ; i++ ){
                arr.push( _lazy.imgList[i] );
                _lazy.filterImg(i);
            };
        };

        return arr;
    },
    filterImg: function(i){
        _lazy.imgList[i].top = null;
        delete _lazy.imgList[i];
    },
    loadImg : function( img , src ){
        var newImg = new Image();
        newImg.onload = newImg.onerror = function(){
            img.attr( 'src' , src ).removeAttr( _lazy.setting.attr );
            _lazy.clearImgFromLoadingList(img[0]);
            newImg = null;
        };

        newImg.src = src;
    },
    getPositionByBody: function(){
        for( var i = 0; i < _lazy.imgList.length ; i++ ){
            var top = $( _lazy.imgList[i] ).offset().top;
            _lazy.imgList[i].top = top;
        };
    },
    resetImgFromImgList: function(){
        var arr = [];
        for( var i = 0; i < _lazy.imgList.length; i++ ){
            var it = _lazy.imgList[i];
            if( it ){
                arr.push( it );
            };
        };
        _lazy.imgList = arr;
        _lazy.timmer();
    },
    clearImgFromLoadingList : function(img){
        for( var i = 0; i < _lazy.loadingList.length; i++ ){
            if( _lazy.loadingList[i] == img ){
                _lazy.loadingList.splice(i,1);
                return;
            };
        };
    },
    scroll: function(){
        if( _lazy.setting.isLock ) return false;
        _lazy.setting.isLock = true;
        if( !_lazy.imgList || !_lazy.imgList.length ){
            window._lazy.complete();
            return false;
        };
        _lazy.start();
    },
    timmer: function(){
        var func = function(){
            _lazy.setting.isLock = false;
        };
        tLazy = setTimeout(func, _lazy.setting.scrollLimit);
    },
    complete: function(){
        $(window).off('scroll', window._lazy.scroll);
        _lazy.setting.isLock = false;
        tLazy && clearTimeout(tLazy);
        if( typeof _lazy.setting.callback == 'function' ){
            _lazy.setting.callback();
        };
        _lazy = null;
    }
};
$.lazyImg.prototype.init.prototype = $.lazyImg.prototype;