/*
    author: 516758517@qq.com
    date:  2014-04-25
    description: 龙渊网站公用JS 
 */

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
    setting.imgList = $('[' + setting.attr + ']');
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

$.Animate = function(setting){
    return new $.Animate.prototype.init(setting);
};
$.Animate.prototype = {
    constructor: $.Animate,
    init:function(setting){
        this.setting = $.extend({
            type : 'slide', //现在支持slide,fade
            leftBtn: '#JS_left_btn',
            rightBtn: '#JS_right_btn',
            listBox: '#JS_slide_list',
            cursor: '#JS_ppt_nav',
            mouseType: 'click',
            current: 'active',
            needPage: false,
            index:0,
            autoPlay:true,
            tag:'li',
            delay: 3000,
            spendTime: 500,
            fadeEndTime: 1000,
            before: null,
            after: null
        },setting);
        if( typeof this.setting.before == 'function' ){
            this.setting.before();
        };
        var list = $(this.setting.listBox);
        this.setting.length = list.find(this.setting.tag).length;
        list.css( 'width' , (list.parent().width() ) * this.setting.length + 'px' );
        if( this.setting.needPage ){
            this.addSwitchPage();
        }
        var that = this;
        if( this.setting.type == 'slide' ){
            $(this.setting.leftBtn).on(this.setting.mouseType, function(){
                clearInterval(window[ that.setting.timeOut ]);
                that.prev();
                that.animate();
            });
            $(this.setting.rightBtn).on(this.setting.mouseType, function(){
                clearInterval(window[ that.setting.timeOut ]);
                that.next();
                that.animate();
            });
        };
        if( this.setting.type == 'fade' || this.setting.needPage){
            $( list ).find(this.setting.tag).eq(0).css('opacity',1);
            $(this.setting.cursor + ' a').eq(0).addClass( this.setting.current );
            $(this.setting.cursor + ' a').on(this.setting.mouseType, function(){
                clearInterval(window[ that.setting.timeOut ]);
                that.setting.index = $(this).index();
                that.getIndex = true;
                var index = $( this ).index(),
                    lastIndex = $( this ).siblings('.active').index();
                that.setting.lastIndex = lastIndex;
                $(this).addClass(that.setting.current);
                $( this ).siblings('.' + that.setting.current).removeClass(that.setting.current);
                that.animate();
                return false;
            });
        };
        if( this.setting.autoPlay ){
            this.timeOut();
        };
    },
    prev: function(){
        this.setting.index--;
        this.getIndex = true;
    },
    next: function(){
        this.setting.index++;
        this.getIndex = true;
    },
    timeOut: function(){
        var that = this;
        if( !this.setting.timeOut ){
            var now = 'timeOut' + new Date().getTime().toString('16') + Math.random();
            this.setting.timeOut = now;
        };
        window[ this.setting.timeOut ] = setInterval(function(){
            that.animate();
        },this.setting.delay);
    },
    isOuter: function(){
        if( this.setting.index >= this.setting.length || this.setting.index < 0 ){
            this.setting.index = 0;
        };
    },
    addSwitchPage: function(){
        if( $( this.setting.cursor ).html() ) return;
        var count = $( this.setting.listBox ).find('li').length,
            html = '';
        for( var i = 0 ; i < count; i++ ){
            html += '<a href="javascript:;" ' + ( i == 0 ? 'class="active"' : '' ) + '>' + ( i + 1) + '</a>';
        };
        $( this.setting.cursor ).html(html);
    },
    animate: function(){
        if( !this.getIndex ) {
            this.setting.index++;
        };
        this.isOuter();
        if( this.setting.type == 'slide' ){
            var width = $( this.setting.listBox ).width(),
                left = -width / this.setting.length * this.setting.index;
            $( this.setting.listBox ).animate({ 'left': left + 'px' }, this.setting.spendTime);
            if( this.setting.needPage ){
                $(this.setting.cursor + ' a').eq(this.setting.index).addClass(this.setting.current).siblings('.' + this.setting.current).removeClass(this.setting.current);
            };
        };
        if( this.setting.type == 'fade' ){
            var list = $(this.setting.listBox).find(this.setting.tag),lastIndex;
            if( !this.getIndex ){
               lastIndex = this.setting.index - 1;
            }else{
               lastIndex = this.setting.lastIndex;
            };
            $(this.setting.cursor + ' a').eq(this.setting.index).addClass(this.setting.current).siblings('.' + this.setting.current).removeClass(this.setting.current);
            list.eq(lastIndex).animate({opacity:0},this.setting.spendTime);
            list.eq(this.setting.index).animate({opacity:1},this.setting.fadeEndTime);
        };
        if( typeof this.setting.after == 'function'){
            this.setting.after( this.setting.index );
        };
        if( this.getIndex ){
            this.getIndex = null;
            if( this.setting.autoPlay ){
                this.timeOut();
            };
        };
    }
};
$.Animate.prototype.init.prototype = $.Animate.prototype;

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
            onSubmit: null,
            onCancel: true,
            title: '提示',
            html: '',
            callback: null
        }, setting);
        $._LayerOut = this;
        this.getHtml();
        this.addEvent();
        if( typeof this.setting.callback == 'function' ) this.setting.callback();
    },
    getHtml: function(){
        setting = this.setting;
        var html = '<div class="modal-backdrop fade in"></div>' + 
                    '<div class="modal" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="display: block;">' +
                        '<div class="modal-dialog">' +
                            '<div class="modal-content" id="JS_modal_content">' +
                                ( this.setting.title ? '<div class="modal-header clearfix"><h4 class="modal-title Left" id="myModalLabel">' + this.setting.title + '</h4><span class="Right">' + ( this.setting.date ? this.setting.date : '' ) + '</span></div>' : '' ) +
                                '<div class="modal-body"><p style="padding:20px">' + this.setting.html + '</p></div>' +
                            '</div>' +
                        '</div>' +
                    '</div>';
        $('body').append( html ); 

        var _content = $('.modal-dialog'),
            height = _content.height(),
            wHieght = $(window).height();
        _content.css( 'marginTop' , ( wHieght - height ) / 2 + 'px' );
    },
    addEvent: function(){
        $('.JS_close_layerout').on('click',this.close);
        $('.JS_submit_layerout').on('click',this.setting.onSubmit);
        var that = this;
        $('#myModal').on('click',function(e){
            e = e || window.event;
            var target = e.target || e.srcElement;
            if( e.target == this ){
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

/**
 * [prettyPhoto description]
 * @param  {[type]} setting [description]
 * @return {[type]}         [description]
 */
$.fn.viewPhoto = function( setting ){
    setting = $.extend({
        width: 860,
        contentBox: '#viewPhoto',
        height: 525,
        showClose: true,
        attr: 'data-src'
    },setting);
    
    this.on('click',function(){

        var src = $(this).attr( setting.attr ),fileType;
        if( src.lastIndexOf ){
            fileType = src.substring(src.lastIndexOf('.') , src.length);
        }else{
            var arr = src.split('.');
            fileType = arr[arr.length - 1];
        };

        var html = '',
            height = $(document).height(),
            sTop = $(window).scrollTop();
        $('#viewPhoto,#JS_viewPhoto_bg').remove();

        html ='<div class="viewPhoto" id="viewPhoto" style="width:' + setting.width + 'px; height:' + setting.height + 'px; top:' + (sTop + ( ( $(window).height() - setting.height ) / 2 ) ) + 'px">' +
                    '<a class="a-icon i-close-viewPhoto" onclick="$(\'#viewPhoto,#JS_viewPhoto_bg\').remove();"></a>';
        switch( fileType ){
            case '.swf':
                html += '<object id="FlashID" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="' + setting.width + '" height="' + setting.height + '">' +
                        '<param name="movie" value="' + src + '" />' +
                        '<param name="quality" value="high" />' +
                        '<param name="wmode" value="opaque" />' +
                        '<param name="swfversion" value="6.0.65.0" />' +
                        '<!-- 此 param 标签提示使用 Flash Player 6.0 r65 和更高版本的用户下载最新版本的 Flash Player。如果您不想让用户看到该提示，请将其删除。 -->' +
                        '<param name="expressinstall" value="Scripts/expressInstall.swf" />' +
                        '<!-- 下一个对象标签用于非 IE 浏览器。所以使用 IECC 将其从 IE 隐藏。 -->' +
                        '<!--[if !IE]>-->' +
                        '<object type="application/x-shockwave-flash" data="' + src + '" width="' + setting.width + '" height="' + setting.height + '">' +
                        '<!--<![endif]-->' +
                        '<param name="quality" value="high" />' +
                        '<param name="wmode" value="opaque" />' +
                        '<param name="swfversion" value="6.0.65.0" />' +
                        '<param name="expressinstall" value="Scripts/expressInstall.swf" />' +
                        '<!-- 浏览器将以下替代内容显示给使用 Flash Player 6.0 和更低版本的用户。 -->' +
                        '<div>' +
                          '<h4>此页面上的内容需要较新版本的 Adobe Flash Player。</h4>' +
                          '<p><a href="http://www.adobe.com/go/getflashplayer"><img src="http://www.adobe.com/images/shared/download_buttons/get_flash_player.gif" alt="获取 Adobe Flash Player" width="112" height="33" /></a></p>' +
                        '</div>' +
                        '<!--[if !IE]>-->' +
                        '</object>' +
                        '<!--<![endif]-->' +
                    '</object>';
                break;
            case '.other':
                html += '<div>others</div>';
                break;
            default :
                html += '<div><img src="' + src + '" alt="" style="max-width: 100%; margin: 0 auto; display: block;"/></div>';
                break;
        };
        html += '</div>' +
                '<div class="viewPhoto-bg" id="JS_viewPhoto_bg" style="height:' + height + 'px" onclick="$(\'#viewPhoto,#JS_viewPhoto_bg\').remove();"></div>';

        $('body').append(html);
        return false;
    });
};

$(function(){
    $.loadBgImg();
    $.lazyImg();
});
