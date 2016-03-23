$(function(){
    var $apply_btn = $('.apply_btn'),
        $show_apply_btn = $('.show_apply_btn');
    $show_apply_btn.on('click', function(e){
        var $this = $(this),
            apply_url = $this.attr('apply_url');
        e.preventDefault();
        $('.modal-backdrop-price, .modal-price').show();
        $('.modal-dialog-price').css({
            marginTop: ( $(window).height() - $('.modal-dialog-price').height() ) / 2 + 'px'
        });
        $apply_btn.attr('apply_url', apply_url);
    });
    $apply_btn.bind('click', function(e){
        e.preventDefault();
        var $this = $(this),
            apply_url = $this.attr('apply_url');
        $(this).attr('disabled', 'disabled');
        $.ajax({
            method: 'get',
            url: apply_url,
            success: function(data){
                $('.apply_btn').removeAttr('disabled');
                $('.modal-backdrop-price,.modal-price').hide();
                if(data.status && data.status === 'ok'){
                    window.location.href = data.redirect_url;
                }else if(data.status && data.status === 'error'){
                    var download_url = data.download_url,
                        html = '<div class="no-feed-alert error-alert">' +
                                    '<i class="i-close closeLayer"></i>' +
                                    '<h2><i class="i-notice"></i>请勿重复提交申请</h2>' +
                                    '<p class="ques">没有下载协议？点此下载<a href="' + download_url + '">纸质协议</a>。还没有签订协议或者还未开通？' +
                                    '</p>' +
                                    '<p class="btn_field">' +
                                        '<a id="JS_trigger_qq">联系聘宝专属顾问</a>' +
                                    '</p>' +
                                '</div>';
                    $.LayerOut(
                        {
                            html: html
                        }
                    );
                    $('.closeLayer').on('click', function(){
                        $('.modal-backdrop,.modal').hide();
                    });
                    $('#JS_trigger_qq').on('click', function(){
                        if( BizQQWPA != undefined ) BizQQWPA.addCustom({
                            aty: '0',
                            nameAccount: '800031490',
                            selector: 'JS_trigger_qq'
                        });
                    });
                }else if(data.status && data.status === 'invalid'){
                    console.log(data.msg);
                    $.alert('<p style="font-size: 16px;">'+ data.msg + '</p>');
                }
            }
        });
    });
    $('.i-close').on('click', function(){
        $('.modal-backdrop-price,.modal-price').hide();
    })
});