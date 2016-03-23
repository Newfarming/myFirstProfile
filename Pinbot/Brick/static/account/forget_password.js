var emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/,
/**验证规则**/
options = {
	rules: {
            username: {
                required: true,
                email: true
            }
    },
    messages: {
        username: {
            required: "邮箱不能为空！",
            email: "请输入正确格式的邮箱！"
        }
    }

};
/**提交后回调函数**/
function showResponse(responseText,statusText) {
    $("#id_submit").removeAttr('disabled').removeClass('disabled');
    var res = responseText;
    if (res && res.status && res.status == 'ok') {
    //发送成功
    $('.reset_send_resp').html('您将会收到重置密码的电子邮件').parent().show();
    $('.reset_send_info').html('没收到激活邮件？请查看垃圾箱或<a>重新发送</a>').parent().show();
    /**忘记密码邮件重新发送点击事件**/
    $('.reset_send_info a').on('click', function(){
        var $this = $(this);
        var email = $('[name = username]').val();
        $.ajax({
            type: 'get',
            dataType: 'json',
            url: '/account/send_reset_email/' + email,
            success: function(data){
                if (data && data.status && data.status == 'ok'){
                    $('.reset_resend_info').html('发送成功！').parent().show();
                } else if(data && data.status && data.status == 'malice'){
                    $('.reset_send_resp').parent().css('display', 'none');
                    $('.reset_resend_info').parent().css('display', 'none');
                    $('.malice').html(data.msg).parent().show();
                    $this.css('color', '#777777').css('border-bottom', '1px solid #777777').unbind('click');
                }
            },
            error: function(data){
                console.log(data.responseText);
            }
        });
    });
    } else if (res && res.status && res.status == 'malice') {
    //同一ip频繁提交
    $('button[type=submit]').attr('disabled', 'disabled').css('background', '#ccc');
    $('.malice').html('提交得太频繁啦，休息一会再试吧！').parent().show();
    } else if (res && res.status && res.status == 'not_found_user'){
    $('.malice').html(res.msg).parent().show();
    }
}
/**提交前回调函数**/
function showRequest(formData,jqForm,options){
    var result = $("#forgetForm").valid()
    if(result)
        $("#id_submit").attr('disabled', 'disabled').addClass('disabled');
    return result;
}
$(document).ready(function(){
	validator=$('#forgetForm').validate(options);
	$("#id_submit").click(function(){
        validator.form();
        var username = $('[name = username]').val();
        var csrfmiddlewaretoken = $('[name = csrfmiddlewaretoken]').val();
        $(this).ajaxSubmit({
            type:"get",
            url: '/account/send_reset_email/' + username,
            dataType: 'json',
            data: { 'username': username, 'csrfmiddlewaretoken': csrfmiddlewaretoken},
            beforeSubmit:showRequest,
            success:showResponse,
            error: function(data){
                $("#id_submit").removeAttr('disabled').removeClass('disabled');
                console.log(data.responseText);
            }
        });

  	});
    $(document).on('keyup', function(event){
        if(event.keyCode ==13){
            $('#id_submit').trigger("click");
        }
    });
});
$('input').on( 'focus' , function(){
    //清除提示信息
    $('.tips').each(function(){
        $(this).parent().css('display', 'none');
    });
    $('button[type=submit]').removeAttr('disabled').css('background', '#0091fa');
});