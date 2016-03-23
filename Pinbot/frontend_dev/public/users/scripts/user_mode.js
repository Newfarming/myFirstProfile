(function(argument) {
    // body...

    var app = angular.module('app.user_mode', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter']),
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
    var pbLib = $django.get('pbLib');
    var orderPay = $django.get('orderPay');

    app.config([
        '$stateProvider', '$urlRouterProvider', '$httpProvider',
        function($stateProvider, $urlRouterProvider, $httpProvider) {
            var otherwiseUrl = '/';

            /*$httpProvider.defaults.cache = false;
            //initialize get if not there
            if (!$httpProvider.defaults.headers.get) {
                $httpProvider.defaults.headers.get = {};
            }
            //disable IE ajax request caching
            $httpProvider.defaults.headers.get['If-Modified-Since'] = '0';*/

            $urlRouterProvider.otherwise(otherwiseUrl);
            //默认模式页面
            $stateProvider.state(
                'userMode', {
                    url: '/',
                    templateUrl: tmpl('users/user_mode.html'),
                    controller: 'userMode'
                }
            );
            //自助模式列表页面
            $stateProvider.state(
                'userModeDiy', {
                    url: '/usermode_diy/',
                    templateUrl: tmpl('users/user_mode_diy.html'),
                    controller: 'userModeDiy'
                }
            );
            //自助模式购买页面
            $stateProvider.state(
                'userModeDiyPay', {
                    url: '/usermode_diy_pay/',
                    templateUrl: tmpl('users/user_mode_diy_pay.html'),
                    controller: 'userModeDiyPay'
                }
            );
            //userModeDiyPayOk
            $stateProvider.state(
                'userModeDiyPayOk', {
                    url: '/usermode_diy_pay_ok/',
                    templateUrl: tmpl('users/user_mode_diy_pay_ok.html'),
                    controller: 'userModeDiyPayOk'
                }
            );
            //省心模式列表页面
            $stateProvider.state(
                'userModeNoWorry', {
                    url: '/usermode_noworry/',
                    templateUrl: tmpl('users/user_mode_noworry.html'),
                    controller: 'userModeNoWorry'
                }
            );
            //省心模式提交页面
            $stateProvider.state(
                'userModeNoWorrySubmit', {
                    /*url: '/usermode_noworry_submit/:order_id/:order_price',*/
                    url: '/usermode_noworry_submit/',
                    templateUrl: tmpl('users/user_mode_noworry_submit.html'),
                    controller: 'userModeNoWorrySubmit'
                }
            );
        }
    ]);

    app.factory('fUserMode', function() {
        return {
            //自助模式列表
            listDiy: [],
            //省心模式列表
            listNoworry: [],
            //用户所选模式列表
            choosedModeList: [],
            //用户所选模式次要列表
            choosedModeListMinor: [],
            //主页loading
            loading: true,
            //订单内容
            currentOrderData: {},
            //套餐ID
            chooseOneModeId: 0,
            //套餐类型
            chooseOneModeType: '',
            //套餐名称
            chooseOneModeName: '',
            //付费金额
            modeFee: 0,
            //所选时长
            servicePeriod: '',
            //到期时间
            serviceExpired: ''
        };
    });

    app.run(function($rootScope, $templateCache) {
        $rootScope.$on('$viewContentLoaded', function() {
            $templateCache.removeAll();
        });
    });



    app.controller(
        'userMode', ['$scope', '$http', '$state', '$templateCache', 'fUserMode',
            function($scope, $http, $state, $templateCache, fUserMode) {
                //console.log('fUserMode', fUserMode);
                $scope.loading = fUserMode.loading;

                $scope.basePriceDiy = 0;
                $scope.basePriceNoworry = 0;

                $scope.loadingDiy = true;
                $scope.loadingNoworry = true;

                //检查url是否包含用户名
                if (document.location.href.toString().match(/\?username=([0-9a-z_%@\.\-]+)/i)) {
                    var username = unescape(RegExp.$1).replace(/[^0-9a-z@_\.\-]/ig, "");
                    pbLib.setCookie('add_user', username);
                }

                //查找自助套餐最低价
                getModeData($http,
                    "/vip/get_self_service_select/",
                    "",
                    function(data) {
                        fUserMode.listDiy = data.data;
                        pbFunc.minPrice($scope, data.data, 'basePriceDiy');
                        $scope.loadingDiy = false;

                        //查找省心套餐最低价
                        getModeData($http,
                            "/vip/get_manual_service_select/",
                            "",
                            function(data2) {
                                fUserMode.listNoworry = data2.data;
                                pbFunc.minPrice($scope, data2.data, 'basePriceNoworry');
                                $scope.loadingNoworry = false;
                            }
                        );
                    }
                );

                //进入套餐页面
                $scope.chooseUserMode = function($event, type) {

                    $('.user-mode').removeClass('selected');
                    $('.user-mode-' + type).addClass('selected');

                    //var api_url = "/vip/get_manual_service_select/";
                    //var has_url = "#/usermode_noworry/";
                    var trgController = 'userModeNoWorry';
                    fUserMode.choosedModeList = fUserMode.listNoworry;
                    if (type.match(/^diy$/i)) {
                        fUserMode.choosedModeList = fUserMode.listDiy;
                        //api_url = "/vip/get_self_service_select/";
                        //has_url = "#/usermode_diy/";
                        trgController = 'userModeDiy';
                    }
                    fUserMode.loading = false;
                    $scope.loading = fUserMode.loading;
                    $state.go(
                        trgController, {}
                    );
                    /*getModeData($http,
                        api_url,
                        has_url,
                        function(data) {
                            fUserMode.choosedModeList = data.data;
                            fUserMode.loading = false;
                            $scope.loading = fUserMode.loading;
                        });*/
                };
            }
        ]
    );

    app.controller(
        'userModeDiy', ['$scope', '$http', '$state', '$templateCache', 'fUserMode',
            function($scope, $http, $state, $templateCache, fUserMode) {
                //$templateCache.remove('/usermode_noworry/');
                //$templateCache.removeAll();

                //是否显示loading
                $scope.loadingThis = true;
                //受否进行选取操作
                $scope.chooseOneMode = false;
                //选取的Id
                $scope.chooseOneModeId = 0;
                //选取的类型
                $scope.chooseOneModeType = '';
                $scope.chooseOneModeName = '';
                $scope.modeFee = 0;
                $scope.agreementChecked = true;

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

                //获取默认时长和到期时间
                $scope.servicePeriod = '3';
                $scope.serviceExpired = '2016-10-29 00:00:00';

                if (fUserMode.choosedModeList.length == 0) {
                    //if (pbDebug) console.log('choosedModeList', fUserMode.choosedModeList);
                    getModeData($http,
                        '/vip/get_self_service_select/',
                        '',
                        function(data) {
                            pbFunc.updateUserModeList(fUserMode, $scope, data, null, null);
                        }
                    );
                } else {
                    $scope.loadingThis = false;
                }
                $scope.modeList = fUserMode.choosedModeList;
                //if(pbDebug) console.log('userModeDiy',$scope.modeList);

                //clickMode($event,mode.pid)
                $scope.clickMode = function($event, type, pid, fee, name, allowBuy, has_manual_service) {
                    //if(pgDebug) console.log('clickMode', type, pid);

                    if (has_manual_service) {
                        pbFunc.orderActAlert($http, $scope, $, '购买失败', '', '您正在使用省心型套餐，不能购买自助型套餐，有疑问，请咨询<a href="javascript:void(0);" id="JS_pbqqdiy_btn" class="c63c2ec">聘宝人才顾问</a>！', '确定', function() {
                            $._LayerOut.close();
                        });
                    } else {
                        if (allowBuy) {
                            if ($('.user-mode-small-' + pid).hasClass('selected')) {
                                $('.user-mode-small').removeClass('selected');
                                $scope.chooseOneModeId = 0;
                                $scope.chooseOneModeType = '';
                                $scope.chooseOneModeName = '';
                                $scope.chooseOneMode = false;
                                $scope.modeFee = 0;
                                fUserMode.chooseOneModeId = $scope.chooseOneModeId;
                                fUserMode.chooseOneModeType = $scope.chooseOneModeType;
                                fUserMode.chooseOneModeName = $scope.chooseOneModeName;
                                fUserMode.modeFee = $scope.modeFee;
                            } else {
                                //todo: 已经是自助B模式的会员了，再选择升级服务时，就不能再选择同一模式了，只能往更高（更贵）的自助模式选择或者选择省心型
                                //if (pbFunc.canBuyDiy(pid, fUserMode.choosedModeList, fUserMode.chooseOneModeId)) {
                                $scope.chooseOneModeId = parseInt(pid);
                                $scope.chooseOneModeType = type;
                                $scope.chooseOneModeName = name;
                                $('.user-mode-small').removeClass('selected');
                                $('.user-mode-small-' + pid).addClass('selected');
                                $scope.chooseOneMode = true;
                                $scope.modeFee = fee;
                                fUserMode.chooseOneModeId = $scope.chooseOneModeId;
                                fUserMode.chooseOneModeType = $scope.chooseOneModeType;
                                fUserMode.chooseOneModeName = $scope.chooseOneModeName;
                                fUserMode.modeFee = $scope.modeFee;
                                //} else {
                                //$.alert('<p class="alert-notice-center"><span>购买！</span></p>');
                                /*pbFunc.pbAlert($http, $scope, $, '购买失败', '', '请选择更高级别的套餐购买！', '确定', function(){

                                    });*/
                                //}


                            }
                        } else {
                            //$.alert('<p class="alert-notice-center"><span>请选择更高级别的套餐购买！</span></p>');
                            pbFunc.orderActAlert($http, $scope, $, '购买失败', '', '请选择更高级别的套餐购买！', '确定', function() {
                                $._LayerOut.close();
                            });
                        }
                    }


                };

                //购买前确认
                $scope.clickToPayAfterConfirm = function(type) {
                    if ($('#agreement').prop('checked') === false) {
                        $scope.agreementChecked = false;
                        $('#agreement-error').text('请先同意聘宝套餐用户协议').css('display', 'block');
                    } else {
                        $scope.agreementChecked = true;
                        $('#agreement-error').text('').css('display', 'none');
                        if (type == 'diy') {
                            var customizeNum = 0;
                            var weeklyPoint = 0;
                            var serviceMonth = 0;
                            for (var i = 0, imax = fUserMode.choosedModeList.length; i < imax; i++) {
                                var curItem = fUserMode.choosedModeList[i];
                                if (curItem.pid == fUserMode.chooseOneModeId) {
                                    customizeNum = curItem.feed_count;
                                    weeklyPoint = curItem.pinbot_point;
                                    serviceMonth = fUserMode.servicePeriod;
                                    break;
                                }
                            }
                            var html = "";
                            html += '<div class="price content box-content box-content-table box-content-table-box pd-top-0 lh180">';
                            html += '<div class="modal-line-big text-center"><span class="f18 c42b4e6">' + fUserMode.chooseOneModeName + '</span></div>';
                            html += '<div class="box-col box-col-center">';
                            html += '<div class="user-mode">';
                            html += '<ul>';
                            html += '    <li class="text-center">';
                            html += '        <span>定制数量</span>';
                            html += '        <span><span class="cf46c62">' + customizeNum + '</span>个</span>';
                            html += '    </li>';
                            html += '    <li class="text-center">';
                            html += '        <span>每周可使用聘点</span>';
                            html += '        <span><span class="cf46c62">' + weeklyPoint + '</span>点</span>';
                            html += '    </li>';
                            html += '    <li class="text-center">';
                            html += '        <span>服务时长</span>';
                            html += '        <span><span class="cf46c62">' + serviceMonth + '</span>个月</span>';
                            html += '    </li>';
                            html += '</ul>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div class="modal-line text-center">服务有效期至：<span class="cf46c62">' + fUserMode.chooseOneModeName + '</span><br></div>';
                            html += '<div class="modal-line text-center">服务费用：<span class="cf46c62">¥ ' + fUserMode.modeFee + '</span></div>';
                            html += '</div>';

                            pbFunc.pbAlert($http, $scope, $, '请确认您要购买的套餐！', '', html, '确认购买', function() {
                                //自助型
                                getModeData($http,
                                    '/vip/self/info/?pid=' + $scope.chooseOneModeId,
                                    '#/usermode_diy_pay/',
                                    function(data) {
                                        //console.log('currentOrderData', data);
                                        fUserMode.currentOrderData = data;
                                        $scope.currentOrderData = fUserMode.currentOrderData;
                                        $scope.loadingThis = false;
                                    }
                                );
                            });

                        } else {
                            //省心型

                        }
                    }
                };

                //购买不用确认
                $scope.clickToPay = function(type) {
                    if ($('#agreement').prop('checked') === false) {
                        $scope.agreementChecked = false;
                        $('#agreement-error').text('请先同意聘宝套餐用户协议').css('display', 'block');
                    } else {
                        $scope.agreementChecked = true;
                        $('#agreement-error').text('').css('display', 'none');
                        if (type == 'diy') {
                            //自助型
                            getModeData($http,
                                '/vip/self/info/?pid=' + $scope.chooseOneModeId,
                                '#/usermode_diy_pay/',
                                function(data) {
                                    //console.log('currentOrderData', data);
                                    fUserMode.currentOrderData = data;
                                    $scope.currentOrderData = fUserMode.currentOrderData;
                                    $scope.loadingThis = false;
                                }
                            );
                        } else {
                            //省心型
                        }
                    }
                };

                $scope.checkAgreement = function($event) {
                    //if(pbDebug) console.log('checkAgreement',$('#agreement').prop('checked'));
                    if ($scope.agreementChecked === false) {
                        $scope.agreementChecked = true;
                        $('#agreement-error').text('').css('display', 'none');
                    } else {
                        $scope.agreementChecked = false;
                    }
                };

                $scope.goNoWorryMode = function() {
                    fUserMode.choosedModeList = [];
                    fUserMode.choosedModeListMinor = [];
                    $scope.loadingThis = true;
                    getModeData($http,
                        '/vip/get_self_service_select/',
                        '',
                        function(data) {

                            pbFunc.updateUserModeList(fUserMode, $scope, data, function() {
                                $state.go(
                                    'userModeNoWorry', {}
                                );
                            }, null);

                            //fUserMode.choosedModeList = data.data;
                            //$scope.modeList = fUserMode.choosedModeList;
                            //$scope.loadingThis = false;
                            /*$state.go(
                                'userModeNoWorry', {}
                            );*/
                            //document.location.href='/vip/role_info/#/usermode_noworry/';
                        }
                    );
                };

                //切换时长
                /*$scope.chooseServicePeriod = function($event, n) {
                    var trg = $event.currentTarget;
                    //console.log('chooseServicePeriod', angular.element(trg).parent().html());
                    for (var i = 0, imax = $scope.servicePeriodList.length; i < imax; i++) {
                        $scope.servicePeriodList[i].selected = false;
                        if ($scope.servicePeriodList[i].n == n) {
                            $scope.servicePeriodList[i].selected = true;
                            //获取到期时间

                            //更新
                            //$scope.servicePeriod = '3';
                            //$scope.serviceExpired = '2016-10-29 00:00:00';
                        }
                    }

                };*/

            }
        ]
    );

    app.controller(
        'userModeDiyPay', ['$scope', '$http', '$state', 'fUserMode',
            function($scope, $http, $state, fUserMode) {
                //console.log('currentOrderData2',fUserMode.currentOrderData);

                $scope.userCoin = false;

                if (fUserMode != undefined && fUserMode.chooseOneModeId != undefined && fUserMode.currentOrderData.coin != undefined) {

                    //是否显示loading
                    $scope.loadingThis = true;
                    $scope.payPid = fUserMode.chooseOneModeId;
                    $scope.payType = fUserMode.chooseOneModeType;
                    $scope.payName = fUserMode.chooseOneModeName;
                    $scope.modeFee = fUserMode.modeFee;
                    $scope.coin = (mockTestWithCoin) ? 1000 : fUserMode.currentOrderData.coin;
                    $scope.payMethod = 'alipay';
                } else {
                    $state.go(
                        'userMode', {}
                    );
                }

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
        'userModeDiyPayOk', ['$scope', '$http', '$state', 'fUserMode',
            function($scope, $http, $state, fUserMode) {
                //console.log('currentOrderData2',fUserMode.currentOrderData);
                $scope.feed_count = 0;
                $scope.pinbot_point = 0;

                pbFunc.currentDiySet($scope, fUserMode.chooseOneModeId, fUserMode.choosedModeList);

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
                fUserMode.chooseOneModeName = '';
                fUserMode.modeFee = 0;*/
            }
        ]
    );

    app.controller(
        'userModeNoWorry', ['$rootScope', '$scope', '$http', '$state', '$templateCache', 'fUserMode',
            function($rootScope, $scope, $http, $state, $templateCache, fUserMode) {
                //$templateCache.remove('/usermode_diy/');
                //$templateCache.removeAll();

                //检查url是否包含用户名
                $scope.username = '';
                if (document.location.href.toString().match(/\?username=([0-9a-z_%@\.\-]+)/i)) {
                    var username = unescape(RegExp.$1).replace(/[^0-9a-z@_\.\-]/ig, "");
                    pbLib.setCookie('add_user', username);
                    $scope.username = username;
                }

                //是否显示loading
                $scope.loadingThis = true;
                //受否进行选取操作
                $scope.chooseOneMode = false;
                //选取的Id
                $scope.chooseOneModeId = 0;
                //选取的类型
                $scope.chooseOneModeType = '';
                $scope.chooseOneModeName = '';
                $scope.chooseCandidateNum = 1;
                $scope.modeFee = 0;
                $scope.packagePrice = 0;
                $scope.agreementChecked = true;

                if (pbDebug) console.log('userModeNoWorry choosedModeList', fUserMode.choosedModeList);

                if (fUserMode.choosedModeListMinor.length == 0) {
                    //if (pbDebug) console.log('choosedModeList', fUserMode.choosedModeList);
                    getModeData($http,
                        '/vip/get_manual_service_select/',
                        '',
                        function(data) {
                            fUserMode.choosedModeList = []; //data.data;
                            fUserMode.choosedModeListMinor = []; //data.data;

                            for (var i = 0, imax = data.data.length; i < imax; i++) {
                                //if (data.data[i].is_commend == true) {
                                //    fUserMode.choosedModeList.push(data.data[i]);
                                //} else {
                                fUserMode.choosedModeListMinor.push(data.data[i]);
                                //}
                            }

                            //$scope.modeListRec = fUserMode.choosedModeList;
                            $scope.modeListMinor = fUserMode.choosedModeListMinor;
                            $scope.loadingThis = false;

                            //if (pbDebug) console.log('modeListRec', $scope.modeListRec);
                            //if (pbDebug) console.log('modeListMinor', $scope.modeListMinor);
                        }
                    );
                } else {
                    $scope.loadingThis = false;
                    var modeList = fUserMode.choosedModeList;

                    //$scope.modeListRec = [];
                    $scope.modeListMinor = [];
                    for (var i = 0, imax = modeList.length; i < imax; i++) {
                        //if (modeList[i].is_commend == true) {
                        //    $scope.modeListRec.push(modeList[i]);
                        //} else {
                        $scope.modeListMinor.push(modeList[i]);
                        //}
                    }
                    fUserMode.choosedModeListMinor = $scope.modeListMinor;
                    //if (pbDebug) console.log('modeListRec', $scope.modeListRec);
                    //if (pbDebug) console.log('modeListMinor', $scope.modeListMinor);

                }
                //if(pbDebug) console.log('fUserMode',fUserMode);

                //clickMode($event,mode.pid)
                $scope.clickMode = function($event, type, pid, fee, num, name) {
                    //console.log('clickMode', type, pid, fee);
                    if ($('.user-mode-small-' + pid).hasClass('selected')) {
                        $scope.chooseCandidateNum = 1;
                        $scope.chooseOneModeId = 0;
                        $scope.chooseOneModeType = '';
                        $scope.chooseOneModeName = '';
                        $('.user-mode-small').removeClass('selected');
                        $scope.chooseOneMode = false;
                        $scope.modeFee = 0;
                        $scope.packagePrice = 0;
                        fUserMode.chooseOneModeId = $scope.chooseOneModeId;
                        fUserMode.chooseOneModeType = $scope.chooseOneModeType;
                        fUserMode.chooseOneModeName = $scope.chooseOneModeName;
                        fUserMode.modeFee = $scope.modeFee;
                    } else {
                        $scope.chooseCandidateNum = parseInt(num);
                        $scope.chooseOneModeId = parseInt(pid);
                        $scope.chooseOneModeType = type;
                        $scope.chooseOneModeName = name;
                        $('.user-mode-small').removeClass('selected');
                        $('.user-mode-small-' + pid).addClass('selected');
                        $scope.chooseOneMode = true;
                        $scope.modeFee = fee;
                        $scope.packagePrice = fee;
                        fUserMode.chooseOneModeId = $scope.chooseOneModeId;
                        fUserMode.chooseOneModeType = $scope.chooseOneModeType;
                        fUserMode.chooseOneModeName = $scope.chooseOneModeName;

                        //console.log('checked',$('#useGuarantee').prop('checked'));
                        if ($('#useGuarantee').prop('checked') === true) {
                            $('.useGuaranteeInfo').text('已选择购买');
                            $scope.modeFee = $scope.packagePrice + 500 * $scope.chooseCandidateNum;
                        } else {
                            $('.useGuaranteeInfo').text('选择购买');
                            $scope.modeFee = $scope.packagePrice;
                        }
                        fUserMode.modeFee = $scope.modeFee;
                    }

                    //检查cookie是否包含用户名
                    if (pbLib.getCookie('add_user') != null) {
                        $scope.username = pbLib.getCookie('add_user');
                    }

                };

                //
                $scope.clickToPay = function(type) {
                    if ($('#agreement').prop('checked') === false) {
                        $scope.agreementChecked = false;
                        $('#agreement-error').text('请先同意聘宝套餐用户协议').css('display', 'block');
                    } else {
                        $scope.agreementChecked = true;
                        $('#agreement-error').text('').css('display', 'none');
                        if (type == 'diy') {
                            //自助型

                        } else {
                            //省心型
                            var product_type = $scope.chooseOneModeType;
                            //支付方式：alipay weixin coin offline
                            var payment_terms = 'offline';
                            var is_insurance = ($('#useGuarantee').prop('checked') === true) ? 1 : 0;
                            if (is_insurance == 1) {
                                $('.useGuaranteeInfo').text('已选择购买');
                                $scope.modeFee = $scope.packagePrice + 500 * $scope.chooseCandidateNum;
                            } else {
                                $('.useGuaranteeInfo').text('选择购买');
                                $scope.modeFee = $scope.packagePrice;
                            }
                            fUserMode.modeFee = $scope.modeFee;

                            var username = $('#username').val().replace(/[^0-9a-z@_\.\-]/ig, "");
                            var postData = {
                                'username': username,
                                'product_type': product_type,
                                'num': 1,
                                'pid': $scope.chooseOneModeId,
                                'payment_terms': payment_terms,
                                'is_insurance': is_insurance
                            };
                            if (pbDebug) console.log('postData', fUserMode, postData);
                            postModeData($http, postData,
                                //创建订单接口
                                '/vip/order/admin_create/', //'/vip/create_user_order/',
                                '',
                                function(data) {
                                    if (pbDebug) console.log('diy paynow', data);
                                    if (data.status != undefined && data.status == 'ok') {
                                        fUserMode.modeFee = data.order_price;
                                        $state.go(
                                            'userModeNoWorrySubmit', {
                                                /*order_id: data.order_id,
                                                order_price: data.order_price*/
                                            }
                                        );
                                    } else {
                                        $.alert('<p class="alert-notice-center"><span>创建订单失败，请稍后再试！</span></p>');
                                    }
                                    $scope.loadingThis = false;
                                }
                            );
                        }
                    }
                };

                $scope.chooseGuarantee = function() {
                    if ($('#useGuarantee').prop('checked') === true) {
                        $('.useGuaranteeInfo').text('已选择购买');
                        $scope.modeFee = $scope.packagePrice + 500 * $scope.chooseCandidateNum;
                    } else {
                        $('.useGuaranteeInfo').text('选择购买');
                        $scope.modeFee = $scope.packagePrice;
                    }
                    fUserMode.modeFee = $scope.modeFee;
                };

                $scope.checkAgreement = function($event) {
                    //if(pbDebug) console.log('checkAgreement',$('#agreement').prop('checked'));
                    if ($scope.agreementChecked === false) {
                        $scope.agreementChecked = true;
                        $('#agreement-error').text('').css('display', 'none');
                    } else {
                        $scope.agreementChecked = false;
                    }
                };

                $scope.goDiyMode = function() {
                    fUserMode.choosedModeList = [];
                    fUserMode.choosedModeListMinor = [];
                    $scope.loadingThis = true;
                    getModeData($http,
                        '/vip/get_self_service_select/',
                        '',
                        function(data) {

                            pbFunc.updateUserModeList(fUserMode, $scope, data, function() {
                                $state.go(
                                    'userModeDiy', {}
                                );
                            }, null);

                            /*fUserMode.choosedModeList = data.data;
                            $scope.modeList = fUserMode.choosedModeList;
                            $scope.loadingThis = false;
                            $state.go(
                                'userModeDiy', {}
                            );*/
                            //document.location.href='/vip/role_info/#/usermode_diy/';
                        }
                    );
                };

                var updateModeFee = function($add) {
                    $scope.$apply(function() {
                        $scope.modeFee = $scope.packagePrice + $add * $scope.chooseCandidateNum;
                    });
                    fUserMode.modeFee = $scope.modeFee;
                };

                $scope.aboutInsurance = function() {
                    $.LayerOut({
                        html: alertBox(
                            '<span class="pay-title">关于入职险的说明</span>',
                            '提交订单后，请等待聘宝人才顾问与您沟通并核对信息',
                            '选择购买入职险<span class="cf46c62">500元/人</span>，我们提供每个候选人<span class="cf46c62">2周</span>的入职保证期具体信息请咨询销售顾问。',
                            '确认购买'
                        ),
                        afterClose: function() {
                            //$._LayerOut.close();
                            /*$state.go(
                                'userModeDiyPayOk', {}
                            );*/

                        }
                    });

                    $(".modal").undelegate(".btn-click-ok").delegate(".btn-click-ok", "click", function(e, $scope) {
                        $._LayerOut.close();
                        $('#useGuarantee').prop('checked', true);
                        $('.useGuaranteeInfo').text('已选择购买');
                        updateModeFee(500);
                    });

                };

                $.Menu();

            }
        ]
    );

    app.controller(
        'userModeNoWorrySubmit', ['$scope', '$http', '$state', 'fUserMode',
            function($scope, $http, $state, fUserMode) {
                //if(pbDebug) console.log('userModeNoWorrySubmit fUserMode',fUserMode);

                //是否显示loading
                $scope.loadingThis = true;

                $scope.salary_range = '';
                $scope.service_month = 0;
                $scope.candidate_num = 0;

                //console.log('params', $state, $state.params);
                /*var order_id = $state.params.order_id;
                var order_price = $state.params.order_price;*/
                $scope.modeFee = fUserMode.modeFee;

                if (fUserMode.choosedModeListMinor.length == 0) {
                    $state.go(
                        'userModeNoWorry', {}
                    );
                    return false;
                }

                //pbFunc.currentNoworrySet($scope, fUserMode.chooseOneModeId, fUserMode.choosedModeList);
                //if ($scope.salary_range == '') {
                pbFunc.currentNoworrySet($scope, fUserMode.chooseOneModeId, fUserMode.choosedModeListMinor);
                //}

                //console.log('scope', $scope);

                /*//清除数据
                //用户所选模式列表
                fUserMode.choosedModeList = [];
                //用户所选模式次要列表
                fUserMode.choosedModeListMinor = [];
                //主页loading
                fUserMode.loading = true;
                //订单内容
                fUserMode.currentOrderData = {};
                fUserMode.chooseOneModeId = 0;
                fUserMode.chooseOneModeType = '';
                fUserMode.chooseOneModeName = '';
                fUserMode.modeFee = 0;*/

                $.Menu();

            }
        ]
    );

    //directive
    app.directive('servicePeriod', function($templateCache) {
        return {
            restrict: 'E',
            templateUrl: '/static/users/servicePeriod.html',
            //controller: 'pbServicePeriod',
            scope: {
                servicePeriodList: '='
            },
            replace: true,
            //transclude: true,
            controller: function($scope, $element) {

                $scope.chooseServicePeriod = function($event, n) {
                    var trg = $event.currentTarget;
                    //console.log('chooseServicePeriod', angular.element(trg).parent().html());
                    for (var i = 0, imax = $scope.servicePeriodList.length; i < imax; i++) {
                        $scope.servicePeriodList[i].selected = false;
                        if ($scope.servicePeriodList[i].n == n) {
                            $scope.servicePeriodList[i].selected = true;
                            //获取到期时间

                            //更新
                            //$scope.servicePeriod = '3';
                            //$scope.serviceExpired = '2016-10-29 00:00:00';
                        }
                    }

                };
            },
            link: function(scope, elem, attrs, ctrl) {
                console.log('directive link', scope, elem, attrs, ctrl);
                /*attrs.$observe("feedId", function(value) {
                    if (value) {
                        //console.log('feedId', value);
                    }
                });
                //console.log('link scope',scope);
                scope.$watch(function() {
                    return scope.feedId;
                }, function(newVal, oldVal) {
                    if (newVal && newVal !== oldVal) {
                        //element.html(newVal);
                        //$compile(element)(scope);
                        //console.log('watch', newVal, oldVal);
                    }
                });*/

            },
            compile: function(tElement, tAttrs, transclude) {　　　　
                return {　　　　　　
                    pre: function preLink(scope, iElement, iAttrs, controller) {
                        //console.log('pre compile', scope);
                    },
                    post: function postLink(scope, iElement, iAttrs, controller) {
                        //console.log('post compile', scope);
                    }　　　　
                }　　
            }
        }
    });

})();