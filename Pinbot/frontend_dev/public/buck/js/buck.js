$.Fade = (function( $ , undefined ){
    var fade = function( setting ){
        return new $.Fade.prototype.init( setting );
    };
    fade.prototype = {
        version: '',
        constructor: fade,
        init: function( setting ){
            this.setting = setting = $.extend({
                selector: '.scroll',
                activeClass: 'faded',
                lockSecond: 50,
                overflow: 50
            } , setting );
            this.cachePosition();
            window.__Fade = this;
            this.bindEvent();
        },
        cachePosition: function(){
            var setting = this.setting,
                doms = $( setting.selector ).not( '.' + setting.activeClass ),
                pos = [];

            doms.each(function(){
                var offset = $( this ).offset(),
                    obj = {};
                obj.dom = this;
                obj.top = offset.top;
                obj.left = offset.left;
                pos.push( obj );
            });
            setting.pos = pos;
        },
        scrollEevent: function( e ){
            window.__Fade.scroll( e );
        },
        bindEvent: function(){
            var that = this;
            $( window ).on( 'scroll' , window , that.scrollEevent);
        },
        scroll: function( e ){
            // if( window._lockFade ) return;
            // window._lockFade = true;
            var setting = this.setting,
                $window = $( window ),
                height = $window.height(),
                scrollTop = $window.scrollTop(),
                total = height + scrollTop + setting.overflow,
                list = $.map( setting.pos , function( c ){ return c} );

            for( var i = 0 , l = list.length ; i < l ; i++ ){
                var dom = list[i].dom,
                    $dom = $( dom );
                if( $dom.hasClass( setting.activeClass ) ){
                    setting.pos.splice( i , 1 );
                    continue;
                };
                if( total <= list[i].top ) continue;

                $dom.addClass( setting.activeClass );

                setting.pos.splice( i , 1 );
            };

            this.timeout();
        },
        timeout: function(){
            var that = this;
            scollTimeout = setTimeout( function(){
                // window._lockFade = undefined;
                if( !that.setting.pos.length ){
                    $( window ).off( 'scroll' , that.scrollEevent);
                    window.__Fade = undefined;
                }
            } , that.setting.lockSecond );
        }
    };
    fade.prototype.init.prototype = fade.prototype;
    return fade;
})(jQuery);

$(function(){
    var resize = function(){
            var wHeight = $( window ).height();
            $('#JS_content').css({
                marginTop: wHeight + 'px',
                display: 'block'
            });
            $('.flowerbg').css({
                top: $('.step-5').position().top-100 + 'px'
            }).show();
        };
    resize();
    $( window ).on( 'resize' , window , resize );
    $.Fade();
});