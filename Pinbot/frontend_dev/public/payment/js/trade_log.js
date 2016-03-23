(function(argument) {
    // body...

    var app = angular.module('app.trade_log', ['app.config', 'ui.router'
        , 'app.django', 'app.utils'
        , 'app.filter']),
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
            //默认模式页面 我的套餐
            $stateProvider.state(
                'tradeLog', {
                    url: '/',
                    templateUrl: tmpl('payment/trade_log.html'),
                    controller: 'tradeLog'
                }
            );
            $stateProvider.state(
                'continuePayOk', {
                    url: '/continue_pay_ok/',
                    templateUrl: tmpl('payment/continue_pay_ok.html'),
                    controller: 'continuePayOk'
                }
            );
        }
    ]);

    app.factory('fTradeLog', function() {
        return {
            //主页loading
            loading: true,
            //记录列表
            logList: {},
        };
    });

    app.run(function($rootScope, $templateCache) {
        $rootScope.$on('$viewContentLoaded', function() {
            $templateCache.removeAll();
        });
    });

    app.controller(
        'tradeLog', ['$scope', '$http', '$state', '$templateCache', 'fTradeLog',
            function($scope, $http, $state, $templateCache, fTradeLog) {
                $scope.loading = fTradeLog.loading;
                $scope.loadingThis = true;
                $scope.chgType = 'all';
                $scope.chgStatus = 'all';

                $scope.api_url = "/payment/payment_record/";
                $scope.api_params = [];
                $scope.api_params_values = {};

                //删除交易记录
                /*$scope.delLog = function($event) {
                    var oid = $($event.currentTarget).attr('data-oid');
                    console.log('delLog oid', oid);
                    var postData = {
                        order_id: oid
                    };
                    if (confirm('确定删除记录？')) {
                        $scope.loadingThis = true;
                        postModeData($http, postData,
                            '/vip/order/delete/',
                            '',
                            function(data) {
                                if (data.status != undefined && data.status == 'ok') {
                                    //载入数据
                                    pbFunc.reloadList($http, $scope, fTradeLog);
                                } else {
                                    $scope.loadingThis = false;
                                    $.alert('<p class="alert-notice">删除记录失败，请稍后再试！[' + data.message + ']</p>');
                                }

                            }
                        );
                    }

                };*/

                //继续支付
                $scope.continuePay = function($event) {

                    var oid = $($event.currentTarget).attr('data-oid');
                    var postData = {
                        'order_id': oid
                    };
                    //console.log('postData',postData);
                    orderPay($scope, $state, $http, $, postData, 'continuePayOk', '/vip/order/repaid/');
                };

                $scope.listType = function($event, type) {
                    var trg = $($event.currentTarget);
                    $('.trade-type li').removeClass('active');
                    trg.parent().addClass('active');
                    $scope.chgType = type;
                    $scope.loadingThis = true;

                    //(1充值｜2提现｜3支付｜4收入)
                    if (type.toString().match(/^(-1|-2|4|5|7)$/i)) {
                        if (!inArray("record_type", $scope.api_params)) $scope.api_params.push("record_type");
                        $scope.api_params_values["record_type"] = type;
                    } else {
                        if (type == 'all') $scope.api_params.pop("record_type");
                    }

                    //载入数据
                    pbFunc.reloadList($http, $scope, fTradeLog);

                };

                $scope.listStatus = function($event, type) {
                    var trg = $($event.currentTarget);
                    $('.trade-status li').removeClass('active');
                    trg.parent().addClass('active');
                    $scope.chgStatus = type;
                    $scope.loadingThis = true;

                    //(unpay进行中|paid交易成功|fail交易失败|refund退款|cancel_refund取消退款|refunded退款成功|closed已关闭|canceled已取消|deleted已删除)
                    if (type.toString().match(/^(unpay|paid|fail|refund|cancel_refund|refunded|closed|canceled|deleted)$/i)) {
                        if (!inArray("order_status", $scope.api_params)) $scope.api_params.push("order_status");
                        $scope.api_params_values["order_status"] = type;
                    } else {
                        if (type == 'all') $scope.api_params.pop("order_status");
                    }
                    //载入数据
                    pbFunc.reloadList($http, $scope, fTradeLog);

                };

                $scope.nextPage = function(pageNum) {
                    pbFunc.nextPage($http, $scope, $, fTradeLog, pageNum);

                };

                //(unpay进行中|paid交易成功|fail交易失败|refund退款|cancel_refund取消退款|refunded退款成功|closed已关闭|canceled已取消|deleted已删除)
                $scope.defaultOrderStatus = function(order_status) {
                    if (order_status != '进行中' && order_status != '交易成功' && order_status != '交易失败' && order_status != '退款中' && order_status != '取消退款' && order_status != '退款成功' && order_status != '已关闭' && order_status != '已取消' && order_status != '已删除') {
                        return true;
                    } else {
                        return false;
                    }
                };



                $scope.hoverBtn = function($event, hover) {
                    /*var trg = $($event.currentTarget);
                    if (hover) {
                        trg.addClass('active');
                    } else {
                        trg.removeClass('active');
                    }
                    if ($scope.chgType == 'all' && !$('.trade-type li').hasClass('active')) {
                        $('.trade-type li:first-child').addClass('active');
                    }
                    if ($scope.chgStatus == 'all' && !$('.trade-status li').hasClass('active')) {
                        $('.trade-status li:first-child').addClass('active');
                    }*/
                };

                //载入数据
                getModeData($http,
                    $scope.api_url,
                    "",
                    function(data) {
                        $scope.loadingThis = false;
                        //console.log('logList',data);
                        fTradeLog.logList = data;
                        fTradeLog.loading = false;
                        $scope.loading = fTradeLog.loading;
                        $scope.logList = fTradeLog.logList;
                    });

            }
        ]
    );

    app.controller(
        'continuePayOk', ['$scope', '$http', '$state', '$templateCache', 'fTradeLog',
            function($scope, $http, $state, $templateCache, fTradeLog) {
                $scope.loading = fTradeLog.loading;
                $scope.loadingThis = true;

                $scope.backToLog = function() {
                    document.location.href = '/payment/trade_log/';
                };

            }
        ]
    );

    // 根据数字正负显示加减符号
    app.filter('numSign', function($sce) {
        return function(num) {
            if(parseInt(num)>=0){
                return "-"+parseInt(num);
            }else{
                return "+"+Math.abs(parseInt(num));
            }
        }
    });
})();


