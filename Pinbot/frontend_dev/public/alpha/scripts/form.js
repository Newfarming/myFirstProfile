/*
    author: 516758517@qq.com
    date:  2014-07-30
    description: 表单JS
 */

$.getMonth = function( tag , selected ){
    var html = '',
        tag = tag || 'option';
    for( var i = 1 ; i < 13 ; i++ ){
        var m = i;
        if( i < 10 ){
            m = '0' + i;
        };
        if( tag == 'option' ){
            html += '<option value="' + i + '" ' + ( i == selected ? 'selected' : '' ) + '>' + m + '</option>';
        }else{
            html += '<li><a ' + ( i == selected ? 'class="active' : '' ) + '>' + m + '</a></li>';
        };
    };
    return html;
};

$.getYear = function( tag , selected ){
    var thisYear = new Date().getFullYear(),
        html = '',
        tag = tag || 'option';
    for( var i = thisYear ; i > 1949 ; i--){
        if( tag == 'option' ){
            html += '<option value="' + i + '" ' + ( i == selected ? 'selected' : '' ) + '>' + i + '</option>';
        }else{
            html += '<li><a ' + ( i == selected ? 'class="active' : '' ) + '>' + i + '</a></li>';
        };
    };
    return html;
};

/**
 * [验证自定义表单]
 * @param  {[array]} $dom         [jquery元素组]
 * @return {[boolean]}            [验证结果，true | false]

 */
var formalVerify = function( $dom ){
    var isOk = true,
        inputs = $dom.find('.input[data-equired]'),
        selects = $dom.find( 'select[data-equired]'),
        textareas = $dom.find( '.textarea[data-equired]' ),
        verify = function( $doms , nodeType ){
            for( var i = 0 , l = $doms.length ; i < l ; i++ ){
                var $dom = $doms.eq(i),
                    val = $dom.val(),
                    reg = $dom.attr('data-reg'),
                    placeholder = $dom.attr('placeholder');
                if( !regs[reg].test( val ) || ( val == placeholder ) ){
                    if( $dom[0].tagName.toLowerCase() == 'select' ){
                        $dom.siblings( '.button' ).addClass( 'tip-error' );
                    }else{
                        $dom.addClass('tip-error');
                    };
                    isOk = false;
                }else{
                    if( $dom[0].tagName.toLowerCase() == 'select' ){
                        $dom.siblings( '.button' ).removeClass( 'tip-error' );
                    }else{
                        $dom.removeClass('tip-error');
                    };
                };
            };
        };
    verify( inputs );
    verify( selects );
    verify( textareas );
    return isOk;
};

/**
 * [默认事件绑定]
 * @param  {[type]} $         [description]
 * @param  {[type]} undefined [description]
 * @return {[type]}           [description]
 */
(function( $ , undefined ){

    $('[placeholder]').each(function(){
        var $this = $( this ),
            holder = $this.attr('placeholder');
        if( !$this.val() && $this.attr( 'data-fixholder' ) ){
            $this.val( holder );
        };
    });

})(jQuery);


var regs = {
    isNull: /\S/,
    email: /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/,
    number: /^\d+$/,
    price: /^(\d+|\d+.{0,1}\d+)$/
};

/**
 * [DOMContentLoaded]
 * @return {[type]} [description]
 */
