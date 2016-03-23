var emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/,
/**验证规则**/
options = {
    rules: {
            username: {
                required: true,
                email: true
            },
            password: {
                required: true
            }
    },
    messages: {
        username: {
            required: "邮箱不能为空！",
            email: "请输入正确格式的邮箱！"
        },
        password: {
            required: "请输入密码！"
        }
    }

};
/**提交后回调函数**/
function showResponse(responseText,statusText) {
  $("#id_submit").removeAttr('disabled').removeClass('disabled');
  var res = responseText;
  if (res && res.status && res.status == 'ok') {
    //登录成功，页面跳转
    window.location.href = res.redirect_url;
  } else if (res && res.status && res.status == 'malice_ip') {
    //同一ip频繁提交
    $('button[type=submit]').attr('disabled', 'disabled').css('background', '#ccc');
    $('.result').html('提交得太频繁啦，休息一会再试吧！').parent().show();
  } else if (res && res.status && res.status == 'not_exist'){
    //邮箱或密码错误
    $('.login_tip_info').html(res.msg).parent().show();
  } else if (res && res.status && res.status == 'not_active'){
    $('.login_tip_info').html(res.msg).parent().show();
    $('.active_span').html('没有收到激活邮件？<a>重新发送</a>').parent().show();
    /**激活邮件重新发送点击事件**/
    $('.active_span a').on('click', function(){
        var $this = $(this);
        var email = $('[name = username]').val();
        $.ajax({
            type: 'get',
            dataType: 'json',
            url: '/account/send_active_email/' + email,
            success: function(data){
                if (data && data.status && data.status == 'ok'){
                    $('.active_send_resp').html(data.msg).parent().show();
                } else if(data && data.status && data.status == 'malice'){
                    $('.active_send_resp').html(data.msg).parent().show();
                    $this.css('color', '#777777').css('border-bottom', '1px solid #777777').unbind('click');
                }
            },
            error: function(data){
                console.log(data.responseText);
            }
        });
    });
  } else if (res && res.errors){

  }
}
/**提交前回调函数**/
function showRequest(formData,jqForm,options){
    var result = $("#loginForm").valid()
    if(result)
        $("#id_submit").attr('disabled', 'disabled').addClass('disabled');
    return result;
}
$(document).ready(function(){
    validator=$('#loginForm').validate(options);
    $("#id_submit").click(function(){
        var $this = $(this);
        validator.form();
        var username = $('[name = username]').val();
        var password = $('[name = password]').val();
        var csrfmiddlewaretoken = $('[name = csrfmiddlewaretoken]').val();
        $this.ajaxSubmit({
          type:"post",
          dataType: 'json',
          data: { 'username': username, 'password': password, 'csrfmiddlewaretoken': csrfmiddlewaretoken},
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
    $('.login_tip_info').parent().css('display', 'none');
    $('.active_span').parent().css('display', 'none');
    $('.active_send_resp').parent().css('display', 'none');
    $('button[type=submit]').removeAttr('disabled').css('background', '#0091fa');
    $('.result').parent().hide();
});
