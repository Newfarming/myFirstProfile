$(function(){
    $('.payway').each(function(){
        var $this = $(this);
        $this.on('click', function(e){
            e.preventDefault();
        });
    });
    $('.confirm_pay_btn').on('click', function(e){
        e.preventDefault();
        $(this).attr('disabled', 'true');
        var url = $(this).attr('url'),
            newTab = window.open('about:blank');
        $.ajax({
            method: 'get',
            url: url,
            success: function(data){
                if(data.status && data.status === 'ok'){
                    var msg = '<div class="payway-alert">' +
                                '<h2>请你在新打开的页面上完成付款，付款完成前请不要关闭此窗口！</h2>' +
                                '<label>完成付款后请根据你的情况点击以下按钮。</label>' +
                                '<a url="/vip/alipay_result/" class="btn finish go_result">我已完成付款</a>' +
                                '<a url="/vip/alipay_result/" class="btn fail go_result">支付遇到问题</a>' +
                              '</div>';
                    $.alert(msg);
                    $('.modal-header').css('display', 'none');
                    $('.modal-handle').css('display', 'none');
                    $('#myModal').unbind('click');
                    newTab.location.href = data.pay_url;
                    var order_id = data.order_id;
                    $('.go_result').each(function(){
                        var $this = $(this),
                            url = $this.attr('url');
                        url = url + order_id;
                        $this.attr('href', url);
                    });
                }else if(data.status && data.status === 'apply_error'){
                    console.log(data.msg);
                    $.alert(data.msg);
                    $('.confirm_pay_btn').removeAttr('disabled');
                    newTab.close();
                }
            },
            error: function(data){
                $('.confirm_pay_btn').removeAttr('disabled');
                console.log(data);
                newTab.close();
            }
        });
    });
});