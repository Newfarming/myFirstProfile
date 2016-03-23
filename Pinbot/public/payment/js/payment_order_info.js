function resetInput( obj ){
    obj.hide().siblings('.JS_save_address').hide().siblings('.JS_edit_address').show().siblings('input').addClass('default').prop('readonly',true);
};

function showAfterPay( res ){
    var html = '<p class="text-right"><a class="i-layerout-close JS_close_layerout" onclick="window.lock = false;" title="关闭" href="javascript:;"></a></p>' +
            '<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请你在新打开的页面上完成付款，付款完成前请不要关闭此窗口！</p>' +
            '<p class="text-center" style="font-size:14px;">完成付款后请根据你的情况点击以下按钮。</p>';

    $.LayerOut({
        html: html,
        closeByShadow: false,
        handlers: [
            {
                title: '<i class="i-bingo"></i>我已完成付款',
                eventType: 'click',
                className: 'layer-button blue-button',
                event: function(){
                    window.location.href = res.alipay_result_url;
                    $._LayerOut.close();
                }
            },
            {
                title: '支付遇到问题',
                eventType: 'click',
                className: 'layer-button grey-button',
                event: function(){
                    window.location.href = res.alipay_result_url;
                    $._LayerOut.close();
                }
            }
        ]
    });
};

function payOrderAjax( url , data ){
    if( !url ){
        window.lock = false;
        return false;
    };
    data = data || {};
    var new_tab = window.open();
    new_tab.opener = null;
    new_tab.open('','_self','');//for IE7
    $.get( url , data , function( res ) {
        if( res && res.status == 'ok' ){
            new_tab.location = res.alipay_url;
            showAfterPay( res );
        }else if( res && res.msg ){
            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + res.msg+ '</p>');
            window.lock = false;
            new_tab.close();
        }else{
            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请求出错了，刷新页面再试一下吧！</p>');
            new_tab.close();
            window.lock = false;
        };
    });
};

function confirmOrderAjax( url , data ){
    if( !url ){
        window.lock = false;
        return false;
    };
    data = data || {};
    $.post( url , data , function( res ) {
        if( res && res.status == 'ok' ){
            $( '#JS_agree_agreement' ).prop( 'checked' , false );
            window.location.href = res.redirect_url;
        }else if( res && res.msg ){
            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + res.msg+ '</p>');
            window.lock = false;
        }else{
            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请求出错了，刷新页面再试一下吧！</p>');
            window.lock = false;
        };
    });
};

