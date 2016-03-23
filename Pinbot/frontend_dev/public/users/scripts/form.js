//emailOrMobile 邮箱或手机号
$.validator.addMethod("emailOrMobile", function(value, element, options) {
        if (value.trim().match(/^[0-9a-z_\.\+\-]+@[0-9a-z\-]+\.[0-9a-z\.\-]+$/i) || value.match(/^1[0-9]{10}$/i)) {
            return true;
        } else {
            return false;
        }
    },
    "Please enter your email or mobile number."
);

//custom validation for 短信验证码
$.validator.addMethod("smscodeRequired", function(value, element, options) {
        if (value.match(/^[0-9]{6}$/i)) {
            return true;
        } else {
            return false;
        }
    },
    "Please enter your sms code."
);

//custom validation for 手机号码
$.validator.addMethod("mobile", function(value, element, options) {
        if (value.match(/^1[0-9]{10}$/i)) {
            return true;
        } else {
            return false;
        }
    },
    "Please enter your mobile number."
);

//custom validation for 联系电话
$.validator.addMethod("phoneNumber", function(value, element, options) {
        if (value.match(/^[0-9,\-]{6,}$/i)) {
            return true;
        } else {
            return false;
        }
    },
    "Please enter your phone number."
);

//custom validation for QQ
$.validator.addMethod("QQ", function(value, element, options) {
        if (value.match(/^[0-9]{5,}$/i)) {
            return true;
        } else {
            return false;
        }
    },
    "Please enter your QQ number."
);

//custom validation for 中文检测
$.validator.addMethod("chinese", function(value, element, options) {
        if (value.match(/[\u4E00-\u9FA5]|[\uFE30-\uFFA0]/ig)) {
            return true;
        } else {
            return false;
        }
    },
    "Please enter some Chinese words."
);

//修复placeholder动画效果
$("input.big-placeholder").focus(function() {
    if ($(this).parent().find('label:nth-child(1)').length == 1) {
        var label = $(this).parent().find('label:nth-child(1)');
        //if (pbDebug) console.log('focus', $(label).text());
        $(label).removeClass('pc-hide');
    }
});
$("input.big-placeholder").blur(function() {
    if ($(this).parent().find('label:nth-child(1)').length == 1) {
        var label = $(this).parent().find('label:nth-child(1)');
        //if (pbDebug) console.log('blur', $(label).text());
        if (!$(label).hasClass('pc-hide') && $(this).prop("value") == "") {
            $(label).addClass('pc-hide');
        }
    }
});
$("input.big-placeholder").change(function() {
    if ($(this).parent().find('label:nth-child(1)').length == 1) {
        var label = $(this).parent().find('label:nth-child(1)');
        if (!$(label).hasClass('pc-hide') && $(this).prop("value") == "") {
            $(label).addClass('pc-hide');
        } else if ($(this).prop("value") != "") {
            if ($(label).hasClass('pc-hide')) $(label).removeClass('pc-hide');
        } else {
            if (!$(label).hasClass('pc-hide')) $(label).addClass('pc-hide');
        }
    }
});
$("input.big-placeholder").keydown(function(e) {
    //console.log('key',e.keyCode);
    /*if(e.keyCode == 8){
            //backspace
        }else{
            if ($(this).parent().find('label:nth-child(1)').length == 1) {
                var label = $(this).parent().find('label:nth-child(1)');
                //console.log('keydown',"["+$(this).prop("value")+"]",$(this).prop("class"));
                if($(label).hasClass('pc-hide')) $(label).removeClass('pc-hide');
                if ($(this).prop("value") == "") {
                    if(!$(label).hasClass('pc-hide')) $(label).addClass('pc-hide');
                } else if ($(this).prop("value") != "") {
                    if($(label).hasClass('pc-hide')) $(label).removeClass('pc-hide');
                } else {
                    if(!$(label).hasClass('pc-hide')) $(label).addClass('pc-hide');
                }
            }
        }*/
    if ($(this).parent().find('label:nth-child(1)').length == 1) {
        var label = $(this).parent().find('label:nth-child(1)');
        if ($(label).hasClass('pc-hide')) $(label).removeClass('pc-hide');
    }
});

