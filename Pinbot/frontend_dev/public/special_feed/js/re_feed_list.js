(function(argument) {
    // body...
    var app = angular.module('app.re_feed_list', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter']),
        $django = angular.injector(['app.django']),
        $funcs = angular.injector(['app.utils']),
        tmpl = $django.get('tmpl'),
        static_url = $django.get('static_url');
    var pbLib = $funcs.get('pbLib');
    var pbFunc = $funcs.get('pbFunc');

    app.config([
        '$stateProvider', '$urlRouterProvider',
        function($stateProvider, $urlRouterProvider) {
            var first_feed = window.asideData.all_feed[0].feed,
                id = first_feed.id,
                otherwiseUrl = '';
            if (first_feed.has_expire) {
                otherwiseUrl = '/feed_renew/' + id + '/';
            } else if (!first_feed.has_expire && first_feed.expire_status) {
                otherwiseUrl = '/feed_active/' + id + '/';
            } else if (!first_feed.has_expire && !first_feed.expire_status) {
                otherwiseUrl = '/feed_resume/' + id + '/';
            }
            $urlRouterProvider.otherwise(otherwiseUrl);
            $stateProvider.state(
                'feedResume', {
                    url: '/feed_resume/:feedId/',
                    templateUrl: tmpl('special_feed/feed_resume.html'),
                    controller: 'feedResume'
                }
            );
            $stateProvider.state(
                'feedRenew', {
                    url: '/feed_renew/:feedId/',
                    templateUrl: tmpl('special_feed/feed_renew.html'),
                    controller: 'feedRenew'
                }
            );
            $stateProvider.state(
                'feedActive', {
                    url: '/feed_active/:feedId/',
                    templateUrl: tmpl('special_feed/feed_active.html'),
                    controller: 'feedActive'
                }
            );
            $stateProvider.state(
                'feedBlank', {
                    url: '/feed_blank/:feedId/?source',
                    templateUrl: tmpl('special_feed/feed_blank.html'),
                    controller: 'feedBlank'
                }
            );
        }
    ]);

    var hideSelect = function($event, $scope) {
        var target = angular.element($event.target);
        if ($scope.show_work_year == true) {
            if (!target.hasClass('js-work-year') && !target.parents().hasClass('js-work-year')) {
                $scope.show_work_year = false;
            }
        }
        if ($scope.show_salary == true) {
            if (!target.hasClass('js-salary') && !target.parents().hasClass('js-salary')) {
                $scope.show_salary = false;
            }
        }
        if ($scope.show_age == true) {
            if (!target.hasClass('js-age') && !target.parents().hasClass('js-age')) {
                $scope.show_age = false;
            }
        }
    };

    app.controller(
        'feedAside', ['$scope', '$http', '$state',
            function($scope, $http, $state) {
                $scope.asideData = window.asideData;
                $scope.asideList = [];
                $scope.aside1 = [];
                $scope.aside2 = [];
                $scope.aside3 = [];
                $scope.on = 1;
                var allFeedLength = $scope.asideData.all_feed.length;
                if (allFeedLength <= 5 && allFeedLength > 0) {
                    $scope.aside1 = $scope.asideData.all_feed.slice(0, allFeedLength);
                    $scope.asideList.push($scope.aside1);
                } else if (allFeedLength > 5 && allFeedLength <= 10) {
                    $scope.aside1 = $scope.asideData.all_feed.slice(0, 5);
                    $scope.aside2 = $scope.asideData.all_feed.slice(5, allFeedLength);
                    $scope.asideList.push($scope.aside1);
                    $scope.asideList.push($scope.aside2);
                } else if (allFeedLength > 10 && allFeedLength <= 15) {
                    $scope.aside1 = $scope.asideData.all_feed.slice(0, 5);
                    $scope.aside2 = $scope.asideData.all_feed.slice(5, 10);
                    $scope.aside3 = $scope.asideData.all_feed.slice(10, allFeedLength);
                    $scope.asideList.push($scope.aside1);
                    $scope.asideList.push($scope.aside2);
                    $scope.asideList.push($scope.aside3);
                } else if (allFeedLength > 15) {
                    $.alert('定制数量超出限制，请删除定制到15个以下后刷新页面再试');
                } else {
                    window.location.href = '/feed/new/';
                }
                /**判断是否展示aside锚点**/
                $scope.isHide = function(num) {
                    if (num === 1 && $scope.aside1.length > 0 && $scope.aside2.length > 0)
                        return false;
                    if (num === 2 && $scope.aside2.length > 0)
                        return false;
                    if (num === 3 && $scope.aside3.length > 0)
                        return false;
                    return true;
                }
                $scope.isOn = function(num) {
                    return num == $scope.on ? true : false;
                }
                /**点击锚点滑动**/
                $scope.slide = function(num, e) {
                    //更改锚点on状态
                    $scope.on = num;
                    e.preventDefault();
                    var className = 'aside-' + num,
                        $aside1 = $('.aside-1'),
                        $aside2 = $('.aside-2'),
                        $aside3 = $('.aside-3'),
                        $target = $('.' + className),
                        tLeft = $target[0].offsetLeft;
                    if (tLeft == 0) return false;
                    //锚点1
                    if (num == 1) {
                        $target.css({
                            'transition': '0.5s',
                            'left': '0'
                        });
                        $aside2.css({
                            'transition': '0.5s',
                            'left': '280px'
                        });
                        $aside3.css({
                            'transition': '0.5s',
                            'left': '560px'
                        });
                    }
                    //锚点2
                    if (num == 2) {
                        $aside1.css({
                            'transition': '0.5s',
                            'left': '-280px'
                        });
                        $target.css({
                            'transition': '0.5s',
                            'left': '0'
                        });
                        $aside3.css({
                            'transition': '0.5s',
                            'left': '280px'
                        });
                    }
                    //锚点3
                    if (num == 3) {
                        $aside1.css({
                            'transition': '0.5s',
                            'left': '-560px'
                        });
                        $aside2.css({
                            'transition': '0.5s',
                            'left': '-280px'
                        });
                        $target.css({
                            'transition': '1s',
                            'left': '0'
                        });
                    }
                }
                $scope.noFeedClick = function(e) {
                    e.preventDefault();
                    var html = '<div class="no-feed-alert">' +
                        '<h2><i class="i-warning"></i>无可用定制！</h2>' +
                        '<p class="tip">请升级会员以获取更多定制数量</p>' +
                        '<p>' +
                        '<a class="btn cancel closeLayer">取消</a>' +
                        '<a class="btn confirm" href="/vip/role_info/">去升级</a>' +
                        '</p>' +
                        '</div>';
                    $.LayerOut({
                        html: html
                    });
                    $('.closeLayer').on('click', function() {
                        $('.modal-backdrop,.modal').remove();
                        delete $._LayerOut;
                    });
                }
                //判断左边菜单项是否为选中
                $scope.checkSelected = function(item) {
                    var hashArr = window.location.hash.split('/'),
                        feedId = hashArr[hashArr.length - 2];
                    return feedId == item.feed.id ? true : false;
                }
                //判断定制是否可删除
                $scope.checkDelete = function(item) {
                    return true;
                }
                // 删除定制
                $scope.deleteFeed = function(id, $event) {
                    $scope.stopBubble($event);
                    var trg = angular.element($event.currentTarget);
                    var title = '';
                    if (trg.parent().find('.title') != null) {
                        title = '[<span class="cf46c62">' + trg.parent().find('.title').text() + '</span>]';
                    }
                    $.alert(
                        '<p class="f16 text-center"><i class="i-l-notice"></i>确定删除该定制' + title + '吗？</p><p class="text-center cf46c62" style="font-size:14px;">删除后不可恢复</p>',
                        function() {
                            var delUrl = '/feed/delete/' + id + '/';
                            location.href = delUrl;
                        }
                    );
                };
                //判断定制是否可编辑
                $scope.checkEditable = function(item) {
                    return !item.feed.has_expire && !item.feed.expire_status;
                }
                //判断定制是否待续期
                $scope.checkRenew = function(item) {
                    return item.feed.has_expire;
                }
                //判断定制是否待激活
                $scope.checkActive = function(item) {
                    return !item.feed.has_expire && item.feed.expire_status;
                }
                //判断定制是否有更新
                $scope.checkUpdate = function(item) {
                    return item.feed.unread_count > 0;
                }
                $scope.stopBubble = function(e) {
                    pbLib.stopBubble(e);
                }
                //点击定制事件
                $scope.changePage = function(item, $event) {
                    //显示更多按钮
                    var trg = angular.element($event.currentTarget);
                    var lis = angular.element(document.getElementsByClassName('feed-btns'));
                    lis.removeClass('selected-hover');
                    if (trg.attr('class').match(/selected\-hover/i)) {
                        //trg.removeClass('selected-hover');
                    } else {
                        trg.addClass('selected-hover');
                    }

                    $('body').scrollTop(0);
                    var feedId = item.feed.id; //定制id

                    if ($scope.checkRenew(item)) {
                        //定制过期，跳转至feed_renew
                        $state.go(
                            'feedRenew', {
                                feedId: feedId
                            }
                        );
                    } else if ($scope.checkActive(item)) {
                        //定制待激活，跳转至feed_active
                        $state.go(
                            'feedActive', {
                                feedId: feedId
                            }
                        );
                    } else {
                        //定制时间正确，跳转至feedResume
                        $state.go(
                            'feedResume', {
                                feedId: feedId
                            }
                        );
                    }
                }

                //定制按钮展示更多hover按钮
                $scope.showMoreBtn = function($event) {
                    $scope.stopBubble($event);
                    var trg = angular.element($event.currentTarget);
                    trg.parent().addClass('selected-hover');
                };

                //定制按钮展示更多hover按钮
                $scope.hideMoreBtn = function($event) {
                    var trg = angular.element($event.currentTarget);
                    setTimeout(function() {
                        trg.removeClass('selected-hover');
                        if (!trg.attr('class').match(/selected/i)) {
                            var trgA = angular.element(trg.find('.hover-bg')[0]);
                            if (!trgA.attr('class').match(/ng\-hide/i)) {
                                trgA.addClass('ng-hide');
                            }
                        }
                    }, 100);
                };

                //hover显示
                $scope.showFirstBtn = function($event) {
                    var trg = angular.element($event.currentTarget);
                    if (!trg.attr('class').match(/selected/i)) {
                        var trgA = angular.element(trg.find('.hover-bg')[0]);
                        if (trgA.attr('class').match(/ng\-hide/i)) {
                            trgA.removeClass('ng-hide');
                        }
                    }
                };

            }
        ]
    );


    app.controller(
        'feedResume', ['$scope', '$http', '$state',
            function($scope, $http, $state) {
                var api_url = '/special_feed/feed_list/', //请求url
                    record_url = '/special_feed/statistic/save_feed_filter/',
                    feedId = $state.params.feedId,
                    hashArr = window.location.hash.split('/');
                // 筛选器属性列表
                $scope.filter_list = {
                    work_years_min: '',
                    work_years_max: '',
                    salary_min: '',
                    salary_max: '',
                    degree: '',
                    age_min: '',
                    age_max: '',
                    gender: '',
                    experience: '',
                    current_area: ''
                };
                //是否提示推荐不准弹窗
                $scope.isShowDisLikeAlert = false;
                $scope.doNotShowDisLikeAlert = (pbLib.getCookie('do-not-show-dislike-alert') == null) ? false : true;
                //定制筛选内容
                var feedCkPrefix = pbLib.feedCkPrefix;
                $scope.getFeedId = feedId;
                $scope.choosedFeeds = pbLib.getFeedConfig(feedId);
                $scope.start = 0;
                $scope.send = 0;
                var curFeedId = $scope.getFeedId;

                $scope.latest = ($scope.choosedFeeds[curFeedId].l != null) ? $scope.choosedFeeds[curFeedId].l : 0;
                $scope.partner = ($scope.choosedFeeds[curFeedId].p != null) ? $scope.choosedFeeds[curFeedId].p : 0;
                $scope.title_match = ($scope.choosedFeeds[curFeedId].t != null) ? $scope.choosedFeeds[curFeedId].t : 1;
                $scope.extend_match = ($scope.choosedFeeds[curFeedId].e != null) ? $scope.choosedFeeds[curFeedId].e : 0;
                $scope.reco_time = ($scope.choosedFeeds[curFeedId].r != null) ? $scope.choosedFeeds[curFeedId].r : 15;
                $scope.filter_list.work_years_min = (parseInt($scope.choosedFeeds[curFeedId].minY) > 0) ? $scope.choosedFeeds[curFeedId].minY : "不限";
                $scope.filter_list.work_years_max = (parseInt($scope.choosedFeeds[curFeedId].maxY) > 0) ? $scope.choosedFeeds[curFeedId].maxY : "不限";
                $scope.filter_list.salary_min = ($scope.choosedFeeds[curFeedId].minS !== '不限' && $scope.choosedFeeds[curFeedId].minS !== '') ? $scope.choosedFeeds[curFeedId].minS : '';
                $scope.filter_list.salary_max = ($scope.choosedFeeds[curFeedId].maxS !== '不限' && $scope.choosedFeeds[curFeedId].maxS !== '') ? $scope.choosedFeeds[curFeedId].maxS : '';
                $scope.filter_list.degree = ($scope.choosedFeeds[curFeedId].degree != '不限' && $scope.choosedFeeds[curFeedId].degree != '') ? $scope.choosedFeeds[curFeedId].degree : '不限';
                $scope.filter_list.age_min = ($scope.choosedFeeds[curFeedId].minA != '不限') ? $scope.choosedFeeds[curFeedId].minA : '';
                $scope.filter_list.age_max = ($scope.choosedFeeds[curFeedId].maxA != '不限') ? $scope.choosedFeeds[curFeedId].maxA : '';
                $scope.filter_list.gender = ($scope.choosedFeeds[curFeedId].gender != '不限' && $scope.choosedFeeds[curFeedId].gender != '') ? $scope.choosedFeeds[curFeedId].gender : '不限';
                $scope.filter_list.current_area = ($scope.choosedFeeds[curFeedId].ca != '不限' && $scope.choosedFeeds[curFeedId].ca != '') ? $scope.choosedFeeds[curFeedId].ca : '不限';
                // 页面元素状态控制
                $scope.showEvaluate = true;
                $scope.total_recommend_count = 0;
                $scope.total_count = 0;
                $scope.search_count = 0;
                $scope.loadingStatus = !0;
                $scope.hasmore = 0;
                $scope.moreLoading = 0;
                $scope.dataBlank = 0;
                $scope.fromActive = '';
                $scope.fromRenew = '';
                $scope.showAgeError = false;
                $scope.show_age = false;
                $scope.show_salary = false;
                $scope.show_work_year = false;
                // 筛选器展示
                $scope.filter = true;
                $scope.showSalaryError = false;
                $scope.show_no_limit = true;
                $scope.show_salary_no_limit = true;
                $scope.show_age_no_limit = true;
                //现居地
                $scope.current_area = [{
                    name: '不限',
                    value: '不限'
                }];
                $scope.showNoLimit = function(min, max, show, string, textobj) {
                    if (min > 0 && (isNaN(max) || max <= 0)) {
                        $scope[show] = true;
                        $(textobj).text(min + string + '以上')
                    } else if ((isNaN(min) || min <= 0) && max > 0) {
                        $scope[show] = true;
                        $(textobj).text(max + string + '以下')
                    } else if ((isNaN(min) || min <= 0) && (isNaN(max) || max <= 0)) {
                        $scope[show] = true;
                        $(textobj).text('不限');
                    } else if (min > 0 && max > 0) {
                        $scope[show] = false;
                    }
                }

                //当前定制的现居地
                var current_area_value = [];
                $scope.asideData = window.asideData;
                //当前定制职位名称
                $scope.currentFeedTitle = '';
                $scope.recent_salary = '';

                $scope.showAge = function() {
                    $scope.show_age = true;
                }
                $scope.showSalary = function() {
                    $scope.show_salary = true;
                }
                $scope.showWorkYear = function() {
                    $scope.show_work_year = true;
                }
                //判断满足筛选条件的薪资
                $scope.hasRecentSalary = function(item) {
                    $scope.recent_salary = item.resume.works[0].salary || item.resume.current_salary || item.resume.latest_salary || '';
                    $scope.recent_salary = $scope.recent_salary.trim();
                    return ($scope.recent_salary === "") ? false : true;
                };

                //salary取整
                var adjustSalry = function(k) {
                    if (parseInt(k) < 1000 || parseInt(k) > 25000) return '';
                    return '' + parseInt(parseInt(k) / 1000);
                };
                for (var i = 0, imax = asideData.all_feed.length; i < imax; i++) {
                    if (asideData.all_feed[i].feed.id == feedId) {
                        current_area_value = asideData.all_feed[i].feed.expect_area.split(',');
                        if ($scope.filter_list.salary_min === '') {
                            $scope.filter_list.salary_min = adjustSalry(asideData.all_feed[i].feed.salary_min);

                        };
                        if ($scope.filter_list.salary_max ==='') {
                            $scope.filter_list.salary_max = adjustSalry(asideData.all_feed[i].feed.salary_max);
                        };
                        $scope.currentFeedTitle = asideData.all_feed[i].feed.title;
                        break;
                    }
                }
                for (var i = 0; i < current_area_value.length; i++) {
                    $scope.current_area[i + 1] = new Object();
                    $scope.current_area[i + 1].name = current_area_value[i];
                    $scope.current_area[i + 1].value = current_area_value[i];
                }
                $scope.showNoLimit($scope.filter_list.work_years_min, $scope.filter_list.work_years_max, 'show_no_limit', '年', '.js-no-limit');
                $scope.showNoLimit($scope.filter_list.salary_min, $scope.filter_list.salary_max, 'show_salary_no_limit', 'k', '.js-salary-no-limit');
                $scope.showNoLimit($scope.filter_list.age_min, $scope.filter_list.age_max, 'show_age_no_limit', '岁', '.js-age-no-limit');
                var loopData = function(dataName, dataLength, num) {
                        if (num) {
                            for (var i = 0; i < dataLength; i++) {
                                dataName[i + 1] = new Object();
                                dataName[i + 1].name = i + 1;
                                dataName[i + 1].value = i + 1;
                            }
                        } else {
                            for (var i = 0; i < dataLength; i++) {
                                dataName[i + 1] = new Object();
                                dataName[i + 1].name = (i + 1) + 'k';
                                dataName[i + 1].value = (i + 1) * 1000;
                            }
                        }
                    }
                    // 需逻辑控制的筛选器列表项
                $scope.work_years_min = [{
                    name: '不限',
                    value: "不限"
                }];
                loopData($scope.work_years_min, 10, true);

                $scope.work_years_max = [{
                    name: '不限',
                    value: "不限"
                }];
                loopData($scope.work_years_max, 10, true);
                // 判断定制激活或续期状态
                if (hashArr[hashArr.length - 2] == feedId) {
                    $scope.fromActive = window.location.hash.indexOf('fromActive') != -1 ? 'fromActive' : '';
                    $scope.fromRenew = window.location.hash.indexOf('fromRenew') != -1 ? 'fromRenew' : '';
                };

                $scope.isShowFavAlert = false;
                $scope.doNotShowFavAlert = (pbLib.getCookie('do-not-show-fav-alert') == null) ? false : true;

                var countDayByDay = function(offsetNum) {
                    var getDateObj = function(t) {
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
                    };
                    var monthStartObj = getDateObj();
                    var monthEnd = new Date(monthStartObj.y, monthStartObj.m - 1, monthStartObj.d + offsetNum, monthStartObj.h, monthStartObj.i, monthStartObj.s);
                    return monthEnd.getFullYear() + '-' + (monthEnd.getMonth() + 1) + '-' + monthEnd.getDate();
                };

                //区分推荐日期
                $scope.today = countDayByDay(0);
                $scope.yesterday = countDayByDay(-1);
                $scope.sevenday = countDayByDay(-7);
                $scope.listDays = [];
                var getDay = function(str) {
                    if (typeof str == 'string' && str.match(/^([0-9]{4})\-([0-9]{1,2})\-([0-9]{1,2}) /i)) {
                        var y = parseInt(RegExp.$1);
                        var m = parseInt(RegExp.$2);
                        var d = parseInt(RegExp.$3);
                        return y + '-' + m + '-' + d;
                    }
                    return '';
                };
                var inArray = function(needle, array) {
                    for (var i = 0, imax = array.length; i < imax; i++) {
                        if (needle == array[i]) {
                            return true;
                        }
                    }
                    return false;
                };
                $scope.getDay = function(displayTime) {
                    return getDay(displayTime);
                };
                $scope.isHideDateBar = function(displayTime) {
                    return false;
                };
                $scope.dateTitle = function($index, displayTime) {
                    if ($scope.isToday(displayTime)) {
                        return " 今天 (" + getDay(displayTime) + ") ";
                    } else if ($scope.isYesterday(displayTime)) {
                        return " 昨天 (" + getDay(displayTime) + ") ";
                    } else if ($scope.isSevenday(displayTime)) {
                        return " 7天前 (" + getDay(displayTime) + ") ";
                    } else {
                        return " " + getDay(displayTime) + " ";
                    }
                };
                $scope.isToday = function(displayTime) {
                    return false;
                    var theDay = getDay(displayTime);
                    if (theDay == countDayByDay(0)) return true;
                    return false;
                };
                $scope.isYesterday = function(displayTime) {
                    return false;
                    var theDay = getDay(displayTime);
                    if (theDay == countDayByDay(-1)) return true;
                    return false;
                };
                $scope.isSevenday = function(displayTime) {
                    return false;
                    var theDay = getDay(displayTime);
                    if (theDay <= countDayByDay(-7)) return true;
                    return false;
                };
                $scope.isOtherday = function(displayTime) {
                    return false;
                    var theDay = getDay(displayTime);
                    if (theDay != countDayByDay(0) && theDay != countDayByDay(-1) && theDay != countDayByDay(-7)) return true;
                    return false;
                };

                // 页面初始化请求地址，加载更多及筛选器请求地址
                $scope.public_url = function() {
                    var salary_min = (parseInt($scope.filter_list.salary_min) > 0) ? $scope.filter_list.salary_min * 1000 : '';
                    var salary_max = (parseInt($scope.filter_list.salary_max) > 0) ? $scope.filter_list.salary_max * 1000 : '';
                    var work_years_min = (parseInt($scope.filter_list.work_years_min) > 0) ? $scope.filter_list.work_years_min : '';
                    var work_years_max = (parseInt($scope.filter_list.work_years_max) > 0) ? $scope.filter_list.work_years_max : '';
                    var age_min = (parseInt($scope.filter_list.age_min) > 0) ? $scope.filter_list.age_min : '';
                    var age_max = (parseInt($scope.filter_list.age_max) > 0) ? $scope.filter_list.age_max : '';
                    var degree = ($scope.filter_list.degree != '不限') ? $scope.filter_list.degree : '';
                    var gender = ($scope.filter_list.gender != '不限') ? $scope.filter_list.gender : '';
                    var current_area = ($scope.filter_list.current_area != '不限') ? $scope.filter_list.current_area : '';
                    return '?start=' + $scope.start +
                        '&latest=' + $scope.latest +
                        '&send=' + $scope.send +
                        '&partner=' + $scope.partner +
                        '&title_match=' + $scope.title_match +
                        '&extend_match=' + $scope.extend_match +
                        '&reco_time=' + $scope.reco_time +
                        '&work_years_min=' + work_years_min +
                        '&work_years_max=' + work_years_max +
                        '&salary_min=' + salary_min +
                        '&salary_max=' + salary_max +
                        '&degree=' + degree +
                        '&age_min=' + age_min +
                        '&age_max=' + age_max +
                        '&gender=' + gender +
                        '&experience=' + $scope.filter_list.experience +
                        '&current_area=' + current_area;
                };

                $scope.ajax_url = api_url + feedId;
                $scope.record_url = record_url + feedId;
                // 页面初始化发起数据请求
                $scope.setRecordAjax = function() {
                    //$scope.start = 0;
                    $http.get($scope.record_url + $scope.public_url()).success(function(data) {})
                };
                $scope.setRecordAjax();
                // 页面初始化发起数据请求
                var httpGet = $http.get($scope.ajax_url + $scope.public_url()).success(function(data) {
                    if (data && data.status == 'ok') {
                        $scope.data = data;
                        $scope.loadingStatus = 0;
                        $scope.total_recommend_count = data.total_recommend_count;
                        $scope.total_count = data.total_count;
                        $scope.search_count = data.feed_query_count;
                        $scope.start = data.next_start;
                        $scope.hasmore = !0;
                        //初始各简历删除状态为0
                        for (var i = $scope.data.data.length - 1; i >= 0; i--) {
                            $scope.data.data[i].deleteStatus = 0;
                        };
                        // 已请求的数据大于等于总数时，隐藏加载更多
                        if (parseInt(data.start + 1) * 5 >= $scope.total_recommend_count) {
                            $scope.hasmore = 0;
                        }
                        // 判断页面初始化时没有推荐数据，跳转至空白页
                        var cookie_exit = false;
                        if ($scope.choosedFeeds[curFeedId].l || $scope.choosedFeeds[curFeedId].p || $scope.choosedFeeds[curFeedId].e || $scope.choosedFeeds[curFeedId].r) {
                            cookie_exit = true;
                        };

                        if (($scope.data.data.length === 0) && cookie_exit) {
                            $scope.hasmore = 0;
                            $scope.dataBlank = !0;
                            $scope.filter = true;
                        } else if (($scope.data.data.length === 0) && !cookie_exit) {
                            $scope.hasmore = 0;
                            $scope.filter = true;
                            /*$state.go(
                                'feedBlank', {
                                    feedId: feedId,
                                    source: $scope.fromActive
                                }
                            );*/
                        }
                        $scope.toggleSearchInfo();

                    };
                }).error(function(data) {
                    console.log(data);
                    window.location.reload();
                });
                $scope.checkFeedPartner = function() {
                    return $scope.partner === 0 ? true : false;
                }
                $scope.checkFeedApply = function() {
                    return $scope.send === 0 ? true : false;
                }
                $scope.checkFeedLatest = function() {
                    return $scope.latest === 0 ? true : false;
                }
                $scope.checkFeedTitle = function() {
                    return $scope.title_match === 1 ? true : false;
                }
                $scope.checkFeedExtend = function() {
                    return $scope.extend_match === 1 ? true : false;
                }
                //切换搜索信息

                $scope.toggleSearchInfo = function(count) {
                    //$('.feed-meta-search .search-target-count').text(count);
                    var isPartner = false;
                    var isApply = false;
                    $('.feed-apply-option').each(function(i) {
                        if ($(this).attr('class').match(/feed\-apply\-option\-partner/i)) {
                            if ($(this).attr('class').match(/feed\-option\-false/i)) {
                                isPartner = false;
                            } else {
                                isPartner = true;
                            }
                        } else if ($(this).attr('class').match(/feed\-apply\-option\-apply/i)) {
                            if ($(this).attr('class').match(/feed\-option\-false/i)) {
                                isApply = false;
                            } else {
                                isApply = true;
                            }
                        }
                    });
                    if ((isPartner && !isApply) || (!isPartner && isApply)) {
                        if (isPartner) $('.feed-meta-search .search-target').text($('.feed-apply-option-partner').text());
                        if (isApply) $('.feed-meta-search .search-target').text($('.feed-apply-option-apply').text());
                    } else {
                        $('.feed-meta-search .search-target').text('');
                    }
                    if (isPartner || isApply) {
                        $('.feed-meta-search').show();
                        $('.feed-meta').hide();
                    } else {
                        $('.feed-meta-search').hide();
                        $('.feed-meta').show();
                    }
                }


                $scope.togglePartner = function() {
                    if ($scope.partner === 0) {
                        $scope.partner = 1;
                        pbLib.setFeedConfig($scope, {
                            p: 1
                        });
                    } else {
                        $scope.partner = 0;
                        pbLib.setFeedConfig($scope, {
                            p: 0
                        });
                    }
                    $scope.getAjaxData();
                    $scope.setRecordAjax();
                }
                $scope.toggleApply = function() {
                    $scope.send = $scope.send === 0 ? 1 : 0;
                    $scope.getAjaxData();
                    $scope.setRecordAjax();
                }
                $scope.toggleLatest = function() {
                    if ($scope.latest === 0) {
                        $scope.latest = 1;
                        pbLib.setFeedConfig($scope, {
                            l: 1
                        });
                    } else {
                        $scope.latest = 0;
                        pbLib.setFeedConfig($scope, {
                            l: 0
                        });
                    }
                    $scope.getAjaxData();
                    $scope.setRecordAjax();
                }
                $scope.timeShow = false;
                $scope.toggleTitle = function() {
                    if ($scope.title_match !== 1) {
                        $scope.title_match = 1;
                        pbLib.setFeedConfig($scope, {
                            t: 1
                        });
                        $scope.extend_match = 0;
                        pbLib.setFeedConfig($scope, {
                            e: 0
                        });
                    }
                    $scope.timeShow = false;
                    $scope.getAjaxData();
                    $scope.setRecordAjax();
                };

                //初始状态判断是否显示筛选日期
                if ($scope.extend_match == 1) {
                    $scope.timeShow = true;
                };
                $scope.toggleExtend = function() {
                    if ($scope.extend_match !== 1) {
                        $scope.extend_match = 1;
                        pbLib.setFeedConfig($scope, {
                            e: 1
                        });
                        $scope.title_match = 0;
                        pbLib.setFeedConfig($scope, {
                            t: 0
                        });
                    }
                    $scope.timeShow = true;
                    $scope.getAjaxData();
                    $scope.setRecordAjax();
                }
                $scope.toggleEvaluate = function(e) {
                    var $target = $(e.currentTarget),
                        $span = $target.find('span');
                    $span.css('display') === 'none' ? $span.removeClass('ng-hide') : $span.addClass('ng-hide');
                }
                //扩展匹配切换筛选日期
                $scope.changeTime = function($event) {
                    var _this = angular.element($event.currentTarget);
                    var extent_time = _this.attr('data-time');
                    if (!_this.hasClass('feed-expand-time-choose')) {
                        $scope.reco_time = extent_time;
                        pbLib.setFeedConfig($scope, {
                            r: extent_time
                        });
                        //setCookie('reco_time_cookie',extent_time);
                        _this.parent().children().removeClass('feed-expand-time-choose');
                        _this.addClass('feed-expand-time-choose');
                        $scope.getAjaxData();
                        $scope.setRecordAjax();
                    }
                }
                // 筛选条件发起ajax请求
                $scope.getAjaxData = function() {
                    $scope.hasmore = 0;
                    $scope.loadingStatus = !0;
                    $scope.dataBlank = 0;
                    $scope.start = 0;
                    $scope.hasmore = 0;
                    $scope.moreLoading = 0;
                    $http.get($scope.ajax_url + $scope.public_url()).success(function(data) {
                        if (data && data.status == 'ok') {
                            $scope.data = data;
                            $scope.loadingStatus = 0;
                            $scope.start = data.next_start;
                            $scope.hasmore = !0;
                            //筛选没有数据
                            if ($scope.data.data.length === 0) {
                                $scope.hasmore = 0;
                                $scope.dataBlank = !0;
                            }
                            $scope.total_recommend_count = data.total_recommend_count;
                            // 已请求的数据大于等于总数时，隐藏加载更多
                            if (parseInt(data.start + 1) * 5 >= $scope.total_recommend_count) {
                                $scope.hasmore = 0;
                            }
                            $scope.search_count = data.feed_query_count;

                            $scope.toggleSearchInfo(data.feed_query_count);
                        };
                    }).error(function(data) {
                        console.log(data);
                        window.location.reload();
                    });
                }

                $scope.reset = function() {
                    pbLib.delCookie(pbLib.feedCkPrefix + $scope.getFeedId);
                    $scope.filter_list.work_years_min = "不限";
                    $scope.filter_list.work_years_max = "不限";
                    $scope.filter_list.salary_min = '';
                    $scope.filter_list.salary_max = '';
                    $scope.filter_list.degree = '不限';
                    $scope.filter_list.age_min = '';
                    $scope.filter_list.age_max = '';
                    $scope.filter_list.gender = '不限';
                    $scope.filter_list.current_area = '不限';
                    $scope.showNoLimit($scope.filter_list.work_years_min, $scope.filter_list.work_years_max, 'show_no_limit', '年', '.js-no-limit');
                    $scope.showNoLimit($scope.filter_list.salary_min, $scope.filter_list.salary_max, 'show_salary_no_limit', 'k', '.js-salary-no-limit');
                    $scope.showNoLimit($scope.filter_list.age_min, $scope.filter_list.age_max, 'show_age_no_limit', '岁', '.js-age-no-limit');
                }

                //简历有更新
                $scope.hasUpdated = false;
                $scope.checkDownloadStatus = function(item) {
                    if (item && item.contact_info && !pbLib.isEmptyObj(item.contact_info)) {
                        return true;
                    } else {
                        return false;
                    }
                }
                $scope.checkReadStatus = function(item, status) {
                    //如果已下载就不显示未读
                    if ($scope.checkDownloadStatus(item)) return false;
                    return status == 'unread';
                }
                $scope.changeReadStatus = function(item) {
                    item.user_read_status = 'read';
                }
                $scope.clickToDetail = function(event, item) {
                    item.user_read_status = 'read';
                    var url = event.currentTarget.getAttribute('data-resume-detail-url');
                    if (event.target.getAttribute("class").match(/^i\-/i)) {
                        $scope.stopBubble(event);
                    } else {
                        window.open(url);
                    }
                    return false;
                }
                $scope.deleteItem = function(item) {
                    if (!item.deleteStatus) {

                        if (!$scope.isShowDisLikeAlert && !$scope.doNotShowDisLikeAlert) {
                            pbFunc.simpleAlert('谢谢您的反馈！', '<div class="text-center"><span class="big-icon big-icon-flower mt20"></span><span class="mt20 block f14 c607d8b">您的反馈<span class="cf46c62">有助于</span>算法为您推荐更匹配<span class="c434343"> ' + $scope.currentFeedTitle + ' </span>的简历！</span><div class="mt20"><input type="checkbox" name="do-not-show-dislike-alert" id="do-not-show-dislike-alert"  value="1" class="" > <label for="do-not-show-dislike-alert"><span class="f14 cf46c62">不再提醒</span></label></div></div>', function(trg, args) {
                                if ($('#do-not-show-dislike-alert').is(':checked')) {
                                    var timeLapse = 365;
                                    pbLib.setCookie('do-not-show-dislike-alert', 1, timeLapse * 86400000);
                                    $scope.doNotShowDisLikeAlert = true;
                                }
                            }, null, '我知道了', false);
                        }
                        //标记为删除
                        item.deleteStatus = !0;
                        $.get("/feed/modify_feed_result", {
                            feed_id: feedId,
                            resume_id: item.resume.id,
                            reco_index: "-150"
                        });
                    } else {
                        //已标记为删除，恢复
                        item.deleteStatus = 0;
                        $.get("/feed/modify_feed_result", {
                            feed_id: feedId,
                            resume_id: item.resume.id,
                            reco_index: "150"
                        });
                    }
                }
                $scope.stopBubble = function(e) {
                    e = e ? e : window.event;
                    if (window.event) {
                        e.cancelBubble = true;
                    }
                    e.stopPropagation();
                }
                //hover show
                $scope.showHoverTip = function(event) {
                    var cls = event.currentTarget.getAttribute('class');
                    if (cls.match(/i\-(fav|delete)\-([0-9a-z]+)/i)) {
                        var trg = RegExp.$1;
                        var baseLen = new String('收藏该候选人').length;
                        var trgId = '.i-' + trg + '-delete-hover-' + RegExp.$2;
                        var trgNoticeId = '.i-' + trg + '-delete-notice-' + RegExp.$2;
                        if (trg != 'fav') {
                            //计算新宽度
                            var newWidth = parseInt(72 * ($(trgId).text().length / baseLen));
                            var newWidth2 = parseInt(72 * ($(trgNoticeId).text().length / baseLen));
                            $(trgId).css('width', newWidth + 'px');
                            $(trgNoticeId).css('width', newWidth2 + 'px');
                        } else {
                            $(trgId).css('width', '72px');
                        }
                        $(trgId).show();
                    }
                }
                //hover hide
                $scope.hideHoverTip = function(event) {
                    var cls = event.currentTarget.getAttribute('class');
                    if (cls.match(/i\-(fav|delete)\-([0-9a-z]+)/i)) {
                        var trg = RegExp.$1;
                        var trgId = '.i-' + trg + '-delete-hover-' + RegExp.$2;
                        $(trgId).hide();
                    }
                }
                $scope.favItem = function(item, $event) {
                    // /resumes/add_watch/{{resume.id}}?feed_keywords={{feed_keywords}}&feed_id={{feed_id}}
                    if (!item.favStatus) {

                        if (!$scope.isShowFavAlert && !$scope.doNotShowFavAlert) {
                            var feed_title = $('.aside-1 > li.selected').find('span.title').text();
                            pbFunc.simpleAlert('简历收藏成功！', '<div class="text-center"><span class="big-icon big-icon-rocket mt20"></span><span class="mt20 block f14 c607d8b">多多收藏喜欢的人才，我们将为你推荐更多匹配<span class="c434343"> ' + feed_title + ' </span>职位的人才～</span><div class="mt20"><input type="checkbox" name="do-not-show-fav-alert" id="do-not-show-fav-alert"  value="1" class=""> <label for="do-not-show-fav-alert"><span class="f14 cf46c62">不再提醒</span></label></div></div>', function(trg, args) {
                                if ($('#do-not-show-fav-alert').is(':checked')) {
                                    var timeLapse = 365;
                                    pbLib.setCookie('do-not-show-fav-alert', 1, timeLapse * 86400000);
                                    $scope.doNotShowFavAlert = true;
                                }
                            }, null, '我知道了', false);
                        }
                        $scope.isShowFavAlert = true;

                        //标记为关注
                        item.favStatus = !0;
                        $.get("/resumes/add_watch/" + item.resume.id, {
                            feed_id: feedId,
                            feed_keywords: item.feed.keywords.join(' ')
                        });
                    } else {
                        //已标记为关注，恢复
                        item.favStatus = 0;
                        $.get("/resumes/remove_watch/" + item.resume.id, {
                            feed_id: feedId,
                            feed_keywords: item.feed.keywords.join(' ')
                        });
                    }
                }

                $scope.showMoreInfo = function($event, item) {
                    var trg = $event.currentTarget;
                    var moreBox = angular.element(trg).find('.item-view-more-info')[0];
                    if ($scope.chkLineNum(item) > 0) {
                        angular.element(moreBox).css('display', 'block');
                        var moreBoxUl = angular.element(trg).find('.item-view-more-info-ul')[0];
                        var oriTop = parseInt(angular.element(moreBoxUl).css('top'));
                        if ($scope.isSingleLine(item)) {
                            angular.element(moreBoxUl).css('top', '-62px');
                        } else {
                            angular.element(moreBoxUl).css('top', '-86px');
                        }
                        angular.element(moreBoxUl).css('opacity', '1.0');
                    }
                };
                $scope.hideMoreInfo = function($event, item) {
                    var trg = $event.currentTarget;
                    var moreBox = angular.element(trg).find('.item-view-more-info')[0];
                    if ($scope.chkLineNum(item) > 0) {

                        var moreBoxUl = angular.element(trg).find('.item-view-more-info-ul')[0];
                        var oriTop = parseInt(angular.element(moreBoxUl).css('top'));
                        angular.element(moreBoxUl).css('top', '0px');
                        angular.element(moreBoxUl).css('opacity', '1.0');
                        setTimeout(function() {
                            angular.element(moreBox).css('display', 'none');
                        }, 300);
                    }
                };
                $scope.chkLineNum = function(item) {
                    var lineNum = 0;
                    if ($scope.isNotEmptyObj(item.mark_log)) {
                        lineNum++;
                    }
                    if ($scope.isNotEmptyObj(item.comment_log)) {
                        lineNum++;
                    }
                    return lineNum;
                };
                $scope.isSingleLine = function(item) {
                    if ($scope.chkLineNum(item) == 1) {
                        return true;
                    } else {
                        return false;
                    }
                };
                $scope.isNotEmptyObj = function(obj) {
                    if (typeof obj != 'object') return false;
                    for (var t in obj) {
                        if (obj[t] != undefined) {
                            return true;
                        }
                    }
                    return false;
                };
                $scope.notEmpty = function(trg) {
                    if (trg != null && trg != undefined) {
                        return false;
                    } else {
                        if (typeof trg == 'string' && trg.trim() != '') {
                            return true;
                        } else {
                            return false;
                        }
                    }
                };

                // 加载更多
                $scope.fetchMore = function() {
                    $scope.hasmore = 0;
                    $scope.moreLoading = !0;
                    if ($scope.start != -1) {
                        $scope.setRecordAjax();
                        $http.get($scope.ajax_url + $scope.public_url()).success(function(data) {
                            if (data && data.status == 'ok') {
                                if (data.data.length != 0) {
                                    $scope.data.data = $scope.data.data.concat(data.data);
                                }
                                $scope.hasmore = !0;
                                $scope.moreLoading = 0;
                                $scope.start = data.next_start;
                            };
                        }).error(function(data) {
                            console.log(data);
                            window.location.reload();
                        });
                    } else {
                        $scope.hasmore = 0;
                        $scope.moreLoading = 0;
                    }
                }
                $scope.closeActiveTip = function() {
                    $('.active-success').hide();
                }
                $scope.closeRenewTip = function() {
                    $('.renew-success').hide();
                }
                var _chooseSearchFilter = function($event, $scope) {
                    var _this = angular.element($event.currentTarget);
                    var search_fields = _this.attr('search-fields');
                    $scope.search_fields = search_fields;
                    $('.filter-factor-choose').removeClass('filter-factor-choose');
                    $('#js-search-filter').text(_this.text())
                    _this.addClass('filter-factor-choose');
                    $scope.showFilter = false;
                };

                // min筛选器的逻辑控制
                $scope.minChange = function(min_obj, dest_list_str, setCookie) {
                    var min_value = min_obj;
                    switch (dest_list_str) {
                        case 'work_years_max':
                            for (var i = $scope.work_years_max.length - 1; i >= 0; i--) {
                                if (min_value != '不限' && $scope.work_years_max[i].value != '不限' && $scope.work_years_max[i].value <= min_value) {
                                    $('#JS_work_years_max option').eq(i).attr('disabled', 'disabled');
                                } else {
                                    $('#JS_work_years_max option').eq(i).removeAttr('disabled');
                                }
                            };
                            if (setCookie) {
                                pbLib.setFeedConfig($scope, {
                                    minY: $scope.filter_list.work_years_min
                                });
                                $scope.showNoLimit($scope.filter_list.work_years_min, $scope.filter_list.work_years_max, 'show_no_limit', '年', '.js-no-limit');
                            }
                            break;
                        default:
                            break;
                    }
                }
                // max筛选器的逻辑控制
                $scope.maxChange = function(max_obj, dest_list_str, setCookie) {
                    var max_value = max_obj;
                    switch (dest_list_str) {
                        case 'work_years_min':
                            for (var i = $scope.work_years_min.length - 1; i >= 0; i--) {
                                if (max_value != '不限' && $scope.work_years_min[i].value != '不限' && $scope.work_years_min[i].value >= max_value) {
                                    $('#JS_work_years_min option').eq(i).attr('disabled', 'disabled');
                                } else {
                                    $('#JS_work_years_min option').eq(i).removeAttr('disabled');
                                }
                            };
                            if (setCookie) {
                                pbLib.setFeedConfig($scope, {
                                    maxY: $scope.filter_list.work_years_max
                                });
                                $scope.showNoLimit($scope.filter_list.work_years_min, $scope.filter_list.work_years_max, 'show_no_limit', '年', '.js-no-limit');
                            }

                            break;
                        default:
                            break;
                    }
                }
                setTimeout(function() {
                    $scope.minChange($scope.filter_list.work_years_min, 'work_years_max', false);
                    $scope.maxChange($scope.filter_list.work_years_max, 'work_years_min', false);
                }, 500);
                $scope.setDegreeCookie = function() {
                    pbLib.setFeedConfig($scope, {
                        degree: $scope.filter_list.degree
                    });
                }
                $scope.setGenderCookie = 　 function() {
                    pbLib.setFeedConfig($scope, {
                        gender: $scope.filter_list.gender
                    });
                }
                $scope.setCaCookie = function() {
                    pbLib.setFeedConfig($scope, {
                        ca: $scope.filter_list.current_area
                    });
                }
                // 验证年龄输入
                $scope.validateAgeInput = function(age) {
                    var numReg = /^[1-9]\d*$/,
                        age = parseInt(age);
                    if (!isNaN(age)) {
                        if ((!numReg.test(age))) {
                            return true;
                        }
                    }
                    return false;
                }
                $scope.validateSalaryInput = function(age) {
                    var plusnumReg = /^[0-9]\d*$/,
                        age = parseInt(age);
                    if (!isNaN(age)) {
                        if ((!plusnumReg.test(age))) {
                            return true;
                        }
                    }
                    return false;
                }
                // 验证age_min和age_min的大小关系
                $scope.validateAge = function($event) {
                    $this = angular.element($event.target);
                    $scope.filter_list.age_max = parseInt($scope.filter_list.age_max);
                    $scope.filter_list.age_min = parseInt($scope.filter_list.age_min);
                    if ($this.attr('name') == 'age_min' || $this.attr('name') == 'age_max') {
                        if (isNaN($scope.filter_list.age_max) || isNaN($scope.filter_list.age_min)) {
                            $scope.showAgeError = false;
                        } else if ($scope.filter_list.age_max < $scope.filter_list.age_min && $scope.filter_list.age_max !== 0) {
                            $scope.showAgeError = true;
                        } else {
                            $scope.showAgeError = false;
                        }
                        if (isNaN($scope.filter_list.age_max)) {
                            $scope.filter_list.age_max = '';
                        };
                        if (isNaN($scope.filter_list.age_min)) {
                            $scope.filter_list.age_min = '';
                        };
                    }
                    if ($this.attr('name') == 'age_min') {
                        pbLib.setFeedConfig($scope, {
                            minA: $scope.filter_list.age_min
                        });
                    };
                    if ($this.attr('name') == 'age_max') {
                        pbLib.setFeedConfig($scope, {
                            maxA: $scope.filter_list.age_max
                        });
                    };
                    $scope.showNoLimit($scope.filter_list.age_min, $scope.filter_list.age_max, 'show_age_no_limit', '岁', '.js-age-no-limit');
                }
                $scope.validateSalary = function($event) {
                    $this = angular.element($event.target);
                    $scope.filter_list.salary_min = parseInt($scope.filter_list.salary_min);
                    $scope.filter_list.salary_max = parseInt($scope.filter_list.salary_max);
                    if ($this.attr('name') == 'salary_min' || $this.attr('name') == 'salary_max') {
                        if (isNaN($scope.filter_list.salary_min) || isNaN($scope.filter_list.salary_max)) {
                            $scope.showSalaryError = false;
                        } else if ($scope.filter_list.salary_max < $scope.filter_list.salary_min && $scope.filter_list.salary_max !== 0) {
                            $scope.showSalaryError = true;
                        } else {
                            $scope.showSalaryError = false;
                        }
                    }
                    if (isNaN($scope.filter_list.salary_max)) {
                        $scope.filter_list.salary_max = '';
                    };
                    if (isNaN($scope.filter_list.salary_min)) {
                        $scope.filter_list.salary_min = '';
                    };
                    if ($this.attr('name') == 'salary_min') {
                        pbLib.setFeedConfig($scope, {
                            minS: $scope.filter_list.salary_min
                        });
                    };
                    if ($this.attr('name') == 'salary_max') {
                        pbLib.setFeedConfig($scope, {
                            maxS: $scope.filter_list.salary_max
                        });
                    }
                    $scope.showNoLimit($scope.filter_list.salary_min, $scope.filter_list.salary_max, 'show_salary_no_limit', 'k', '.js-salary-no-limit');
                }

                // 触发筛选器
                $scope.triggerFilter = function() {
                    if ($('.age-error').css('display') === undefined) {
                        $scope.getAjaxData();
                        $scope.setRecordAjax();
                    }
                };
                //隐藏select
                $scope.hideSelect = function($event) {
                    hideSelect($event, $scope);
                };

            }
        ]
    );

    app.controller(
        'feedBlank', ['$scope', '$http', '$state',
            function($scope, $http, $state) {
                var feedId = $state.params.feedId,
                    hashArr = window.location.hash.split('/');
                if (hashArr[hashArr.length - 2] == feedId) {
                    $scope.fromActive = window.location.hash.indexOf('fromActive') != -1 ? 'fromActive' : '';
                    $scope.fromRenew = window.location.hash.indexOf('fromRenew') != -1 ? 'fromRenew' : '';
                }
                $scope.closeActiveTip = function() {
                    $('.active-success').hide();
                }
                $scope.closeRenewTip = function() {
                    $('.renew-success').hide();
                }
            }
        ]
    );
    app.controller(
        'feedRenew', ['$scope', '$http', '$state',
            function($scope, $http, $state) {
                $scope.feedId = $state.params.feedId;
                $scope.asideData = window.asideData;
                for (var i = $scope.asideData.all_feed.length - 1; i >= 0; i--) {
                    if ($scope.asideData.all_feed[i].feed.id === $scope.feedId) {
                        $scope.feedItem = $scope.asideData.all_feed[i];
                    }
                };
                $scope.continue_feed = function(feedItem) {
                    var continue_url = '/special_feed/renewal_feed/' + feedItem.feed['id'];
                    $http.get(continue_url).success(function(data) {
                        if (data && data.status == 'ok') {
                            var hash = '#/feed_resume/' + feedItem.feed['id'] + '/?fromRenew';
                            window.location.hash = hash;
                            feedItem.feed.has_expire = false;
                        } else {
                            $.alert('<p class="alert-notice-center"><span>请求失败，请稍后再试！</span></p>');
                        }
                    }).error(function(data) {
                        console.log(data);
                        window.location.reload();
                    });
                };
                $scope.finish = function(feedItem) {
                    var delete_url = '/feed/delete/' + feedItem.feed['id'],
                        html = '<div class="feed-finish-alert">' +
                        '<p class="info">' +
                        '<i class="i-warning"></i>' +
                        '恭喜！点击确定立即删除该条定制<br>之后你可以开始创建新的定制' +
                        '</p>' +
                        '<p>' +
                        '<a class="btn cancel closeLayer">取消</a>' +
                        '<a class="btn confirm" href="' +
                        delete_url +
                        '">确定</a>' +
                        '</p>' +
                        '</div>';
                    $.LayerOut({
                        html: html
                    });
                    $('.closeLayer').on('click', function() {
                        $('.modal-backdrop,.modal').remove();
                        delete $._LayerOut;
                    });
                };
                $scope.JS_viewHistory = function(feedItem) {
                    var feedId = feedItem.feed['id'];
                    $state.go(
                        'feedResume', {
                            feedId: feedId
                        }
                    );
                }
            }
        ]
    );
    app.controller(
        'feedActive', ['$scope', '$http', '$state',
            function($scope, $http, $state) {
                $scope.feedId = $state.params.feedId;
                $scope.asideData = window.asideData;
                for (var i = $scope.asideData.all_feed.length - 1; i >= 0; i--) {
                    if ($scope.asideData.all_feed[i].feed['id'] === $scope.feedId) {
                        $scope.feedItem = $scope.asideData.all_feed[i];
                    }
                };
                $scope.continue_feed = function(feedItem) {
                    var continue_url = '/special_feed/reset_feed_expire/' + feedItem.feed['id'];
                    $http.get(continue_url).success(function(data) {
                        if (data && data.status == 'ok') {
                            var hash = '#/feed_resume/' + feedItem.feed['id'] + '/?fromActive';
                            window.location.hash = hash;
                            feedItem.feed.expire_status = false;
                        } else {
                            $.alert('<p class="alert-notice-center"><span>请求失败，请稍后再试！</span></p>');
                        }
                    }).error(function(data) {
                        console.log(data);
                        window.location.reload();
                    });
                };
                $scope.finish = function(feedItem) {
                    var delete_url = '/feed/delete/' + feedItem.feed['id'],
                        html = '<div class="feed-finish-alert">' +
                        '<i class="closeLayer i-close"></i>' +
                        '<p class="info">' +
                        '<i class="i-warning"></i>' +
                        '恭喜！点击确定立即删除该条定制<br>现在你可以开始创建新的定制' +
                        '</p>' +
                        '<p>' +
                        '<a class="btn cancel closeLayer">取消</a>' +
                        '<a class="btn confirm" href="' +
                        delete_url +
                        '">确定</a>' +
                        '</p>' +
                        '</div>';
                    $.LayerOut({
                        html: html
                    });
                    $('.closeLayer').on('click', function() {
                        $('.modal-backdrop,.modal').remove();
                        delete $._LayerOut;
                    });
                };
            }
        ]
    );

    app.directive('asideInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('special_feed/feed_aside.html'),
            controller: 'feedAside',
            link: function(scope, elem, attrs) {},
            scope: {
                re_feed_list: "=re_feed_list"
            }
        }
    });

    // 禁用option方法
    app.directive('optionsDisabled', function($parse) {
        var disableOptions = function(scope, attr, element, data, fnDisableIfTrue) {
            // refresh the disabled options in the select element.
            $("option[value!='?']", element).each(function(i, e) {
                var locals = {};
                locals[attr] = data[i];
                $(this).attr("disabled", fnDisableIfTrue(scope, locals));
            });
        };
        return {
            priority: 0,
            require: 'ngModel',
            link: function(scope, iElement, iAttrs, ctrl) {
                // parse expression and build array of disabled options
                var expElements = iAttrs.optionsDisabled.match(/^\s*(.+)\s+for\s+(.+)\s+in\s+(.+)?\s*/);
                var attrToWatch = expElements[3];
                var fnDisableIfTrue = $parse(expElements[1]);
                scope.$watch(attrToWatch, function(newValue, oldValue) {
                    if (newValue)
                        disableOptions(scope, expElements[2], iElement, newValue, fnDisableIfTrue);
                }, true);
                // handle model updates properly
                scope.$watch(iAttrs.ngModel, function(newValue, oldValue) {
                    var disOptions = $parse(attrToWatch)(scope);
                    if (newValue)
                        disableOptions(scope, expElements[2], iElement, disOptions, fnDisableIfTrue);
                });
            }
        };
    });

    //区分日期
    app.directive('dateBar', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('special_feed/date_bar.html'),
            controller: function($scope, $element) {
                //console.log('dateBar',$scope);
                /*//区分推荐日期
                $scope.today = countDayByDay(0);
                $scope.yesterday = countDayByDay(-1);
                $scope.sevenday = countDayByDay(-7);
                $scope.listDays = [];*/
                var countDayByDay = function(offsetNum) {
                    var getDateObj = function(t) {
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
                    };
                    var monthStartObj = getDateObj();
                    //year, month, day, hour, minute, second, and millisecond
                    var monthEnd = new Date(monthStartObj.y, monthStartObj.m - 1, monthStartObj.d + offsetNum, monthStartObj.h, monthStartObj.i, monthStartObj.s);
                    return monthEnd.getFullYear() + '-' + (monthEnd.getMonth() + 1) + '-' + monthEnd.getDate();
                };
                var getDay = function(str) {
                    if (typeof str == 'string' && str.match(/^([0-9]{4}\-[0-9]{1,2}\-[0-9]{1,2}) /i)) {
                        return RegExp.$1;
                    }
                    return '';
                };
                var inArray = function(needle, array) {
                    for (var i = 0, imax = array.length; i < imax; i++) {
                        if (needle == array[i]) {
                            return true;
                        }
                    }
                    return false;
                };
                $scope.isShowDateBar = function(displayTime) {
                    var theDay = getDay(displayTime);
                    if (!inArray(theDay, $scope.$parent.$parent.listDays)) {
                        //$scope.$parent.$parent.listDays.push(theDay);
                        //console.log('isShowDataBar', theDay, $scope.$parent.$parent.listDays);
                        return true;
                    } else {
                        return false;
                    }
                };
                $scope.isToday = function(displayTime) {
                    var theDay = getDay(displayTime);
                    if (theDay == countDayByDay(0)) return true;
                    return false;
                };
                $scope.isYesterday = function(displayTime) {
                    var theDay = getDay(displayTime);
                    if (theDay == countDayByDay(-1)) return true;
                    return false;
                };
                $scope.isSevenday = function(displayTime) {
                    var theDay = getDay(displayTime);
                    if (theDay == countDayByDay(-7)) return true;
                    return false;
                };
                $scope.isOtherday = function(displayTime) {
                    var theDay = getDay(displayTime);
                    if (theDay != countDayByDay(0) && theDay != countDayByDay(-1) && theDay != countDayByDay(-7)) return true;
                    return false;
                };
            },
            link: function(scope, elem, attrs) {},
            scope: {
                displayTime: "="
            }
        }
    });

    app.filter('trustHtml', function($sce) {
        //限高最多2行
        var limitLinesTwo = function(str) {
            var lineWidth = 56;
            var splitor = null;
            var brNum = str.match(/(<br[ \/]*>)/ig);
            if (brNum != undefined && typeof brNum == 'object' && brNum.length >= 1) {
                splitor = RegExp.$1;
                var tempArr = str.split(splitor);
                //console.log('limitLinesTwo',tempArr[0],tempArr[0].length,tempArr[1]);
                //如果一行文字超过56个字符，就是没有换行符，也自动换行了
                if (tempArr[0].length > lineWidth) {
                    str = tempArr[0];
                } else {
                    str = tempArr[0] + splitor + tempArr[1];
                }
                if (!str.match(/\.\.\.$/i)) {
                    str += '...';
                }
            }
            return str;
        };
        return function(input) {
            //default 150 - 147
            var limitLen = 104;
            if (typeof input != 'string') return '';
            input = limitLinesTwo(input.length > limitLen ? (input.substr(0, limitLen - 3) + "...") : input);
            return $sce.trustAsHtml(input);
        }
    });

    //可在title内查看完整内容
    app.filter('trustHtmlAllForTitle', function($sce) {
        return function(input) {
            if (typeof input != 'string') return '';
            var re = new RegExp("<br[ \/]*>", "ig");
            input = input.replace(re, "\n\n");
            return $sce.trustAsHtml(input);
        }
    });

    app.filter('noSpace', function($sce) {
        return function(input) {
            return input.split(/\s+/)[0];
        }
    });

    app.filter('titleOrKey', function() {
        return function(input) {
            input = input.title.length > 0 ? input.title : input.keywords
            return input;
        }
    });

    app.filter('gender', function() {
        return function(input) {
            if (input === 'male') {
                input = '男';
            } else if (input === 'female') {
                input = '女';
            }
            return input;
        }
    });

    app.filter('meetIfEmpty', ['$sce',
        function($sce) {
            return function(input) {
                if (input === '' || input === undefined || input === null) {
                    return '面议/月';
                } else {
                    return input;
                }
            }
        }
    ]);


    app.filter('formatOpt', function() {
        return function(input) {
            return input === '不限' ? '' : input;
        }
    });

    //formatDate
    app.filter('formatDate', function() {
        var formatTwo = function(n) {
            if (parseInt(n) <= 9) {
                return '0' + n;
            } else {
                return n;
            }
        };
        return function(input) {
            var dt = new Date(parseInt(input['$date']) - (28800000));
            return dt.getFullYear() + '-' + formatTwo(dt.getMonth() + 1) + '-' + formatTwo(dt.getDate()) + ' ' + formatTwo(dt.getHours()) + ':' + formatTwo(dt.getMinutes());
        }
    });

})();

$(function() {
    $(window).on('scroll', function() {
        var $feed_aside = $('.feed-aside'),
            $doc = $(document),
            $hasmore = $('a[ng-if="hasmore"]'),
            top = 125,
            scrollY = window.scrollY ? window.scrollY : document.documentElement.scrollTop;
        if (scrollY >= 125) {
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
});