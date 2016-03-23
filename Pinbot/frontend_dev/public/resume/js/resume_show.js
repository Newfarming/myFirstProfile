(function(argument) {

    var app = angular.module('app.resume_show', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter']),
        $django = angular.injector(['app.django']),
        $funcs = angular.injector(['app.utils']),
        tmpl = $django.get('tmpl'),
        static_url = $django.get('static_url');

    app.config([
        '$interpolateProvider',
        function($interpolateProvider) {
            $interpolateProvider.startSymbol('{-');
            $interpolateProvider.endSymbol('-}');
        }
    ]);

    app.factory('$', [
        '$window',
        function($window) {
            return $window.jQuery.noConflict();
        }
    ]);

    var pbLib = $funcs.get('pbLib');
    var confirmBox = $funcs.get('confirmBox');
    var confirmBoxRed = $funcs.get('confirmBoxRed');
    var alertBox = $funcs.get('alertBox');
    var getModeData = $funcs.get('getModeData');
    var postModeData = $funcs.get('postModeData');
    var inArray = $funcs.get('inArray');
    var pbFunc = $funcs.get('pbFunc');

    app.config([
        '$stateProvider', '$urlRouterProvider',
        function($stateProvider, $urlRouterProvider) {
            var otherwiseUrl = '/';
            $urlRouterProvider.otherwise(otherwiseUrl);
            $stateProvider.state(
                'default', {
                    url: '/',
                    template: '', //tmpl('resume/feed_resume.html'),
                    controller: 'resumeDetail'
                }
            );
        }
    ]);

    //pbFunc.simpleAlert('简单alert弹窗', '未发送企业名片直接下载');

    //获取当前页IDs
    var getResumeFeedIdKws = function() {
        var trg = angular.element(document.getElementById('main'));
        //console.log('getResumeFeedIdKws',trg[0]);
        if (trg.attr('data-resumeid') != "") {
            return [trg.attr('data-resumeid'), trg.attr('data-feed_id'), trg.attr('date-feed_keywords'), trg.attr('data-is_fav'), trg.attr('data-mark_logs')];
        } else {
            return null;
        }
    }

    app.controller(
        'resumeDetail', ['$rootScope', '$scope', '$http', '$state',
            function($rootScope, $scope, $http, $state) {

                $scope.saveResume = function($event) {
                    var html = $('#JS_download_local').html();
                    var ckPrefix = 'downloadCk_';
                    $.LayerOut({
                        html: html,
                        dialogCss: 'width:660px;'
                    });

                        if (pbLib.getCookie(ckPrefix + 'name') == 1) {
                            $('#candidate-name').attr("checked",'true');
                        }
                        if (pbLib.getCookie(ckPrefix + 'contact_info') == 1) {
                            $('#candidate-contact').attr("checked",'true');
                        }
                        if (pbLib.getCookie(ckPrefix + 'salary') == 1) {
                            $('#candidate-money').attr("checked",'true');
                        }


                    $('.modal-body').on('click', function() {
                        var pdf = $('.js-pdf'),
                            html = $('.js-html'),
                            hrefpdf = pdf.attr('xhref'),
                            hrefhtml = html.attr('xhref');
                        var content = $('form.js-download-list').serialize();
                        hrefpdf += '?' + content;
                        hrefhtml += '?' + content;
                        $('.js-pdf').attr('href', hrefpdf);
                        $('.js-html').attr('href', hrefhtml);
                    });
                    $('.download-list').on('click', function() {
                        var timeLapse = 365;

                        if ($('#candidate-name').is(':checked')) {
                            pbLib.setCookie(ckPrefix + 'name', 1, timeLapse * 86400000);
                        } else {
                            pbLib.setCookie(ckPrefix + 'name', 0, timeLapse * 86400000);
                        }
                        if ($('#candidate-contact').is(':checked')) {
                            pbLib.setCookie(ckPrefix + 'contact_info', 1, timeLapse * 86400000);
                        } else {
                            pbLib.setCookie(ckPrefix + 'contact_info', 0, timeLapse * 86400000);
                        }
                        if ($('#candidate-money').is(':checked')) {
                            pbLib.setCookie(ckPrefix + 'salary', 1, timeLapse * 86400000);
                        } else {
                            pbLib.setCookie(ckPrefix + 'salary', 0, timeLapse * 86400000);
                        }

                    });


                };

                $scope.shrinkToggle = function($event) {
                    var btn = angular.element($event.currentTarget);
                    if (btn.hasClass('btn-toggle-span')) {
                        btn.removeClass('btn-toggle-span');
                        btn.parents('.sec-resume').find('dl').show();
                    } else {
                        btn.addClass('btn-toggle-span');
                        btn.parents('.sec-resume').find('dl').hide();
                    }
                };

                $scope.showHoverTip = function(event) {
                    var cls = event.currentTarget.getAttribute('class');
                    if (cls.match(/i\-(fav|delete|download)\-([0-9a-z]+)/i)) {
                        var trg = RegExp.$1;
                        var baseLen = new String('收藏该候选人').length;
                        var trgId = '.i-' + trg + '-delete-hover-' + RegExp.$2;
                        var trgNoticeId = '.i-' + trg + '-delete-notice-' + RegExp.$2;
                        if (trg == 'download') trgNoticeId = '.i-' + trg + '-delete-hover-' + RegExp.$2;
                        if (trg != 'fav') {
                            //计算新宽度
                            var newWidth = parseInt(72 * ($(trgId).text().length / baseLen));
                            var newWidth2 = parseInt(72 * ($(trgNoticeId).text().length / baseLen));
                            $(trgId).css('width', newWidth + 'px');
                            $(trgNoticeId).css('width', (newWidth2 + 10) + 'px');
                            var downloadTipRight = 51;
                            if (trg == 'download') {
                                $(trgNoticeId).css('right', (downloadTipRight - 50) + 'px');
                            } else {
                                $(trgNoticeId).css('right', downloadTipRight + 'px');
                            }
                        } else {
                            $(trgId).css('width', '72px');
                        }
                        $(trgId).show();
                    }
                };
                //hover hide
                $scope.hideHoverTip = function(event) {
                    var cls = event.currentTarget.getAttribute('class');
                    if (cls.match(/i\-(fav|delete|download)\-([0-9a-z]+)/i)) {
                        var trg = RegExp.$1;
                        var trgId = '.i-' + trg + '-delete-hover-' + RegExp.$2;
                        $(trgId).hide();
                    }
                };

            }
        ]
    );

    app.controller(
        'resumeAside', ['$rootScope', '$scope', '$http', '$state', '$window', '$timeout',
            function($rootScope, $scope, $http, $state, $window, $timeout) {

                var responseMsga = {
                    8: '<span class="text-center f16">恭喜，简历购买成功！</span>',
                    9: '<span class="text-center f16">聘宝正在为您准备简历</span>',
                    1: '<span class="text-center f16">请先购买简历套餐，便能购买您喜欢的简历了。</span>',
                    2: '<span class="text-center f16">您已购买过此简历，请到简历中心查查看！</span>',
                    3: '<span class="text-center f16">抱歉，您的点数不足，请先购买点数！</span>',
                    4: '<span class="text-center f16">抱歉，操作失败了，请刷新重试一下？</span>'
                };

                $scope.isPrepareResume = true;
                $scope.showBtnTip = false;

                //收藏简历
                $scope.isFav = false;
                var ids = getResumeFeedIdKws();
                $scope.pageData = {};
                $scope.pageData['resume_id'] = '';
                $scope.pageData['feed_id'] = '';
                $scope.pageData['feed_keywords'] = [];
                $scope.logs = [];
                if (ids) {
                    $scope.pageData['resume_id'] = ids[0];
                    $scope.pageData['feed_id'] = ids[1];
                    $scope.pageData['feed_keywords'] = angular.fromJson(ids[2]);
                    $scope.isFav = (ids[3] == '1') ? true : false;
                    $scope.logs = angular.fromJson(ids[4]);
                }

                $scope.isShowFavAlert = false;
                $scope.doNotShowFavAlert = (pbLib.getCookie('do-not-show-fav-alert') == null) ? false : true;

                var sendCardCookieName = 'isSendCompanyCard' + $scope.pageData['resume_id'];
                $scope.isGetMousePos = false;
                $scope.btnReadyTop = 0;

                //用户聘点数
                $scope.user_data = {};
                //如果聘点数小于十，需要弹窗提示
                $scope.pinbot_point_limit = 10;

                var findElemPos = function(id) {
                    var node = document.getElementById(id);
                    var curtop = 0;
                    var curtopscroll = 0;
                    if (node.offsetParent) {
                        do {
                            curtop += node.offsetTop;
                            curtopscroll += node.offsetParent ? node.offsetParent.scrollTop : 0;
                        } while (node = node.offsetParent);
                        if (curtop - curtopscroll >= 0) $scope.btnReadyTop = curtop - curtopscroll;
                    }
                    //console.log('findElemPos', $scope.btnReadyTop);
                };
                $scope.showTooltips = function($event) {
                    findElemPos('btn-under-ready');
                    $event.stopPropagation();
                    $scope.showBtnTip = true;
                    var isDirectDown = false;
                    var tips = angular.element(document.getElementsByClassName('pb-tips'));
                    tips.css('top', ($scope.btnReadyTop + 40) + 'px');
                    tips.css('display', 'none');
                    if (tips.css('display') != 'block') {
                        tips.css('left', $event.pageX);
                        tips.css('display', 'block');
                    }
                };
                $scope.hideTooltips = function($event) {
                    var tips = angular.element(document.getElementsByClassName('pb-tips'));
                    tips.css('display', 'none');
                };
                $scope.moveTooltips = function($event) {
                    $event.stopPropagation();
                    if ($scope.showBtnTip) {
                        var tips = angular.element(document.getElementsByClassName('pb-tips'));
                        //console.log('currentTop', $event.pageX, $event.pageY);
                        if (!$scope.isGetMousePos) {
                            setTimeout(function() {
                                tips.css('top', $event.pageY);
                                tips.css('left', $event.pageX);
                                $scope.isGetMousePos = true;
                            }, 50);
                        } else {
                            setTimeout(function() {
                                //tips.css('top', $event.pageY);
                                tips.css('left', $event.pageX);
                                $scope.isGetMousePos = true;
                            }, 50);
                        }
                    }
                };

                //未发送企业名片直接下载
                $scope.directDownload = function($event) {
                    //Popup.pending();
                    var $this = angular.element($event.currentTarget);
                    var payTimer = null;
                    var data = {
                            feed_id: $this.attr('data-feed_id'),
                            resume_id: $this.attr('data-resumeid'),
                            sendid: $this.attr('data-sendid'),
                            job_id: $this.attr('data-job_id')
                        },
                        msg = responseMsga;
                    if ($this.attr('disabled')) return false;
                    $this.attr('disabled', true);
                    $scope.isPrepareResume = true;
                    var req = getModeData($http,
                        '/transaction/buy?' + pbFunc.urlString(data),
                        "",
                        function(ret) {
                            $this.attr('disabled', false);
                            if (payTimer) {
                                clearTimeout(payTimer);
                            };
                            if (ret && ret.status) {
                                if (ret.status == false) {
                                    pbFunc.simpleAlert(msg[ret.data], '', function() {
                                        location.reload();
                                    });
                                } else {
                                    if (ret.data == 8 || ret.data == 9) {
                                        /*$.alert(msg[ret.data], function() {
                                            location.reload();
                                        });*/
                                        if (ret.data == 9) {
                                            $scope.isPrepareResume = true;
                                            pbFunc.simpleAlert('聘宝正在为您准备简历', '<div class="text-center mt30"><span class="mt20 block f13 c607d8b">小宝提示：请稍后刷新页面，并在简历中心查收简历！</span></div>', function(trg, args) {

                                            }, null, '确定', true);
                                        } else {
                                            pbFunc.simpleAlert(msg[ret.data], '', function() {
                                                location.reload();
                                            });
                                        }
                                    }
                                }
                            } else {
                                if (/^[1234]$/.test(ret.data)) {
                                    //$.alert(msg[ret.data]);
                                    pbFunc.simpleAlert(msg[ret.data], '');
                                };
                            };
                        }, undefined, function(err) {
                            req.abort();
                            //$.alert(msg[4]);
                            pbFunc.simpleAlert(msg[4], '');
                        }, true);

                    payTimer = setTimeout(function() {
                        req.abort();
                        //$.alert(msg[4]);
                        pbFunc.simpleAlert(msg[4], '');
                    }, 20000);
                };

                var alertUpgrade = function(point, userType, title) {
                    var more = '';
                    var btnTitle = '';
                    if (userType == 'experience') {
                        more = '升级成为聘宝会员';
                        btnTitle = '升级聘宝会员';
                    } else if (userType == null || userType == undefined) {
                        more = '';
                        btnTitle = '';
                    } else {
                        more = '<a href="/payment/point_recharge/" class="c63c2ec">购买聘点</a>';
                        btnTitle = '购买聘点';
                    }
                    $.LayerOut({
                        html: pbFunc.alertModal(
                            '<span class="pay-alert"></span><span class="pay-title">' + title + '失败，您的聘点不足！</span>',
                            '',
                            '您的聘点数量：<span class="cf46c62">' + point + '</span>个，请' + more + '，<br><br><a href="javascript:void(0);"  id="JS_service_btn_modal" class="c63c2ec">有疑问请联系我们</a>',
                            btnTitle,
                            null
                        ),
                        afterClose: function() {
                            //$._LayerOut.close();
                        }
                    });
                    $(".modal").undelegate(".btn-click-ok").delegate(".btn-click-ok", "click", function(e) {
                        $._LayerOut.close();
                        document.location.href = '/vip/role_info/';
                    });
                    pbFunc.openQQ('JS_service_btn_modal');
                };

                var isHasCompanyInfo = function(callback) {
                    /*console.log('$scope.user_data', $scope.user_data);*/
                    var url = '/companycard/get/json/?' + Math.random();
                    getModeData($http,
                        url,
                        "",
                        function(res) {
                            if (res.data && res.data == '3') {
                                //点数不足
                                getModeData($http,
                                    '/vip/get_user_info/',
                                    "",
                                    function(data) {
                                        if (data.status != undefined && data.status == 'ok') {
                                            $scope.user_data = data;
                                            if (parseInt(data.pinbot_point) < $scope.pinbot_point_limit) {
                                                alertUpgrade(data.pinbot_point, data.user_type, '查看联系方式');
                                            }
                                        } else {
                                            alertUpgrade(0, null, '查看联系方式');
                                        }
                                    }, false, undefined, undefined, {
                                        /*pinbot_point: 2,
                                        self_pinbot_point: 600,
                                        status: "ok",
                                        user_status: "自助套餐A",
                                        user_type: "self"*/
                                    });
                            } else {
                                if (res && res.jobs) $window.infos = res;
                                if (typeof callback == 'function') {
                                    callback(res);
                                }
                            }
                        }, false, undefined, undefined, {
                            /*data: 3,
                            error: "3.点数不够",
                            status: false*/
                        });
                };
                var hasCompanyCard = function() {
                    var html = $('#JS_has_card_html').html();
                    $.LayerOut({
                        html: html,
                        dialogCss: 'width:540px;'
                    });
                    $(document).on('click', '#JS_send_card_btn', chooseCard);
                    $(".modal").undelegate(".JS_buy_not_sendcard").delegate(".JS_buy_not_sendcard", "click", function(e) {
                        $scope.directDownload(e);
                    });
                };
                var chooseCard = function() {
                    var notHasCard = function() {
                        var html = $('#JS_no_card').html();
                        $.LayerOut({
                            html: html,
                            dialogCss: 'width:540px;'
                        });
                        $(".modal").undelegate(".JS_buy_not_sendcard").delegate(".JS_buy_not_sendcard", "click", function(e) {
                            $scope.directDownload(e);
                        });
                    };
                    var html = $('#JS_choose_cards').html(),
                        jobs = ($window.infos && $window.infos.jobs) || [],
                        width = 925;

                    //把jobs转成数组
                    jobs = pbFunc.objToArr(jobs);
                    if (!jobs.length) {
                        notHasCard();
                        return;
                    };

                    if (jobs.length == 1) {
                        width = 490;
                    };

                    $.LayerOut({
                        html: html,
                        closeByShadow: false,
                        dialogCss: 'width:' + width + 'px; height:610px;'
                    });

                    $.intentionCard({
                        list: jobs,
                        allowSend: true,
                        contentDom: '#JS_jobs_ajax_content',
                        callback: cardScroll
                    });
                };

                var handleCompanyInfo = function(res) {
                    var markResume = function() {
                        var html = $('#JS_to_mark').html();
                        $.LayerOut({
                            html: html,
                            closeByShadow: false,
                            dialogCss: 'height:250px;'
                        });
                    };
                    if (res && res.status) {
                        if (res.has_mark) {
                            markResume();
                            return;
                        };

                        /*var html = $('#JS_has_card_html').html();
                        $.LayerOut({
                            html: html,
                            dialogCss: 'width:540px;'
                        });
                        //选择需要发送的企业名片
                        $( document ).on( 'click' , '#JS_send_card_btn' , chooseCard );*/
                        chooseCard();
                    } else if (res && res.data) {
                        //购买成功
                        if (res.data == 8) {
                            $('#js-nav-meet').addClass('nav-red');
                            $('#js-nav-qusetion').removeClass('nav-blue');
                            $('#js-faq-click').addClass('faq-robot-meet').removeClass('faq-robot-qusetion').find('span').text('约面话术');
                            $('#js-meet-content').show();
                            $('#js-qusetion-content').hide();
                        }
                        pbFunc.simpleAlert(msg[res.data], '');
                    } else {
                        pbFunc.simpleAlert('请求失败，请刷新重试！', '');
                    }
                };

                //发送企业名片
                $scope.isSendCompanyCard = (pbLib.getCookie(sendCardCookieName) == null) ? false : true;
                $scope.sendCompanyCard = function($event) {

                    var sendCard = function(data) {
                        $scope.isSendCompanyCard = (pbLib.getCookie(sendCardCookieName) == null) ? false : true;
                        if ($scope.isSendCompanyCard) {
                            pbFunc.simpleConfirm('需要您的确认', '<p class="mt30 f14 c607d8b">您已发送了企业名片进行意向确认，还要再直接获取该简历联系方式吗？</p><p class="mt50 cf46c62 f13">小宝提示：确认会在已扣3个聘点的基础上再扣除您10个聘点</p>', function(args) {
                                $._LayerOut.close();
                            }, null, '取消', true, '确认', function(args) {
                                isHasCompanyInfo(hasCompanyCard);
                            });
                        } else {
                            isHasCompanyInfo(function(res) {
                                handleCompanyInfo(res);
                            });
                        }
                    };

                    //检查是否是聘宝会员
                    getModeData($http,
                        '/vip/get_user_info/',
                        "",
                        function(data) {
                            if (data.status != undefined && data.status == 'ok') {
                                $scope.user_data = data;
                                if (parseInt(data.pinbot_point) < $scope.pinbot_point_limit) {
                                    alertUpgrade(data.pinbot_point, data.user_type, '发送企业名片');
                                } else {
                                    sendCard(data);
                                }
                            } else {
                                alertUpgrade(0, null, '发送企业名片');
                            }
                        });

                };

                var toggleFav = function($event) {
                    var trg = angular.element($event.currentTarget);
                    var t = ($scope.isFav == false) ? 'add_watch' : 'remove_watch';
                    if ($scope.pageData['resume_id'] != '') {
                        var req = getModeData($http,
                            '/resumes/' + t + '/' + $scope.pageData['resume_id'] + '?' + pbFunc.urlString({
                                feed_id: $scope.pageData['feed_id'],
                                feed_keywords: angular.fromJson($scope.pageData['feed_keywords']).join(' ')
                            }),
                            "",
                            function(data) {
                                if (t == 'add_watch') {
                                    if (!$scope.isShowFavAlert && !$scope.doNotShowFavAlert) {
                                        var feed_title = $('#main').attr('data-feed_title');
                                        pbFunc.simpleAlert('简历收藏成功！', '<div class="text-center"><span class="big-icon big-icon-rocket mt20"></span><span class="mt20 block f14 c607d8b">多多收藏喜欢的人才，我们将为你推荐更多匹配<span class="c434343"> ' + feed_title + ' </span>职位的人才～</span><div class="mt20"><input type="checkbox" name="do-not-show-fav-alert" id="do-not-show-fav-alert"  value="1" class=""> <label for="do-not-show-fav-alert"><span class="f14 cf46c62">不再提醒</span></label></div></div>', function(trg, args) {
                                            if ($('#do-not-show-fav-alert').is(':checked')) {
                                                var timeLapse = 365;
                                                pbLib.setCookie('do-not-show-fav-alert', 1, timeLapse * 86400000);
                                                $scope.doNotShowFavAlert = true;
                                            }
                                        }, null, '我知道了', false);
                                    }
                                    $scope.isFav = true;
                                    trg.find('span').text('取消收藏');
                                    $scope.isShowFavAlert = true;
                                } else {
                                    $scope.isFav = false;
                                    trg.find('span').text('收藏简历');
                                }
                            }, undefined, function(err) {

                            });
                    }
                };
                $scope.favResume = function($event) {
                    toggleFav($event);
                };
                $scope.favCancelResume = function($event) {
                    toggleFav($event);
                };

                //转发简历
                $scope.forwardResume = function($event) {
                    var copyUrl = 'http://www.pinbot.me/resumes/display/' + $scope.pageData['resume_id'] + '/?feed_id=' + $scope.pageData['feed_id'];
                    $.LayerOut({
                        html: pbFunc.alertModal(
                            '<span class="pay-alert"></span><span class="pay-title">请复制以下简历链接并发送给其他同事</span>',
                            '',
                            '<a class="c607d8b" href="' + copyUrl + '" target="_blank">' + copyUrl + '</a>',
                            '复制',
                            null, ''
                        ),
                        afterClose: function() {
                            //$._LayerOut.close();
                        }
                    });
                    $(".modal").undelegate(".btn-click-ok").delegate(".btn-click-ok", "click", function(e) {
                        $._LayerOut.close();
                        var client = new ZeroClipboard($('.resume-meta-tip'));
                        $('.resume-meta-tip')[0].click();
                    });
                };

                //举报
                $scope.reportResume = function($event) {
                    $('.modal-backdrop-tip-toreport,.modal-tip-toreport').show();
                    $('.modal-dialog-tip-toreport').css({
                        marginTop: ($(window).height() - $('.modal-dialog-tip-toreport').height()) / 2 + 'px'
                    });
                    $('.JS_close_tip').on('click', function() {
                        $('.modal-backdrop-tip-toreport,.modal-tip-toreport').hide();
                    });
                };
                $(document).on('click', '.m-radio', function() {
                    var $this = $(this),
                        name = $this.attr('data-name'),
                        hasInfo = $this.attr('has-info')
                    checkbox = $this.find('input'),
                    checked = checkbox.prop('checked'),
                    $submitToReport = $('#JS_submit_toreport'),
                    $feedbackInfo = $('#JS_feedback_info');

                    $this.toggleClass('active');
                    $('.m-radio[data-name="' + name + '"]').not($this).removeClass('active').find('input').prop('checked', false);
                    checkbox.prop('checked', !checked);

                    if (name == 'code_name') {
                        if ($('input[name="code_name"]:checked').length) {
                            $('#JS_submit_btn').attr('disabled', false);
                        } else {
                            $('#JS_submit_btn').attr('disabled', true);
                        };
                    };

                    if (name == 'back_count') {
                        if (hasInfo === undefined) {
                            $feedbackInfo.hide();
                            if ($('input[name="back_count"]:checked').length) {
                                $submitToReport.attr('disabled', false);
                            } else {
                                $submitToReport.attr('disabled', true);
                            };
                        } else {
                            $feedbackInfo.toggle().find('input').focus();
                            $submitToReport.attr('disabled', true);
                        }
                    };

                });
                $(document).on('keyup', '#JS_feedback_value', function() {
                    var $this = $(this),
                        value = $this.val(),
                        $submitToReport = $('#JS_submit_toreport');
                    value === '' ? $submitToReport.attr('disabled', true) : $submitToReport.attr('disabled', false);
                });
                $(document).on('click', '#JS_submit_btn', function() {
                    var that = this;
                    if ($(this).attr('disabled')) return false;
                    var txt = $('input[name="code_name"]:checked').parent().text();
                    if (!txt) return false;
                    $.confirm('<p style="font-size:20px;color:#434343;text-align:center"><i class="i-l-notice"></i>您选择的状态是: <span style="color:#3ab2e7;">' + txt + '</span></p><p style="margin-top:50px;color:#f23748;font-size:14px;text-align:center;">注：请确认提交，提交后不能修改</p>', function() {
                        $.commonAjax.call(that);
                    });

                });
                $(document).on('click', '#JS_submit_toreport', function() {
                    var saveCallback = function(res) {
                        $('#JS_submit_toreport').attr('disabled', false);
                        if (res && (res.status == 'ok' || res.status == 'success')) {
                            var url = $('#JS_header').attr('data-url');
                            if (url) {
                                location.href = url;
                            } else {
                                location.reload();
                            };
                        } else {
                            if (res && res.msg) {
                                //$.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + res.msg + '</p>');
                                pbFunc.simpleAlert(res.msg, '');
                            } else {
                                //$.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请求失败了，刷新再试一下吧！</p>');
                                pbFunc.simpleAlert('请求失败了，刷新再试一下吧！', '');
                            };
                        };
                    };
                    var $this = $(this),
                        id = $this.attr('data-id'),
                        back_id = $('input[name="back_count"]:checked').val(),
                        feedback_value = $('input[name="feedback_value"]').val();
                    if ($(this).attr('disabled')) return false;
                    if (!id || !back_id) return;
                    $('#JS_submit_toreport').attr('disabled', true);
                    $.post('/taocv/add_feedback/', {
                        feedback_id: back_id,
                        resume_id: id,
                        feedback_value: feedback_value,
                        ___: new Date().getTime()
                    }, function(res) {
                        saveCallback(res);
                    }, 'json');

                });
                $(document).on('click', '#JS_goto_detail', function() {
                    var newWin = window.open();
                    newWin.opener = null;
                    newWin.open('', '_self', '');
                    newWin.location = $(this).attr('data-url');
                });

                //不感兴趣简历
                $scope.isDel = ($('#main').attr('data-is_del').match(/true/i)) ? true : false;
                //是否提示推荐不准弹窗
                $scope.isShowDisLikeAlert = false;
                $scope.doNotShowDisLikeAlert = (pbLib.getCookie('do-not-show-dislike-alert') == null) ? false : true;
                var toggleDislike = function($event, t) {
                    ////标记为删除 -150 恢复 150
                    var t = (t && t == 1) ? '-150' : '150';
                    if ($scope.pageData['resume_id'] != '') {
                        if ($scope.isDel) {
                            t = '150';
                            var req = getModeData($http,
                                '/feed/modify_feed_result?' + pbFunc.urlString({
                                    feed_id: $scope.pageData['feed_id'],
                                    resume_id: $scope.pageData['resume_id'],
                                    reco_index: t
                                }),
                                "",
                                function(data) {
                                    $scope.isDel = false;
                                }, undefined, function(err) {

                                });
                        } else {
                            t = '-150';
                            var req = getModeData($http,
                                '/feed/modify_feed_result?' + pbFunc.urlString({
                                    feed_id: $scope.pageData['feed_id'],
                                    resume_id: $scope.pageData['resume_id'],
                                    reco_index: t
                                }),
                                "",
                                function(data) {

                                    $scope.isDel = true;

                                    if (!$scope.isShowDisLikeAlert && !$scope.doNotShowDisLikeAlert) {
                                        var feed_title = $('#main').attr('data-feed_title');
                                        pbFunc.simpleAlert('谢谢您的反馈！', '<div class="text-center"><span class="big-icon big-icon-flower mt20"></span><span class="mt20 block f14 c607d8b">您的反馈<span class="cf46c62">有助于</span>算法为您推荐更匹配<span class="c434343"> ' + feed_title + ' </span>的简历！</span><div class="mt20"><input type="checkbox" name="do-not-show-dislike-alert" id="do-not-show-dislike-alert"  value="1" class="" > <label for="do-not-show-dislike-alert"><span class="f14 cf46c62">不再提醒</span></label></div></div>', function(trg, args) {
                                            if ($('#do-not-show-dislike-alert').is(':checked')) {
                                                var timeLapse = 365;
                                                pbLib.setCookie('do-not-show-dislike-alert', 1, timeLapse * 86400000);
                                                $scope.doNotShowDisLikeAlert = true;
                                            }
                                        }, null, '我知道了', false);
                                    }
                                    //pbFunc.simpleAlert('聘小宝已收到你的反馈！我们将不再为你推荐该类型的简历', '');

                                }, undefined, function(err) {

                                });
                        }

                    }
                };
                $scope.dislikeResume = function($event) {
                    toggleDislike($event, 1);
                };


                //标记
                $scope.tagWaiting = function() {

                };
                $scope.tagUnchoose = function() {

                };

                //被选状态
                $scope.selectedFav = function() {
                    return $scope.isFav;
                };
                //是否不感兴趣
                $scope.selectedDislike = function() {
                    return $scope.isDel;
                };
                $scope.selectedWaiting = function() {

                };
                $scope.selectedUnchoose = function() {

                };

                //添加备注
                $scope.openDialog = false;
                $scope.comment = '';
                $scope.currPos = 0;
                $scope.maxRow = 3;
                $scope.maxLength = 0;
                $scope.notes_cp = 1;
                $scope.notes_pages = 1;
                $scope.remarkLoading = true;
                $scope.sliceData = function() {
                    return ($scope.cachedData || []).slice($scope.currPos, $scope.currPos + $scope.maxRow);
                };
                var req = getModeData($http,
                    '/resumes/get_comments/' + $scope.pageData['resume_id'] + '/',
                    "",
                    function(result) {
                        if (result.status) {
                            $timeout(function() {
                                $scope.cachedData = result.data || [];
                                $scope.remarkData = $scope.sliceData();
                                $scope.maxLength = $scope.cachedData.length;
                                $scope.notes_pages = Math.ceil($scope.maxLength / $scope.maxRow);
                            });
                        }
                        $scope.remarkLoading = false;
                    }, undefined, function(err) {
                        req.abort();
                        $scope.remarkLoading = false;
                    });

                //操作记录
                $scope.openDialogLog = false;
                $scope.commentLog = '';
                $scope.currPosLog = 0;
                $scope.maxRowLog = 5;
                $scope.notes_cpLog = 1;
                $scope.remarkLoadingLog = false;
                $scope.cachedDataLog = $scope.logs;
                $scope.sliceDataLog = function() {
                    return ($scope.cachedDataLog || []).slice($scope.currPosLog, $scope.currPosLog + $scope.maxRowLog);
                };
                $scope.remarkDataLog = $scope.sliceDataLog();
                $scope.maxLengthLog = $scope.cachedDataLog.length;
                $scope.notes_pagesLog = Math.ceil($scope.maxLengthLog / $scope.maxRowLog);


                //检查标记状态按钮
                $scope.chkStatus = function(code) {
                    var trg = angular.element(document.getElementsByClassName('code-' + code));
                    if (trg && trg.attr('data-status_selected') && trg.attr('data-status_pn')) {
                        if (trg.attr('data-status_selected').match(/true/i) && trg.attr('data-status_pn').match(/true/i)) {
                            return '1';
                        } else if (trg.attr('data-status_selected').match(/true/i) && trg.attr('data-status_pn').match(/false/i)) {
                            return '0';
                        } else {
                            return null;
                        }
                    } else {
                        return null;
                    }
                };
                $scope.chkStatusP = function(code) {
                    if (code == 'invite_interview' || code == 'next_interview') {
                        return false;
                    } else {
                        if ($scope.chkStatus(code) == '1') {
                            return true;
                        } else {
                            return false;
                        }
                    }
                };
                $scope.chkStatusN = function(code) {
                    if (code == 'invite_interview' || code == 'next_interview') {
                        return false;
                    } else {
                        if ($scope.chkStatus(code) == '0') {
                            return true;
                        } else {
                            return false;
                        }
                    }
                };
                //标记状态按钮
                $scope.tagStatusList = [];
                //面试组件
                $scope.interviewTimeComponent = function($scope, $http, JQ, pbFunc, curDay, curTime, postDataMore, postUrl, cbOk, isDisable) {
                    var disabled = (isDisable != undefined && isDisable == true) ? 'disabled' : '';
                    var dtObj = pbFunc.getDateObj();
                    var curDayPlaceHolder = (curDay != undefined && typeof curDay == 'string' && JQ.trim(curDay) != "") ? curDay : "";
                    var curTimePlaceHolder = (curTime != undefined && typeof curTime == 'string' && JQ.trim(curTime) != "") ? curTime : "";

                    if (curDayPlaceHolder == "") {
                        curDayPlaceHolder = dtObj.y + '-' + pbFunc.feedZero(dtObj.m) + '-' + pbFunc.feedZero(dtObj.d);
                    }
                    if (curTimePlaceHolder == "") {
                        curTimePlaceHolder = pbFunc.feedZero(dtObj.h) + ':' + pbFunc.feedZero(dtObj.i);
                    }

                    JQ.LayerOut({
                        html: pbFunc.alertModal(
                            '<span class="pay-alert"></span><span class="pay-title">请选择面试时间</span>',
                            '',
                            '<div class="table-line"><div class="table-line-left">面试日期：</div><div class="table-line-right"><input type="text" class="input-width-100" name="ym-date" id="ym-date" value="' + curDay + '" placeholder="' + '请选择面试日期' + '"></div></div><div class="table-line"><div class="table-line-left">面试时间：</div><div class="table-line-right"><input type="text" class="input-width-100" name="ym-time" id="ym-time" value="' + curTime + '" placeholder="' + '请选择面试时间' + '"></div></div><br><br>',
                            //<div class="table-line"><div class="table-line-left">面试地点</div><div class="table-line-right"><input type="text" class="input-width-100" name="ym-addr" id="ym-addr" value="" placeholder=""><br><br></div></div>
                            '确定',
                            null, disabled,
                            '<div class="mt20 text-center clearfix"><span class="notice">小宝提示：我们将会在面试前通过短信提醒您！<br><br></span></div>'
                        ),
                        afterClose: function() {
                            //JQ._LayerOut.close();
                        }
                    });
                    JQ('#ym-date').datetimepicker({
                        yearOffset: 0,
                        lang: 'ch',
                        timepicker: false,
                        format: 'Y-m-d',
                        formatDate: 'Y-m-d',
                        minDate: '-1970/01/02' // yesterday is minimum date
                        //maxDate: '+1970/01/02' // and tommorow is maximum date calendar
                    });
                    JQ('#ym-time').datetimepicker({
                        datepicker: false,
                        format: 'H:i',
                        step: 30
                    });
                    JQ(".modal").undelegate("#ym-date").delegate("#ym-date", "blur focus change", function(e) {
                        if (JQ('#ym-date').prop('value') != "" && !JQ('#ym-date').prop('value').match(/^[0-9]{4}\-[0-9]{1,2}\-[0-9]{1,2}$/i)) {
                            JQ('#ym-date').addClass('err');
                        } else {
                            JQ('#ym-date').removeClass('err');
                        }
                    });
                    JQ(".modal").undelegate("#ym-time").delegate("#ym-time", "blur focus change", function(e) {
                        if (JQ('#ym-time').prop('value') != "" && !JQ('#ym-time').prop('value').match(/^[0-9]{2}:[0-9]{2}$/i)) {
                            JQ('#ym-time').addClass('err');
                        } else {
                            JQ('#ym-time').removeClass('err');
                            JQ('.modal .btn-click-ok').removeClass('disabled');
                        }
                    });
                    /*JQ(".modal").undelegate("#ym-addr").delegate("#ym-addr", "blur", function(e) {
                        if (JQ('#ym-date').prop('value').match(/^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$/i) && JQ('#ym-time').prop('value').match(/^[0-9]{2}:[0-9]{2}$/i) && JQ('#ym-addr').prop('value') != "") {
                            JQ('.modal .btn-click-ok').removeClass('disabled');
                        }
                    });*/
                    JQ(".modal").undelegate(".btn-click-ok").delegate(".btn-click-ok", "click", function(e) {
                        //$._LayerOut.close();
                        var canSubmit = true;
                        if (JQ(this).attr('class').match(/disabled/i)) {
                            canSubmit = false;
                            //如果未激活状态，重新判断是否是active
                            if (JQ('#ym-date').prop('value').match(/^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$/i) && JQ('#ym-time').prop('value').match(/^[0-9]{2}:[0-9]{2}$/i)) {
                                // && $('#ym-addr').prop('value') != ""
                                canSubmit = true;
                            }
                        }
                        if (canSubmit) {
                            var postData = {
                                interview_time: JQ('#ym-date').prop('value').trim() + ' ' + JQ('#ym-time').prop('value').trim()
                            };
                            if (postDataMore != undefined && typeof postDataMore == 'object') {
                                JQ.extend(postData, postDataMore);
                            }
                            postModeData($http, postData,
                                postUrl,
                                '',
                                function(data) {
                                    if (data && data.status == 'ok') {
                                        if (typeof cbOk == 'function') {
                                            cbOk(data);
                                        }
                                    }
                                    JQ._LayerOut.close();
                                }, null, function(err) {
                                    JQ._LayerOut.close();
                                });
                        }
                    });
                };

                //标记状态
                $scope.tagStatus = function($event) {
                    var trg = angular.element($event.currentTarget);
                    var code = trg.attr('data-code_name');
                    var name = trg.attr('data-name');
                    var id = trg.attr('data-record_id');
                    var pn = trg.attr('data-status_pn');

                    //变色后不能点击
                    if (trg.attr('data-status_selected').match(/true/i)) {
                        return false;
                    }

                    //更新当前状态文字
                    var updateStatusText = function(pn, name) {
                        var currentStatus = angular.element(document.getElementsByClassName('current-resume-status'));
                        currentStatus.removeClass('c44b5e8');
                        currentStatus.removeClass('cf46c62');
                        //console.log('currentStatus',currentStatus,name);
                        if (pn.match(/^true$/i)) {
                            //正向颜色
                            currentStatus.addClass('c44b5e8');
                        } else {
                            //负向颜色
                            currentStatus.addClass('cf46c62');
                        }
                        currentStatus[0].innerHTML = name;
                    };

                    //取消所有已选状态
                    var restoreSelectFalse = function() {
                        var trg = angular.element(document.getElementsByClassName('resume-status-btns'));
                        trg.find('.code-assign').attr('data-status_selected', 'false');
                    };

                    //invite_interview 和 next_interview 是安排面试, 需要使用新接口
                    if (code == 'invite_interview' || code == 'next_interview') {
                        $scope.interviewTimeComponent($scope, $http, $, pbFunc, '', '', {
                            code_name: code
                        }, '/resume/interview/send/' + id + '/', function(data) {
                            restoreSelectFalse();
                            //trg.attr('data-status_selected', 'true');
                            if (!inArray(code, $scope.tagStatusList)) $scope.tagStatusList.push(code);
                            document.location.reload();
                            updateStatusText(pn, name);
                        }, true);
                    } else {

                        if (id != "" && code != "") {
                            var postData = {
                                code_name: code,
                                __: pbFunc.getTimestamp()
                            };
                            postModeData($http, postData,
                                '/transaction/mark_resume/' + id + '/',
                                '',
                                function(data) {
                                    restoreSelectFalse();
                                    trg.attr('data-status_selected', 'true');
                                    $scope.tagStatusList.push(code);
                                    updateStatusText(pn, name);
                                    if (code == 'entry') {
                                        pbFunc.simpleAlert('<span class="pb-icon pb-icon-smile"></span>恭喜收入候选人一枚，再接再厉哦！', '<div class="text-center"><span class="big-icon big-icon-robot mt20"></span></div>', function(trg, args) {

                                        }, null, '确定', false, 'red');
                                    } else {
                                        if ($._LayerOut) $._LayerOut.close();
                                    }
                                    //document.location.reload();
                                }, null, function(err) {
                                    if ($._LayerOut) $._LayerOut.close();
                                });
                        }
                    }
                };
                $scope.$watchCollection('tagStatusList', function(newValue, oldValue) {
                    //同一时间只能有一个按钮被标记
                    if (newValue != oldValue) {
                        $('.code-assign').removeClass('btn-red');
                        $('.code-assign').removeClass('btn-blue');
                        var tempArr = newValue;
                        var code = tempArr.pop();
                        if ($scope.chkStatus(code) == '1') {
                            $('.code-' + code).addClass('btn-blue');
                            $('.code-' + code).removeClass('btn-red');
                        } else if ($scope.chkStatus(code) == '0') {
                            $('.code-' + code).addClass('btn-red');
                            $('.code-' + code).removeClass('btn-blue');
                        } else {
                            $('.code-' + code).removeClass('btn-red');
                            $('.code-' + code).removeClass('btn-blue');
                        }
                    }
                });

                //修改面试时间
                $scope.chgInterviewTime = function($event) {
                    var trg = angular.element($event.currentTarget);
                    var rid = trg.attr('data-record_id');
                    var timeStr = trg.attr('data-mod_time');
                    var timeArr = timeStr.split(' ');
                    $scope.interviewTimeComponent($scope, $http, $, pbFunc, timeArr[0], timeArr[1], {}, '/resume/interview_time/change/' + rid + '/', function(data) {

                    });

                };

                //添加简历到自定义文件夹
                $scope.addFolder = function($event) {
                    //alert('coming soon');
                };
                //查看联系方式
                $scope.getContactInfo = function($event) {
                    var sendCard = function(data) {
                        $scope.isSendCompanyCard = (pbLib.getCookie(sendCardCookieName) == null) ? false : true;
                        if ($scope.isSendCompanyCard) {
                            pbFunc.simpleConfirm('需要您的确认', '<p class="mt30 f14 c607d8b">您已发送了企业名片进行意向确认，还要再直接获取该简历联系方式吗？</p><p class="mt50 cf46c62 f13">小宝提示：确认会在已扣3个聘点的基础上再扣除您10个聘点</p>', function(args) {
                                $._LayerOut.close();
                            }, null, '取消', true, '确认', function(args) {
                                //isHasCompanyInfo(hasCompanyCard);
                                $scope.directDownload($event);
                            });
                        } else {
                            isHasCompanyInfo(hasCompanyCard);
                        }
                    };
                    //检查是否是聘宝会员
                    getModeData($http,
                        '/vip/get_user_info/',
                        "",
                        function(data) {
                            if (data.status != undefined && data.status == 'ok') {
                                //非会员
                                if (parseInt(data.pinbot_point) < $scope.pinbot_point_limit) {
                                    alertUpgrade(data.pinbot_point, data.user_type, '查看联系方式');
                                } else {
                                    sendCard(data);
                                }
                            } else {
                                alertUpgrade(0, null, '查看联系方式');
                            }
                        });
                };

                var Keywords = (function() {
                    var Style = (function() {
                        /**
                         * Create an instance of Style
                         * @param {Object} pre-defined variables
                         */
                        function Style(map) {
                            if (!(this instanceof Style)) {
                                return new Style(map);
                            }
                            this.map = _mixin({}, map);
                            this.rules = '';
                            this.elem = null;
                        };
                        Style.prototype = {
                            /**
                             * Define new variables.
                             * @param {object}
                             */
                            define: function(map) {
                                this.map = _mixin(this.map, map);
                                return this;
                            },
                            /**
                             * Add new css but won't refresh the style element's content.
                             * @param {string} Accepts multiple params
                             */
                            add: function() {
                                var rules = _getRules(arguments);
                                rules && (this.rules += rules);
                                return this;
                            },
                            /**
                             * Append new css to the style element or refresh its content.
                             * @param {string}
                             */
                            load: function() {
                                if (!this.elem) {
                                    this.elem = _createStyleElem();
                                }
                                if (arguments.length) {
                                    this.add.apply(this, arguments);
                                }
                                _refreshStyleContent(this.elem, this.rules, this.map);
                                return this;
                            },
                            /**
                             * Clear the style and varialbes.
                             */
                            clear: function() {
                                _setStyleContent(this.elem, '');
                                this.rules = '';
                                this.map = {};
                                return this;
                            },
                            /**
                             * Remove the style element completely.
                             */
                            remove: function() {
                                var elem = this.elem;
                                if (elem && elem.parentNode) {
                                    this.clear();
                                    this.elem = null;
                                    elem.parentNode.removeChild(elem);
                                }
                                return this;
                            }
                        };


                        function _mixin() {
                            var mix = {},
                                idx, arg, name;
                            for (idx = 0; idx < arguments.length; idx += 1) {
                                arg = arguments[idx];
                                for (name in arg) {
                                    if (arg.hasOwnProperty(name)) {
                                        mix[name] = arg[name];
                                    }
                                }
                            }
                            return mix;
                        }


                        // Make a list of parameters of css into a single string.
                        function _getRules(args) {
                            return [].join.call(args, '');
                        }


                        // Create new stylesheet.
                        function _createStyleElem() {
                            var elem = document.createElement('style'),
                                head = document.getElementsByTagName('head')[0];
                            head && head.appendChild(elem);
                            return elem;
                        }


                        // Substitute variables in the string with defined map.
                        function _substitute(str, map) {
                            for (var name in map) {
                                if (map.hasOwnProperty(name)) {
                                    str = str.replace(new RegExp('@' + name, 'gi'), map[name]);
                                }
                            }
                            return str;
                        }


                        // Set the style element's content.
                        function _setStyleContent(el, content) {
                            if (el && el.tagName.toLowerCase() === 'style') {
                                el.styleSheet ? (el.styleSheet.cssText = content) : (el.innerHTML = content);
                            }
                        }


                        // Refresh the content with the rules and defined variables.
                        function _refreshStyleContent(elem, rules, map) {
                            _setStyleContent(elem,
                                _substitute(rules, map)
                            );
                        }

                        return Style;

                    }());
                    /**
                     * Original JavaScript code by Chirp Internet: www.chirp.com.au
                     */
                    var Hilitor = function(input, cname) {
                        if (input == undefined || !input) return;
                        var cname = cname || '';
                        var targetNode = document.getElementById('resume-content') || document.body;
                        var hiliteTag = "EM";
                        var skipTags = new RegExp("^(?:" + hiliteTag + "|SCRIPT|FORM)$");
                        var matchRegex = "";
                        var openLeft = false;
                        var openRight = false;
                        var formatInput = function(i, v, arr) {
                            return '\\' + i;
                        };
                        var setRegex = function(input) {
                            //input = input.replace(/[^\w0-9\\u ]+/, "").replace(/[ ]+/g, "|");
                            input = input.replace(/[+|.|*|$|^|?]/gi, formatInput);
                            var re = "(" + input + ")";
                            matchRegex = new RegExp(re, "i");
                        };
                        // recursively apply word highlighting
                        var hiliteWords = function(node) {
                            if (node == undefined || !node) return;
                            if (!matchRegex) return;
                            if (skipTags.test(node.nodeName)) return;
                            if (node.hasChildNodes()) {
                                for (var i = 0; i < node.childNodes.length; i++)
                                    hiliteWords(node.childNodes[i]);
                            }
                            if (node.nodeType == 3) { // NODE_TEXT
                                if ((nv = node.nodeValue) && (regs = matchRegex.exec(nv))) {

                                    var matchKeywrod = regs[0];
                                    if (matchKeywrod && matchKeywrod.match(/^[0-9a-z]{3,}$/i)) {
                                        //resolve keywords hilight bugs
                                        var nvZm = nv.replace(/[^0-9a-z]/ig, " ");
                                        var nvZmArr = nvZm.split(" ");
                                        for (var i = 0, imax = nvZmArr.length; i < imax; i++) {
                                            var currentKw = matchKeywrod;
                                            var findMatch = new RegExp("" + currentKw + "", "i");
                                            if (matchKeywrod != nvZmArr[i] && nvZmArr[i].match(findMatch)) {
                                                matchKeywrod = nvZmArr[i];
                                            }
                                        }
                                    }
                                    var match = document.createElement(hiliteTag);
                                    match.appendChild(document.createTextNode(matchKeywrod));
                                    match.style.fontStyle = "inherit";
                                    match.className = cname;
                                    var after = node.splitText(regs.index);
                                    after.nodeValue = after.nodeValue.substring(matchKeywrod.length);
                                    node.parentNode.insertBefore(match, after);
                                    //console.log('NODE_TEXT nv^^',nv,regs,regs.index,matchKeywrod,match, after);

                                }
                            };
                        };

                        var convertCharStr2jEsc = function(str, cstyle) {
                            var dec2hex4 = function(textString) {
                                var hexequiv = new Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F");
                                return hexequiv[(textString >> 12) & 0xF] + hexequiv[(textString >> 8) & 0xF] + hexequiv[(textString >> 4) & 0xF] + hexequiv[textString & 0xF];
                            };
                            // Converts a string of characters to JavaScript escapes
                            // str: sequence of Unicode characters
                            var highsurrogate = 0;
                            var suppCP;
                            var pad;
                            var n = 0;
                            var outputString = '';
                            for (var i = 0; i < str.length; i++) {
                                var cc = str.charCodeAt(i);
                                if (cc < 0 || cc > 0xFFFF) {
                                    outputString += '!Error in convertCharStr2UTF16: unexpected charCodeAt result, cc=' + cc + '!';
                                }
                                if (highsurrogate != 0) { // this is a supp char, and cc contains the low surrogate
                                    if (0xDC00 <= cc && cc <= 0xDFFF) {
                                        suppCP = 0x10000 + ((highsurrogate - 0xD800) << 10) + (cc - 0xDC00);
                                        if (cstyle) {
                                            pad = suppCP.toString(16);
                                            while (pad.length < 8) {
                                                pad = '0' + pad;
                                            }
                                            outputString += '\\U' + pad;
                                        } else {
                                            suppCP -= 0x10000;
                                            outputString += '\\u' + dec2hex4(0xD800 | (suppCP >> 10)) + '\\u' + dec2hex4(0xDC00 | (suppCP & 0x3FF));
                                        }
                                        highsurrogate = 0;
                                        continue;
                                    } else {
                                        outputString += 'Error in convertCharStr2UTF16: low surrogate expected, cc=' + cc + '!';
                                        highsurrogate = 0;
                                    }
                                }
                                if (0xD800 <= cc && cc <= 0xDBFF) { // start of supplementary character
                                    highsurrogate = cc;
                                } else { // this is a BMP character
                                    switch (cc) {
                                        case 0:
                                            outputString += '\\0';
                                            break;
                                        case 8:
                                            outputString += '\\b';
                                            break;
                                        case 9:
                                            outputString += '\\t';
                                            break;
                                        case 10:
                                            outputString += '\\n';
                                            break;
                                        case 13:
                                            outputString += '\\r';
                                            break;
                                        case 11:
                                            outputString += '\\v';
                                            break;
                                        case 12:
                                            outputString += '\\f';
                                            break;
                                        case 34:
                                            outputString += '\\\"';
                                            break;
                                        case 39:
                                            outputString += '\\\'';
                                            break;
                                        case 92:
                                            outputString += '\\\\';
                                            break;
                                        default:
                                            if (cc > 0x1f && cc < 0x7F) {
                                                outputString += String.fromCharCode(cc);
                                            } else {
                                                pad = cc.toString(16).toUpperCase();
                                                while (pad.length < 4) {
                                                    pad = '0' + pad;
                                                }
                                                outputString += '\\u' + pad;
                                            }
                                    }
                                }
                            }
                            return outputString;
                        };

                        setRegex(convertCharStr2jEsc(input));
                        hiliteWords(targetNode);
                    };
                    var randClass = function() {
                        var pre = 'pinbot-keyword-';
                        return pre + Math.random().toString(16).substr(2)
                    };
                    var findPos = function(obj) {
                        var curtop = 0;
                        if (obj.offsetParent) {
                            do {
                                curtop += obj.offsetTop;
                            } while (obj = obj.offsetParent);
                            return [curtop];
                        }
                    };
                    var createIndex = function(from, to) {
                        var curr = from;
                        return {
                            prev: function() {
                                return curr <= from ? (curr = to) : --curr;
                            },
                            next: function() {
                                return curr >= to ? (curr = from) : ++curr;
                            },
                            curr: function(idx) {
                                return curr = (idx === undefined) ? curr : idx;
                            }
                        }
                    };

                    var selector = window.selector = (function() {
                        function selector(el) {
                            this.el = el || document.createElement('div');
                        };
                        selector.prototype = {
                            hasClass: function(cname) {
                                var str = (this.el.className || '').split(/\s+/);
                                for (var i = 0; i < str.length; ++i) {
                                    if (cname == str[i]) return true;
                                }
                                return false;
                            },
                            addClass: function(cname) {
                                var str = this.el.className;
                                if (!this.hasClass(cname)) {
                                    this.el.className += (' ' + cname);
                                }
                                return this;
                            },
                            removeClass: function(cname) {
                                var str = this.el.className;
                                var array = str.split(/\s+/);
                                var temp = [];
                                for (var i = 0; i < array.length; ++i) {
                                    if (array[i] != cname) {
                                        temp.push(array[i]);
                                    }
                                }
                                this.el.className = temp.join(' ');
                                return this;
                            }
                        }
                        return function(el) {
                            return new selector(el);
                        }
                    }());



                    var cycle = (function() {
                        var container = {};
                        return {
                            add: function(cname) {
                                var all = document.querySelectorAll('.' + cname);
                                container[cname] = {
                                    index: createIndex(0, all.length - 1),
                                    element: all,
                                    get: function() {
                                        return this.element[this.index.next()]
                                    }
                                }
                            },
                            get: function(cname) {
                                if (!container[cname]) return {};
                                return container[cname].get()
                            },
                            currIndex: function(cname) {
                                if (container[cname]) {
                                    return container[cname].index.curr();
                                }
                            }
                        }
                    }());

                    var cache = {};
                    var currentKeyword = '';
                    var myStyle = new Style();
                    return {
                        init: function(word) {
                            if (cache.hasOwnProperty(word)) return this;
                            var cname = randClass();
                            Hilitor(word, cname);
                            cache[word] = cname;
                            cycle.add(cname);
                            return this;
                        },
                        locate: function(word) {
                            var cname = cache[word];
                            if (cname) {
                                if (currentKeyword != word) {
                                    currentKeyword = word;
                                    myStyle.load(
                                        '.pinbot-keyword-current{ background: #44b5e8 !important; color: #fff;}',
                                        '.' + cname + '{background: #44b5e8; color: #fff;-webkit-transition: all 1s ease; transition: all 1s ease}'
                                    )
                                }
                                var span = cycle.get(cname);
                                selector(document.querySelector('.pinbot-keyword-current')).removeClass('pinbot-keyword-current');
                                selector(span).addClass('pinbot-keyword-current');
                                // span && $('body, html').stop().animate({
                                //   scrollTop: findPos(span) - 100
                                // }, 'normal')
                            }
                        }
                    }
                }());
                //关键词标注
                if ($scope.pageData['feed_keywords'].length > 0) {
                    for (var i = $scope.pageData['feed_keywords'].length - 1; i >= 0; i--) {
                        (function(arg) {
                            var word = $scope.pageData['feed_keywords'][arg];
                            Keywords.init(word).locate(word);
                        })(i);
                    };
                }
            }
        ]
    );

    //用户端增删改组件
    /*app.directive('userCrud', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('resume/user_crud.html'),
            controller: 'userCrud',
            link: function(scope, elem, attrs) {},
            scope: {
                data: "=data"
            }
        }
    });*/

    //简单带分页备注列表
    app.directive('notesList', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('resume/notes_list.html'),
            controller: function($scope, $element, $http, $timeout) {
                var $prev = $('.ic-notes-prev');
                var $next = $('.ic-notes-next');
                $scope.sliceData = function() {
                    return ($scope.cachedData || []).slice($scope.currPos, $scope.currPos + $scope.maxRow);
                };
                $scope.updatePagerState = function() {
                    $scope.notesPages = Math.ceil($scope.maxLength / $scope.maxRow);
                    $scope.remarkData = $scope.sliceData();
                    if (!$scope.remarkData.length && $scope.currPos) {
                        $scope.currPos -= $scope.maxRow;
                        $scope.remarkData = $scope.sliceData();
                    }
                    if ($scope.currPos >= $scope.maxRow) {
                        $prev.removeClass('disabled');
                    } else {
                        $prev.addClass('disabled');
                    }
                    if ($scope.currPos < $scope.maxLength - $scope.maxRow) {
                        $next.removeClass('disabled');
                    } else {
                        $next.addClass('disabled');
                    }
                };
                $scope.addRemark = function($event) {
                    if ($scope.openDialog = !$scope.openDialog) {
                        setTimeout(function() {
                            $('.notes-textbox textarea').focus();
                        });
                    }
                };
                $scope.addComment = function($event) {
                    var resumeid = $scope.pageData['resume_id'];
                    if ($scope.comment.trim() == "") {
                        setTimeout(function() {
                            $('.notes-textbox textarea').focus();
                        });
                        return;
                    }
                    postModeData($http, {
                            comment: $scope.comment
                        },
                        '/resumes/add_comment/' + resumeid + '/',
                        '',
                        function(result) {
                            if (result.status) {
                                $timeout(function() {
                                    if ($scope.cachedData) {
                                        $scope.cachedData.unshift({
                                            'id': result.data.comment_id,
                                            'date': pbFunc.formatDate('yyyy-MM-dd hh:mm:ss'),
                                            'text': $scope.comment
                                        });
                                        $scope.remarkData = $scope.cachedData;
                                    }
                                    $scope.comment = '';
                                    //$scope.toggle();
                                    $scope.currPos = 0;
                                    $scope.maxLength = $scope.cachedData.length;
                                    $scope.updatePagerState();
                                    $scope.openDialog = false;
                                });
                            }
                        }, null, function(err) {

                        });
                };
                $scope.delComment = function(id, index) {
                    var resumeid = $scope.pageData['resume_id'];
                    postModeData($http, {},
                        '/resumes/delete_comment/' + resumeid + '/' + id + '/',
                        '',
                        function(result) {
                            $timeout(function() {
                                $scope.cachedData.splice(index, 1);
                                $scope.maxLength = $scope.cachedData.length;
                                $scope.updatePagerState();
                                $scope.remarkData = $scope.cachedData;
                            });
                        }, null, function(err) {

                        });
                };
                $scope.prevPage = function() {
                    $timeout(function() {
                        if ($scope.currPos >= $scope.maxRow) {
                            $scope.currPos -= $scope.maxRow;
                            $scope.notesCp -= 1;
                            $scope.updatePagerState();
                        }
                    });
                };
                $scope.nextPage = function() {
                    $timeout(function() {
                        if ($scope.currPos < $scope.maxLength - $scope.maxRow) {
                            $scope.currPos += $scope.maxRow;
                            $scope.notesCp += 1;
                            $scope.updatePagerState();
                        }
                    });
                };
            },
            link: function(scope, elem, attrs) {},
            scope: {
                title: "=title",
                maxLength: "=maxLength",
                remarkLoading: "=remarkLoading",
                remarkData: "=remarkData",
                notesCp: "=notesCp",
                notesPages: "=notesPages",
                comment: "=comment",
                openDialog: "=openDialog",
                pageData: "=pageData",
                cachedData: "=cachedData",
                currPos: "=currPos",
                maxRow: "=maxRow"
            }
        }
    });

    //简单带分页操作记录列表
    app.directive('logList', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('resume/log_list.html'),
            controller: function($scope, $element, $http, $timeout) {
                var $prev = $('.ic-notes-prev');
                var $next = $('.ic-notes-next');
                $scope.sliceData = function() {
                    return ($scope.cachedData || []).slice($scope.currPos, $scope.currPos + $scope.maxRow);
                };
                $scope.updatePagerState = function() {
                    $scope.notesPages = Math.ceil($scope.maxLength / $scope.maxRow);
                    $scope.remarkData = $scope.sliceData();
                    if (!$scope.remarkData.length && $scope.currPos) {
                        $scope.currPos -= $scope.maxRow;
                        $scope.remarkData = $scope.sliceData();
                    }
                    if ($scope.currPos >= $scope.maxRow) {
                        $prev.removeClass('disabled');
                    } else {
                        $prev.addClass('disabled');
                    }
                    if ($scope.currPos < $scope.maxLength - $scope.maxRow) {
                        $next.removeClass('disabled');
                    } else {
                        $next.addClass('disabled');
                    }
                };
                $scope.addRemark = function($event) {
                    if ($scope.openDialog = !$scope.openDialog) {
                        setTimeout(function() {
                            $('.notes-textbox textarea').focus();
                        });
                    }
                };
                $scope.addComment = function($event) {
                    //console.log('pageData', $scope.pageData);
                    var resumeid = $scope.pageData['resume_id'];
                    if (!$scope.comment.length) {
                        setTimeout(function() {
                            $('.notes-textbox textarea').focus();
                        });
                        return;
                    }
                    postModeData($http, {
                            comment: $scope.comment
                        },
                        '/resumes/add_comment/' + resumeid + '/',
                        '',
                        function(result) {
                            if (result.status) {
                                $timeout(function() {
                                    if ($scope.cachedData) {
                                        $scope.cachedData.unshift({
                                            'id': result.data.comment_id,
                                            'date': pbFunc.formatDate('yyyy-MM-dd hh:mm:ss'),
                                            'text': $scope.comment
                                        });
                                        $scope.remarkData = $scope.cachedData;
                                    }
                                    $scope.comment = '';
                                    //$scope.toggle();
                                    $scope.currPos = 0;
                                    $scope.maxLength = $scope.cachedData.length;
                                    $scope.updatePagerState();
                                    $scope.openDialog = false;
                                });
                            }
                        }, null, function(err) {

                        });
                };
                $scope.delComment = function(id, index) {
                    var resumeid = $scope.pageData['resume_id'];
                    postModeData($http, {},
                        '/resumes/delete_comment/' + resumeid + '/' + id + '/',
                        '',
                        function(result) {
                            $timeout(function() {
                                $scope.cachedData.splice(index, 1);
                                $scope.maxLength = $scope.cachedData.length;
                                $scope.updatePagerState();
                                $scope.remarkData = $scope.cachedData;
                            });
                        }, null, function(err) {

                        });
                };
                $scope.prevPage = function() {
                    $timeout(function() {
                        if ($scope.currPos >= $scope.maxRow) {
                            $scope.currPos -= $scope.maxRow;
                            $scope.notesCp -= 1;
                            $scope.updatePagerState();
                        }
                    });
                };
                $scope.nextPage = function() {
                    $timeout(function() {
                        if ($scope.currPos < $scope.maxLength - $scope.maxRow) {
                            $scope.currPos += $scope.maxRow;
                            $scope.notesCp += 1;
                            $scope.updatePagerState();
                        }
                    });
                };
            },
            link: function(scope, elem, attrs) {},
            scope: {
                title: "=title",
                maxLength: "=maxLength",
                remarkLoading: "=remarkLoading",
                remarkData: "=remarkData",
                notesCp: "=notesCp",
                notesPages: "=notesPages",
                comment: "=comment",
                openDialog: "=openDialog",
                pageData: "=pageData",
                cachedData: "=cachedData",
                currPos: "=currPos",
                maxRow: "=maxRow"
            }
        }
    });


})();

/*$(function() {
    $(window).on('scroll', function() {
        var $feed_aside = $('.feed-aside'),
            $doc = $(document),
            $hasmore = $('a[ng-if="hasmore"]'),
            top = 153,
            scrollY = window.scrollY ? window.scrollY : document.documentElement.scrollTop;
        if (scrollY >= 153) {
            $feed_aside.css('top', '10px');
        } else {
            $feed_aside.css('top', (top - scrollY) + 'px');
        }
        if (!$hasmore.length) return !1;
        if (!$hasmore.is(":hidden")) {
            var n = $doc.height() - $doc.scrollTop() - $(window).height();
            100 > n && $hasmore.get(0).click();
        }
    });
});*/