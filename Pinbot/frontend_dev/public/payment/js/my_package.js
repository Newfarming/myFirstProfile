(function(argument) {
    // body...

    var app = angular.module('app.my_package', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter']),
        $django = angular.injector(['app.django', 'app.utils']),
        tmpl = $django.get('tmpl'),
        static_url = $django.get('static_url');

    //公用库
    var mockTest = $django.get('mockTest');
    //是否测试：使用金币支付
    var mockTestWithCoin = $django.get('mockTestWithCoin');
    var confirmBox = $django.get('confirmBox');
    var confirmBoxRed = $django.get('confirmBoxRed');
    var alertBox = $django.get('alertBox');
    var getModeData = $django.get('getModeData');
    var postModeData = $django.get('postModeData');
    var inArray = $django.get('inArray');
    var pbFunc = $django.get('pbFunc');
    var orderPay = $django.get('orderPay');

    app.config([
        '$stateProvider', '$urlRouterProvider', '$httpProvider',
        function($stateProvider, $urlRouterProvider, $httpProvider) {
            var otherwiseUrl = '/';

            //$httpProvider.defaults.cache = false;
            /*//initialize get if not there
            if (!$httpProvider.defaults.headers.get) {
                $httpProvider.defaults.headers.get = {};
            }
            //disable IE ajax request caching
            $httpProvider.defaults.headers.get['If-Modified-Since'] = '0';*/

            $urlRouterProvider.otherwise(otherwiseUrl);
            //自助套餐续期
            $stateProvider.state(
                'myPackageDiyResume', {
                    url: '/diy_resume/:orderId',
                    templateUrl: tmpl('payment/my_package_diy_resume.html'),
                    controller: 'myPackageDiyResume'
                }
            );
            //默认模式页面 我的套餐
            $stateProvider.state(
                'myPackage', {
                    url: '/',
                    templateUrl: tmpl('payment/my_package.html'),
                    controller: 'myPackage'
                }
            );
            //自助模式续期购买页面
            $stateProvider.state(
                'myPackageDiyResumePay', {
                    url: '/diy_resume_pay/',
                    templateUrl: tmpl('payment/my_package_diy_resume_pay.html'),
                    controller: 'myPackageDiyResumePay'
                }
            );
            //续期结果成功页面
            $stateProvider.state(
                'userModeDiyResumeOk', {
                    url: '/diy_resume_ok/',
                    templateUrl: tmpl('payment/my_package_diy_resume_ok.html'),
                    controller: 'userModeDiyResumeOk'
                }
            );
            //续期结果失败页面
            $stateProvider.state(
                'userModeDiyResumeFailed', {
                    url: '/diy_resume_failed/',
                    templateUrl: tmpl('payment/my_package_diy_resume_failed.html'),
                    controller: 'userModeDiyResumeFailed'
                }
            );
        }
    ]);

    app.factory('fMyPackage', function() {
        return {
            //主页loading
            loading: true,
            //记录列表
            logList: {},
            vipName: '',
            feedCount: 0,
            pinbotPoint: 0,
            id: 0,
            monthPrice: 0,
            payPrice: 0,
            servicePeriod: '',
            serviceNow: '',
            serviceExpired: '',
            serviceNowTs: 0,
            serviceExpiredTs: 0,
            orderId: '',
            userInfo: {}
        };
    });

    app.run(function($rootScope, $templateCache) {
        $rootScope.$on('$viewContentLoaded', function() {
            $templateCache.removeAll();
        });
    });

    app.controller(
        'myPackage', ['$scope', '$http', '$state', '$templateCache', 'fMyPackage',
            function($scope, $http, $state, $templateCache, fMyPackage) {
                $scope.loading = fMyPackage.loading;
                $scope.loadingThis = true;
                $scope.chgStatus = 'all';

                //删除交易记录
                /*$scope.delLog = function($event) {
                    var oid = $($event.currentTarget).attr('data-oid');
                    //console.log('oid',oid);
                    var postData = {
                        order_id: oid
                    };
                    getModeData($http, postData,
                        '/payment/payment_record/',
                        '',
                        function(data) {
                            $scope.loadingThis = false;
                            fMyPackage.logList = data;
                            fMyPackage.loading = false;
                            $scope.loading = fMyPackage.loading;
                            $scope.logList = fMyPackage.logList;
                        });
                };*/

                $scope.api_url = "/payment/service_list/";
                $scope.api_params = [];
                $scope.api_params_values = {};



                $scope.listStatus = function($event, type) {
                    var trg = $($event.currentTarget);
                    $('.trade-status li').removeClass('active');
                    trg.parent().addClass('active');
                    $scope.chgStatus = type;
                    $scope.loadingThis = true;

                    //(applying: 申请中|success: 已开通|refund: 退款中|cancel_refund: 取消退款|refunded: 退款成功|closed: 已关闭|canceled: 已取消|deleted: 已删除|expired: 已过期)
                    if (type.toString().match(/^(applying|success|refund|cancel_refund|refunded|closed|canceled|deleted|expired|finished)$/i)) {
                        if (!inArray("status", $scope.api_params)) $scope.api_params.push("status");
                        $scope.api_params_values["status"] = type;
                    } else {
                        if (type == 'all') $scope.api_params.pop("status");
                    }

                    //载入数据
                    pbFunc.reloadList($http, $scope, fMyPackage);
                };

                $scope.nextPage = function(pageNum) {
                    pbFunc.nextPage($http, $scope, $, fMyPackage, pageNum);
                };

                //(applying: 申请中|success: 已开通|refund: 退款中|cancel_refund: 取消退款|refunded: 退款成功|closed: 已关闭|canceled: 已取消|deleted: 已删除|expired: 已过期)
                $scope.defaultOrderStatus = function(order_status) {
                    var order_status = order_status.trim();
                    if (order_status != '申请中' && order_status != '已开通' && order_status != '退款中' && order_status != '取消退款' && order_status != '退款成功' && order_status != '已关闭' && order_status != '已取消' && order_status != '已删除' && order_status != '已过期' && order_status != '已完结') {
                        return true;
                    } else {
                        return false;
                    }
                };

                //是否使用normal颜色样式
                $scope.normalStatus = function(status) {
                    var status = status.trim();
                    if (status == "已开通" || status == "申请中" || status == "退款中") {
                        return true;
                    } else {
                        return false;
                    }
                };

                //下拉按钮
                $scope.showOpt = function($event) {
                    var trg = $($event.currentTarget);
                    if (trg.parent().parent().find('.select-btn-opts')) {
                        var opts = $(trg.parent().parent().find('.select-btn-opts'))[0];
                        //console.log('opts', $(opts).css('display'));
                        if ($(opts).css('display') == 'none') {
                            $(opts).css('display', 'block');
                            trg.removeClass('arrow-close');
                        } else {
                            $(opts).css('display', 'none');
                            trg.addClass('arrow-close');
                        }
                    }
                };

                $scope.showDoApply = function(status) {
                    if (status == '申请中') {
                        $.Menu();
                        return true;
                    } else {
                        return false;
                    }
                };

                //取消订单
                $scope.doCancel = function($event) {

                    pbFunc.orderActConfirm($http, $scope, $, '<span class="pay-alert"></span><span class="pay-title">取消订单</span>',
                        '订单取消后，聘宝将不再为您提供相关服务',
                        '重新购买',
                        '确认取消', function() {
                            //用户重新购买相当于直接到支付页面提交订单
                            //重新购买需要保险吗？
                            /*var postData = {
                                'product_type': product_type,
                                'num': 1,
                                'pid': $scope.payPid,
                                'payment_terms': payment_terms,
                                'is_insurance': is_insurance
                            };
                            if (pbDebug) console.log('postData', fUserMode, postData);

                            orderPay($scope, $state, $http, $, postData, 'userModeDiyPayOk');*/

                            document.location.href = '/vip/role_info/';

                        }, function() {
                            pbFunc.orderAct($http, $scope, $, fMyPackage, $event, '/vip/order/cancel/');
                        });
                };

                //我要退款
                $scope.doRefund = function($event) {
                    var trg = $($event.currentTarget);
                    var service_id = trg.attr('data-oid');
                    pbFunc.orderActGet($http, $scope, $, fMyPackage, $event, '/vip/order/pre_refund/' + service_id, function(data) {

                        var refundHtml = '';
                        refundHtml += '<div class="price content box-content box-content-table box-content-table-box box-content-table-box50 pd-top-0 lh180">';
                        refundHtml += '<div class="box-col box-col-center"><div class="user-mode"><div class="box-col-bar"></div><ul>';
                        //refundHtml += '<li class="text-center"><span>套餐支付款项</span><span><span class="cf46c62">¥ ' + data.data.pay_fee + '</span></span></li>';
                        refundHtml += '<li class="text-center"><span>服务期</span><span>第<span class="cf46c62">' + data.data.service_months + '</span>个月</span></li>';
                        refundHtml += '<li class="text-center"><span>退款比例</span><span><span class="cf46c62">' + data.data.refund_percent + '</span></span></li>';
                        refundHtml += '</ul></div></div></div>';
                        //refundHtml += '<div class="price content box-content pd-top-0 text-center"><span class="c607d8b f14">您的退款金额：<span class="price-focus">¥ ' + data.data.refund_fee + '</span><br></div>';

                        refundHtml += '<div class="price content box-content pd-top-0 text-center"><span class="c607d8b f14"><span class="price-focus-txt">实际退款金额，请咨询您的顾问</span><br></div>';

                        pbFunc.orderActAlert($http, $scope, $, '<span class="pay-alert"></span><span class="pay-title">你正在申请退款！</span>', '退款提交后，请等待聘宝人才顾问与您沟通并核对信息', refundHtml, '确认', function() {

                            pbFunc.orderAct($http, $scope, $, fMyPackage, $event, '/vip/order/refund/', function(data) {


                            });

                        });
                    });

                };

                //续期自助套餐
                $scope.doResumeDiyPackage = function($event, oid) {
                    document.location.href = '/payment/my_package/#/diy_resume/' + oid + '';
                };

                //检查会员套餐是否显示联系我们
                $scope.chkUserNeedContact = function(status) {
                    if (status == '已开通') {
                        $.Menu();
                        return true;
                    } else {
                        return false;
                    }
                };
                $scope.chkUserNeedContact2 = function(status) {
                    if (status == '退款中') {
                        $.Menu();
                        return true;
                    } else {
                        return false;
                    }
                };

                //联系我们
                $scope.doContact = function($event) {
                    /*pbFunc.orderAct($http, $scope, $, fMyPackage, $event, '/vip/order/refund/');*/

                };

                //取消退款
                $scope.cancelRefund = function($event) {
                    pbFunc.orderActConfirm($http, $scope, $, '<span class="pay-alert"></span><span class="pay-title">取消退款</span>',
                        '退款取消后，聘宝人才顾问将继续为您提供相关服务',
                        '返回',
                        '确认取消', null, function() {
                            pbFunc.orderAct($http, $scope, $, fMyPackage, $event, '/vip/order/cancel_refund/');
                        });
                    /*$.LayerOut({
                        html: confirmBoxRed(
                            '<span class="pay-alert"></span><span class="pay-title">取消退款</span>',
                            '退款取消后，聘宝人才顾问将继续为您提供相关服务',
                            '返回',
                            '',
                            '确认取消',
                            ''
                        ),
                        afterClose: function() {
                            //$._LayerOut.close();
                            $state.go(
                                'userModeDiyPayOk', {}
                            );
                        }
                    });

                    $(".modal").undelegate(".btn-pay-problem").delegate(".btn-pay-problem", "click", function(e) {
                        $._LayerOut.close();
                    });
                    $(".modal").undelegate(".btn-pay-ok").delegate(".btn-pay-ok", "click", function(e) {
                        $._LayerOut.close();
                        pbFunc.orderAct($http, $scope, $, fMyPackage, $event, '/vip/order/cancel_refund/');
                    });*/

                };

                //重新购买
                $scope.doRebuy = function($event) {
                    //如果能拿到套餐类型，就可以跳到对应套餐选择页面
                    document.location.href = '/vip/role_info/';
                };

                //删除记录
                $scope.doDelete = function($event) {
                    pbFunc.orderAct($http, $scope, $, fMyPackage, $event, '/vip/order/delete/');
                };

                //我要续期
                $scope.doResume = function($event) {
                    /* pbFunc.orderAct($http, $scope, $, fMyPackage, $event, '/vip/order/resume/');*/
                    document.location.href = '/vip/role_info/';
                };

                //载入数据
                getModeData($http,
                    $scope.api_url,
                    "",
                    function(data) {
                        $scope.loadingThis = false;
                        fMyPackage.logList = data;
                        fMyPackage.loading = false;
                        $scope.loading = fMyPackage.loading;
                        $scope.logList = fMyPackage.logList;
                    });

                //$.Menu();

            }
        ]
    );

    app.controller(
        'myPackageDiyResume', ['$q', '$stateParams', '$scope', '$http', '$state', '$templateCache', 'fMyPackage',
            function($q, $stateParams, $scope, $http, $state, $templateCache, fMyPackage) {
                $scope.loading = fMyPackage.loading;
                $scope.loadingThis = true;
                $scope.chgStatus = 'all';
                $scope.orderId = $stateParams.orderId;

                //获取服务时长列表
                $scope.servicePeriodList = [{
                    n: 3,
                    selected: true
                }, {
                    n: 4,
                    selected: false
                }, {
                    n: 5,
                    selected: false
                }, {
                    n: 6,
                    selected: false
                }, {
                    n: 7,
                    selected: false
                }, {
                    n: 8,
                    selected: false
                }, {
                    n: 9,
                    selected: false
                }, {
                    n: 10,
                    selected: false
                }, {
                    n: 11,
                    selected: false
                }, {
                    n: 12,
                    selected: false
                }];

                //console.log('$scope', $scope);

                //获取默认时长和到期时间
                $scope.servicePeriod = '';
                $scope.serviceNow = '';
                $scope.serviceExpired = '';
                $scope.serviceNowTs = 0;
                $scope.serviceExpiredTs = 0;

                $scope.feedCount = 0;
                $scope.id = 0;
                $scope.monthPrice = 0;
                $scope.pinbotPoint = 0;
                $scope.vipName = '';
                $scope.payPrice = 0;

                $scope.payMethod = 'alipay';
                $scope.payType = 'diy';

                $scope.paynow = function() {
                    //console.log('paynow', $scope.payType, $scope.orderId);
                    /*if ($scope.payType == 'diy') {
                        //自助型续期
                        var postData = {
                            renew_month: parseInt($scope.servicePeriod)
                        };
                        orderPay($scope, $state, $http, $, postData, 'userModeDiyResumeOk', '/vip/renew/create/' + $scope.orderId + '/', 'json', 'userModeDiyResumeFailed');

                    }*/
                    $state.go(
                        'myPackageDiyResumePay', {}
                    );
                };

                $scope.$watch('payPrice', function(newValue, oldValue) {
                    if (newValue != oldValue) {
                        fMyPackage.payPrice = $scope.payPrice;
                        fMyPackage.servicePeriod = $scope.servicePeriod;
                    }
                    //console.log('watch payPrice', $scope.payPrice, newValue, oldValue, scope);
                });

                var getPackageInfo = pbFunc.getDataWithPromise($q, $http, '/vip/renew/info/' + $scope.orderId + '/');
                getPackageInfo.then(function(data) {
                    //console.log('getPackageInfo', data.data.active_time);
                    $scope.servicePeriod = '3';
                    //timestamp转成时间
                    $scope.serviceNowTs = data.data.expire_time['$date'];
                    $scope.serviceExpiredTs = data.data.expire_time['$date'];
                    $scope.serviceNow = pbFunc.formatDate('yyyy-MM-dd hh:mm:ss', $scope.serviceNowTs);

                    var expiredDateArr = pbFunc.getExpiredDateArr($scope.serviceNowTs, parseInt($scope.servicePeriod));
                    $scope.serviceExpiredTs = expiredDateArr[0];
                    $scope.serviceExpired = expiredDateArr[1];

                    $scope.feedCount = data.data.feed_count;
                    $scope.id = data.data.id;
                    $scope.monthPrice = data.data.month_price;
                    $scope.pinbotPoint = data.data.pinbot_point;
                    $scope.vipName = data.data.vip_name;
                    $scope.payPrice = parseInt($scope.servicePeriod) * parseInt(data.data.month_price);

                    fMyPackage.vipName = $scope.vipName;
                    fMyPackage.feedCount = $scope.feedCount;
                    fMyPackage.id = $scope.id;
                    fMyPackage.monthPrice = $scope.monthPrice;
                    fMyPackage.pinbotPoint = $scope.pinbotPoint;
                    fMyPackage.payPrice = $scope.payPrice;

                    fMyPackage.servicePeriod = $scope.servicePeriod;
                    fMyPackage.serviceNow = $scope.serviceNow;
                    fMyPackage.serviceExpired = $scope.serviceExpired;
                    fMyPackage.serviceNowTs = $scope.serviceNowTs;
                    fMyPackage.serviceExpiredTs = $scope.serviceExpiredTs;
                    fMyPackage.orderId = $scope.orderId;
                    //console.log('$scope',$scope);
                }, function(data) {
                    alert('暂无套餐信息，无法续期。');
                    history.go(-1);

                });

            }
        ]
    );

    app.controller(
        'myPackageDiyResumePay', ['$q', '$scope', '$http', '$state', 'fMyPackage',
            function($q, $scope, $http, $state, fMyPackage) {

                $scope.loadingThis = true;
                $scope.userCoin = false;
                $scope.payType = 'diy';

                if (fMyPackage.servicePeriod == '' || fMyPackage.orderId == '') {
                    document.location.href = '/payment/my_account/';
                    return false;
                }
                //console.log('fMyPackage', fMyPackage);

                //获取当前金币数
                var getUserInfo = pbFunc.getDataWithPromise($q, $http, "/vip/get_user_info/");
                getUserInfo.then(function(data) {
                    $scope.loadingThis = false;
                    fMyPackage.userInfo = data;
                    $scope.userInfo = fMyPackage.userInfo;
                    $scope.modeFee = fMyPackage.payPrice;

                }, function(data) {
                    //$.alert('<p class="alert-notice-center"><span>获取用户信息失败，请稍后再试！</span></p>');
                    alert('获取用户信息失败，请稍后再试！');
                    history.go(-1);
                });

                $scope.hoverMe = function($event, status) {
                    if (status === true) {
                        $($event.currentTarget).addClass('hover');
                    } else {
                        $($event.currentTarget).removeClass('hover');
                    }
                };

                $scope.choosePayMethod = function($event, method) {
                    $scope.payMethod = method;
                    if ($($event.currentTarget).hasClass('active')) {
                        $($event.currentTarget).removeClass('active');
                    } else {
                        $('.user-mode-pay').removeClass('active');
                        $($event.currentTarget).addClass('active');
                    }
                    $('.agreement-error').text('').css('display', 'none');
                };

                $scope.paynow = function() {
                    //console.log('paynow', $scope.payType, $scope.orderId);
                    if ($scope.payType == 'diy') {
                        //自助型续期
                        var postData = {
                            renew_month: parseInt(fMyPackage.servicePeriod)
                        };
                        orderPay($scope, $state, $http, $, postData, 'userModeDiyResumeOk', '/vip/renew/create/' + fMyPackage.orderId + '/', 'json', 'userModeDiyResumeFailed');

                    }
                };

                $scope.paynowold = function() {
                    //console.log('payMethod',$scope.payMethod);
                    if ($scope.payMethod == '') {
                        //$scope.userCoin = false;
                        $('.agreement-error').text('请先选择支付方式！').css('display', 'block');
                    } else {
                        //$scope.userCoin = true;
                        $('.agreement-error').text('').css('display', 'none');
                        if ($scope.payType == 'diy') {
                            //自助型
                            var product_type = fUserMode.currentOrderData.order_info.product_type;
                            var payment_terms = 'alipay';
                            if ($scope.coin > $scope.modeFee && $('#userCoin').prop('checked') === true) {
                                payment_terms = 'coin';
                            } else {
                                payment_terms = 'alipay';
                            }
                            /*console.log('payment_terms',payment_terms);
                            return false;*/
                            var is_insurance = 0;
                            var postData = {
                                'product_type': product_type,
                                'num': 1,
                                'pid': $scope.payPid,
                                'payment_terms': payment_terms,
                                'is_insurance': is_insurance
                            };
                            if (pbDebug) console.log('postData', fUserMode, postData);

                            orderPay($scope, $state, $http, $, postData, 'userModeDiyPayOk');

                        } else {
                            //省心型
                            //
                        }
                    }
                };

                $.Menu();

            }
        ]
    );

    app.controller(
        'userModeDiyResumeOk', ['$scope', '$http', '$state', 'fMyPackage',
            function($scope, $http, $state, fMyPackage) {

                $scope.reload = function() {
                    document.location.href = '/payment/my_package/';
                };

                if (fMyPackage.vipName == "") {
                    document.location.href = '/payment/my_account/';
                }

                /*fMyPackage.vipName = $scope.vipName;
                fMyPackage.feedCount = $scope.feedCount;
                fMyPackage.id = $scope.id;
                fMyPackage.monthPrice = $scope.monthPrice;
                fMyPackage.pinbotPoint = $scope.pinbotPoint;
                fMyPackage.payPrice = $scope.payPrice;
                fMyPackage.serviceExpired = $scope.serviceExpired;*/

                $scope.vipName = fMyPackage.vipName;
                $scope.feedCount = fMyPackage.feedCount;
                $scope.pinbotPoint = fMyPackage.pinbotPoint;
                $scope.serviceExpired = fMyPackage.serviceExpired;
                $scope.orderId = fMyPackage.orderId;

            }
        ]
    );

    app.controller(
        'userModeDiyResumeFailed', ['$scope', '$http', '$state', 'fMyPackage',
            function($scope, $http, $state, fMyPackage) {

                $scope.reload = function() {
                    document.location.href = '/payment/my_account/';
                };

                if (fMyPackage.vipName == "") {
                    document.location.href = '/payment/my_account/';
                }

                /*fMyPackage.vipName = $scope.vipName;
                fMyPackage.feedCount = $scope.feedCount;
                fMyPackage.id = $scope.id;
                fMyPackage.monthPrice = $scope.monthPrice;
                fMyPackage.pinbotPoint = $scope.pinbotPoint;
                fMyPackage.payPrice = $scope.payPrice;
                fMyPackage.serviceExpired = $scope.serviceExpired;*/

                $scope.vipName = fMyPackage.vipName;
                $scope.feedCount = fMyPackage.feedCount;
                $scope.pinbotPoint = fMyPackage.pinbotPoint;
                $scope.serviceExpired = fMyPackage.serviceExpired;
                $scope.orderId = fMyPackage.orderId;

            }
        ]
    );

    //directive
    app.directive('servicePeriod', function($templateCache) {
        return {
            restrict: 'E',
            templateUrl: '/static/users/servicePeriod.html',
            scope: {
                servicePeriodList: '=',
                orderId: '=',
                monthPrice: '='
            },
            replace: true,
            controller: function($scope, $element) {

                $scope.chooseServicePeriod = function($event, n) {
                    var trg = $event.currentTarget;
                    //console.log('chooseServicePeriod', angular.element(trg).parent().html());
                    for (var i = 0, imax = $scope.$parent.servicePeriodList.length; i < imax; i++) {
                        $scope.$parent.servicePeriodList[i].selected = false;
                        if ($scope.$parent.servicePeriodList[i].n == n) {
                            $scope.$parent.servicePeriodList[i].selected = true;
                            //获取到期时间

                            //更新，重新计算时间和价格
                            $scope.$parent.servicePeriod = '' + n + '';

                            var expiredDateArr = pbFunc.getExpiredDateArr($scope.$parent.serviceNowTs, parseInt(n));
                            $scope.$parent.serviceExpiredTs = expiredDateArr[0];
                            $scope.$parent.serviceExpired = expiredDateArr[1];

                            $scope.$parent.payPrice = parseInt(n) * parseInt($scope.$parent.monthPrice);

                            //break;
                        }
                    }

                };


            }
        }
    });

})();