//
var countDown = function(secs, surl) {
    var jumpTo = $('.jumpTo')[0];
    if (jumpTo.innerHTML != null) {
        jumpTo.innerHTML = secs;
        if (--secs > 0) {
            setTimeout("countDown(" + secs + ",'" + surl + "')", 1000);
        } else {
            window.location.href = surl;
        }
    }
}

//$(function() {
//check if from new industry: /users/account_register/?from=new_industry /signin/?from=new_industry
var isFromNewIndustry = false;
var loc = document.location.href.toString();
if (loc.match(/from=new_industry/i)) {
    isFromNewIndustry = true;
}
//console.log('isFromNewIndustry',isFromNewIndustry);

//init领域
var objFromDataStr = function(trg, dataName) {
    var industryFields = [];
    if ($(trg).length) {
        var fieldsStr = $(trg).attr(dataName).replace(/\\\"/ig, "\"");
        if (fieldsStr != "") {
            industryFields = jQuery.parseJSON(fieldsStr);
            industryFields.pop();
            if (industryFields.length) {
                return industryFields;
            }
        }
    }
    return industryFields;
};
var renderList = function(currentIndustry) {
    $('.field_list').html('');
    for (var t in fieldsArr) {
        if (fieldsArr[t].industry == currentIndustry) {
            $('.field_list').append('<li><a href="#" industry_id="' + fieldsArr[t].industry + '" field_id="' + fieldsArr[t].id + '">' + fieldsArr[t].category + '</a></li>');
        }
    }
};
var currentIndustry = 'internet';
var industryArr = objFromDataStr('#regForm', 'data-industry');
var fieldsArr = objFromDataStr('#regForm', 'data-industry-fields');

for (var n in industryArr) {
    var t = industryArr[n];
    if (t.id !== 'internet' && $('.u-industry-btn > li > a[data-id="' + t.id + '"]').length === 0) {
        $('.u-industry-btn').append('<li><a class="" data-id="' + t.id + '" href="javascript:void(0);">' + t.name + '</a></li>');
    }
}
renderList(currentIndustry);
//console.log('length', $('.u-industry-btn > li > a[data-id="0"]').length);

$('.u-industry-btn > li > a').on('click', function(e) {
    if (!$(this).attr('class').match(/selected/i)) {
        $('.u-industry-btn > li > a').removeClass('selected');
        $(this).addClass('selected');
        //console.log($(this).attr('data-id'), $(this).text());
        currentIndustry = $(this).attr('data-id');
        $('.select_fields').each(function(i) {
            if(i == 0){
                $(this).attr('data-industry', currentIndustry);
                $(this).val('');
            }else{
                $(this).remove();
            }
        });
        renderList(currentIndustry);
    }
});

//test
var bookin_type = ""; //bookin_type: "1" 为4月16日北京场, "2" 为4月16日成都场
var successBox = function(bookin_type, currentIndustry, internetUrl, redirectUrl) {
    var trgDate = (bookin_type === '1') ? '4月16日·北京场' : '4月24日·成都场';
    var trgUrl = (currentIndustry === 'internet') ? internetUrl : redirectUrl;
    var content = '';
    content += '<div class="text-center j-choose-place">';
    content += '<p class="c607d8b f14 mt10"><span class="big-icon big-icon-flower"></span></p>';
    content += '<p class="f14 mt10">您已成功报名参加<span class="c44b5e8 f18"> ' + trgDate + ' </span>聘宝智能招聘服务新品发布会<br>活动开始前聘宝将通过电话或短信的方式通知您到场！</p>';
    content += '</div>';
    var modalHtml = PB.boxHtml('<span class="u-icon-delta"></span> Pinbot 聘宝智能招聘服务新品发布会', content, false, '', '我知道啦', undefined, 'btn-red');
    PB.modal(modalHtml, function() {
        //直接关闭
        document.location.href = trgUrl;
    }, undefined, function(e) {
        e.stopPropagation();
        document.location.href = trgUrl;
    }, undefined, 'btn-red');
};

