/**验证规则**/
var pwdReg = /^(?![^a-zA-Z]+$)(?!\D+$).{8,20}$/,
options = {
	rules: {
            password: {
              required: true,
              rangelength:[8,20]
            },
            confirm_password: {
              required: true,
              equalTo: "#id_password"
            }
    },
    messages: {
        password: {
          required: '新密码不能为空！',
          rangelength: '密码应为8-20个数字+字母'
        },
        confirm_password: {
          required: '密码确认不能为空！',
          equalTo: '两次输入不一致！'
        }
    }

};
/**提交后回调函数**/
function showResponse(responseText,statusText) {
    $("#id_submit").removeAttr('disabled').removeClass('disabled');
    var res = responseText;
    if (res && res.status && res.status == 'ok') {
    //修改成功，跳转登录页
    window.location.href = '/account/login';
    } else if (res && res.status && res.status == 'token_error'){
    //链接无效
    alert(res.msg);
    } else if (res && res.status && res.status == 'token_expire'){
    //链接失效
    alert(res.msg);
    } else if (res && res.status && res.status == 'form_error'){
    alert(res.msg);
    }
}
/**提交前回调函数**/
function showRequest(formData,jqForm,options){
    var result = $("#resetForm").valid()
    if(result)
        $("#id_submit").attr('disabled', 'disabled').addClass('disabled');
    return result;
}
$(document).ready(function(){
	validator=$('#resetForm').validate(options);
	$("#id_submit").click(function(){
      var $this = $(this);
  	  validator.form();
      var password = $('[name = password]').val();
      var confirm_password = $('[name = confirm_password]').val();
      var csrfmiddlewaretoken = $('[name = csrfmiddlewaretoken]').val();
      $this.ajaxSubmit({
        type:"post",
        url: '.',
        dataType: 'json',
        data: { 'password': password, 'confirm_password': confirm_password, 'csrfmiddlewaretoken': csrfmiddlewaretoken},
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
$('#id_password').on('blur', function(){
  var $this = $(this),
      val = $this.val(),
      id = $this.attr('id');
      if (!pwdReg.test(val))
      {
        var $error = $('#' + id + '-error'),
            err = '密码应为8-20个数字+字母';
        if( $error.length ){
            $error.html( err ).show();
            $this.addClass('error');
        }else{
            $this.after('<label id="' + id + '-error" class="error" for="' + id + '">' + err + '</label>');
            $this.addClass('error');
        };
      };
});
$('input').on( 'focus' , function(){
    //清除提示信息
    var $this = $(this),
        id = $this.attr('id');
    $this.removeClass('error');
    $('#' + id + '-error').each(function(){
        $(this).css('display', 'none');
    });
    $('.tips').each(function(){
        $(this).parent().css('display', 'none');
    });
    $('button[type=submit]').removeAttr('disabled').css('background', '#0091fa');
});