$(function() {
    var $bill_form = $('#JS_bill_form'),
        save_bill_url = $bill_form.attr('action');

    $('#JS_save_bill_btn').click(function() {
        var $this = $(this),
            post_data = {
                csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val(),
                bill_type : $('input[name="bill_type"]:checked').val(),
                content : $('input[name="content"]').val(),
                title : $('input[name="title"]').val()
            };

        if( !post_data.csrfmiddlewaretoken ){
            $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>非法操作！</p>');
            return false;
        };

        if( !post_data.content ){
            $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>没有内容！</p>');
            return false;
        };

        if( !post_data.bill_type ){
            $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请选择抬头类型！</p>');
            return false;
        };

        $.post(save_bill_url, post_data, function(res) {
            if( res && res.status == 'ok' ){
                $('#JS_saved_bill').text( post_data.bill_type == 'company' ? '单位' : '个人' );
                $('#JS_saved_title').text( post_data.title );
                $('#JS_saved_content').text(post_data.content);
                $this.hide();
                $('#JS_notneed_invoice').hide();
                $('#JS_edit_invoice').show();
                $('#JS_saveed_info').show().siblings().hide();
                invoiceId = res.id;
                $('#JS_receiver_box').show();
            }else if( res.msg ){
                $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + res.msg + '</p>' );
            }else{
                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>保存失败，请稍后再试！</p>');
            };
        });
    });

    $(document).on( 'click' , '#JS_view_agreement' , function(){
        var html = $('#JS_agreement').html();
        $.LayerOut({
            html: html
        });
    });

    $('#JS_edit_invoice').on( 'click' , function(){
        $(this).hide().siblings().show();
        $('#JS_saveed_info').hide().siblings().show();
    });

    $(document).on( 'click' , '.JS_form_radio' , function(){
        var $this = $( this ),
            input = $( '#JS_bill_title' );
            console.log( $this.attr( 'data-company' ),input );
        if( $this.attr( 'data-company' ) ){
            input.show();
        }else{
            input.hide().val('');
        };
        $this.find('i').addClass('active').end().find('input').prop( 'checked' , true ).end().closest('p').siblings().find('.JS_form_radio').find('i').removeClass('active').end().find('input').prop( 'checked' , false );
    });

    $(document).on( 'click' , '#JS_receiver>div' , function(){
        var $this = $( this );
        if( $this.hasClass('add-address') ){
            $this.find('div').show();
        }else{
            $('.add-address').find('div').hide();
        };
        $this.find('i').addClass('active').end().siblings().find('i').removeClass('active').end().not('.add-address').find('.JS_cancel_edit').each(function(){
            resetInput( $(this) );
        });
    });

    var $receiver_form = $('#JS_save_receiver_form'),
        save_receiver_url = $receiver_form.attr('action');

    $('#JS_save_receiver_btn').click(function() {
        if( window.receiver_btn_lock ) {
            return;
        };
        window.receiver_btn_lock = true;

        var $this = $( this ),
            parent = $( '.add-address' ),
            name = parent.find('input[name^="name"]').val(),
            address = parent.find('input[name^="address"]').val(),
            phone = parent.find('input[name^="phone"]').val(),
            csrfmiddlewaretoken = $('#JS_address_csrf').val();
        if( !name || !address || !phone ){
            $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>收件人信息不完整！</p>' );
            window.receiver_btn_lock = false;
            return false;
        };

        if( !/^\d+$/g.test(phone) ){
            $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>联系格式不对！</p>' );
            window.receiver_btn_lock = false;
            return false;
        };

        $.post(save_receiver_url, {
            name: name,
            address: address,
            phone: phone,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        } , function(res) {
            if( res && res.status == 'ok' ){
                var html = '<div class="p10x0" data-id="' + res.id + '" data-edit_url="' + res.edit_url + '" data-delete_url="' + res.delete_url + '">' +
                            '<label class="toggle-radio ml10"><i class="i-radio active"></i></label>' +
                            '<input class="input w70 inline default" readonly="" type="text" name="name_' + res.id + '" value="' + name + '"> ' +
                            '<input class="input w100 inline default" type="text" readonly="" name="phone_' + res.id + '" value="' + phone + '">' +
                            '<input class="input w150 inline default" type="text" readonly="" name="address_' + res.id + '" value="' + address + '"> ' +
                            '<a href="javascript:;" title="编辑" class="blue-btn JS_edit_address ml10">编辑</a>' +
                            '<a href="javascript:;" title="编辑" class="blue-btn JS_save_address none ml10" style="display: none;">保存</a>' +
                            '<a href="javascript:;" title="编辑" class="grey-btn JS_cancel_edit none ml10" style="display: none;">取消</a>' +
                            '<a href="javascript:void(0);" title="删除" class="blue-btn JS_remove_address ml10" delete_url="/payment/delete_receiver_info/13/">删除</a>' +
                        '</div>';
                $('.add-address').before(html);
                $('.add-address').find('div').hide().end().find('i').removeClass('active').end().find('input').val('');
            }else if( res.msg ){
                $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + res.msg + '</p>' );
            }else{
                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>保存失败，请稍后再试！</p>');
            };
            window.receiver_btn_lock = false;
        },'json').fail(function() {
            window.receiver_btn_lock = false;
        });
    });

    $(document).on( 'click' , '.JS_edit_address' , function(){
        $( this ).hide().siblings('.JS_save_address,.JS_cancel_edit').show().end().siblings('input').removeClass('default').prop('readonly',false).parent().siblings().not('.add-address').find('input').addClass('default').prop('readonly',true);;
    });

    $(document).on( 'click' , '.JS_cancel_edit' , function( e ){
        resetInput( $(this) );
    });

    $(document).on( 'click' , '.JS_save_address' ,function(){
        var $this = $( this ),
            name = $this.siblings('input[name^=name_]').val(),
            address = $this.siblings('input[name^=address_]').val(),
            phone = $this.siblings('input[name^=phone_]').val(),
            url = $this.parent().attr('data-edit_url'),
            id = $this.parent().attr('data-id'),
            csrfmiddlewaretoken = $('#JS_address_csrf').val();
        if( !name || !address || !phone ){
            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>收件人信息不完整！</p>');
            return false;
        };
        if( !/^\d+$/g.test(phone) ){
            $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>联系格式不对！</p>' );
            return false;
        };
        $.post( url , {
            name: name,
            address: address,
            phone: phone,
            id: id,
            csrfmiddlewaretoken: csrfmiddlewaretoken
        }, function( res ){
            if( res && res.status == 'ok' ){
                resetInput( $this.siblings( '.JS_cancel_edit' ) );
            }else if( res.msg ){
                $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + res.msg + '</p>' );
            }else{
                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>保存失败，请稍后再试！</p>');
            };
        }, 'json');
    });

    $(document).on( 'click' , '.JS_remove_address' , function( e ){
        var $this = $( this ),
            url = $this.attr('delete_url');

        $.get( url , function( res ){
            if( res && res.status == 'ok' ){
                $this.parent().remove();
            };
        }, 'json');
        e.stopPropagation();
    });

    $('#JS_notneed_invoice').on( 'click' , function(){
        $( this ).closest('.invoice').hide().next().show();
        $('#JS_receiver_box').hide();
        invoiceId = null;
    });

    $('#JS_need_invoice').on( 'click' , function(){
        $( this ).closest('.invoice').hide().prev().show();
    });

    $( document ).on( 'change' , '#JS_agree_agreement' , function(){
        var btn = $('#JS_confirm_pay_btn, #JS_confirm_order_pay');
        if( $( this ).prop('checked') ){
            btn.removeClass( 'disabled' );
        }else{
            btn.addClass( 'disabled' );
        };
    });

    var csrf_token = $('#JS_address_csrf').attr('value');

    //确认订单并在线支付
    $('#JS_confirm_pay_btn').click(function() {
        if( window.lock ){
            return false;
        };
        window.lock = true;
        if( !$( '#JS_agree_agreement' ).prop('checked') ){
            window.lock = false;
            return false;
        };

        var confirm_pay_url = $(this).attr('data-confirm_pay_url'),
            receiver_id = $('#JS_receiver').find('i.active').parent().parent().attr('data-id'),
            data = {};

        if( invoiceId && !receiver_id ){
            $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请先保存收件人信息</p>');
            window.lock = false;
            return false;
        };

        data = {
            'need_bill': invoiceId ? 'yes' : 'no',
            'bill_id': invoiceId,
            'receiver_id': receiver_id,
            'csrfmiddlewaretoken': csrf_token
        };
        confirmOrderAjax( confirm_pay_url , data );

    });

    //立即支付
    $('#JS_immediately_pay_btn').on( 'click' , function(){
        if( window.lock ){
            return false;
        };
        window.lock = true;
        var url = $( this ).attr('data-confirm_pay_url');
        payOrderAjax( url );
    });

    $('#JS_confirm_order_pay').click(function() {
        if( window.lock ){
            return false;
        };
        window.lock = true;
        if( !$( '#JS_agree_agreement' ).prop('checked') ){
            window.lock = false;
            return false;
        }else{
            $( '#JS_agree_agreement' ).prop('checked' , false );
        };
    });
});