var chooseMeetPlace = function(cancelUrl, postUrl, redirectUrl, isFromNewIndustry, currentIndustry) {
    var content = '';
    content += '<div class="text-center j-choose-place">';
    content += '<p class="c607d8b f14 mt10">现场行业领袖、大咖汇聚、诚邀您莅临</p>';
    content += '<p class="cf46c62 f14 mt20"><a href="javascript:void(0);" class="btn btn-white f-btn-210-45 f-btn-grey j-bj-416">4月16日北京场</a></p>';
    content += '<p class="cf46c62 f14 mt10"><a href="javascript:void(0);" class="btn btn-white f-btn-210-45 f-btn-grey j-cd-424">4月24日成都场</a></p>';
    content += '<p class="cf46c62 f14 mt20">活动报名需要请您选择场次与城市！</p>';
    content += '</div>';
    var modalHtml = PB.boxHtml('<span class="u-icon-delta"></span> Pinbot 聘宝智能招聘服务新品发布会', content, true, '不感兴趣', '我要报名');
    var postHandler = function(e) {
        //我要报名
        e.stopPropagation();
        var trgCss = '.u-btn-grey-blue';

        if (bookin_type === "") {
            $(trgCss).addClass('live');
            $(trgCss).tooltips('请先选择场次与城市！', undefined, true, false);
            return false;
        }

        var postData = {
            bookin_type: bookin_type
        };
        PB.request('post', postUrl, 'json', function(data) {
            PB.formErrHandler(data, function(data) {
                if (isFromNewIndustry) {
                    successBox(bookin_type, currentIndustry, cancelUrl, redirectUrl);
                } else {
                    document.location.href = cancelUrl;
                }
            }, null, trgCss, '我要报名！');

        }, function(data, status) {
            //PB.btnAlert('.btn-grey-blue', '网络貌似有问题～重新试试');
            $(trgCss).addClass('live');
            $(trgCss).tooltips('网络貌似有问题～重新试试', undefined, true, false);
            return false;
        }, postData, 'json');
    };
    PB.modal(modalHtml, function() {
        //直接关闭
        document.location.href = cancelUrl;
    }, function(e) {
        //不感兴趣
        e.stopPropagation();
        document.location.href = cancelUrl;
    }, postHandler);

    $(".modal").undelegate(".j-bj-416").delegate(".j-bj-416", "click", function() {
        bookin_type = "1";
        $('.j-choose-place a.btn-white').removeClass('f-btn-red');
        $(this).addClass('f-btn-red');
    });
    $(".modal").undelegate(".j-cd-424").delegate(".j-cd-424", "click", function() {
        bookin_type = "2";
        $('.j-choose-place a.btn-white').removeClass('f-btn-red');
        $(this).addClass('f-btn-red');
    });

};



//点击发送激活邮件
$('.send_active').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var email = $this.attr('email');
    if (pbDebug) console.log('send_active', email);
    if (isValidEmail(email)) {
        $.ajax({
            type: 'get',
            dataType: 'json',
            url: '/users/send_active_email/' + email + '/',
            success: function(data) {
                if (data && data.status && data.status == 'ok') {
                    $('.resp_info').html(data.msg).css('display', 'block');
                } else if (data && data.status && data.status == 'malice') {
                    $('.resp_info').html(data.msg).css('display', 'block');
                }
            }
        });
    } else {
        $('.resp_info').html('请登录邮箱激活邮件～').css('display', 'block');
    }

});
//去激活
$('.got-to-activate').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var email = $this.attr('email');
    if (pbDebug) console.log('got-to-activate', email);
    if (isValidEmail(email)) {
        if (email.match(/^([^@]+)@([0-9a-z\.\-]+)/i)) {
            var url = 'http://www.' + RegExp.$2;
            if (confirm('确定打开网址：[' + url + ']？')) {
                window.open(url);
            }
        }
    } else {
        $('.resp_info').html('请尽快登录邮箱激活邮件～').css('display', 'block');
    }
});

if ($('.captcha').length) {
    $('.captcha').click(function(e) {
        var src = $('.captcha').attr('src') + '?t=' + (+new Date());
        $('.captcha').attr('src', src);
    });
}

