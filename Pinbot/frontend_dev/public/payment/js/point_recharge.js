(function(argument) {
    // body...

    var app = angular.module('app.point_recharge', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter']),
        $django = angular.injector(['app.django', 'app.utils']),
        tmpl = $django.get('tmpl'),
        static_url = $django.get('static_url');

    //公用库
    var mockTest = $django.get('mockTest');
    //是否测试：使用金币支付
    var mockTestWithCoin = $django.get('mockTestWithCoin');
    var confirmBox = $django.get('confirmBox');
    var alertBox = $django.get('alertBox');
    var getModeData = $django.get('getModeData');
    var postModeData = $django.get('postModeData');
    //var pbFunc = $django.get('pbFunc');
    var inArray = $django.get('inArray');
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
            //默认模式页面 我的套餐
            $stateProvider.state(
                'pointRecharge', {
                    url: '/',
                    templateUrl: tmpl('payment/point_recharge.html'),
                    controller: 'pointRecharge'
                }
            );
            //pointRechargeOk
            $stateProvider.state(
                'pointRechargeOk', {
                    url: '/ok/',
                    templateUrl: tmpl('payment/point_recharge_ok.html'),
                    controller: 'pointRechargeOk'
                }
            );

        }
    ]);

    app.factory('fPointRecharge', function() {
        return {
            //主页loading
            loading: true,
            //记录列表
            logList: {},
            myPoint: 0,
            myCoin: 0,
            modeFee: 0
        };
    });

    app.run(function($rootScope, $templateCache) {
        $rootScope.$on('$viewContentLoaded', function() {
            $templateCache.removeAll();
        });
    });

    app.controller(
        'pointRecharge', ['$scope', '$http', '$state', '$templateCache', 'fPointRecharge',
            function($scope, $http, $state, $templateCache, fPointRecharge) {
                $scope.loading = fPointRecharge.loading;
                $scope.loadingThis = true;

                //我的聘点
                $scope.myPoint = 0;
                //我的金币
                $scope.coin = 0;
                //消费额
                $scope.modeFee = 100;//400;
                //消费聘点
                $scope.modePoint = 50;//200;
                //消费金币
                $scope.modeCoin = 0;
                //下载简历数
                $scope.modeResume = 5;//20;
                //是否使用金币
                $scope.userCoin = false;

                fPointRecharge.modeFee = $scope.modeFee;
                fPointRecharge.modePoint = $scope.modePoint;
                fPointRecharge.modeResume = $scope.modeResume;

                if ($('.layout').attr('data-point').match(/([0-9]+)$/i)) {
                    $scope.myPoint = parseInt(RegExp.$1);
                    fPointRecharge.myPoint = $scope.myPoint;
                }

                if ($('.layout').attr('data-coin').match(/([0-9]+)$/i)) {
                    $scope.coin = (mockTestWithCoin) ? 100 : parseInt(RegExp.$1);
                    fPointRecharge.myCoin = $scope.coin;
                }

                $scope.payMethod = 'alipay';
                $scope.chargeSuccess = false;

                //聘点套餐
                $scope.modeListMinor = [{
                    id: 1,
                    point: 50,//200,
                    price: 100,//400,
                    oldPrice: 0,
                    resume: 5//20
                }];

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
                };

                //clickMode($event,mode.pid)
                $scope.clickMode = function($event, pid, point, price, resume) {

                    if ($('.user-mode-small-point-' + pid).hasClass('selected')) {
                        $scope.modeFee = 0;
                        $scope.modePoint = 0;
                        $scope.modeResume = 0;
                        $('.user-mode-small-point').removeClass('selected');
                        fPointRecharge.modeFee = $scope.modeFee;
                        fPointRecharge.modePoint = $scope.modePoint;
                        fPointRecharge.modeResume = $scope.modeResume;
                    } else {
                        $scope.modeFee = price;
                        $scope.modePoint = point;
                        $scope.modeResume = resume;
                        $('.user-mode-small-point').removeClass('selected');
                        $('.user-mode-small-point-' + pid).addClass('selected');

                        fPointRecharge.modeFee = $scope.modeFee;
                        fPointRecharge.modePoint = $scope.modePoint;
                        fPointRecharge.modeResume = $scope.modeResume;
                    }

                };

                var confirmPayByCoin = function(cb) {
                    //var trg = $('#userCoin');
                    var patTrg = ($('#userCoin').prop('checked') === true) ? '金币' : '元';
                    //if (trg.prop('checked') == true) {
                    $.LayerOut({
                        html: alertBox(
                            '<span class="pay-alert"></span><span class="pay-title">需要您的确认！</span>',
                            '',
                            '您选购了：<span class="cf46c62">' + $scope.modePoint + '</span> 聘点<br>需要支付：<span class="cf46c62">' + $scope.modeFee + '</span> ' + patTrg,
                            '确认购买'
                        ),
                        afterClose: function() {
                            //$._LayerOut.close();

                        }
                    });

                    $(".modal").undelegate(".btn-click-ok").delegate(".btn-click-ok", "click", function(e, $scope) {
                        $._LayerOut.close();
                        //$('#payNow').trigger('click');
                        if (typeof cb == 'function') {
                            cb();
                        }
                    });
                    //}
                };

                $scope.paynow = function() {
                    console.log('payMethod', $scope.payMethod);

                    confirmPayByCoin(function() {
                        console.log('confirmPayByCoin', 1);
                        if (fPointRecharge.modeFee < 1) {
                            $('.agreement-error').text('请选择购买套餐！').css('display', 'block');
                            return false;
                        } else {
                            $('.agreement-error').text('').css('display', 'none');
                        }

                        if ($scope.payMethod == '') {
                            $('.agreement-error').text('请选择支付方式！').css('display', 'block');
                            return false;
                        } else {
                            $('.agreement-error').text('').css('display', 'none');
                        }

                        if ($scope.coin > $scope.modeFee && $('#userCoin').prop('checked') === true) {
                            //使用金币购买
                            var product_type = 'pinbot_point';
                            var payment_terms = 'coin';
                            var postData = {
                                'product_type': product_type,
                                'num': 1, //fPointRecharge.modeFee,
                                'pid': 1,
                                'payment_terms': payment_terms,
                                'is_insurance': 0
                            };

                        } else {
                            //
                            var product_type = 'pinbot_point';
                            var payment_terms = 'alipay';
                            var postData = {
                                'product_type': product_type,
                                'num': 1, //fPointRecharge.modeFee,
                                'pid': 1,
                                'payment_terms': payment_terms,
                                'is_insurance': 0
                            };

                        }
                        //console.log('postData',postData);
                        orderPay($scope, $state, $http, $, postData, 'pointRechargeOk');
                    });

                };

            }
        ]
    );

    app.controller(
        'pointRechargeOk', ['$scope', '$http', '$state', 'fPointRecharge',
            function($scope, $http, $state, fPointRecharge) {
                $scope.modeFee = fPointRecharge.modeFee;
                $scope.modePoint = fPointRecharge.modePoint;
                $scope.modeCoin = fPointRecharge.modeCoin;
                $scope.modeResume = fPointRecharge.modeResume;

                //清除数据

                /*//用户所选模式列表
                fUserMode.choosedModeList = [];
                //用户所选模式次要列表
                fUserMode.choosedModeListMinor = [];
                //主页loading
                fUserMode.loading = true;
                //订单内容
                fUserMode.currentOrderData = {};
                fUserMode.chooseOneModeId = 0;
                fUserMode.chooseOneModeType = '';
                fUserMode.modeFee = 0;*/
            }
        ]
    );

})();

/*

 */