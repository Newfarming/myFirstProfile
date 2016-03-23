(function(argument) {
    // body...

    var app = angular.module('app.coin_recharge', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter']),
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
                'coinRecharge', {
                    url: '/',
                    templateUrl: tmpl('payment/coin_recharge.html'),
                    controller: 'coinRecharge'
                }
            );
            //coinRechargeOk
            $stateProvider.state(
                'coinRechargeOk', {
                    url: '/ok/',
                    templateUrl: tmpl('payment/coin_recharge_ok.html'),
                    controller: 'coinRechargeOk'
                }
            );

        }
    ]);

    app.factory('fCoinRecharge', function() {
        return {
            //主页loading
            loading: true,
            //记录列表
            logList: {},
            modeFee: 0
        };
    });

    app.run(function($rootScope, $templateCache) {
        $rootScope.$on('$viewContentLoaded', function() {
            $templateCache.removeAll();
        });
    });

    app.controller(
        'coinRecharge', ['$scope', '$http', '$state', '$templateCache', 'fCoinRecharge',
            function($scope, $http, $state, $templateCache, fCoinRecharge) {
                $scope.loading = fCoinRecharge.loading;
                $scope.loadingThis = true;

                $scope.modeFee = 0;
                $scope.modeFeeCoin = 0;
                $scope.payMethod = 'alipay';
                $scope.chargeSuccess = false;

                $scope.chkCoinNum = function(t) {
                    var trg = $(t);
                    if (!trg.prop('value').match(/^[0-9]{1,6}$/i)) {
                        trg.prop('value', '0');
                    }
                };

                $scope.$watch('modeFee', function(newValue, oldValue, scope) {
                    if (newValue.toString().match(/^[0-9]{1,6}$/i)) {
                        fCoinRecharge.modeFee = parseInt(newValue);
                        $scope.modeFeeCoin = fCoinRecharge.modeFee;
                        $('.agreement-error').text('').css('display', 'none');
                    } else {
                        $scope.modeFeeCoin = 0;
                    }
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
                };

                $scope.paynow = function() {
                    //console.log('payMethod',$scope.payMethod);

                    if (fCoinRecharge.modeFee < 1) {
                        $('.agreement-error').text('请输入金币数量！').css('display', 'block');
                        return false;
                    } else {
                        $('.agreement-error').text('').css('display', 'none');
                    }

                    //自助型
                    var product_type = 'coin';
                    var payment_terms = 'alipay';
                    var postData = {
                        'product_type': product_type,
                        //除了充值金币，其它num都是1
                        'num': fCoinRecharge.modeFee,
                        'pid': 1,
                        'payment_terms': payment_terms,
                        'is_insurance': 0
                    };

                    orderPay($scope, $state, $http, $, postData, 'coinRechargeOk');

                };

            }
        ]
    );

    app.controller(
        'coinRechargeOk', ['$scope', '$http', '$state', 'fCoinRecharge',
            function($scope, $http, $state, fCoinRecharge) {
                $scope.modeFee = fCoinRecharge.modeFee;


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