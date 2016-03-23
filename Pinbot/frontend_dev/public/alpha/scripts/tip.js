/*
    author: 516758517@qq.com
    date:  2014-11-24
    description: 基于jquery气泡弹窗
 */

$.Tip = function( $ , fundefined ){

    var tip = function( setting ){
        return new tip.prototype.init( setting );
    };

    tip.prototype = {
        constructor: tip,
        init: function( setting ){
            this.setting = setting = $.extend( {
                selector: '.JS_tip_a',
                mouseHandle: 'click',
                cssText: '',
                closeWay: 'clickOutSide',
                success: null,
                content: '',
                className: '',
                needAjax: true,
                callback: null
            } , setting );
            var that = this;
            window.__tip = this;
            $( document ).on( setting.mouseHandle , setting.selector , function( e ){
                if( $( this ).hasClass('JS_sock_tip') ){
                    return false;
                };
                $( '.JS_sock_tip' ).not($(this)).removeClass('JS_sock_tip');
                that.setting.eventTarget = this;
                $( this ).addClass('JS_sock_tip');
                that.showModel();
                that.bindHideEvent();
                that.setPosition();
                if( that.setting.needAjax ){
                    that.loadData();
                }else{
                    if( typeof that.setting.callback == 'function' ){
                        that.setting.callback();
                    };
                };
                e.stopPropagation();
            });
        },
        getHtml: function(){
            var html = '<p style="text-align: center;"><img src="http://www.pinbot.me/static/alpha/images/loading.gif" alt="" style="vertical-align: -3px; margin-right:10px;">加载中...</p>';
            return html;
        },
        showModel: function(){
            $('#JS_tip_model').remove();
            var html = '';
            if( this.setting.needAjax ){
                html = this.getHtml();
            }else{
                html = this.setting.content;
            };
            html = '<div class="tip-model ' + this.setting.className + '" id="JS_tip_model" style="' + this.setting.cssText + '">' + html +'</div>';
            $('body').append( html );
        },
        setPosition: function(){

            var $han = $( this.setting.eventTarget ),
                pos = $han.offset(),
                h_width = $han.outerWidth(),
                h_height = $han.outerHeight(),
                $dom = $( '#JS_tip_model' ),
                width = $dom.outerWidth(),
                height = $dom.outerHeight(),
                s_width = $( window ).width(),
                s_height = $( document ).height(),
                scrollTop = $( document ).scrollTop(),
                isOuterX = pos.left + ( h_width / 2 ) + ( width / 2 ) + 5 > s_width,
                isLowerX = pos.left + ( h_width / 2 ) - width / 2 < 0,
                isOuterY = h_height + height + pos.top + 5 > s_height,
                left,
                top;

            if( isOuterX && isOuterY ){
                top = pos.top + h_height - height;
                left = pos.left - 5 - width;
                $dom.addClass('right-bottom-side');
            }else if( !isOuterX && isOuterY && !isLowerX ){
                top = pos.top - 5 - height;
                left = pos.left + h_width / 2 - width / 2;
                $dom.addClass('down-side');
            }else if( isOuterX && !isOuterY ){
                top = pos.top + h_height + 5;
                left = pos.left + h_width - width;
                $dom.addClass('right-top-side');
            }else if( isLowerX && !isOuterY ){
                top = pos.top - 5;
                left = pos.left + h_width + 5;
                $dom.addClass('left-top-side');
            }else if( isLowerX && isOuterY ){
                top = pos.top + h_height - height;
                left = pos.left + h_width + 5;
                $dom.addClass('left-bottom-side');
            }else{
                top = pos.top + h_height + 5;
                left = pos.left + h_width / 2 - width / 2;
            };

            $dom.css({
                left: left + 'px',
                top: top + 'px'
            });
        },
        bindHideEvent: function(){
            var that = this,
                func = function( e ){
                    var list = $( that.setting.selector );
                    if( e.target != $('#JS_tip_model')[0] && !$( e.target ).closest('#JS_tip_model').length ){
                        var $target = $(e.target),
                            $pTarget = $target.closest('.JS_sock_tip');
                        if( $target.hasClass('JS_sock_tip') ){
                            $('.JS_sock_tip').not( $target ).removeClass('JS_sock_tip');
                        }else if( $pTarget.length ){
                            $('.JS_sock_tip').not( $pTarget ).removeClass('JS_sock_tip');
                        }else{
                            $('.JS_sock_tip').removeClass('JS_sock_tip');
                        };
                        if( window._tipAjax ){
                            window._tipAjax.abort();
                            window._tipAjax = null;
                        };

                        $( document ).off( 'click'  , func );

                        if( $.inArray( e.target , list ) == -1 ){
                            $( '#JS_tip_model' ).remove();
                        };

                    };
                };
            $( document ).on( 'click' , document , func );
        },
        loadData: function( obj ){
            var that = this,
                $obj = $( obj || that.setting.eventTarget ),
                data = $.extend( true , {} , $obj.data() ),
                method = data.method ? data.method : 'get',
                url = data.url;

            delete data.url;

            that.setting.url = url;

            window._tipAjax = $[ method ]( url , data , function( res ){
                if( res ){
                    if( typeof that.setting.success == 'function' ){
                        that.setting.success.apply( that , [res] );
                    }else{
                        that.insertHtml( res );
                    };
                };
            });
        },
        insertHtml: function( datas ){
            var that = this,
                $model = $('#JS_tip_model'),
                html = '',
                data = datas.data;

            if( !$model.length ) return false;

            if( data.length ){
                html += '<table cellpadding="0" cellspacing="0" class="ajax-tip-list" width="100%">';
                for( var i = 0 , l = data.length ; i < l ; i++ ){
                    var item = data[ i ];
                    html += '<tr>';
                    for( var j in item ){
                        html += '<td>' + item[j] + '</td>';
                    };
                    html += '</tr>';
                };
                html += '</table>';
            }else{
                html += '<p class="text-center">暂无数据！</p>';
            };

            html += '<p class="tip-pages clearfix">';
            if( datas.current > 1 ){
                html += '<a class="JS_tip_page" href="javascript:;" data-url="' + this.setting.url + '" data-page="' + ( datas.current - 1 )  + '">上一页</a>';
            };
            if( datas.current < datas.pages ){
                html += '<a class="JS_tip_page" href="javascript:;" data-url="' + this.setting.url + '" data-page="' + ( datas.current + 1 )  + '">下一页</a>';
            }
            html += '</p>';

            $model.html( html );
            this.setPosition( that.setting.eventTarget );

            $('.JS_tip_page').on( 'click' , function(){
                that.loadData( this );
            });

            if( typeof this.setting.callback == 'function' ){
                this.setting.callback();
            };

        }
    };
    tip.prototype.init.prototype = tip.prototype;

    return function( setting ){
        return tip( setting );
    };
}( jQuery );