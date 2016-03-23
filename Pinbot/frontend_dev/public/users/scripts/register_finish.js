(function(argument) {
    // body...

    var app = angular.module('app.register_finish', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter']),
        $django = angular.injector(['app.django', 'app.utils']),
        tmpl = $django.get('tmpl'),
        static_url = $django.get('static_url');

    //公用库
    //是否测试：第三方支付
    var mockTest = $django.get('mockTest');
    //是否测试：使用金币支付
    var mockTestWithCoin = $django.get('mockTestWithCoin');
    var confirmBox = $django.get('confirmBox');
    var alertBox = $django.get('alertBox');
    var getModeData = $django.get('getModeData');
    var postModeData = $django.get('postModeData');
    var pbFunc = $django.get('pbFunc');
    var orderPay = $django.get('orderPay');

    app.config([
        '$stateProvider', '$urlRouterProvider', '$httpProvider',
        function($stateProvider, $urlRouterProvider, $httpProvider) {
            var otherwiseUrl = '/';

            $httpProvider.defaults.cache = false;
            //initialize get if not there
            if (!$httpProvider.defaults.headers.get) {
                $httpProvider.defaults.headers.get = {};
            }
            //disable IE ajax request caching
            $httpProvider.defaults.headers.get['If-Modified-Since'] = '0';

            $urlRouterProvider.otherwise(otherwiseUrl);
            //默认模式页面
            /*$stateProvider.state(
                'registerFinish', {
                    url: '/',
                    templateUrl: tmpl('users/register_finish_main.html'),
                    controller: 'registerFinish'
                }
            );*/
        }
    ]);

    app.factory('fRegisterFinish', function() {
        return {
            //主页loading
            loading: true,
            data: {}

        };
    });

    app.run(function($rootScope, $templateCache) {
        $rootScope.$on('$viewContentLoaded', function() {
            $templateCache.removeAll();
        });
    });

    app.controller(
        'registerFinish', ['$scope', '$http', '$state', '$templateCache', 'fRegisterFinish',
            function($scope, $http, $state, $templateCache, fRegisterFinish) {
                $scope.loading = fRegisterFinish.loading;

                var oid = $('.extra_common_param').attr('data-oid');
                var order_price = $('.extra_common_param').attr('data-price');

                if ($('.layout').attr('data-invalid-order') == "true") {
                    //document.location.href='/vip/role_info/';
                }

                var postData2 = {
                    order_id: oid
                };
                $scope.isCharge = true;

                postModeData($http, postData2,
                    //创建订单接口
                    '/vip/order/get_order_status/',
                    '',
                    function(data2) {
                        console.log('coin_paid_order', data2);
                        if (data2.status != undefined && data2.status == 'ok' && data2.order_status == 'paid') {

                            if ($('.extra_common_param').attr('data-extra') == "pinbot_point") {
                                //购买聘点成功
                                //document.location.href = '/vip/role_info/';

                                $('.header h1').html('您的聘点购买成功！');
                                //$('.header .sub-title').html('您的聘点购买成功！');

                                var info = '<div class="payway_field">';
                                if (data2.pinbot_point != undefined) info += '<label>购买聘点：<span class="cf46c62">' + data2.pinbot_point + '</span>点<br><br>';
                                //info += '消费金币：<span  class="cf46c62">' + order_price + '金币</span>';
                                info + '</label></div>';
                                info += '<p class="form-control align-center" ><br><br><a class="btn btn-blue" href="/payment/my_account/">查看我的聘点</a></p>';

                                $('.box-content-info').html(info);


                            } else if ($('.extra_common_param').attr('data-extra') == "renew_service") {

                                $('.header h1').html('自助套餐续费成功！');

                                var info = '<div class="payway_field">';
                                /*if (data2.pinbot_point != undefined) info += '<label>购买聘点：<span class="cf46c62">' + data2.pinbot_point + '</span>点<br><br>';
                                //info += '消费金币：<span  class="cf46c62">' + order_price + '金币</span>';
                                info + '</label></div>';
                                info += '<p class="form-control align-center" ><br><br><a class="btn btn-blue" href="/payment/my_package/">查看我的套餐</a></p>';*/

                                info += '<div class="price content box-content lh180" >';
                                info += '    <img class="info-icon" src="/static/b_common/img/pinbot380x380_icon_resume_ok.png" border="0" width="180">';
                                info += '            <br>';
                                info += '    <span class="c607d8b f14">您是聘宝<a class="c63c2ec" href="javascript:void(0);">自助型会员</a>，现在您可以使用聘点下载简历了！快来试试吧！';
                                info += '    </span>';
                                info += '</div>';

                                info += '<p class="form-control align-center" >';
                                info += '    <a class="btn btn-welcome-submit" href="/special_feed/page/">我的职位定制</a>';
                                info += '</p>';

                                $('.box-content-info').html(info);

                            } else if ($('.extra_common_param').attr('data-extra') == "coin") {
                                //充值金币成功
                                //document.location.href = '/vip/role_info/';
                                $('.header h1').html('您的金币充值成功！');
                                //$('.header .sub-title').html('您的金币充值成功！');

                                var info = '<div class="payway_field"><label>充值金币：<span class="cf46c62">' + order_price + '</span>金币<br><br>支付金额：<span  class="cf46c62">' + order_price + '元</span></label></div>';
                                info += '<p class="form-control align-center" ><br><br><a class="btn btn-blue" href="/payment/my_account/#mycoin">查看我的金币</a></p>';

                                $('.box-content-info').html(info);
                            } else {
                                $scope.isCharge = false;
                            }
                        } else {
                            $.alert('<p class="alert-notice-center"><span>抱歉，您的支付尚未成功！</span></p>');

                            window.close();

                        }
                        $('.header').css('display', 'block');
                        $('.content').css('display', 'block');
                        $.Menu();
                    });

                $scope.repay = function($event) {
                    var url = $($event.currentTarget).attr('data-url');
                    var oid = $($event.currentTarget).attr('data-order-id');
                    //console.log('url',url);
                    var postData = {
                        'order_id': oid
                    };
                    postModeData($http, postData,
                        url,
                        '',
                        function(data) {

                            var pay_url = data.pay_url;
                            var order_id = data.order_id;
                            fRegisterFinish.data = data;

                            //如果是Alipay,打开支付新窗口
                            if (typeof pay_url == "string" && pay_url.match(/^https?:\/\//i)) {
                                window.open(pay_url, "_blank");
                            }

                            $.LayerOut({
                                html: confirmBox(
                                    '<span class="pay-alert"></span><span class="pay-title">请在新开页面上完成付款，付款完成前请勿关闭此窗口！</span>',
                                    '完成付款后请点击',
                                    '支付遇到问题',
                                    '',
                                    '我已完成付款',
                                    ''
                                ),
                                afterClose: function() {
                                    //$._LayerOut.close();
                                    /*$state.go(
                                        'userModeDiyPayOk', {}
                                    );*/
                                }
                            });

                            $(".modal").undelegate(".btn-pay-problem").delegate(".btn-pay-problem", "click", function(e) {
                                //console.log('payProblem', e);
                                $('.header h1').html('<span class="pay-failed"></span>Sorry...支付失败');
                                $._LayerOut.close();
                                //return false;
                            });
                            $(".modal").undelegate(".btn-pay-ok").delegate(".btn-pay-ok", "click", function(e) {
                                //console.log('paySuccess', e);
                                $._LayerOut.close();
                                $('.header h1').html('支付成功！恭喜您成为聘宝会员！');
                                var payOkData = '';
                                payOkData += '<div class="payway_field">';
                                payOkData += '<label>立即完成新手任务，领<span class="cf46c62">现金红包！</span></label>';
                                payOkData += '</div>';
                                payOkData += '<div class="confirm_pay pd-top-20">';
                                payOkData += '<a href="' + $('.layout').attr('data-tutorial-url') + '" class="btn btn-welcome-submit">开始新手任务</a>';
                                payOkData += '</div>';
                                $('.box-content').html(payOkData);
                            });

                        }
                    );
                };

            }
        ]
    );

})();

