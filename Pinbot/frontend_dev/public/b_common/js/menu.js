/*
    author: 516758517@qq.com
    date:  2015-04-15
    description: 公共小导航菜单
 */

/**
 * [$.Menu]
 * @param setting {[type:object]}
 */
$.Menu = (function( $ , undefined ){
    var menu = function( setting ){
        return new menu.prototype.init( setting );
    };
    menu.prototype = {
        version: '',
        constructor: menu,
        init: function( setting ){
            this.setting = $.extend({
                container: '#JS_fast_menu',
                mouseType: 'click',
                events: {
                    backTop: function(){
                        $( 'body,html' ).animate({ scrollTop: 0 }, 500);
                        //$(window).scrollTop(0);
                    }
                }
            }, setting);
            this.addEvent();
            this.scroll();
            //if(pbDebug) console.log('initQQ');
            this.loadWebQQ();
        },
        addEvent: function(){
            var that = this,
                list = $( this.setting.container ).find( 'a' );

            list.each(function( i ){
                var $dom = list.eq( i ),
                    event = $dom.attr('data-event');
                if( event ){
                    $dom.on( that.setting.mouseType , that.setting.events[event]);
                };
            });
        },
        scroll: function(){
            var $dom = $('#JS_back_top');
            if( !$dom.length ) return;
            $( window ).on( 'scroll' , window , function(){
                var top = $(window).scrollTop();
                if( top <= 100 ){
                    $dom.css({ display: 'none' });
                }else{
                    $dom.css({ display: 'inline-block' });
                };
            });
        },
        loadWebQQ: function(){
            $.getScript( 'http://wpa.b.qq.com/cgi/wpa.php' ).done(function(){
                BizQQWPA.addCustom([

                {
                    aty: '0',
                    nameAccount: '800031490',
                    selector: 'JS_pbqqdiy_btn'
                },

                {
                    aty: '0',
                    nameAccount: '800031490',
                    selector: 'JS_pbqqnoworry_btn'
                },

                {
                    aty: '0',
                    nameAccount: '800031490',
                    selector: 'JS_service_btn'
                }

                ]);
            });
        }
    };
    menu.prototype.init.prototype = menu.prototype;

    return function( setting ){
        menu( setting );
    };
})(jQuery);

$(document).ready(function(){
    $.Menu();
});