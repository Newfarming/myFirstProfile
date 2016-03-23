var emailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/,
    gmailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([gG][mM][aA][iI][lL])+\.[a-zA-Z]{2,3}$/,
/**验证规则**/
options = {
     rules: {
            username: {
                required: true,
                email: true
            },
            password: {
                required: true
            },
            invite_code: {
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
        },
        invite_code: {
            required: "请输入邀请码！"
        }
    }

};
/**提交后回调函数**/
function showResponse(responseText,statusText) {
    $("#id_submit").removeAttr('disabled').removeClass('disabled');
    var res = responseText;
    if (res && res.status && res.status == 'ok') {
    //注册成功
    $('button[type=submit]').attr('disabled', 'disabled').css('background', '#ccc');
    $('.result').html('激活邮件已发送至你的注册邮箱，请激活后登录').parent().show();
    } else if (res && res.status && res.status == 'malice_ip') {
    //同一ip频繁提交
    $('button[type=submit]').attr('disabled', 'disabled').css('background', '#ccc');
    $('.result').html('提交得太频繁啦，休息一会再试吧！').parent().show();
    } else if(res && res.errors){
    //表单错误
    //1、邮箱格式错误
    //2、邮箱已存在
    //3、密码错误
    //4、邀请码错误
    for( var i in res.errors ){
        var $dom = $('[name="' + i + '"]'),
            id = $dom.attr('id'),
            $error = $('#' + id + '-error'),
            err = res.errors[i];
        if( $error.length ){
            $error.html( err ).show();
            $dom.addClass('error');
        }else{
            $dom.after('<label id="' + id + '-error" class="error" for="' + id + '">' + err + '</label>');
            $dom.addClass('error');
        };
    };
    }
}
/**提交前回调函数**/
function showRequest(formData,jqForm,options){
    var result = $("#registerForm").valid()
    if(result)
        $("#id_submit").attr('disabled', 'disabled').addClass('disabled');
    return result;
}
$(document).ready(function(){
    validator=$('#registerForm').validate(options);
    $("#id_submit").click(function(){
        var $this = $(this);
        validator.form();
        var username = $('[name = username]').val();
        var password = $('[name = password]').val() ? $('[name = password]').val() : '123456as';
        var invite_code = $('[name = invite_code]').val();
        var csrfmiddlewaretoken = $('[name = csrfmiddlewaretoken]').val();
        $this.ajaxSubmit({
            type: 'post',
            dataType: 'json',
            data: {'username': username,'password': password,'invite_code': invite_code, 'csrfmiddlewaretoken': csrfmiddlewaretoken},
            beforeSubmit: showRequest,
            success: showResponse,
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
$('#id_username').on( 'focus' , function(){
    $('.info').remove();
    $('[name = password]').parent().css('display', 'block');
    var $this = $( this ),
        val = $this.val();
    if (gmailReg.test(val)) {
        var $dom = $('[name=username]'),
            id = $dom.attr('id'),
            $error = $('#' + id + '-error'),
            err = 'Gmail可能会收不到验证邮件，建议使用其他邮箱';
        if( $error.length ){
            $error.html( err ).show();
        }else{
            $dom.after('<label id="' + id + '-error" class="error gmail" for="' + id + '">' + err + '</label>');
        };
    };

});
$('#id_username').on( 'keyup' , function(){
    var $this = $( this ),
        val = $this.val();
    if (gmailReg.test(val)) {
        var $dom = $('[name=username]'),
            id = $dom.attr('id'),
            $error = $('#' + id + '-error'),
            err = 'Gmail可能会收不到验证邮件，建议使用其他邮箱';
        if( $error.length ){
            $error.html( err ).show();
        }else{
            $dom.after('<label id="' + id + '-error" class="error gmail" for="' + id + '">' + err + '</label>');
        };
    };
});
$('#id_username').on( 'blur' , function(){
    $('.gmail').remove();
    var $this = $( this ),
        val = $this.val(),
        valid_email_url = $this.attr('valid_email');
    $this.data( 'username' , val );
    $this.data( 'valid_email_url' , valid_email_url );
    if( emailReg.test( val ) ){
        $.ajax({
            type: 'get',
            dataType: 'json',
            url: $this.data( 'valid_email_url'),
            data: {'username': $this.data( 'username' )},
            success: function(data){
                if (data && data.status && data.status == 'user_exists'){
                    var $dom = $('[name = username]'),
                        id = $dom.attr('id'),
                        $info = $('#' + id + '-info'),
                        msg = data.msg;
                    if( $info.length ){
                        $info.html( msg + '<a href="/account/login">登录</a>').show();
                        $info.find('a').on('click', function(){
                            window.location.href = '/account/login';
                        });
                    }else{
                        $dom.after('<label id="' + id + '-info" class="info" for="' + id + '">' + msg + '<a href="/account/login">登录</a></label>');
                        $('label').find('a').on('click', function(){
                            window.location.href = '/account/login';
                        });
                    };
                }else if (data && data.status && data.status == 'company_user'){
                    var $dom = $('[name = username'),
                        $info = $('#' + id + '-info'),
                        id = $dom.attr('id'),
                        $password = $('[name = password]'),
                        msg = data.msg;
                    if( $info.length ){
                        $info.html( msg ).show();
                        if($password.length != 0){
                            $password.parent().css('display', 'none');
                        }
                    }else{
                        $dom.after('<label id="' + id + '-info" class="info" for="' + id + '">' + msg + '</label>');
                        if($password.length != 0){
                            $password.parent().css('display', 'none');
                        }
                    };
                    $password.val('');
                }
            },
            error: function(data){
                console.log(data.responseText);
            }
        });
    };
});
