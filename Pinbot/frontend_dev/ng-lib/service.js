(function() {
    var utils = angular.module('app.utils', ['ng']);
    utils.factory('id_url', function() {
        return function(prefix, id) {
            return prefix + id + '/';
        }
    });

    //点击自定义select箭头，打开下拉
    utils.factory('open_select', function() {
        return function(selector) {
            var element = $(selector)[0],
                worked = false;
            if (document.createEvent) { // all browsers
                var e = document.createEvent("MouseEvents");
                e.initMouseEvent("mousedown", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                worked = element.dispatchEvent(e);
            } else if (element.fireEvent) { // ie
                worked = element.fireEvent("onmousedown");
            }
            if (!worked) { // unknown browser / error
                //alert("It didn't worked in your browser.");
            }
        }
    });

    //注意发布正式版本时：记得清除mock数据。

    //是否测试：第三方支付
    //var mockTest = false;
    //是否测试：使用金币支付
    //var mockTestWithCoin = false;

    utils.value('mockTest', false);
    utils.value('mockTestWithCoin', false);


    //是否存在于数组中
    utils.factory('inArray', function() {
        return function(needle, array) {
            for (var i = 0, imax = array.length; i < imax; i++) {
                if (needle == array[i]) {
                    return true;
                }
            }
            return false;
        }
    });

    //确认弹框
    utils.factory('confirmBox', function() {
        return function(title, msg, yesTitle, yesFunc, noTitle, noFunc) {
            var lineTitle = (typeof title == 'string' && title.match(/[<>]/i)) ? '<h3 class="text-center">' + title + '</h3>' : '<h3 class="text-center"><i class="i-ms"></i>' + title + '</h3>';
            return '<div class="mission-success pay-mission-success">' +
                lineTitle +
                '<div class="c607d8b f14 text-center clearfix">' + msg + '</div>' +
                '<p class="mt20 text-center">' +
                '<a class="btn btn-default btn-pay-problem" href="javascript:void(0);">' + yesTitle + '</a>' +
                '<a class="btn btn-blue btn-pay-ok" href="javascript:void(0);">' + noTitle + '</a>' +
                '</p>' +
                '</div>';
        }
    });
    utils.factory('confirmBoxRed', function() {
        return function(title, msg, yesTitle, yesFunc, noTitle, noFunc) {
            var lineTitle = (typeof title == 'string' && title.match(/[<>]/i)) ? '<h3 class="text-center">' + title + '</h3>' : '<h3 class="text-center"><i class="i-ms"></i>' + title + '</h3>';
            return '<div class="mission-success pay-mission-success">' +
                lineTitle +
                '<div class="annotation annotation-star f14 text-center clearfix">' + msg + '</div>' +
                '<p class="mt20 text-center">' +
                '<a class="btn btn-default btn-pay-problem" href="javascript:void(0);">' + yesTitle + '</a>' +
                '<a class="btn btn-red btn-pay-ok" href="javascript:void(0);">' + noTitle + '</a>' +
                '</p>' +
                '</div>';
        }
    });

    //提示弹框
    utils.factory('alertBox', function() {
        return function(title, annotation, msg, btnTitle, btnFunc, styleColor) {
            var cssStar = (annotation != undefined && typeof annotation == 'string' && annotation != '') ? '<span class="annotation annotation-star">' + annotation + '</span>' : '';
            var lineTitle = (title != undefined && typeof title == 'string' && title.match(/[<>]/i)) ? '<h3 class="text-center">' + title + '</h3>' : '<h3 class="text-center"><i class="i-ms"></i>' + title + '</h3>';
            var msgHtml = (!msg.match(/<(div|p) /i)) ? '<p class="c607d8b f14 text-center pd-bottom-20">' + msg + '</p>' : msg;
            var styleColor = (styleColor != undefined && typeof styleColor == 'string') ? 'red' : 'blue';
            return '<div class="mission-success pay-mission-success">' +
                lineTitle +
                cssStar +
                msgHtml +
                '<p class="mt20 text-center">' +
                '<a class="btn btn-' + styleColor + ' btn-click-ok" href="javascript:void(0);">' + btnTitle + '</a>' +
                '</p>' +
                '</div>';
        }
    });
    utils.factory('alertBoxRed', function() {
        return function(title, annotation, msg, btnTitle, btnFunc) {
            var cssStar = (annotation == '') ? '' : '<span class="annotation annotation-star">' + annotation + '</span>';
            var lineTitle = (typeof title == 'string' && title.match(/[<>]/i)) ? '<h3 class="text-center">' + title + '</h3>' : '<h3 class="text-center"><i class="i-ms"></i>' + title + '</h3>';
            return '<div class="mission-success pay-mission-success">' +
                lineTitle +
                cssStar +
                '<p class="c607d8b f14 text-center pd-bottom-20">' + msg + '</p>' +
                '<p class="mt20 text-center">' +
                '<a class="btn btn-red btn-click-ok" href="javascript:void(0);">' + btnTitle + '</a>' +
                '</p>' +
                '</div>';
        }
    });

    //获取API数据
    utils.factory('getModeData', ['mockTest', '$q',

        function(mockTest, $q) {
            return function($http, continue_url, hash, cb, mockData, errCb, noHandleErr, fakeData) {
                var fakeData = (fakeData != undefined) ? fakeData : {};
                //不自动处理错误提示
                var noHandleErr = (noHandleErr != undefined) ? true : false;
                var deferredAbort = $q.defer();
                if (continue_url === undefined) continue_url = "";
                //var deferred = $q.defer();
                //正常返回数据处理
                var responseHandler = function(continue_url, hash, data, cb, noHandleErr) {
                    if (continue_url.match(/^\/vip\/(self|manual)\/info/i) && data.status != undefined && data.status == "ok") {
                        //下一步付费模式
                        if (typeof hash == 'string' && hash != '') {
                            window.location.hash = hash;
                        }
                        if (typeof cb == 'function') {
                            cb(data);
                        }
                    } else if (!noHandleErr && data.status != undefined && data.status != "ok" && data.status != true && data.status != false) {
                        //显示错误
                        if (data.msg) {
                            $.alert('<p class="alert-notice-center"><span>请求错误提示：[' + data.msg.toString() + ']</span></p>');
                        } else if (data.error) {
                            $.alert('<p class="alert-notice-center"><span>请求错误提示：[' + data.error.toString() + ']</span></p>');
                        } else {
                            $.alert('<p class="alert-notice-center"><span>请求错误！</span></p>');
                        }
                    } else if (data && data.count > 0) {
                        //获取列表
                        if (typeof hash == 'string' && hash != '') {
                            window.location.hash = hash;
                        }
                        if (typeof cb == 'function') {
                            cb(data);
                        }
                    } else if (data.status == "ok" || data.status == true || data.status == false) {
                        //返回错误信息
                        if (data.status == false) {
                            if (data.data) {
                                if (typeof cb == 'function') {
                                    cb(data);
                                }
                            }else{
                                if (data.msg) {
                                    $.alert('<p class="alert-notice-center"><span>请求错误提示：' + data.msg.toString() + '</span></p>');
                                } else {
                                    if (data.error) {
                                        $.alert('<p class="alert-notice-center"><span>请求错误提示：' + data.error.toString() + '</span></p>');
                                    } else {
                                        $.alert('<p class="alert-notice-center"><span>请求错误！</span></p>');
                                    }
                                }
                            }
                        } else {
                            if (typeof hash == 'string' && hash != '') {
                                window.location.hash = hash;
                            }
                            if (typeof cb == 'function') {
                                cb(data);
                            }
                        }
                    } else {
                        if (typeof hash == 'string' && hash != '') {
                            window.location.hash = hash;
                        }
                        if (typeof cb == 'function') {
                            cb(data);
                        }
                    }
                };

                if (mockData != undefined && mockData === true) {
                    if (typeof hash == 'string' && hash != '') {
                        window.location.hash = hash;
                    }
                    if (typeof cb == 'function') {
                        var _fakeData = fakeData;
                        if (continue_url.match(/^\/vip\/get_self_service_select\/$/i)) {
                            _fakeData = {};
                        } else if (continue_url.match(/^\/vip\/get_manual_service_select\/$/i)) {
                            _fakeData = {};
                        }
                        responseHandler(continue_url, hash, _fakeData, cb, noHandleErr);
                    }
                    return null;
                } else {
                    var req = $http.get(continue_url, {
                        cache: false
                    }).success(function(data) {
                        //deferred.resolve(data);
                        if (pbDebug) console.log('getModeData', continue_url, hash, data);
                        loading = false;
                        responseHandler(continue_url, hash, data, cb, noHandleErr);
                    }).error(function(data) {
                        //deferred.reject(data);
                        //if (pbDebug) console.log(data);
                        //window.location.reload();
                        if (typeof errCb == 'function') {
                            errCb(data);
                        }
                        var handleErr = function(data) {
                            if (data.msg != undefined && typeof data.msg == 'string' && data.msg.match(/[<>]/i)) {
                                $.alert('<p class="alert-notice-center"><span>请求失败，请稍后再试！</span></p>');
                            } else {
                                $.alert('<p class="alert-notice-center"><span>请求失败，请稍后再试！</span></p>');
                            }
                        };
                        if (data.msg && typeof data.msg == 'string') {
                            handleErr(data);
                        } else {
                            handleErr(data);
                        }
                        throw new Error('请求数据失败! [' + data.toString() + ']');
                    });
                    req.abort = function() {
                        deferredAbort.resolve();
                    };
                    return req;
                }
                //return deferred.promise;
            }
        }
    ]);

    //post API数据
    utils.factory('postModeData', ['mockTest', '$q',
        function(mockTest, $q) {
            return function($http, postData, continue_url, hash, cb, mockData, errCb, format) {
                var deferredAbort = $q.defer();
                if (continue_url === undefined) continue_url = "";

                var format = (format != undefined && typeof format == 'string' && format != 'post') ? 'json' : 'post';
                var transFn = function(postData) {
                        var postStr = '';
                        if (format == 'post') {
                            for (var i in postData) {
                                if (postStr == '') {
                                    postStr += '' + i + '=' + encodeURIComponent(postData[i]);
                                } else {
                                    postStr += '&' + i + '=' + encodeURIComponent(postData[i]);
                                }
                            }
                        } else {
                            postStr = angular.toJson(postData);
                        }
                        //if (pbDebug) console.log('postStr', postData);
                        return postStr;
                    },
                    postCfg = {
                        headers: {
                            'Content-Type': (format == 'json') ? 'application/json' : 'application/x-www-form-urlencoded; charset=UTF-8'
                        },
                        transformRequest: transFn
                    };
                //
                if (mockTest || (mockData != undefined && mockData === true)) {
                    //if (pbDebug) console.log('mock data', postData);
                    if (typeof hash == 'string' && hash != '') {
                        window.location.hash = hash;
                    }
                    if (typeof cb == 'function') {
                        if (continue_url.match(/coin_paid_order/i) && !postData.hasOwnProperty('product_type')) {
                            //金币支付
                            cb({
                                status: 'ok',
                                msg: '订单支付成功',
                                order_id: 1075
                            });
                        } else {
                            if (postData.product_type.match(/self_service/i)) {
                                var payment_terms = 'alipay';
                                if (postData.payment_terms == "coin") payment_terms = 'coin';
                                //自助型
                                //订单创建
                                cb({
                                    status: 'ok',
                                    msg: '订单生成成功',
                                    pay_url: 'https://mapi.alipay.com/gateway.do',
                                    order_id: 1075,
                                    payment_terms: payment_terms
                                });
                            } else {
                                //省心型
                                cb({
                                    status: 'ok',
                                    msg: '订单生成成功',
                                    pay_url: '',
                                    order_id: 1075,
                                    payment_terms: ''
                                });
                            }
                        }

                    }
                    return null;
                } else {
                    var req = $http.post(continue_url, postData, postCfg).success(function(data) {
                        //if (pbDebug) console.log('postModeData', continue_url, hash, data);
                        var errInfoMore = '';
                        if (data.msg == '支付失败,请勿重新购买!') errInfoMore = '<br>注：自助型用户请选择更高的级别的套餐，省心型用户不能同时购买自助服务';

                        loading = false;
                        if (continue_url.match(/^\/vip\/(self|manual)\/info/i) && data.status != undefined && data.status == "ok") {
                            //下一步付费模式
                            if (typeof hash == 'string' && hash != '') {
                                window.location.hash = hash;
                            }
                            if (typeof cb == 'function') {
                                cb(data);
                            }
                        } else if (data.status != undefined && data.status != "ok" && data.status != true) {
                            //显示错误
                            $.alert('<p class="alert-notice-center"><span>提交错误提示：[' + data.msg + ']' + errInfoMore + '</span></p>');
                        } else if (data && data.count > 0) {
                            //获取列表
                            if (typeof hash == 'string' && hash != '') {
                                window.location.hash = hash;
                            }
                            if (typeof cb == 'function') {
                                cb(data);
                            }
                        } else if (data.status == "ok" || data.status == true) {
                            if (typeof hash == 'string' && hash != '') {
                                window.location.hash = hash;
                            }
                            if (typeof cb == 'function') {
                                cb(data);
                            }
                        } else {
                            $.alert('<p class="alert-notice-center"><span>提交错误提示：[' + data.msg + ']' + errInfoMore + '</span></p>');
                        }
                    }).error(function(data) {
                        //if (pbDebug) console.log(data);
                        //window.location.reload();
                        if (typeof errCb == 'function') {
                            errCb(data);
                        }
                        var handleErr = function(data) {
                            if (data.msg != undefined && typeof data.msg == 'string' && data.msg.match(/[<>]/i)) {
                                $.alert('<p class="alert-notice-center"><span>请求失败，请稍后再试！</span></p>');
                            } else {
                                $.alert('<p class="alert-notice-center"><span>请求失败，请稍后再试！</span></p>');
                            }
                        };
                        if (data.msg && typeof data.msg == 'string') {
                            handleErr(data);
                        } else {
                            handleErr(data);
                        }
                        throw new Error('提交数据失败! [' + data.toString() + ']');
                    });
                    req.abort = function() {
                        deferredAbort.resolve();
                    };
                    return req;
                }
            }
        }
    ]);

    utils.factory('pbFunc', [
        'getModeData',
        'postModeData',
        'confirmBox',
        'confirmBoxRed',
        'alertBox',
        'alertBoxRed',

        function(
            getModeData,
            postModeData,
            confirmBox,
            confirmBoxRed,
            alertBox,
            alertBoxRed) {
            return {
                minPrice: function($scope, priceList, name) {
                    for (var i in priceList) {
                        if (priceList[i].is_show != undefined) {
                            if (priceList[i].is_show == true && priceList[i].price != undefined && parseFloat(priceList[i].price) > 0 &&
                                parseInt($scope[name]) == 0) {
                                $scope[name] = priceList[i].price;
                            } else if (priceList[i].is_show == true && priceList[i].price != undefined && parseFloat(priceList[i].price) > 0 && parseFloat(priceList[i].price) <
                                parseInt($scope[name])) {
                                $scope[name] = priceList[i].price;
                            }
                        } else {
                            if (priceList[i].price != undefined && parseFloat(priceList[i].price) > 0 &&
                                parseInt($scope[name]) == 0) {
                                $scope[name] = priceList[i].price;
                            } else if (priceList[i].price != undefined && parseFloat(priceList[i].price) > 0 && parseFloat(priceList[i].price) <
                                parseInt($scope[name])) {
                                $scope[name] = priceList[i].price;
                            }
                        }
                    }
                },
                //更新套餐列表
                updateUserModeList: function(fUserMode, $scope, data, cb, args) {
                    //list load
                    fUserMode.choosedModeList = data.data;
                    $scope.modeList = fUserMode.choosedModeList;
                    $scope.loadingThis = false;

                    //page load
                    /*fUserMode.choosedModeList = data.data;
                    fUserMode.loading = false;
                    $scope.loading = fUserMode.loading;*/
                    if (typeof cb == 'function') {
                        cb(args);
                    }
                },
                createOrder: function($http, $scope, jQ, postData, cb, args) {
                    postModeData($http, postData,
                        //创建订单接口
                        '/vip/create_user_order/',
                        '',
                        function(data) {
                            //console.log('create_user_order', data);
                            if (data.status != undefined && data.status == 'ok') {
                                if (typeof cb == 'function') {
                                    cb(args);
                                }
                            } else {
                                jQ.alert('<p class="alert-notice-center"><span>创建订单失败，请稍后再试！[' + data.msg + ']</span></p>');
                            }
                            $scope.loadingThis = false;
                        }
                    );
                },
                loadApiUrl: function($scope, api_url, page) {
                    var page = (typeof page != "number") ? 1 : page;
                    var imax = $scope.api_params.length;
                    var getStr = '?page=' + page + '&';
                    for (var i = 0; i < imax; i++) {
                        var paraName = $scope.api_params[i];
                        getStr += paraName + '=' + $scope.api_params_values[paraName] + '&';
                    }
                    return api_url + getStr;
                },
                reloadList: function($http, $scope, fMyPackage) {
                    //载入数据
                    getModeData($http,
                        this.loadApiUrl($scope, $scope.api_url),
                        "",
                        function(data) {
                            $scope.loadingThis = false;
                            fMyPackage.logList = data;
                            $scope.logList = fMyPackage.logList;
                        });
                },
                nextPage: function($http, $scope, jQ, fMyPackage, pageNum) {
                    $scope.loadingThis = true;

                    //载入数据
                    getModeData($http,
                        this.loadApiUrl($scope, $scope.api_url, pageNum),
                        "",
                        function(data) {
                            $scope.loadingThis = false;
                            fMyPackage.logList = data;
                            $scope.logList = fMyPackage.logList;

                            if (pageNum > $scope.logList.pages) pageNum = $scope.logList.pages;
                            if (pageNum < 1) pageNum = 1;

                            //update footer link
                            jQ('.offset-start').text((parseInt($scope.logList.current) - 1) * parseInt($scope.logList.per_page) + 1);

                            var countSum = parseInt($scope.logList.current) * parseInt($scope.logList.per_page);
                            if ($scope.logList.count < countSum) {
                                jQ('.offset-end').text($scope.logList.count);
                            } else {
                                jQ('.offset-end').text(countSum);
                            }

                        });
                },
                orderAct: function($http, $scope, jQ, fMyPackage, e, url, cb) {
                    var _this = this;
                    var trg = jQ(e.currentTarget);
                    var postData = {
                        'service_id': trg.attr('data-oid')
                    };
                    //如果是删除，要post service_id
                    if (url.match(/^\/vip\/order\/delete\/$/i)) {
                        var postData = {
                            'service_id': trg.attr('data-oid')
                        };
                    }
                    $scope.loadingThis = true;
                    postModeData($http, postData,
                        url,
                        '',
                        function(data) {
                            if (data.status != undefined && data.status == 'ok') {
                                //载入数据
                                _this.reloadList($http, $scope, fMyPackage);
                                if (typeof cb == 'function') {
                                    cb(data);
                                }
                            } else {
                                $scope.loadingThis = false;
                                jQ.alert('<p class="alert-notice-center"><span>操作失败，请稍后再试！[' + data.msg + ']</span></p>');
                            }

                        }
                    );
                },
                orderActGet: function($http, $scope, jQ, fMyPackage, e, url, cb) {
                    var _this = this;
                    //var trg = jQ(e.currentTarget);
                    //var service_id = trg.attr('data-oid');

                    $scope.loadingThis = true;
                    getModeData($http,
                        url,
                        '',
                        function(data) {
                            if (data.status != undefined && data.status == 'ok') {
                                //载入数据
                                _this.reloadList($http, $scope, fMyPackage);
                                if (typeof cb == 'function') {
                                    cb(data);
                                }
                            } else {
                                $scope.loadingThis = false;
                                jQ.alert('<p class="alert-notice-center"><span>操作失败，请稍后再试！[' + data.msg + ']</span></p>');
                            }

                        }
                    );
                },
                orderActConfirm: function($http, $scope, jQ, title, info, cancelTitle, continueTitle, cancelCb, continueCb) {
                    jQ.LayerOut({
                        html: confirmBoxRed(
                            title,
                            info,
                            cancelTitle,
                            '',
                            continueTitle,
                            ''
                        ),
                        afterClose: function() {
                            //$._LayerOut.close();
                            /*$state.go(
                                'userModeDiyPayOk', {}
                            );*/
                        }
                    });

                    jQ(".modal").undelegate(".btn-pay-problem").delegate(".btn-pay-problem", "click", function(e) {
                        jQ._LayerOut.close();
                        if (typeof cancelCb == 'function') {
                            cancelCb();
                        }
                    });
                    jQ(".modal").undelegate(".btn-pay-ok").delegate(".btn-pay-ok", "click", function(e) {
                        jQ._LayerOut.close();
                        if (typeof continueCb == 'function') {
                            continueCb();
                        }
                    });
                },
                orderActAlert: function($http, $scope, jQ, title, info, detail, continueTitle, continueCb) {
                    jQ.LayerOut({
                        html: alertBoxRed(
                            title,
                            info,
                            detail,
                            continueTitle
                        ),
                        afterClose: function() {
                            //$._LayerOut.close();

                        }
                    });
                    $.Menu();

                    jQ(".modal").undelegate(".btn-click-ok").delegate(".btn-click-ok", "click", function(e, $scope) {
                        jQ._LayerOut.close();
                        if (typeof continueCb == 'function') {
                            continueCb();
                        }
                    });
                },
                pbAlert: function($http, $scope, jQ, title, info, detail, continueTitle, continueCb) {
                    jQ.LayerOut({
                        html: alertBox(
                            title,
                            info,
                            detail,
                            continueTitle
                        ),
                        afterClose: function() {
                            //$._LayerOut.close();

                        }
                    });

                    jQ(".modal").undelegate(".btn-click-ok").delegate(".btn-click-ok", "click", function(e, $scope) {
                        jQ._LayerOut.close();
                        if (typeof continueCb == 'function') {
                            continueCb();
                        }
                    });
                },
                //通过id获取当前自助套餐信息
                currentDiySet: function($scope, payPid, modeList) {
                    for (var i = 0, imax = modeList.length; i < imax; i++) {
                        if (modeList[i].pid == payPid) {
                            $scope.feed_count = modeList[i].feed_count;
                            $scope.pinbot_point = modeList[i].pinbot_point;
                            $scope.name = modeList[i].name;
                            break;
                        }
                    }
                },
                //通过id获取当前省心套餐信息
                currentNoworrySet: function($scope, payPid, modeList) {
                    for (var i = 0, imax = modeList.length; i < imax; i++) {
                        if (modeList[i].pid == payPid) {
                            $scope.salary_range = modeList[i].salary_range;
                            $scope.service_month = modeList[i].service_month;
                            $scope.candidate_num = modeList[i].candidate_num;
                            break;
                        }
                    }
                },
                //判断这个自助套餐是否可以购买: 已经是自助B模式的会员了，再选择升级服务时，就不能再选择同一模式了，只能往更高（更贵）的自助模式选择或者选择省心型
                canBuyDiy: function(payPid, modeList, choosedId) {
                    var newPrice = 0;
                    var curPrice = 0;
                    for (var i = 0, imax = modeList.length; i < imax; i++) {
                        if (modeList[i].pid == payPid) {
                            newPrice = modeList[i].price;
                            break;
                        }
                    }
                    for (var i = 0, imax = modeList.length; i < imax; i++) {
                        if (modeList[i].pid == choosedId) {
                            curPrice = modeList[i].price;
                            break;
                        }
                    }
                    console.log('canBuyDiy', payPid, modeList, choosedId, newPrice, curPrice);
                    if (newPrice > curPrice) {
                        return true;
                    } else {
                        return false;
                    }
                },
                //获取用户当前数据
                getUserData: function($http, cbOk, cbFailed) {
                    //载入数据
                    getModeData($http,
                        '/vip/get_user_info/',
                        "",
                        function(data) {
                            if (data.status != undefined && data.status == 'ok') {
                                if (typeof cbOk == 'function') {
                                    cbOk(data);
                                }
                                return data;
                            } else {
                                if (typeof cbFailed == 'function') {
                                    cbFailed();
                                }
                                return null;
                            }
                        });
                },
                //获取订单状态
                getOrderStatus: function($http, order_id, cbOk, cbFailed) {
                    //载入数据
                    var postData = {
                        order_id: order_id
                    };
                    postModeData($http, postData,
                        '/vip/order/get_order_status/',
                        "",
                        function(data) {
                            //console.log('getOrderStatus', data);
                            if (data.status != undefined && data.status == 'ok') {
                                if (typeof cbOk == 'function') {
                                    cbOk(data);
                                }
                                return data;
                            } else {
                                if (typeof cbFailed == 'function') {
                                    cbFailed();
                                }
                                return null;
                            }
                        });
                },
                formatDate: function(format, ts) {
                    var tsDate = (ts != undefined && typeof ts == 'number') ? new Date(ts) : new Date();
                    var o = {
                        "M+": tsDate.getMonth() + 1,
                        // month
                        "d+": tsDate.getDate(),
                        // day
                        "h+": tsDate.getHours(),
                        // hour
                        "m+": tsDate.getMinutes(),
                        // minute
                        "s+": tsDate.getSeconds(),
                        // second
                        "q+": Math.floor((tsDate.getMonth() + 3) / 3),
                        // quarter
                        "S": tsDate.getMilliseconds()
                        // millisecond
                    };
                    //console.log('o',o);
                    if (/(y+)/.test(format) || /(Y+)/.test(format)) {
                        format = format.replace(RegExp.$1, (tsDate.getFullYear() + "").substr(4 - RegExp.$1.length));
                    }
                    for (var k in o) {
                        if (o.hasOwnProperty(k) && new RegExp("(" + k + ")").test(format)) {
                            format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
                        }
                    }
                    return format;
                },
                getDateObj: function(t) {
                    var dt;
                    if (t != undefined) {
                        if (typeof t == 'string' || typeof t == 'number') {
                            dt = new Date(t); //'9/24/2015 14:52:10' || 1450656000000
                        } else {
                            dt = new Date();
                        }
                    } else {
                        dt = new Date();
                    }
                    return {
                        y: dt.getFullYear(),
                        m: dt.getMonth() + 1,
                        d: dt.getDate(),
                        h: dt.getHours(),
                        i: dt.getMinutes(),
                        s: dt.getSeconds()
                    };
                },
                getTimestamp: function(dateStr) {
                    var dt = new Date(dateStr);
                    return Math.round(dt.getTime() / 1000);
                },
                getTimestampMs: function(dateStr) {
                    var dt = new Date(dateStr);
                    return Math.round(dt.getTime());
                },
                countDaysByMonth: function(currentTs, monthNum) {
                    var monthStart = new Date(currentTs);
                    var monthStartObj = this.getDateObj(currentTs);
                    //year, month, day, hour, minute, second, and millisecond
                    var monthEnd = new Date(monthStartObj.y, monthStartObj.m - 1 + monthNum, monthStartObj.d, monthStartObj.h, monthStartObj.i, monthStartObj.s);
                    var dayLength = (monthEnd - monthStart) / 86400000;
                    return dayLength;
                },
                getExpiredDateArr: function(currentTs, monthNum) {
                    var monthStart = new Date(currentTs);
                    var monthStartObj = this.getDateObj(currentTs);
                    var monthEnd = new Date(monthStartObj.y, monthStartObj.m - 1 + monthNum, monthStartObj.d, monthStartObj.h, monthStartObj.i, monthStartObj.s);
                    var endTs = this.getTimestampMs(monthEnd);
                    return [endTs, this.formatDate('yyyy-MM-dd hh:mm:ss', endTs)];
                },
                getDataWithPromise: function($q, $http, url) {
                    var deferred = $q.defer();
                    //获取自助服务信息
                    getModeData($http,
                        url,
                        '',
                        function(data) {
                            deferred.resolve(data);
                        },
                        undefined,
                        function(data) {
                            deferred.reject(data);
                        }
                    );
                    return deferred.promise;
                },
                urlString: function(obj) {
                    var str = '';
                    for (var i in obj) {
                        if (str == '') {
                            str += '' + i + '=' + obj[i];
                        } else {
                            str += '&' + i + '=' + obj[i];
                        }
                    }
                    return str;
                },
                alertModal: function(title, annotation, msg, btnTitle, btnFunc, moreBtnClass, moreInfo) {
                    var cssStar = (annotation == '') ? '' : 'annotation-star';
                    var moreBtnClass = (moreBtnClass != undefined && typeof moreBtnClass == 'string') ? moreBtnClass : '';
                    var moreInfo = (moreInfo != undefined && typeof moreInfo == 'string') ? moreInfo : '';
                    return '<div class="mission-success pay-mission-success">' +
                        '<h3 class="text-center"><i class="i-ms"></i>' + title + '</h3>' +
                        //'<span class="annotation ' + cssStar + '">' + annotation + '</span>' +
                        '<div class="c607d8b f14 text-center pd-bottom-20 clearfix">' + msg + '</div>' +
                        moreInfo +
                        '<div class="mt20 text-center clearfix">' +
                        '<a class="btn btn-blue btn-click-ok ' + moreBtnClass + '" href="javascript:void(0);">' + btnTitle + '</a>' +
                        '</div>' +
                        '</div>';
                },
                //简单alert弹窗
                simpleAlert: function(title, msg, cbClose, args, btnTitle, showAlert, styleColor) {
                    var btnTitle = (btnTitle != undefined && typeof btnTitle == 'string') ? btnTitle : '确定';
                    var showAlert = (showAlert != undefined && showAlert == true) ? '<span class="pay-alert"></span>' : '';
                    var styleColor = (styleColor != undefined && typeof styleColor == 'string') ? 'red' : 'blue';
                    $.LayerOut({
                        html: alertBox(
                            showAlert + '<span class="pay-title">' + title + '</span>',
                            '',
                            msg,
                            btnTitle,
                            null,
                            styleColor
                        ),
                        afterClose: function() {
                            if (typeof cbClose == 'function') cbClose(args);
                        }
                    });
                    $(".modal").undelegate(".btn-click-ok").delegate(".btn-click-ok", "click", function(e) {
                        if (typeof cbClose == 'function') cbClose($(this), args);
                        $._LayerOut.close();
                    });
                },
                //简单confirm弹窗
                simpleConfirm: function(title, msg, cbClose, args, btnTitle, showAlert, okTitle, cbOk, confirmStyle) {
                    var btnTitle = (btnTitle != undefined && typeof btnTitle == 'string') ? btnTitle : '确定';
                    var showAlert = (showAlert != undefined && showAlert == true) ? '<span class="pay-alert"></span>' : '';
                    var confirmBoxObj = (confirmStyle != undefined && confirmStyle == 'red') ? confirmBoxRed : confirmBox;
                    $.LayerOut({
                        html: confirmBoxObj(
                            showAlert + '<span class="pay-title">' + title + '</span>',
                            msg,
                            btnTitle,
                            '',
                            okTitle,
                            ''
                        ),
                        afterClose: function() {
                            //$._LayerOut.close();
                        }
                    });
                    $(".modal").undelegate(".btn-pay-problem").delegate(".btn-pay-problem", "click", function(e) {
                        if (typeof cbClose == 'function') cbClose($(this), args);
                        //$._LayerOut.close();
                    });
                    $(".modal").undelegate(".btn-pay-ok").delegate(".btn-pay-ok", "click", function(e) {
                        if (typeof cbOk == 'function') cbOk($(this), args);
                        //$._LayerOut.close();
                    });
                },
                //整数前补零
                feedZero: function(n) {
                    if (n != undefined && n.toString().match(/^[0-9]+$/i)) {
                        if (parseInt(n) < 10) {
                            return '0' + parseInt(n);
                        }
                    }
                    return n;
                },
                openQQ: function(id) {
                    console.log('openQQ', id, jQuery);
                    if (typeof jQuery != 'undefined') {
                        $.getScript('http://wpa.b.qq.com/cgi/wpa.php').done(function() {
                            BizQQWPA.addCustom([{
                                aty: '0',
                                nameAccount: '800031490',
                                selector: id
                            }]);
                        });
                    }
                },
                objToArr: function(Obj) {
                    //把obj转成数组
                    var tmpObj = [];
                    if (typeof Obj != 'object') return tmpObj;
                    for (var t in Obj) {
                        tmpObj.push(Obj[t]);
                    }
                    return tmpObj;
                }
            };
        }
    ]);

    //支付处理接口
    utils.factory('orderPay', ['getModeData', 'postModeData', 'confirmBox',
        function(getModeData, postModeData, confirmBox) {
            return function($scope, $state, $http, jQ, postData, okControllerName, createOrderUrl, format, failedControllerName) {

                /*
                //其实可以先检查用户金币数，再判断是否弹出新窗口
                getModeData($http,
                    '/vip/get_user_info/',
                    "",
                    function(data) {
                        if(data.status!=undefined && data.status=='ok'){
                            return data;
                        }else{
                            return null;
                        }
                    });*/
                var createOrderUrl = (createOrderUrl != undefined && typeof createOrderUrl == 'string') ? createOrderUrl : '/vip/create_user_order/';

                var newWindow = window.open('about:blank');
                newWindow.document.write('<meta charset="utf-8"><img src="/static/partner/images/loading.gif" alt="loading"><br>页面装载中...');
                //获取支付接口
                postModeData($http, postData,
                    //创建订单接口
                    createOrderUrl,
                    '',
                    function(data) {
                        //console.log('create_user_order', data);
                        if (data.status != undefined && data.status == 'ok') {
                            if (data.payment_terms != undefined && data.payment_terms == 'coin') {
                                newWindow.close();
                                //使用金币支付
                                var postData2 = {
                                    order_id: data.order_id
                                };
                                postModeData($http, postData2,
                                    //创建订单接口
                                    '/vip/coin_paid_order/',
                                    '',
                                    function(data2) {
                                        //console.log('coin_paid_order', data2);
                                        if (data2.status != undefined && data2.status == 'ok') {
                                            $state.go(
                                                okControllerName, {}
                                            );
                                        } else {
                                            jQ.alert('<p class="alert-notice-center"><span>支付金币失败，请稍后再试！［' + data2.msg + '］</span></p>');
                                        }
                                    });
                            } else {
                                //console.log('pay_url', data);
                                //使用第三方支付
                                var pay_url = data.pay_url;
                                //如果是Alipay,打开支付新窗口
                                if (data.payment_terms == 'alipay' && typeof data.pay_url == "string" && data.pay_url.match(/^https?:\/\//i)) {
                                    //window.open(data.pay_url, "_blank");
                                    newWindow.location.href = data.pay_url;
                                } else {
                                    newWindow.close();
                                }

                                jQ.LayerOut({
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

                                jQ(".modal").undelegate(".btn-pay-problem").delegate(".btn-pay-problem", "click", function(e) {
                                    //console.log('payProblem', e);
                                    jQ('.header h1').html('<span class="pay-failed"></span>Sorry...支付失败');
                                    jQ('.header .sub-title').html('您未成功支付，若支付成功请尝试刷新页面。遇到问题？<a href="javascript:void(0);" id="JS_pbqqdiy_btn">联系聘宝人才顾问</a>');
                                    jQ._LayerOut.close();

                                    jQ.Menu();
                                    //return false;
                                });
                                jQ(".modal").undelegate(".btn-pay-ok").delegate(".btn-pay-ok", "click", function(e) {
                                    //console.log('paySuccess', e);

                                    var postData2 = {
                                        order_id: data.order_id
                                    };
                                    postModeData($http, postData2,
                                        //创建订单接口
                                        '/vip/order/get_order_status/',
                                        '',
                                        function(data2) {
                                            //console.log('coin_paid_order', data2);
                                            if (data2.status != undefined && data2.status == 'ok' && data2.order_status == 'paid') {
                                                jQ._LayerOut.close();
                                                if (okControllerName != undefined && typeof okControllerName == 'string') {
                                                    $state.go(
                                                        okControllerName, {}
                                                    );
                                                }
                                            } else {
                                                if (failedControllerName != undefined && typeof failedControllerName == 'string') {
                                                    $state.go(
                                                        failedControllerName, {}
                                                    );
                                                } else {
                                                    jQ.alert('<p class="alert-notice-center"><span>抱歉，您的支付尚未成功！</span></p>');
                                                    jQ('.header h1').html('<span class="pay-failed"></span>Sorry...支付失败');
                                                    jQ('.header .sub-title').html('您未成功支付，若支付成功请尝试刷新页面。遇到问题？<a href="javascript:void(0);" id="JS_pbqqdiy_btn">联系聘宝人才顾问</a>');
                                                    jQ.Menu();
                                                }

                                            }
                                        });

                                });
                            }

                        } else {
                            newWindow.close();
                            jQ.alert('<p class="alert-notice-center"><span>创建订单失败，请稍后再试！[' + data.msg + ']</span></p>');
                        }
                        $scope.loadingThis = false;
                    }, undefined, undefined, format
                );
            };
        }
    ]);

    utils.factory('pbLib', [

        function() {
            return {
                setCookie: function(key, value, timeLapse) {
                    var timeLapse = (timeLapse != undefined && typeof timeLapse == 'number') ? timeLapse : 86400000;
                    var expires = new Date();
                    expires.setTime(expires.getTime() + timeLapse);
                    document.cookie = key + '=' + value + ';expires=' + expires.toUTCString() + ';path=/;';
                },
                delCookie: function(key) {
                    var expires = new Date();
                    expires.setTime(expires.getTime() - 86400);
                    document.cookie = key + '=;expires=' + expires.toUTCString() + ';path=/;';
                },
                getCookie: function(key) {
                    var keyValue = document.cookie.match('(^|;) ?' + key + '=([^; ]*)(;|$)');
                    return keyValue ? keyValue[2] : null;
                },
                utf8_to_b64: function(t) {
                    return window.btoa(unescape(encodeURIComponent(t)))
                },
                b64_to_utf8: function(str) {
                    var str = str.replace(/\s/g, '');
                    return decodeURIComponent(escape(window.atob(str)));
                },
                stopBubble: function(e) {
                    e = e ? e : window.event;
                    if (window.event) {
                        e.cancelBubble = true;
                    }
                    e.stopPropagation();
                },
                //deprecated
                getFeedIdByUrl: function() {
                    var curFeedId = '0';
                    if (document.location.href.toString().match(/\/#\/feed_resume\/([0-9a-z]+)\//i)) {
                        curFeedId = RegExp.$1;
                    }
                    return curFeedId;
                },
                feedCkPrefix: 'fdc_',
                getFeedConfig: function(curFeedId) {
                    var choosedFeedsLocal = {};
                    if (choosedFeedsLocal[curFeedId] === undefined) {
                        choosedFeedsLocal[curFeedId] = {
                            l: null, //latest_cookie
                            p: null, //partner_cookie
                            t: null, //title_match_cookie
                            e: null, //extend_match_cookie
                            r: null, //reco_time_cookie
                            minY: '', //$scope.filter_list.work_years_min
                            maxY: '', //$scope.filter_list.work_years_max
                            minS: '', //$scope.filter_list.salary_min
                            maxS: '', //$scope.filter_list.salary_max
                            degree: '', //$scope.filter_list.degree
                            minA: '', //$scope.filter_list.age_min
                            maxA: '', //$scope.filter_list.age_max
                            gender: '', //$scope.filter_list.gender
                            ca: '', //$scope.filter_list.current_area
                        };
                    }
                    // 请求条件
                    if (curFeedId != '0' && this.getCookie(this.feedCkPrefix + curFeedId) != null) {
                        var feed_data_cookie = angular.fromJson(this.b64_to_utf8(this.getCookie(this.feedCkPrefix + curFeedId)));
                        choosedFeedsLocal[curFeedId].l = feed_data_cookie.l;
                        choosedFeedsLocal[curFeedId].p = feed_data_cookie.p;
                        choosedFeedsLocal[curFeedId].t = feed_data_cookie.t;
                        choosedFeedsLocal[curFeedId].e = feed_data_cookie.e;
                        choosedFeedsLocal[curFeedId].r = feed_data_cookie.r;
                        choosedFeedsLocal[curFeedId].minY = feed_data_cookie.minY;
                        choosedFeedsLocal[curFeedId].maxY = feed_data_cookie.maxY;
                        choosedFeedsLocal[curFeedId].minS = feed_data_cookie.minS;
                        choosedFeedsLocal[curFeedId].maxS = feed_data_cookie.maxS;
                        choosedFeedsLocal[curFeedId].degree = feed_data_cookie.degree;
                        choosedFeedsLocal[curFeedId].minA = feed_data_cookie.minA;
                        choosedFeedsLocal[curFeedId].maxA = feed_data_cookie.maxA;
                        choosedFeedsLocal[curFeedId].gender = feed_data_cookie.gender;
                        choosedFeedsLocal[curFeedId].ca = feed_data_cookie.ca;
                    }

                    return choosedFeedsLocal;
                },
                setFeedConfig: function($scope, updateObj) {
                    var getFeedId = $scope.getFeedId;
                    var update = function($scope, getFeedId, updateObj, name) {
                        if (typeof updateObj == 'object' && updateObj[name] != undefined && updateObj[name] != null) $scope.choosedFeeds[getFeedId][name] = updateObj[name];
                    };
                    if (getFeedId != '0' && $scope.choosedFeeds[getFeedId] != undefined) {
                        update($scope, getFeedId, updateObj, 'l');
                        update($scope, getFeedId, updateObj, 'p');
                        update($scope, getFeedId, updateObj, 't');
                        update($scope, getFeedId, updateObj, 'e');
                        update($scope, getFeedId, updateObj, 'r');
                        update($scope, getFeedId, updateObj, 'minY');
                        update($scope, getFeedId, updateObj, 'maxY');
                        update($scope, getFeedId, updateObj, 'minS');
                        update($scope, getFeedId, updateObj, 'maxS');
                        update($scope, getFeedId, updateObj, 'degree');
                        update($scope, getFeedId, updateObj, 'minA');
                        update($scope, getFeedId, updateObj, 'maxA');
                        update($scope, getFeedId, updateObj, 'gender');
                        update($scope, getFeedId, updateObj, 'ca');
                        this.setCookie(this.feedCkPrefix + getFeedId, this.utf8_to_b64(angular.toJson($scope.choosedFeeds[getFeedId])), 3 * 86400000);
                    }
                },
                isEmptyObj: function(obj) {
                    if (typeof obj != 'object') return false;
                    var size = 0;
                    for (var t in obj) {
                        if (obj[t] != undefined) {
                            size++;
                            break;
                        }
                    }
                    return (size == 0) ? true : false;
                }
            };
        }
    ]);


})();