$(function(){

    $(document).on( 'focus' , '[data-fixholder]' , function(){
        var $this = $( this ),
            val = $this.val(),
            holder = $this.attr('placeholder');
        if( val == holder ){
            $this.val('');
        };
    });

    $(document).on( 'blur' , '[data-fixholder]' , function(){
        var $this = $( this ),
            val = $this.val(),
            holder = $this.attr('placeholder');
        if( val == '' && !$this.hasClass( 'data-fixholder' )){
            $this.val( holder );
        };
    });

    $(document).on( 'click' , '[data-toggle]' , function( e ){
        e = e || window.event;
        var $this = $( this );
        if( $this.closest('.drop-select').attr('disabled') ){
            return false;
        };
        $('.button.open').removeClass('open').siblings('.drop-box').hide();
        $this.toggleClass('open').siblings('.drop-box').toggle();
        if( e.stopPropagation ){
            e.stopPropagation();
        }else{
            e.cancelBubble  = true;
        };
    });

    $(document).on( 'click' , document , function( e ){
        var hideLayer = function( list , className ){
            list.each(function(){
                $( this ).removeClass( className ).siblings('.drop-box').hide();
            });
        };
        var buttonOpen = $('.button.open');
        if( buttonOpen.length ){
            hideLayer( buttonOpen , 'open' );
        };
    });

    $(document).on('click', '.drop-down li', function(){
        var $this = $( this ),
            index = $this.index(),
            text = $this.text(),
            btn = $this.parent().parent().siblings('button'),
            button = $this.closest('.drop-box').siblings('.button'),
            saved = $this.closest('.saved');

        if( saved.length ){
            var present = btn.text();
            if( present != text ){
                saved.removeClass('saved').find('.JS_save_someone').show().end().find('.disabled').hide();
            };
        };
        if( index != 0 ){
            button.removeClass('tip-error');
        };
        var nowMonth = $this.closest('td').find('.nowMonth'),
            drop = nowMonth.closest('.drop-select');
        if( $this.hasClass('now') ){
            nowMonth.show().click();
            drop.attr('disabled',true);
        }else{
            if( drop.attr('disabled') ){
                nowMonth.hide();
                drop.removeAttr('disabled').find('li:first').click();
            };
        };
        $this.find('a').addClass('active').end().siblings().find('a').removeClass('active');
        btn.html( text+ '<i class="i-barr"></i>' ).siblings('select').find('option').eq( index ).prop( 'selected' , true );
    });

    $(document).on( 'keyup' , 'input[data-ajax]' , function(){
        var $this = $( this ),
            val = $this.val();
        if( !val ){
            $this.siblings('.drop-box').hide();
            $('div[data-caller="' + $this.attr('data-call') + '"]').remove();
            return;
        };
        $this.siblings('.drop-box').show();
    });

    $(document).on( 'click' , '.drop-ajaxdown li' , function(){
        var $this = $(this),
            text = $this.text(),
            input = $this.parent().parent().hide().siblings('input[data-ajax]'),
            offset = input.offset();
        input.val( text );

        var div = $('<div class="error" data-caller="' + input.attr('data-call') + '">输入无效城市!</div>');
        div.css({ top: offset.top-10 + 'px' , left: offset.left +'px' });
        $('body').append(div);
    });

    $(document).on( 'keyup' , 'textarea[data-lengthlimit]' , function(){
        var $this = $( this ),
            val = $this.val(),
            presentLength = val.length,
            maxLength = parseInt( $this.attr('data-lengthlimit') ) || 100,
            present = $this.siblings('.limit-count').find('span').eq(0);
        if( presentLength >= maxLength ){
            $this.val( val.substring( 0 , maxLength ) );
            present.text('0');
        }else{
            present.text( maxLength - presentLength );
        };

        if( val.length > 0 ){
            present.css('color','red');
        }else{
            present.css('color','#999');
        };

    });

    $(document).on( 'keyup' , 'textarea[data-lenlimit]' , function(){
        var $this = $( this ),
            val = $this.val(),
            presentLength = val.length,
            maxLength = parseInt( $this.attr('data-lenlimit') ) || 100;
        if( presentLength && presentLength <= maxLength ){
            $this.removeClass('tip-error');
        };
    });

    $(document).on( 'blur' , '[data-equired]' , function(){
        var $this = $(this),
            reg = $this.attr('data-reg'),
            val = $.trim( $this.val() ),
            placeholder = $this.attr('placeholder');
        if( !regs[reg].test( val ) || ( val == placeholder ) ){
            $this.addClass('tip-error');
        }else{
            $this.removeClass('tip-error');
        };
    });

    $(document).on( 'blur' , '[data-notequired]' , function(){
        var $this = $(this),
            reg = $this.attr('data-reg'),
            val = $.trim( $this.val() ),
            placeholder = $this.attr('placeholder');
        if( ( val && !regs[reg].test( val ) ) || ( val == placeholder ) ){
            $this.addClass('tip-error');
        }else{
            $this.removeClass('tip-error');
        };
    });

});