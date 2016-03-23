/**验证规则**/
var options = {
    rules: {
            user_email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 6,
                maxlength: 20
            },
            name: {
                required: true
            },
            phone: {
                required: true
            },
            qq: {
                required: true
            },
            company_name: {
                required: true
            },
            select_fields: {
                required: true
            },
            agreement: {
                required: true
            }
    },
    messages: {
        user_email: {
            required: "邮箱不能为空！",
            email: "请输入正确格式的邮箱！"
        },
        password: {
            required: "密码不能为空！",
            minlength: "密码应为6-20位的数字加字母",
            maxlength: "密码应为6-20位的数字加字母"
        },
        name: {
            required: "真实姓名不能为空！"
        },
        phone: {
            required: "联系电话不能为空！"
        },
        qq: {
            required: "联络QQ不能为空！"
        },
        company_name: {
            required: "企业名称不能为空！"
        },
        select_fields: {
            required: "请选择所在领域！"
        },
        agreement: {
            required: "请同意聘宝会员协议！"
        }
    },
    errorClass: "invalid"

};
$(function() {
    if (!('placeholder' in document.createElement('input'))) {
        $('input[placeholder]').each(function() {

            var $input = $(this);
            var $label = $('<label>');
            $label.html($input.attr('placeholder'));
            $label.css({
            'font-size': '12px',
            'position': 'absolute',
            'left': '110px',
            'top': '13px',
            'color': '#999',
            'cursor': 'text',
            'width': '90%',
            'text-align': 'left'
        });

        $input.on('keydown paste', function() {
            setTimeout(function() {
              $label[ $input.val() ? 'hide' : 'show' ]();
            }, 0);
        }).parent().append(
            $label.on('click', function() {
              $input.focus();
            })
          );
        });
    }
    $('.field_list').on('click', function(e){
        e.preventDefault();
        var $target = $(e.target),
            $select_fields = $('.select_fields');
        $('label#select_fields-error').css('display', 'none');
        if ($target.is("a")) {
            var id = $target.attr('field_id');
            if($target.parent().hasClass('selected')){
                $target.parent().removeClass('selected');
                $select_fields.each(function(){
                    var $this = $(this);
                    if($this.val() == id){
                        $this.val('');
                        if($select_fields.length > 1 && $this.val() == ''){
                          $this.remove();
                        }
                        return false;
                    }
                });
            } else if ($('.selected').length < 3) {
                $target.parent().addClass('selected');
                $select_fields.each(function(){
                    var $this = $(this);
                    if($this.val() == ''){
                        $this.val(id);
                        return false;
                    }else{
                        $this.parent().append('<input type="hidden" name="select_fields" class="select_fields" value="'+id+'" required/>');
                        return false;
                    }
                });
            }
        } else if($target.is("li")){
            var id = $target.find('a').attr('field_id');
            if($target.hasClass('selected')){
                $target.removeClass('selected');
                $select_fields.each(function(){
                    var $this = $(this);
                    if($this.val() == id){
                        $this.val('');
                        if($select_fields.length > 1 && $this.val() == ''){
                          $this.remove();
                        }
                        return false;
                    }
                });
            } else if ($('.selected').length < 3) {
                $target.addClass('selected');
                $select_fields.each(function(){
                    var $this = $(this);
                    if($this.val() == ''){
                        $this.val(id);
                        return false;
                    }else{
                        $this.parent().append('<input type="hidden" name="select_fields" class="select_fields" value="'+id+'" required/>');
                        return false;
                    }
                });
            }
        }
    });

    $('.confirm').on('click', function(){
        var $form = $('form'),
            data = $form.serialize(),
            validator = $form.validate(options),
            $confirm = $(this);
        if($("form").valid()){
            $confirm.attr('disabled', 'true');
            $.ajax({
                url: '.',
                method: 'post',
                data: data,
                success: function(data) {
                    $('.confirm').removeAttr('disabled');
                    console.log(data.msg);
                    var errors = data.errors;
                    if(errors){
                        for (var key in errors) {
                            $('#' + key + '-error').html(errors[key]).css('display','block');
                        };
                    }else {
                        $('form')[0].reset();
                        $('.selected').removeClass('selected');
                        $.alert('<p style="font-size: 16px;">激活邮件已发送至你的企业邮箱！</p>');
                    }
                },
                error: function(data) {
                    console.log(data.responseText);
                }
            });
        }
        $('body').scrollTop(0);
    });
});