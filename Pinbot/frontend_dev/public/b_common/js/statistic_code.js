   var setCookie = function(key, value) {
       var expires = new Date();
       expires.setTime(expires.getTime() + 86400000);
       document.cookie = key + '=' + value + ';expires=' + expires.toUTCString() + ';path=/;';
   }
   var getCookie = function(key) {
       var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
       return keyValue ? keyValue[2] : null;
   }
   var isReSend = false;
   var timeInterval;
   var barObj = {};
   barObj.runningChkId = null;
   barObj.isNoAlert = getCookie('barObj.isNoAlert');

   var barObj2 = {};
   barObj2.runningChkId = null;
   barObj2.isNoAlert = getCookie('barObj2.isNoAlert');
    //console.log('barObj2.isNoAlert',barObj2.isNoAlert);

   var userStatusData = null;
   if (pbDebug == undefined) var pbDebug = false;
   if (typeof jQuery != 'undefined') {

       $(document).ready(function() {

           if ($(window).width() < 1024) {
               if ($('.new-footer').length) $('.new-footer').hide();
           }

           if ($('.fast-menu a.i-weixin-barcode').length == 1) {
               $('.fast-menu a.i-weixin-barcode').hover(function() {
                   $('.fast-menu a.i-weixin-barcode span.bigger').css('display', 'block');
                   /*$( '.fast-menu a.i-weixin-barcode span.bigger' ).fadeIn( 300, function() {

                      });*/
               }, function() {
                   $('.fast-menu a.i-weixin-barcode span.bigger').css('display', 'none');
                   /*$( '.fast-menu a.i-weixin-barcode span.bigger' ).fadeOut( 100, function() {

                      });*/
               });
           }

           var timeStamp = function() {
               return Date.now() / 1000 | 0;
           };
           barObj.lastChkUserTime = getCookie('barObj.chkUser');
           if (barObj.lastChkUserTime === null) {
               barObj.lastChkUserTime = timeStamp();
               setCookie('barObj.chkUser', barObj.lastChkUserTime);
           }
           barObj.startAlert = false;
           barObj.isJustChk = 0;

           barObj2.lastChkUserTime = getCookie('barObj2.chkUser');
           if (barObj2.lastChkUserTime === null) {
               barObj2.lastChkUserTime = timeStamp();
               setCookie('barObj2.chkUser', barObj2.lastChkUserTime);
           }
           barObj2.startAlert = false;
           barObj2.isJustChk = 0;

           //网页提示栏
           var infoBar = function(data, barClass, info, url, cbOk, cbErr, cbClick) {
               if ($('.' + barClass).length == 0) {
                   $('#header').after('<div class="header-bar ' + barClass + '" style="display:none;"></div>');
               }
               var warnInfo = '';
               warnInfo += '<div class="warn-info"><span class="warn-msg">' + info + '</span>';
               if (url != undefined && typeof url == 'string' && url.trim() != "") warnInfo += '<a class="arrow-link" href="' + url + '"></a>';
               warnInfo += '</div>';
               warnInfo += '<div class="warn-info-close"><a title="关闭提示" href="javascript:void(0);"></a></div>';
               $('.' + barClass).html(warnInfo);
               if (data.status != undefined && data.status == 'ok') {
                   if (typeof cbOk == 'function') cbOk(data);
               } else {
                   if (typeof cbErr == 'function') cbErr(data);
               }
               $("." + barClass + " .warn-info-close").undelegate("a").delegate("a", "click", function(e) {
                   $('.' + barClass).slideUp("100", function() {
                       if (typeof cbClick == 'function') cbClick();
                   });
               });
           };
           //检查是否是聘宝会员
           var warningBar = function(data) {

               infoBar(data, 'header-warning-bar', '您还不是聘宝会员，点击这里<a href="/vip/role_info/">开通会员</a>', '/vip/role_info/', function(data) {
                   userStatusData = data;
                   if (data.user_type == 'manual') {
                       //如果是省心型
                       barObj.isNoAlert = 1;
                       setCookie('barObj.isNoAlert', barObj.isNoAlert);
                       barObj.lastChkUserTime = timeStamp();
                       setCookie('barObj.chkUser', barObj.lastChkUserTime);
                   } else {
                       if (data.user_type == 'experience') {
                           //非会员
                           $('.header-warning-bar').slideDown("500", function() {
                               barObj.startAlert = true;
                               //barObj.lastChkUserTime=timeStamp();
                           });
                           barObj.lastChkUserTime = timeStamp();
                           setCookie('barObj.chkUser', barObj.lastChkUserTime);
                       } else {
                           barObj.isNoAlert = 1;
                           setCookie('barObj.isNoAlert', barObj.isNoAlert);
                           if (data.is_expired == true) {
                               //已过期
                               //document.location.href='/vip/user_expired/';
                               $('.header-warning-bar').css('display', 'none');
                           } else {
                               $('.header-warning-bar').css('display', 'none');
                           }
                           barObj.lastChkUserTime = timeStamp();
                           setCookie('barObj.chkUser', barObj.lastChkUserTime);
                       }
                   }
               }, function(data) {
                   barObj.lastChkUserTime = timeStamp();
                   setCookie('barObj.chkUser', barObj.lastChkUserTime);
                   barObj.startAlert = true;
                   barObj.isNoAlert = 1;
                   setCookie('barObj.isNoAlert', barObj.isNoAlert);
                   //alertUpgrade(data.pinbot_point);
                   //$.alert('<p class="alert-notice">获取用户状态失败，请刷新再试！</p>');
                   //throw new Error('无效用户状态! ['+data.toString()+']');
               }, function() {
                   barObj.startAlert = false;
                   barObj.lastChkUserTime = timeStamp();
                   setCookie('barObj.chkUser', barObj.lastChkUserTime);
                   barObj.isNoAlert = 1;
                   setCookie('barObj.isNoAlert', barObj.isNoAlert);
               });
           };

           //检查是否绑定接收邮箱
           var warningBarForEmail = function(data) {

               infoBar(data, 'header-warning-email-bar', '请验证并绑定接收通知邮箱 <span class="current-email" style="color:#f46c62;">' + data.notify_email + '</span> | <a href="/users/bind_notify_email/" class="">修改邮箱</a>', '/users/bind_notify_email/', function(data) {
                   //未绑定
                   if (data.is_bind != true) {
                       //非会员
                       $('.header-warning-email-bar').slideDown("500", function() {
                           barObj2.startAlert = true;
                           barObj2.lastChkUserTime = timeStamp();
                       });
                       barObj2.lastChkUserTime = timeStamp();
                       setCookie('barObj2.chkUser', barObj2.lastChkUserTime);
                   } else {
                       barObj2.startAlert = false;
                       barObj2.lastChkUserTime = timeStamp();
                       barObj2.isNoAlert = 1;
                       setCookie('barObj2.chkUser', barObj2.lastChkUserTime);
                       setCookie('barObj2.isNoAlert', barObj2.isNoAlert);
                   }

                   $('.header-bar').undelegate('.chg-notify-email').delegate('.chg-notify-email', 'click', function() {
                       //如果是新版LayerOut
                       if ($.LayerOut.prototype.version.match(/^1\./i)) {
                           $.getScript('/static/b_common/js/pb.js', function() {
                               PB.chgNotifyEmail(isReSend, timeInterval);
                           });
                       }
                   });

               }, function(data) {
                   barObj2.lastChkUserTime = timeStamp();
                   setCookie('barObj2.chkUser', barObj2.lastChkUserTime);
                   barObj2.startAlert = true;
                   barObj2.isNoAlert = 1;
                   setCookie('barObj2.isNoAlert', barObj2.isNoAlert);
                   //alertUpgrade(data.pinbot_point);
                   //$.alert('<p class="alert-notice">获取用户状态失败，请刷新再试！</p>');
                   //throw new Error('无效用户状态! ['+data.toString()+']');
               }, function() {
                   barObj2.startAlert = false;
                   barObj2.lastChkUserTime = timeStamp();
                   setCookie('barObj2.chkUser', barObj2.lastChkUserTime);
                   barObj2.isNoAlert = 1;
                   setCookie('barObj2.isNoAlert', barObj2.isNoAlert);
               });
           };

           var isSending = false;
           var isSending2 = false;

           var chkBar = function(lastChkUserTime) {
               var currentTime = timeStamp();
               //每600秒检查一次
               var timeConsume = parseInt(currentTime) - parseInt(lastChkUserTime);
               //console.log('t',timeConsume);

               var threshold = 300;
               var chkApi = function() {
                   isSending2 = true;
                   $.ajax({
                       type: 'get',
                       url: '/vip/get_user_info/',
                       success: function(data) {
                           isSending2 = false;
                           //lastChkUserTime=timeStamp();
                           warningBar(data);
                           /*setTimeout(function(){
                                chkBar(lastChkUserTime);
                            },1000)*/
                       },
                       error: function() {
                           isSending2 = false;
                           lastChkUserTime = timeStamp();
                           setCookie('barObj.chkUser', lastChkUserTime);

                           barObj.startAlert = true;
                           barObj.isNoAlert = 1;
                           //throw new Error('获取用户状态失败! ');
                           //$.alert('<p class="alert-notice">获取用户状态失败，请刷新再试！</p>');
                       }
                   });
               };
               if ($('#header').length && $('.main-user-control').length && parseInt(timeConsume) > threshold) {
                   if (barObj.isJustChk == 0 || barObj.isJustChk >= 10) {
                       barObj.isJustChk++;
                       if (barObj.isJustChk > 10) barObj.isJustChk = 0;
                       chkApi();
                   } else {
                       barObj.isJustChk++;
                   }
               } else {
                   //if(pbDebug && timeConsume%10==0) console.log('oops',timeConsume);
               }
           };

           var chkEmailBar = function(lastChkUserTime) {
               var currentTime = timeStamp();
               //每600秒检查一次
               var timeConsume = parseInt(currentTime) - parseInt(lastChkUserTime);
               //console.log('t',timeConsume);

               var threshold = 400;
               var chkApi = function() {
                   isSending = true;
                   $.ajax({
                       type: 'get',
                       url: '/users/notify_email_is_bind/',
                       success: function(data) {
                           isSending = false;
                           //console.log('notify_email_is_bind',data);
                           warningBarForEmail(data);
                       },
                       error: function() {
                           isSending = false;
                           lastChkUserTime = timeStamp();
                           setCookie('barObj2.chkUser', lastChkUserTime);

                           barObj2.startAlert = false;
                           barObj2.isNoAlert = 1;
                           setCookie('barObj2.isNoAlert', barObj2.isNoAlert);

                       }
                   });
               };
               if ($('#header').length && $('.main-user-control').length && parseInt(timeConsume) > threshold) {
                   if (barObj2.isJustChk == 0 || barObj2.isJustChk >= 10) {
                       barObj2.isJustChk++;
                       if (barObj2.isJustChk > threshold) barObj2.isJustChk = 0;
                       if (!isSending) chkApi();
                   } else {
                       barObj2.isJustChk++;
                   }
               } else {
                   //if(pbDebug && timeConsume%10==0) console.log('oops eml',timeConsume);
               }
           };

           if (parseInt(barObj.isNoAlert) == 1) {
               if (barObj.runningChkId != null) clearInterval(barObj.runningChkId);
           } else {
               barObj.runningChkId = setInterval(function() {
                   if (barObj.startAlert == false) chkBar(barObj.lastChkUserTime);
               }, 1000);
           }

           if (parseInt(barObj2.isNoAlert) == 1) {
               if (barObj2.runningChkId != null) clearInterval(barObj2.runningChkId);
           } else {
               barObj2.runningChkId = setInterval(function() {
                   if (barObj2.startAlert == false) chkEmailBar(barObj2.lastChkUserTime);
               }, 1000);
           }

           //bd trace: .bd-trace + id + .trace-title
           setTimeout(function() {
               if (!is_staff && $('.bd-trace').length) {
                   $('.bd-trace').each(function(i) {
                       if ($(this).attr('id') != null && typeof $(this).attr('id') == 'string' && $(this).attr('trace-title') != null && typeof $(this).attr('trace-title') == 'string') {
                           $(this).click(function(e) {
                               _hmt.push(['_trackEvent', $(this).attr('id'), 'click', $(this).attr('trace-title')]);
                               /*var url = '/dash/ui_check/?ui_check=' + $(this).attr('trace-title').trim();
                               $.get(url, function(res) {}, 'json').fail(function() {

                               });*/
                           });
                       }
                   });
               }
           }, 400);

       });

   } else {
       //console.log('undefined');
   }

    //继续购买链接
    //console.log('continue-buy-link',$('.continue-buy-link').length , userStatusData);
    if ($('.continue-buy-link').length && userStatusData != null) {
       if (userStatusData.can_update) {
           $('.continue-buy-link').attr('href', '/vip/role_info/#/usermode_diy/');
           $('.continue-buy-link').html('继续购买自助套餐');
       } else {
           $('.continue-buy-link').attr('href', '/vip/role_info/#/usermode_noworry/');
           $('.continue-buy-link').html('继续购买省心套餐');
       }
   }