if ($('#JS_reset_submit').length) {
    $('#JS_reset_submit').click(function() {
        var form = $(this).closest('form'),
            data = form.serializeObject(),
            url = '/users/password_confirm_ajax/';
        if (!data.new_password1 || !data.new_password2) {
            $.alert('<p style="text-align:center;color:#333;font-size:14px;">请填写完整！</p>');
            return false;
        };
        if (data.new_password1.length < 6 || data.new_password2 < 6) {
            $.alert('<p style="text-align:center;color:#333;font-size:14px;">密码长度不能小于6！</p>');
            return false;
        };
        if (data.new_password1 != data.new_password2) {
            $.alert('<p style="text-align:center;color:#333;font-size:14px;">2次输入的密码不一致！</p>');
            return false;
        };
        $.post(url, JSON.stringify(data), function(res) {
            if (res && res.status == 'ok') {
                var html = $('#JS_no_card').html();
                $.LayerOut({
                    html: html,
                    dialogCss: 'width:540px;'
                });
            } else if (res && res.msg) {
                $.alert('<p style="text-align:center;color:#333;font-size:14px;">' + res.msg + '</p>');
            } else {
                $.alert('<p style="text-align:center;color:#333;font-size:14px;">请填写完整！</p>');
            };
        }, 'json');

    });
}

//});

