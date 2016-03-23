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
                    templateUrl: tmpl('users/user_mode_no_noworry.html'),
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

            //省心模式列表页面
            $stateProvider.state(
                'userModeNoWorry', {
                    url: '/usermode_noworry/',
                    templateUrl: tmpl('users/user_mode_noworry.html'),
                    controller: 'userModeNoWorry'
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
            modeFee: 0
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

                //查找自助套餐最低价
                getModeData($http,
                    "/vip/get_self_service_select_example/",
                    "",
                    function(data) {
                        fUserMode.listDiy = data.data;
                        pbFunc.minPrice($scope, data.data, 'basePriceDiy');
                        $scope.loadingDiy = false;

                        //查找省心套餐最低价
                        getModeData($http,
                            "/vip/get_manual_service_select_example/",
                            "",
                            function(data2) {
                                fUserMode.listNoworry = data2.data;
                                pbFunc.minPrice($scope, data2.data, 'basePriceNoworry');
                                $scope.loadingNoworry = false;
                            }
                        );
                    }
                );

                setTimeout(function(){
                    BizQQWPA.addCustom({
                        aty: '0',
                        nameAccount: '800031490',
                        selector: 'contact_us_noworry'
                    });
                },500);

                //进入套餐页面
                $scope.chooseUserMode = function($event, type) {

                    $('.user-mode').removeClass('selected');
                    $('.user-mode-' + type).addClass('selected');

                    var trgController = 'userModeNoWorry';
                    fUserMode.choosedModeList = fUserMode.listNoworry;
                    if (type.match(/^diy$/i)) {
                        fUserMode.choosedModeList = fUserMode.listDiy;
                        trgController = 'userModeDiy';

                        fUserMode.loading = false;
                        $scope.loading = fUserMode.loading;
                        $state.go(
                            trgController, {}
                        );
                    }else{
                        BizQQWPA.addCustom({
                            aty: '0',
                            nameAccount: '800031490',
                            selector: 'contact_us_noworry'
                        });
                    }

                };
            }
        ]
    );

    app.controller(
        'userModeDiy', ['$scope', '$http', '$state', '$templateCache', 'fUserMode',
            function($scope, $http, $state, $templateCache, fUserMode) {

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

                if (fUserMode.choosedModeList.length == 0) {
                    //if (pbDebug) console.log('choosedModeList', fUserMode.choosedModeList);
                    getModeData($http,
                        '/vip/get_self_service_select_example/',
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

                    document.location.href='/signin/?next=/vip/role_info/#/usermode_diy/';

                };

                $scope.goNoWorryMode = function() {
                    fUserMode.choosedModeList = [];
                    fUserMode.choosedModeListMinor = [];
                    $scope.loadingThis = true;
                    getModeData($http,
                        '/vip/get_self_service_select_example/',
                        '',
                        function(data) {

                            pbFunc.updateUserModeList(fUserMode, $scope, data, function() {
                                $state.go(
                                    'userModeNoWorry', {}
                                );
                            }, null);

                        }
                    );
                };

            }
        ]
    );

    app.controller(
        'userModeNoWorry', ['$scope', '$http', '$state', '$templateCache', 'fUserMode',
            function($scope, $http, $state, $templateCache, fUserMode) {
                //$templateCache.remove('/usermode_diy/');
                //$templateCache.removeAll();

                $state.go(
                    'userMode', {}
                );
                return false;

            }
        ]
    );



})();

