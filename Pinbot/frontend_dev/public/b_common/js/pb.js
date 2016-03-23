/**
 * pinbot新版公用库 by Adam at 2015-10-20(Tuesday)
 * 本库依赖于lib.js和common.js
 *
 */
var PB = (function() {
    return {
        debug: false,
        setCookie: function(key, value, timeout) {
            var timeout = (timeout != undefined && typeof timeout == 'number') ? timeout : 86400000;
            var expires = new Date();
            expires.setTime(expires.getTime() + timeout);
            document.cookie = key + '=' + value + ';expires=' + expires.toUTCString() + ';path=/;';
        },
        //漂移到对应元素
        jumpTo: function(className) {
            //console.log('jumpToPanel', className);
            var top = $(className).offset().top;
            if (top != undefined && typeof top == 'number') $(window).scrollTop(top);
        },
        getCookie: function(key) {
            var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
            return keyValue ? keyValue[2] : null;
        },
        fakePromise: function(data, status) {
            var d = $.Deferred();
            if (status != undefined && status == "ok") {
                d.resolve(data);
            } else {
                d.reject(data);
            }
            return d.promise();
        },
        et: function(b, a, t, p) {
            b.prototype = a;
            a.apply(t, p);
        },
        request: function(method, url, format, cbOk, cbErr, postData, postFormat) {
            var format = (format != undefined && typeof format == 'string' && format == 'post') ? 'post' : 'json';
            var postFormat = (postFormat != undefined && typeof postFormat == 'string' && postFormat == 'post') ? 'post' : 'json';
            var method = (method != undefined && typeof method == 'string' && method == 'post') ? 'post' : 'get';
            var transPostVars = function(postData) {
                var postStr = '';
                for (var i in postData) {
                    if (postData.hasOwnProperty(i)) {
                        if (postStr == '') {
                            postStr += '' + i + '=' + postData[i];
                        } else {
                            postStr += '&' + i + '=' + postData[i];
                        }
                    }
                }
                return postStr;
            };
            var getCookie = function(key) {
                var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
                return keyValue ? keyValue[2] : null;
            }
            var config = {
                url: url,
                type: method,
                cache: false,
                //csrftoken
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                },
                success: function(data) {
                    if (typeof cbOk == 'function') cbOk(data);
                },
                error: function(err, status) {
                    if (typeof cbErr == 'function') cbErr(err, status);
                }
            };
            if (format == 'json') config.dataType = 'json';
            if (method == 'post') {
                if (postFormat == 'json') {
                    config.headers['Content-Type'] = 'application/json';
                    config.data = JSON.stringify(postData);
                } else {
                    config.data = transPostVars(postData);
                }
            }
            if (1 == 2 && this.debug != undefined && this.debug && url.match(/send_sms_code/i)) {
                var data = {
                    status: 'ok',
                    msg: "发送验证短成功"
                };
                if (typeof cbOk == 'function') cbOk(data);
                return this.fakePromise(data, 'ok');
            } else {
                return $.ajax(config);
            }
        },
        formErrHandler: function(data, cbOk, cbErr, submitBtnClass, btnTitle) {
            var _this = this;
            var errors = data.errors;
            if (errors) {
                console.log('errors', errors);
                var i = 0;
                for (var key in errors) {
                    if (errors.hasOwnProperty(key)) {
                        if (i == 0) {
                            //code email phone username
                            if (key == 'code' && $('#' + key + '').length == 0) {
                                if ($('#smscode').length) {
                                    $('#smscode').focus();
                                } else if ($('#code-email').length) {
                                    $('#code-email').focus();
                                }
                            } else if (key == 'email' && $('#' + key + '').length == 0) {
                                if ($('#to-chg-email').length) {
                                    $('#to-chg-email').focus();
                                }
                            } else if (key == 'phone' && $('#' + key + '').length == 0) {
                                if ($('#new-phone').length) {
                                    $('#new-phone').focus();
                                }
                            } else {
                                $('#' + key + '').focus();
                            }
                        }
                        //console.log('key', key, errors[key]);
                        var errMsg = (typeof errors[key] == 'object') ? errors[key][0] : errors[key];
                        if (key == 'code' && $('#' + key + '').length == 0) {
                            if ($('#smscode').length) {
                                $('#smscode-error').html(errMsg).css('display', 'block');
                            } else if ($('#code-email').length) {
                                $('#code-email-title-error').css('display', 'block');
                                $('#code-email-error').html(errMsg).css('display', 'block');
                            }
                        } else if (key == 'email' && $('#' + key + '').length == 0) {
                            if ($('#to-chg-email').length) {
                                $('#to-chg-email-title-error').css('display', 'block');
                                $('#to-chg-email-error').html(errMsg).css('display', 'block');
                            }
                        } else if (key == 'phone' && $('#' + key + '').length == 0) {
                            if ($('#new-phone').length) {
                                $('#new-phone-title-error').css('display', 'block');
                                $('#new-phone-error').html(errMsg).css('display', 'block');
                            }
                        } else {
                            $('#' + key + '-error').html(errMsg).css('display', 'block');
                            if ($('#' + key + '-title-error').length) $('#' + key + '-title-error').css('display', 'block');
                        }
                        //break;
                    }
                    i++;
                };
                if (typeof cbErr == 'function') cbErr(data);
            } else {
                //form.reset();
                if (data.status != undefined && data.status != 'ok') {
                    if (submitBtnClass != undefined) _this.btnAlert(submitBtnClass, data.msg, btnTitle);
                } else {
                    if (typeof cbOk == 'function') cbOk(data);
                }
            }
        },
        func: function() {
            //var args = [].slice.call(arguments)
        },
        captcha: function(t) {
            $(t).html('<img title="看不请？点击刷新" name="code" src="/users/get_check_code_image/" alt="点击刷新" width="135px" height="40px" />');
            $(t).find('img').on('click', function(e) {
                var src = $(this).attr('src') + '?t=' + (+new Date());
                $(this).attr('src', src);
            });
        },
        box: function(html, okClass, okCb, closeCb, phoneIdName, isReSend, timeInterval, actionName) {
            var _this = this;
            $.LayerOut({
                closeByShadow: false,
                html: html
            });
            _this.close = function() {
                $('.modal-backdrop,.modal').remove();
                delete $._LayerOut;
            };
            if (html.match(/use\-captcha/i)) _this.captcha('.no-feed-alert .use-captcha');
            if (html.match(/use\-sms\-code/i) && phoneIdName != undefined) {
                _this.smsCodeHtml('.no-feed-alert .use-sms-code', phoneIdName, timeInterval, isReSend, actionName);
            } else if (html.match(/use\-email\-code/i) && phoneIdName != undefined && phoneIdName.match(/ /i)) {
                var tmpArr = [];
                if (typeof phoneIdName == 'string') tmpArr = phoneIdName.split(' ');
                if (tmpArr.length == 2) {
                    _this.emailCodeHtml('.no-feed-alert .use-email-code', tmpArr[0], tmpArr[1], timeInterval, isReSend);
                }
            }

            $('.closeLayer').on('click', function() {
                $('.modal-backdrop,.modal').remove();
                delete $._LayerOut;
                if (typeof closeCb == 'function') closeCb($(this));
            });
            $(okClass).on('click', function() {
                if (typeof okCb == 'function') okCb($(this), _this);
            });
        },
        btnAlert: function(trg, info, btnTitle, dfBg) {
            //console.log('btnAlert', trg, info);
            var old = $(trg).html();
            if (btnTitle != undefined && typeof btnTitle == 'string') old = btnTitle;
            var dfBg = (dfBg != undefined && typeof dfBg == 'string') ? dfBg : '#cccccc';
            var oldBg = $(trg).css("background-color");
            $(trg).css("background-color", dfBg);
            $(trg).html('').hide();
            $(trg).html('<span class="error">' + info + '</span>').fadeIn(200).delay(1000).fadeOut(200, function() {
                $(trg).css("background-color", oldBg);
                $(trg).html(old).fadeIn(200);
            });
        },
        getSmsCode: function(phoneNumber, trg, btnTitle, actionName) {
            var _this = this;
            var actionName = (actionName != undefined && typeof actionName == 'string') ? actionName : 'AccountReg';
            $('.smscode').focus();
            var promise = _this.request('post', '/users/send_sms_code/', 'json', function(data) {
                _this.formErrHandler(data, function(data) {
                    return true;
                }, null, trg, btnTitle);
            }, function(data, status) {
                //var errMsg = '获取验证码失败！请重新获取';
                _this.formErrHandler(data, function(data) {
                    return false;
                }, null, trg, btnTitle);
                /*if ($('#smscode-error').length) {
                    $('#smscode-error').html(errMsg).css('display', 'block');
                } else {
                    if (trg != undefined) _this.btnAlert(trg, errMsg, btnTitle);
                }*/
            }, {
                action_name: actionName, //(AccountReg/ChangePwd/ChangeMobile)
                mobile: phoneNumber
            }, 'json');
            return promise;
        },
        smsCodeHtml: function(t, phoneInputName, timeInterval, isReSend, actionName) {
            var _this = this;
            $(t).append('<button type="button" class="btn btn-blue-submit-small smscode"><span>获取验证码</span></button>');
            var smsBtnTitle = $('.smscode', t).html();

            $(t).undelegate('.smscode', 'click').delegate('.smscode', 'click', function(e) {
                //console.log('click smscode',t, phoneInputName, timeInterval, isReSend);
                var me = $(this);
                var timeLeft = 60;
                if (!$('#' + phoneInputName).prop('value').match(/^1[0-9]{10}$/i)) {
                    if ($('#' + phoneInputName + '-error').length) {
                        $('#' + phoneInputName + '-error').text('请输入手机号码！').show();
                    } else {
                        _this.btnAlert('.smscode', '请输入手机号码！', smsBtnTitle);
                    }
                    return false;
                } else {

                    if ($('#' + phoneInputName + '-error').length) {
                        $('#' + phoneInputName + '-error').text('').hide();
                        $('#' + phoneInputName + '-title-error').hide();
                    } else {
                        //_this.btnAlert('.smscode', '获取验证码', smsBtnTitle);
                    }
                }
                var phoneNumber = $('#' + phoneInputName).prop('value');

                var promise;
                var promise_err = false;
                var countDownLeft = 0;
                if (!me.prop('disabled')) {
                    promise = _this.getSmsCode(phoneNumber, '.smscode', smsBtnTitle, actionName);
                    promise.fail(function() {
                        promise_err = true;
                        //countDownLeft = 0;
                    });
                }
                me.prop('disabled', true);
                $('.smscode', t).html('<span><span class="count-down">' + timeLeft + '</span>s后重新获取</span>');
                timeInterval = setInterval(function() {
                    var leftSeconds = $('.smscode .count-down', t).text();
                    if (!leftSeconds.match(/[0-9]/i)) leftSeconds = '0';
                    countDownLeft = parseInt(leftSeconds);
                    countDownLeft--;
                    //console.log('setInterval', leftSeconds, countDownLeft, isReSend, timeInterval);
                    if (countDownLeft <= 0) {
                        clearInterval(timeInterval);
                        me.prop('disabled', false);
                        if (!promise_err) $('.smscode', t).html(smsBtnTitle);
                        isReSend = true;
                    } else {
                        $('.smscode .count-down', t).text(countDownLeft);
                    }
                }, 1000);

                return false;

            });
        },
        getEmailCode: function(password, email, trg, btnTitle) {
            var _this = this;
            $('.emailcode').focus();
            var promise = _this.request('post', '/users/send_email_code/', 'json', function(data) {
                _this.formErrHandler(data, function(data) {
                    return true;
                }, null, trg, btnTitle);
            }, function(data, status) {
                /*var errMsg = '获取邮箱验证码失败！请重新获取';
                if ($('#emailcode-error').length) {
                    $('#emailcode-error').html(errMsg).css('display', 'block');
                } else {
                    if (trg != undefined) _this.btnAlert(trg, errMsg, btnTitle);
                }*/
                _this.formErrHandler(data, function(data) {
                    return false;
                }, null, trg, btnTitle);
            }, {
                password: password,
                email: email
            }, 'json');
            return promise;
        },
        emailCodeHtml: function(t, pwdInputName, emailInputName, timeInterval, isReSend) {
            var _this = this;
            $(t).append('<button type="button" class="btn btn-blue-submit-small emailcode"><span>获取邮箱验证码</span></button>');
            var smsBtnTitle = $('.emailcode', t).html();

            $(t).undelegate('.emailcode', 'click').delegate('.emailcode', 'click', function(e) {
                //console.log('click emailcode',t, pwdInputName, timeInterval, isReSend);
                var me = $(this);
                var timeLeft = 60;
                if ($('#' + pwdInputName).prop('value').trim().length < 6) {
                    if ($('#' + pwdInputName + '-error').length) {
                        $('#' + pwdInputName + '-error').text('请输入登录密码！').show();
                    } else {
                        _this.btnAlert('.emailcode', '请输入登录密码！', smsBtnTitle);
                    }
                    return false;
                } else if (!_this.isValidEmail($('#' + emailInputName).prop('value'))) {
                    if ($('#' + emailInputName + '-error').length) {
                        $('#' + emailInputName + '-error').text('请输入邮箱！').show();
                    } else {
                        _this.btnAlert('.emailcode', '请输入邮箱！', smsBtnTitle);
                    }
                    return false;
                } else {

                    if ($('#' + pwdInputName + '-error').length) {
                        $('#' + pwdInputName + '-error').text('').hide();
                        $('#' + pwdInputName + '-title-error').hide();
                        $('#' + emailInputName + '-error').text('').hide();
                        $('#' + emailInputName + '-title-error').hide();
                    } else {
                        //_this.btnAlert('.emailcode', '获取邮箱验证码', smsBtnTitle);
                    }
                }
                var password = $('#' + pwdInputName).prop('value');
                var email = $('#' + emailInputName).prop('value');
                var promise;
                var promise_err = false;
                var countDownLeft = 0;
                if (!me.prop('disabled')) {
                    promise = _this.getEmailCode(password, email, '.emailcode', smsBtnTitle);
                    promise.fail(function() {
                        console.log('promise_err', promise);
                        promise_err = true;
                        //countDownLeft = 0;
                    });
                }
                me.prop('disabled', true);
                $('.emailcode', t).html('<span><span class="count-down">' + timeLeft + '</span>s后重新获取</span>');
                timeInterval = setInterval(function() {
                    var leftSeconds = $('.emailcode .count-down', t).text();
                    if (!leftSeconds.match(/[0-9]/i)) leftSeconds = '0';
                    countDownLeft = parseInt(leftSeconds);
                    countDownLeft--;
                    //console.log('setInterval', leftSeconds, countDownLeft, isReSend, timeInterval);
                    if (countDownLeft <= 0) {
                        clearInterval(timeInterval);
                        me.prop('disabled', false);
                        if (!promise_err) $('.emailcode', t).html(smsBtnTitle);
                        isReSend = true;
                    } else {
                        if (!promise_err) $('.emailcode .count-down', t).text(countDownLeft);
                    }
                }, 1000);

                return false;

            });
        },
        /**
         * [formSerializeToObject 将jquery serialize表单数据转成object对象]
         * @param  {[object]} form [表单对象]
         * @return {[object]}      [返回object对象]
         */
        formSerializeToObject: function(form) {
            var unindexed_array = form.serializeArray();
            var indexed_array = {};
            var getCookie = function(key) {
                var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
                return keyValue ? keyValue[2] : null;
            };
            $.map(unindexed_array, function(n, i) {
                var name = n['name'];
                if (indexed_array.hasOwnProperty(name)) {
                    var current = indexed_array[name];
                    if (typeof indexed_array[name] == 'object') {
                        indexed_array[name].push(n['value'].trim());
                    } else {
                        indexed_array[name] = [];
                        indexed_array[name].push(current);
                        indexed_array[name].push(n['value'].trim());
                    }
                } else {
                    indexed_array[name] = n['value'].trim();
                }
                if (name == 'select_fields' && typeof indexed_array[name] == 'string') {
                    var current = indexed_array[name];
                    indexed_array[name] = [];
                    indexed_array[name].push(current);
                }
                if (!indexed_array.hasOwnProperty('next') && document.location.href.toString().match(/next=([0-9a-z_#&:=%\/\.\-]+)/i)) {
                    var nextUrl = RegExp.$1;
                    indexed_array['next'] = nextUrl;
                }
                //csrf login bug
                if (indexed_array.hasOwnProperty('csrftoken') && indexed_array['csrftoken'] != getCookie('csrftoken')) {
                    indexed_array['csrftoken'] = getCookie('csrftoken');
                }
                if (indexed_array.hasOwnProperty('csrfmiddlewaretoken') && indexed_array['csrfmiddlewaretoken'] != getCookie('csrftoken')) {
                    indexed_array['csrfmiddlewaretoken'] = getCookie('csrftoken');
                }
            });

            return indexed_array;
        },
        isValidEmail: function(eml) {
            return (eml.match(/^[0-9a-z\._\+\-]+@[0-9a-z\._\+\-]+$/i) != null);
        },
        //依赖jq validate插件
        validateFormSubmit: function($form, loginOptions, btnClass, postDataFix, postUrl, cbOk, btnTitle, dataType) {
            var _this = this;
            var dataType = (dataType != undefined && typeof dataType == 'string') ? dataType : 'json';
            var validator = $form.validate(loginOptions);
            $btn = $(btnClass);
            if ($form.valid()) {
                $btn.attr('disabled', 'true');

                var postData = _this.formSerializeToObject($form);
                if (typeof postDataFix == 'function') postData = postDataFix(postData);

                var promise = _this.request('post', postUrl, 'json', function(data) {
                    $btn.removeAttr('disabled');
                    //console.log(data.msg);
                    _this.formErrHandler(data, function(data) {
                        if (typeof cbOk == 'function') cbOk(data);
                    }, null, btnClass, btnTitle);

                }, function(data, status) {
                    _this.btnAlert(btnClass, '系统错误，无法登录。', btnTitle);
                    return false;
                }, postData, dataType);
                return promise;
            }
        },
        modalLine3Col: function(title, name, type, useCode, morePStyle, defaultValue) {
            var type = (type != undefined && typeof type == 'string' && type == 'password') ? 'password' : 'text';
            var useCode = (useCode != undefined && typeof type == 'string') ? useCode : '';
            var morePStyle = (morePStyle != undefined && typeof morePStyle == 'string') ? morePStyle : '';
            var defaultValue = (defaultValue != undefined && typeof defaultValue == 'string') ? defaultValue : '';
            var html = '';
            if (useCode) {
                html += '<p class="tip line ' + morePStyle + '"><span class="line-title line-width-33">' + title + '：</span><span class="line-input line-width-33"><input type="' + type + '" class="' + name + ' dark-border" name="' + name + '" id="' + name + '" value="' + defaultValue + '"></span><span class="line-input line-width-33 ' + useCode + '"></span><span id="' + name + '-title-error" class="line-title line-width-33 invalid" style="display:none;"></span><span id="' + name + '-error" class="line-input line-width-66 invalid" style="display:none;"></span></p>';
            } else {
                html += '<p class="tip line ' + morePStyle + '"><span class="line-title line-width-33">' + title + '：</span><span class="line-input line-width-66"><input type="' + type + '" class="' + name + ' dark-border" name="' + name + '" id="' + name + '" value="' + defaultValue + '"></span><span id="' + name + '-title-error" class="line-title line-width-33 invalid" style="display:none;"></span><span id="' + name + '-error" class="line-input line-width-66 invalid" style="display:none;"></span></p>';
            }
            return html;
        },
        //修改接收邮箱
        chgNotifyEmail: function(isReSend, timeInterval, cbOk) {
            var _this = this;
            var btnTitle = '确认修改';
            var currentEmail = $('.current-email').text();
            if (!_this.isValidEmail(currentEmail)) {
                currentEmail = '';
            }
            var html = '<div class="no-feed-alert">' +
                '<h2><i class="i-warning"></i>修改简历接收邮箱</h2>' +
                _this.modalLine3Col('请输入登录密码', 'login-passwd', 'password', null, 'mg-top-30') +
                _this.modalLine3Col('请输入新的邮箱', 'to-chg-email', 'text', null, null, currentEmail) +
                _this.modalLine3Col('请输入邮箱验证码', 'code-email', 'text', 'use-email-code') +
                '<p class="tip line mg-bottom-30"><span class=" line-width-100">该邮箱仅用于接收简历推荐，不用于登录，您可至“<a class="c42b4e6" href="/users/profile/">个人设置</a>”中修改</span></p>' +
                '<p>' +
                '<a class="btn confirm chg-email-now" href="javascript:void(0);">确认修改</a>' +
                //'<a class="btn cancel closeLayer" href="javascript:void(0);">取消</a>' +
                '</p>' +
                '</div>';

            _this.box(html, '.chg-email-now', function(trg, box) {
                var toChgEmail = trg.parent().parent().find('.to-chg-email').prop('value');
                var codeEmail = trg.parent().parent().find('.code-email').prop('value');
                var loginPasswd = trg.parent().parent().find('.login-passwd').prop('value');

                if ($.trim(loginPasswd) == "") {
                    //_this.btnAlert('.chg-email-now', '请输入登录密码！', btnTitle);
                    _this.labelErr('login-passwd', '请输入登录密码！');
                    trg.parent().parent().find('.login-passwd').focus();
                    return false;
                }

                if (!_this.isValidEmail(toChgEmail)) {
                    //_this.btnAlert('.chg-email-now', '请输入要新的邮箱！', btnTitle);
                    _this.labelErr('to-chg-email', '请输入要新的邮箱！');
                    trg.parent().parent().find('.to-chg-email').focus();
                    return false;
                }

                if ($.trim(codeEmail) == "") {
                    //_this.btnAlert('.chg-email-now', '请输入邮箱验证码！', btnTitle);
                    _this.labelErr('code-email', '请输入邮箱验证码！');
                    trg.parent().parent().find('.code-email').focus();
                    return false;
                }



                $('.chg-email-now').attr('disabled', 'true');

                _this.request('post', '/users/change_notify_email/', 'json', function(data) {
                    //console.log('change_notify_email', data, cbOk);
                    $('.chg-email-now').removeAttr('disabled');
                    if (typeof cbOk == 'function') {
                        cbOk(data);
                    } else {
                        _this.formErrHandler(data, function(data) {
                            box.close();
                            document.location.href = '/users/profile/';
                        }, null, '.chg-email-now', '确认修改');
                    }
                }, function(data, status) {
                    _this.btnAlert('.chg-email-now', '修改接收失败！请重新获取', btnTitle);
                    return false;
                }, {
                    password: loginPasswd,
                    code: codeEmail,
                    email: toChgEmail
                }, 'json');
            }, null, 'login-passwd to-chg-email', isReSend, timeInterval);
        },
        countDown: function(t, url) {
            if ($(t + ' .jumpTo').length) {
                console.log('countDown', $(t + ' .jumpTo').length);
                timeInterval = setInterval(function() {
                    var leftSeconds = $(t + ' .jumpTo').text();
                    if (!leftSeconds.match(/[0-9]/i)) leftSeconds = '0';
                    countDownLeft = parseInt(leftSeconds);
                    countDownLeft--;
                    if (countDownLeft <= 0) {
                        clearInterval(timeInterval);
                        document.location.href = url;
                    } else {
                        $(t + ' .jumpTo').text(countDownLeft);
                    }
                }, 1000);
            }
        },
        chgMobile: function(title, btnTitle, btnClass, isReSend, timeInterval) {
            var _this = this;
            var html = '<div class="no-feed-alert">' +
                '<h2><i class="i-warning"></i>' + title + '</h2><br><br>' +
                _this.modalLine3Col('请输入登录密码', 'login-passwd', 'password') +
                _this.modalLine3Col('请输入新的手机号码', 'new-phone') +
                _this.modalLine3Col('请输入短信验证码', 'code', 'text', 'use-sms-code') +
                '<br>' +

                '<p>' +
                '<a class="btn confirm ' + btnClass + '-now" href="javascript:void(0);">' + btnTitle + '</a>' +
                //'<a class="btn cancel closeLayer" href="javascript:void(0);">取消</a>' +
                '</p>' +
                '</div>';
            _this.box(html, '.' + btnClass + '-now', function(trg, box) {
                var verifyCode = trg.parent().parent().find('.code').prop('value');
                var phoneNumber = trg.parent().parent().find('.new-phone').prop('value');
                var loginPasswd = trg.parent().parent().find('.login-passwd').prop('value');

                if ($.trim(loginPasswd) == "") {
                    //_this.btnAlert('.' + btnClass + '-now', '请输入登录密码！');
                    _this.labelErr('login-passwd', '请输入登录密码！');
                    trg.parent().parent().find('.login-passwd').focus();
                    return false;
                }

                if (!phoneNumber.match(/^1[0-9]{10}$/i)) {
                    //_this.btnAlert('.' + btnClass + '-now', '请输入新的手机号码！');
                    _this.labelErr('new-phone', '请输入新的手机号码！');
                    trg.parent().parent().find('.new-phone').focus();
                    return false;
                }

                if (!verifyCode.match(/^[0-9]{6}$/i)) {
                    //_this.btnAlert('.' + btnClass + '-now', '请输入六位短信验证码！');
                    _this.labelErr('sms-code', '请输入六位短信验证码！');
                    trg.parent().parent().find('.sms-code').focus();
                    return false;
                }
                var smsBtnTitle = $('.sms-code').html();
                $('.' + btnClass + '-now').attr('disabled', 'true');

                //PB.getSmsCode(phoneNumber, '.' + btnClass + '-now', smsBtnTitle, 'ChangeMobile');

                PB.request('post', '/users/change_mobile/', 'json', function(data) {

                    $('.' + btnClass + '-now').removeAttr('disabled');

                    PB.formErrHandler(data, function(data) {
                        console.log('change_mobile', data);
                        box.close();
                        document.location.href = '/users/profile/';
                    }, null, '.' + btnClass + '-now', '确认修改');

                }, function(data, status) {
                    PB.btnAlert('.' + btnClass + '-now', '修改绑定手机失败！请重新获取');
                    return false;
                }, {
                    password: loginPasswd,
                    mobile: phoneNumber,
                    code: verifyCode
                }, 'json');
            }, null, 'new-phone', isReSend, timeInterval, 'ChangeMobile');
        },
        labelErr: function(trgName, msg) {
            if ($('#' + trgName + '-error').length) {
                var msg = (msg != undefined && typeof msg == 'string') ? msg : '';
                if (msg == '') {
                    $('#' + trgName + '-error').text(msg).css('display', 'none');
                    $('#' + trgName + '-title-error').css('display', 'none');
                } else {
                    $('#' + trgName + '-error').text(msg).css('display', 'block');
                    $('#' + trgName + '-title-error').css('display', 'block');
                }
            }
            $('#' + trgName + '').on('blur', function() {
                if ($(this).prop('value').trim() != "") {
                    $('#' + trgName + '-error').text('').css('display', 'none');
                    $('#' + trgName + '-title-error').css('display', 'none');
                }
            });
        },
        //返回弹窗Html
        boxHtml: function(title, info, isConfirm, noTitle, yesTitle, noCss, yesCss, useBtn) {
            var html = '';
            var _useBtn = (useBtn != undefined && typeof useBtn == 'boolean') ? useBtn : true;
            var _isConfirm = (isConfirm != undefined && typeof isConfirm == 'boolean') ? isConfirm : false;
            var _noCss = (noCss != undefined && typeof noCss == 'string') ? noCss : 'u-btn-red';
            var _yesCss = (yesCss != undefined && typeof yesCss == 'string') ? yesCss : 'u-btn-grey-blue';
            html += '<div class="mission-success">' +
                '<h3 class="text-center"><i class="i-ms"></i>' + title + '</h3>' +
                '<p class="text-center">' + info + '</p>' +
                '<p class="mt20 text-center">';
            if (_useBtn && _isConfirm) html += '<a class="btn btn-small button ' + _noCss + ' f-mg-lr-20" href="javascript:void(0);">' + noTitle + '</a>';
            if(_useBtn) html += '<a class="btn btn-small ' + _yesCss + ' f-mg-lr-20" href="javascript:void(0);">' + yesTitle + '</a>';
            html += '</p></div>';
            return html;
        },
        //使用layerout弹窗
        modal: function(html, cbClose, cancelCb, continueCb, noCss, yesCss) {
            var _noCss = (noCss != undefined && typeof noCss == 'string') ? noCss : 'u-btn-red';
            var _yesCss = (yesCss != undefined && typeof yesCss == 'string') ? yesCss : 'u-btn-grey-blue';
            $.LayerOut({
                html: html,
                afterClose: function() {
                    if (typeof cbClose === 'function') cbClose();
                }
            });
            $("." + _noCss).on("click", function(e) {
                //$._LayerOut.close();
                if (typeof cancelCb == 'function') {
                    cancelCb(e);
                }
            });
            $("." + _yesCss).on("click", function(e) {
                //$._LayerOut.close();
                if (typeof continueCb == 'function') {
                    continueCb(e);
                }
            });
        }
    };
}());