/**注册验证规则**/
var regOptions = {
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
        phone: {
            required: true,
            phoneNumber: true
        },
        smscode: {
            required: true,
            smscodeRequired: true,
            minlength: 6,
            maxlength: 6
        },
        name: {
            required: true
            //,
            //chinese: true
        },
        qq: {
            required: true,
            QQ: true
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
        phone: {
            required: "联系电话不能为空！",
            phoneNumber: "请输入联系电话"
        },
        smscode: {
            required: "短信验证码不能为空！",
            smscodeRequired: "请输入短信验证码",
            minlength: "请输入六位短信验证码",
            maxlength: "请输入六位短信验证码"
        },
        name: {
            required: "真实姓名不能为空！"
            //,
            //chinese: "请输入中文！"
        },
        qq: {
            required: "联络QQ不能为空！",
            QQ: "请输入有效QQ号码！"
        },
        company_name: {
            required: "企业名称不能为空！"
        },
        select_fields: {
            required: "请选择所在领域！"
        },
        agreement: {
            required: "请同意聘宝用户协议！"
        }
    },
    errorClass: "invalid",
    invalidHandler: function(event, validator) {
        var errors = validator.errorList;
        $(errors[0].element).focus();
    }

};
var loginOptions = {
    rules: {
        username: {
            required: true,
            emailOrMobile: true
        },
        password: {
            required: true,
            minlength: 6,
            maxlength: 20
        }
    },
    messages: {
        username: {
            required: "邮箱/手机号不能为空！",
            emailOrMobile: "请输入正确格式的邮箱/手机号！"
        },
        password: {
            required: "密码不能为空！",
            minlength: "密码应为6-20位的数字加字母",
            maxlength: "密码应为6-20位的数字加字母"
        }
    },
    errorClass: "invalid",
    invalidHandler: function(event, validator) {
        var errors = validator.errorList;
        $(errors[0].element).focus();
    }
};
//resetMobileOptions
var resetMobileOptions = {
    rules: {
        phone: {
            required: true,
            mobile: true
        },
        code: {
            required: true,
            minlength: 4,
            maxlength: 8
        },
        password: {
            required: true,
            minlength: 6
        },
        re_password: {
            required: true,
            equalTo: "#password"
        }
    },
    messages: {
        phone: {
            required: "手机号不能为空！",
            mobile: "请输入正确的手机号！"
        },
        code: {
            required: "验证码不能为空！",
            minlength: "验证码应为4-8位的数字加字母",
            maxlength: "验证码应为4-8位的数字加字母"
        },
        password: {
            required: "新密码不能为空！",
            minlength: "新密码不少于六位！"
        },
        re_password: {
            required: "确认密码不能为空！",
            equalTo: "确认密码不对！"
        }
    },
    errorClass: "invalid",
    invalidHandler: function(event, validator) {
        var errors = validator.errorList;
        $(errors[0].element).focus();
    }
};
var resetOptions = {
    rules: {
        email: {
            required: true,
            email: true
        },
        code: {
            required: true,
            minlength: 4,
            maxlength: 8
        }
    },
    messages: {
        email: {
            required: "邮箱不能为空！",
            email: "请输入正确格式的邮箱！"
        },
        code: {
            required: "验证码不能为空！",
            minlength: "验证码应为4-8位的数字加字母",
            maxlength: "验证码应为4-8位的数字加字母"
        }
    },
    errorClass: "invalid",
    invalidHandler: function(event, validator) {
        var errors = validator.errorList;
        $(errors[0].element).focus();
    }
};
var resetOptions2 = {
    rules: {
        new_password1: {
            required: true,
            minlength: 6,
            maxlength: 20
        },
        new_password2: {
            required: true,
            minlength: 6,
            maxlength: 20,
            equalTo: "#password_new"
        }
    },
    messages: {
        new_password1: {
            required: "新密码不能为空！",
            minlength: "新密码应为6-20位的数字加字母",
            maxlength: "新密码应为6-20位的数字加字母"
        },
        new_password2: {
            required: "确认密码不能为空！",
            minlength: "确认密码应为6-20位的数字加字母",
            maxlength: "确认密码应为6-20位的数字加字母",
            equalTo: "确认密码不匹配"
        }
    },
    errorClass: "invalid",
    invalidHandler: function(event, validator) {
        var errors = validator.errorList;
        $(errors[0].element).focus();
    }
};
$(function() {

    if (!('placeholder' in document.createElement('input'))) {
        $('input[placeholder]').each(function() {

            var $input = $(this);
            var $label = $('<label>');
            $label.html($input.attr('placeholder'));
            $label.css({
                'height': '20px',
                'font-size': '16px',
                'position': 'absolute',
                'left': '10px',
                'top': '23px',
                'color': '#aaa',
                'cursor': 'text',
                'width': '90%',
                'text-align': 'left'
            });
            $input.on('focus', function() {
                $label.hide();
            });
            $input.on('blur', function() {
                $input.val() == "" ? $label.show() : $label.hide();
            });
            $input.on('keydown paste', function() {
                // setTimeout(function() {
                //     $label[$input.val() ? 'hide' : 'show']();
                // }, 0);
            }).parent().append(
                $label.on('click', function() {
                    $input.focus();
                })
            );
        });
    }
    $('.field_list').on('click', function(e) {
        e.preventDefault();
        var _current = $(this);
        var $target = $(e.target),
            $select_fields = $('.select_fields');

        $('label#select_fields-error').css('display', 'none');
        if ($target.is("a")) {
            var id = $target.attr('field_id');
            if ($target.parent().hasClass('selected')) {
                $target.parent().removeClass('selected');
                $select_fields.each(function() {
                    var $this = $(this);
                    if ($this.val() == id) {
                        $this.val('');
                        if ($select_fields.length > 1 && $this.val() == '') {
                            $this.remove();
                        }
                        return false;
                    }
                });
            } else if ($('.selected').length <= 3) {
                $target.parent().addClass('selected');
                $select_fields.each(function() {
                    var $this = $(this);
                    console.log("test",$this.val());
                    if ($this.val() == '') {
                        $this.val(id);
                        return false;
                    } else {
                        $this.parent().append('<input type="hidden" name="select_fields" data-industry="' + currentIndustry + '" class="select_fields" value="' + id + '" required/>');
                        return false;
                    }
                });
            } else {
                if ($target.parent().hasClass('selected')) {
                    $target.parent().removeClass('selected');
                }
            }
        } else if ($target.is("li")) {
            var id = $target.find('a').attr('field_id');

            if ($target.hasClass('selected')) {
                $target.removeClass('selected');
                $select_fields.each(function() {
                    var $this = $(this);
                    if ($this.val() == id) {
                        $this.val('');
                        if ($select_fields.length > 1 && $this.val() == '') {
                            $this.remove();
                        }
                        return false;
                    }
                });
            } else if ($('.selected').length <= 3) {
                $target.addClass('selected');
                $select_fields.each(function() {
                    var $this = $(this);
                    if ($this.val() == '') {
                        $this.val(id);
                        return false;
                    } else {
                        $this.parent().append('<input type="hidden" name="select_fields" data-industry="' + ' + currentIndustry + ' + '" class="select_fields" value="' + id + '" required/>');
                        return false;
                    }
                });
            }
        }
    });

    //注册
    var btnTitle = $('.register-confirm').html();
    $('.register-confirm').on('click', function() {
        //JSON.stringify
        var $form = $('#regForm'),
            //data = $form.serialize(),
            validator = $form.validate(regOptions),
            $confirm = $(this);
        if ($form.valid()) {
            //console.log('regForm data', data);
            //return false;
            $confirm.attr('disabled', 'true');

            var postData = PB.formSerializeToObject($form);
            if (postData.hasOwnProperty('smscode')) {
                postData['code'] = postData['smscode'];
                delete postData['smscode'];
            }

            PB.request('post', '/users/account_register/', 'json', function(data) {
                $('.register-confirm').removeAttr('disabled');

                PB.formErrHandler(data, function(data) {
                    $form[0].reset();
                    $('.selected').removeClass('selected');
                    $.cookie('wait_to_activate', data.username, {
                        expires: 365,
                        path: '/'
                    });
                    if (isFromNewIndustry) {
                        chooseMeetPlace(data.redirect_url, '/users/new_industry_bookin/', '/activity/medicine/success/', isFromNewIndustry, currentIndustry);
                    } else {
                        document.location.href = data.redirect_url;
                    }
                }, null, '.register-confirm', btnTitle);

            }, function(data, status) {
                PB.btnAlert('.register-confirm', '网络貌似有问题～重新试试');
                return false;
            }, postData, 'json');
            return false;
        }
        //$('body').scrollTop(0);
    });

    var pbLogin = function() {
        var $form = $('#loginForm'),
            //data = $form.serialize(),
            validator = $form.validate(loginOptions),
            $confirm = $(this);
        if ($form.valid()) {
            $('.login-btn').attr('disabled', 'true');
            //$form.submit();
            //$('body').scrollTop(0);

            var postData = PB.formSerializeToObject($form);
            /*if (postData.hasOwnProperty('email')) {
                postData['username'] = postData['email'];
                delete postData['email'];
            }*/

            PB.request('post', '/users/account_login/', 'json', function(data) {
                $('.login-btn').removeAttr('disabled');

                PB.formErrHandler(data, function(data) {

                    currentIndustry = data.user_industry;

                    if (isFromNewIndustry) {
                        chooseMeetPlace(data.redirect_url, '/users/new_industry_bookin/', '/activity/medicine/success/', isFromNewIndustry, currentIndustry);
                    } else {
                        document.location.href = data.redirect_url;
                    }
                    //document.location.href = data.redirect_url;
                }, null, '.login-btn', '立即登录');

            }, function(data, status) {
                PB.btnAlert('.login-btn', '网络貌似有问题～重新试试');
                $('.login-btn').attr('disabled', 'false');
                return false;
            }, postData, 'json');
            return false;
        }
        //$('body').scrollTop(0);
    };
    var enterEventBind = function(t, cb, args) {
        $(t).keypress(function(e) {
            var key = e.which;
            if (key == 13) {
                if (typeof cb == 'function') {
                    cb(args);
                }
            }
        });
    };
    enterEventBind('#password', function() {
        pbLogin();
    });

    //verify-by-mobile
    $('.verify-by-mobile').on('click', function() {
        document.location.href = '/users/change_pwd_by_mobile/';
    });

    //verify-by-email
    $('.verify-by-email').on('click', function() {
        document.location.href = '/users/resetpassword/';
    });

    //登录
    $('.login-btn').on('click', function() {
        pbLogin();
    });
    //通过手机重设密码
    var resetByMobileBtnTitle = $('.reset-mobile-btn').html();
    $('.reset-mobile-btn').on('click', function() {

        PB.validateFormSubmit($('#resetByMobileForm'), resetMobileOptions, '.reset-mobile-btn', function(postData) {
            if (postData.hasOwnProperty('phone')) {
                postData['mobile'] = postData['phone'];
                delete postData['phone'];
            }
            return postData;
        }, '/users/change_pwd_by_mobile/', function(data) {
            //修改成功
            $('#resetByMobileForm')[0].reset();
            PB.btnAlert('.reset-mobile-btn', '新密码设置成功！', resetByMobileBtnTitle, '#fff');
        }, '找回密码');

    });

    //重设密码
    $('.reset-btn').on('click', function() {

        /*PB.validateFormSubmit($('#resetForm'), resetOptions, '.reset-btn', function(postData) {
            return postData;
        }, '/users/resetpassword/', function(data) {
            $('#resetForm')[0].reset();
            //PB.btnAlert('.reset-btn', '新密码设置成功！', resetByMobileBtnTitle, '#fff');
        }, '找回密码', 'post');*/

        var $form = $('#resetForm'),
            data = $form.serialize(),
            validator = $form.validate(resetOptions),
            $confirm = $(this);
        if ($form.valid()) {
            $confirm.attr('disabled', 'true');
            $form.submit();
            $('body').scrollTop(0);
        }

    });
    //重设密码 2
    $('.reset2-btn').on('click', function() {
        var $form = $('#resetForm2'),
            data = $form.serialize(),
            validator = $form.validate(resetOptions2),
            $confirm = $(this);
        if ($form.valid()) {
            $confirm.attr('disabled', 'true');
            $form.submit();
            $('body').scrollTop(0);
        }

    });

    //获取验证码
    var isReSend = false;
    var timeInterval;
    if ($('.smscodeBox').length) PB.smsCodeHtml('.smscodeBox', 'phone', timeInterval, isReSend);

    var isReSendOnReset = false;
    var timeIntervalOnReset;
    if ($('#code-mobile').length) PB.smsCodeHtml('#code-mobile', 'phone', timeIntervalOnReset, isReSendOnReset, 'ChangePwd');

    //修改邮箱 modify-email
    $('.modify-email').on('click', function(e) {
        var html = '<div class="no-feed-alert">' +
            '<p class="text-center f14">请重新输入接收邮箱：<input type="text" name="new-email" value="" id="new-email" class="dark-border f14"><br><br></p>' +
            '<p class="text-center f14"><span class="city-no-star">该邮箱仅为您接受聘宝推荐简历的邮箱，不用于登录，您可至“个人设置”中修改</span><br><br></p>' +
            '<p class="text-center">' +
            //'<a class="btn cancel closeLayer">取消</a>' +
            '<button class="btn btn-blue-light-submit-small confirm">发送验证链接</button>' +
            '</p>' +
            '</div>';
        $.LayerOut({
            html: html
        });
        $('.modal').delegate('.confirm', 'click', function() {
            //$('.modal-backdrop,.modal').remove();
            //delete $._LayerOut;
            console.log('confirm');

        });
    });

    //resend-email
    $('.resend-email').on('click', function(e) {
        $('.pb-wait-resend').removeClass('pb-hide');
        PB.request('get', '/users/resend_bind_email/', 'json', function(data) {
            $('.done-resend').removeClass('pb-hide');
            $('.pb-wait-resend').addClass('pb-hide');
        }, function(data, status) {
            $('.done-resend-err').removeClass('pb-hide');
            $('.pb-wait-resend').addClass('pb-hide');
        });
    });

    //修改接收邮箱
    $("p").undelegate(".chg-email").delegate(".chg-email", "click", function(e) {
        PB.chgNotifyEmail(isReSend, timeInterval, function(data) {

            PB.formErrHandler(data, function(data) {
                box.close();
                //document.location.href = '/users/profile/';
                $('.pb-layer').addClass('pb-hide');
                $('.email-valid-ok').removeClass('pb-hide');
                PB.countDown('.email-valid-ok', '/users/profile/');
                $('.link-guide').on('click', function(e) {
                    document.location.href = '/tut/';
                });
            }, null, '.chg-email', '确认修改');

            /*$('.pb-layer').addClass('pb-hide');
            if(data.status!=undefined){
                if(data.status=='ok'){
                    $('.email-valid-ok').removeClass('pb-hide');
                    PB.countDown('.email-valid-ok','/users/profile/');
                    $('.link-guide').on('click', function(e) {
                        document.location.href='/tut/';
                    });
                }else{
                    $('.email-valid-failed').removeClass('pb-hide');
                    PB.countDown('.email-valid-failed','/users/profile/');
                    $('.link-guide').on('click', function(e) {
                        document.location.href='/tut/';
                    });
                }
            }else{
                $('.email-valid-wrong').removeClass('pb-hide');
                $('.verify-email-again').on('click', function(e) {
                        document.location.reload();
                });
            }*/
        });
    });

});