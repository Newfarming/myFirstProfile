$(function() {
    $('body').on('click', function() {
        var menu = $('.main-user-control-dropdown-menu');
        if (menu.is(':visible')) menu.hide();
    });

    $('body').on('click', '.main-user-control-icon', function(e) {
        e.stopPropagation();
        $(this).parent().find('.main-user-control-dropdown-menu').toggle();
    });

    // banner轮播图
    var active = 0,
        as = document.getElementById('pagenavi').getElementsByTagName('a');

    for (var i = 0; i < as.length; i++) {
        (function() {
            var j = i;
            as[i].onclick = function() {
                t2.slide(j);
                return false;
            }
        })();
    }

    var t2 = new TouchSlider({
            id: 'slider',
            speed: 600,
            timeout: 6000,
            before: function(index) {
                as[active].className = '';
                active = index;
                as[active].className = 'active';
            }
        }),
        t3 = new TouchSlider({
            id: 'comment',
            speed: 600,
            timeout: 6000
        }),
        t4 = new TouchSlider({
            auto: false,
            id: 'list-faq',
            speed: 600,
            timeout: 6000
        })
    $user_ctrl_menu = $('.user-ctrl-menu');

    $('#JS_toggle_user_menu').hover(function() {
        $user_ctrl_menu.toggle();
    }, function() {
        $user_ctrl_menu.toggle();
    });

    $('.slider-arrows .prev-page').click(function(e) {
        t4.prev();
    });
    $('.slider-arrows .next-page').click(function(e) {
        t4.next();
    });

    // $('#JS_toggle_tip').on('click', function(){
    //     $('p.tips').toggle();
    // });
    $(document).ready(function() {
        $('.faq:before').click(function(e) {
            //consoloe.log('faq:before');
        });
        $('.faq:after').click(function(e) {
            //consoloe.log('faq:after');
        });
    });

    if ($('.fast-menu a.i-weixin-barcode').length == 1) {
        $('.fast-menu a.i-weixin-barcode').hover(function() {
            $('.fast-menu a.i-weixin-barcode span.bigger').css('display', 'block');
            /*$( '.fast-menu a.i-weixin-barcode span.bigger' ).fadeIn( 300, function() {

                  });*/
        }, function() {
            $('.fast-menu a.i-weixin-barcode span.bigger').css('display', 'none');
            /*$( '.fast-menu a.i-weixin-barcode span.bigger' ).fadeOut( 100, function() {

                  });*/
        });
    }

});