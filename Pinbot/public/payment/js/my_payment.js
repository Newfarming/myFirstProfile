function initCustom(){
    $( '.custom-service' ).find( 'li' ).removeClass('active').find('input').val('0');
};
$(function() {

    $('.package-item').on( 'click' , function(){
        var $this = $( this),
            id = $this.attr('data-id'),
            packageDom = $( '#JS_package' ),
            doms = $( '.custom-service,#JS_click_buy' );
        $this.addClass('active').siblings('.active').removeClass('active');
        packageDom.val( id );
        initCustom();
    });

    $('#JS_click_buy').on( 'click' , function(){
        $( this ).toggleClass('active').parent().siblings('ul').toggle();
        initCustom();
    });

    $( '.custom-service li' ).click(function(){
        var $this = $( this ),
            id = $this.attr('data-feed_id'),
            feedDom = $('#JS_feed_id');
        if( $this.hasClass('active') ){
            $this.find('input').val('0');
            feedDom.val( '' );
        }else{
            $this.find('input').val('1');
            feedDom.val( id );
        };
        $this.toggleClass('active').siblings().removeClass('active').find('input').val('0');
    });

    $( '.custom-service li input' ).click(function( e ){
        if( $(this).parent().hasClass('active') ){
            e.stopPropagation();
        }
    });

    $('#JS_buy_btn').click(function() {
        var csrf_token = $(this).attr('csrf_token'),
            packageId = $( '#JS_package' ).val(),
            feedId = $('#JS_feed_id').val() || '',
            count = $( '.custom-service li.active' ).find('input').val(),
            reg = /^\d+$/g;
        //console.log( packageId , feedId , count ); return;
        if( !packageId ){
            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请先选择需要购买的套餐！</p>');
            return false;
        };
        if( feedId ){
            if( !count || !reg.test( count ) ){
                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>定制数量格式为正整数！</p>');
                return false;
            };
        };

        $.post( '' , {
            'package': packageId,
            'feed_service': feedId,
            'feed_count': count,
            'csrfmiddlewaretoken': csrf_token
        } , function( res ){
            if( res && res.status === 'ok' ){
                window.location.href = res.redirect_url;
            }else if( res && res.msg ){
                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>'+res.msg+'</p>');
            }else{
                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请求失败!请刷新页面再试！</p>');
            };
        } , 'json' );
    });
});
