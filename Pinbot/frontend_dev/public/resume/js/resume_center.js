(function(argument) {
    var app = angular.module('app.resume_center', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter']),
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
    //var confirmBox = $funcs.get('confirmBox');
    //var confirmBoxRed = $funcs.get('confirmBoxRed');
    var alertBox = $funcs.get('alertBox');
    var getModeData = $funcs.get('getModeData');
    var postModeData = $funcs.get('postModeData');
    //var inArray = $funcs.get('inArray');
    var pbFunc = $funcs.get('pbFunc');
    //var orderPay = $funcs.get('orderPay');

    //获取侧栏数据
    var getsideGetData = function($http, $scope, pbFunc) {
        var sideGetData = getModeData($http,
            '/resume/side/?t=' + pbFunc.getTimestamp(new Date()),
            "",
            function(ret) {
                if (ret.status == "ok") {
                    $scope.sideData = ret.data;
                }
            }, undefined, function(err) {
                sideGetData.abort();
            });
        return sideGetData;
    };

    //获取简历数据
    //search_fields: 搜索类型(position_title职位名 company_name公司名 name姓名 school学校 all简历全文)
    //keywords: 搜索关键词
    //mark: 简历类型.no_will: 无求职意愿;send_offer: 发送;offerentry: 入职;eliminate: 淘汰;pending: 待处理;interview_stage: 面试阶段;next_interview: 下一轮面试;invite_interview: 安排面试;unconfirm: 待定;break_invite: 爽约;entry_stage: 入职阶段;
    //category: 自定义文件夹名字;
    var getListData = function($scope, $http, url, page, mark, category, search_fields, keywords, isParent) {
        var scope = (isParent != undefined && isParent == true) ? $scope.$parent : $scope;
        var src = url + '?page=' + page;
        var loadingState = false;
        getListDataLoading(loadingState);
        if (mark) {
            src += ('&mark=' + mark);
        };
        if (category) {
            src += ('&category=' + category);
        };
        if (search_fields) {
            src += ('&search_fields=' + search_fields);
        };
        if (keywords) {
            src += ('&keywords=' + keywords);
        };

        var returnHandler = function(scope, ret, isMock) {
            var isMock = (isMock != undefined) ? true : false;
            //准备分页
            var pageScale = 5;
            var pagingVars = function(scope, pageScale) {
                var pagesArray = [];
                var endPage = (scope.pageNum <= pageScale) ? scope.pageNum : scope.startPage + pageScale;
                if (scope.pageNum > pageScale && scope.cp > 1) {
                    var checkPoint = Math.ceil((scope.startPage + pageScale) / 2);
                    if (scope.pageDirect == 'next' && scope.cp > checkPoint && scope.pageNum - scope.cp >= 2) {
                        scope.startPage += 1;
                        if (scope.startPage > scope.pageNum) scope.startPage = scope.pageNum;
                        endPage = scope.startPage + pageScale;
                    } else if (scope.pageDirect == 'prev' && scope.cp >= 1) {
                        scope.startPage -= 1;
                        if (scope.startPage < 1) scope.startPage = 1;
                        endPage = scope.startPage + pageScale;
                    }
                }
                if (endPage > scope.pageNum) endPage = scope.pageNum + 1;
                if (endPage < 1) endPage = 1;
                //console.log('returnHandler', scope.startPage, endPage);
                if (endPage <= pageScale) {
                    for (var i = scope.startPage; i <= endPage; i++) {
                        pagesArray.push(i);
                    }
                } else {
                    for (var i = scope.startPage; i < endPage; i++) {
                        pagesArray.push(i);
                    }
                }
                return pagesArray;
            };

            loadingState = true;
            getListDataLoading(loadingState);

            if (!isMock) scope.cp = ret.current;
            scope.sum = (isMock) ? 30 : ret.count;
            scope.listData = (isMock) ? [] : ret.data;
            scope.pageNum = (isMock) ? 3 : ret.pages;
            scope.pages = pagingVars(scope, pageScale);
            if (scope.chooseResume && scope.chooseResume.length > 0) {
                scope.chooseResume.splice(0);
            };
            showNullImg(ret.data.length);
            $('.check-box').removeClass('check-box-choose');
        };
        //returnHandler(scope, {}, true);
        var listGetData;
        listGetData = getModeData($http,
            src,
            "",
            function(ret) {
                if (ret.status == "ok") {
                    returnHandler(scope, ret);
                }
            }, undefined, function(err) {
                listGetData.abort();
            });
        return listGetData;
    };
    var showNullImg = function(num) {
        if (num > 0) {
            $('.null-data').css('display', 'none');
            $('.resume-center-tabel-bottom').css('display', 'block');
        } else {
            $('.null-data').css('display', 'block');
            $('.resume-center-tabel-bottom').css('display', 'none');
        }
    }
    var getListDataLoading = function(state) {
        if (!state && ($('.resume-center-loading').css('display') != 'block')) {
            $('.js-resume').remove();
            $('.resume-center-loading').css('display', 'block');
        } else if (state && ($('.resume-center-loading').css('display') == 'block')) {
            $('.resume-center-loading').css('display', 'none');
        }
    };
    var _createFolder = function($scope) {
        if ($scope.createFolderState == false) {
            $scope.createFolderState = true;
            $scope.showFolderName = true;
        } else {
            $scope.createFolderState = false;
            $scope.showFolderName = false;
        }
    };
    var _saveFolder = function($http, $scope, pbFunc) {
        var category_name = $('#js-category-name').val().replace(/[<>%&\-\+\'\"\*\?\(\)\[\]\{\} \$\r\n]/ig, "");
        if (category_name.length > 0) {
            var save_folder = postModeData($http, {
                    'category_name': category_name
                },
                '/resume/category/create/',
                "",
                function(data) {
                    if (data.status == "ok") {
                        getsideGetData($http, $scope, pbFunc);
                    }
                }, undefined, function(err) {
                    save_folder.abort();
                }, 'json');
        }

    };
    var _editFolder = function($event, pbFunc, JQ, $http, $scope) {
        var _this = angular.element($event.currentTarget);
        var category_name = _this.parent().find('a').attr('folder-name');
        var category_id = _this.parent().find('a').attr('folder-id');
        pbFunc.simpleConfirm(
            '编辑自定义文件夹',
            '<div class="rename-input-box"><input type="text" value="' + category_name + '" id="js-rename-floder"></div><p class="mt50 cf46c62 f13">小宝提示：你可以自由添加简历到自定义文件夹哦~</p>',
            function(args) {
                pbFunc.simpleConfirm('需要你的确认', '<div class="del-confirm">你确定删除<span>' + category_name + '</span>自定义文件夹吗？</div><p class="mt50 cf46c62 f13">小宝提示：删除的文件夹不能恢复，但简历不会被删除，仍然存在于对应简历状态菜单中~</p>', function(args) {
                        JQ._LayerOut.close();
                    }, null, '返回', true, '确认删除',
                    function(args) {
                        var src = '/resume/category/delete/' + category_id + '/?category_name' + category_name;
                        var deleteFolderName = getModeData($http,
                            src,
                            "",
                            function(ret) {
                                JQ._LayerOut.close();
                                getsideGetData($http, $scope, pbFunc);
                            }, undefined, function(err) {
                                deleteFolderName.abort();
                            });
                    });


            },
            null, '删除文件夹', true, '保存',
            function(args) {
                var category_new_name = $('#js-rename-floder').val();
                var editFolderName = postModeData($http, {
                        "category_name": category_new_name
                    },
                    '/resume/category/update/' + category_id + '/',
                    "",
                    function(ret) {
                        if (ret.status == 'ok') {
                            JQ._LayerOut.close();
                            pbFunc.simpleAlert('保存成功！', '', function(trg, args) {}, null, '我知道了', false);
                            _this.parent().find('.js-folder-name').text(category_new_name);
                            _this.parent().find('a').attr('folder-name', category_new_name);
                            getsideGetData($http, $scope, pbFunc);
                        }
                    }, undefined, function(err) {
                        editFolderName.abort();
                    }, 'json');
            });
    };
    var _clickToDetail = function($event) {
        $event.stopPropagation();
        var _this = angular.element($event.currentTarget);
        var resume_id = _this.attr('resume-id');
        var feed_id = _this.attr('feed-id');
        var url = '/resumes/display/' + resume_id + '/?feed_id=' + feed_id;
        window.open(url);
    };

    var _chooseSearchFilter = function($event, $scope) {
        var _this = angular.element($event.currentTarget);
        var search_fields = _this.attr('search-fields');
        $scope.search_fields = search_fields;
        $('.filter-factor-choose').removeClass('filter-factor-choose');
        $('#js-search-filter').text(_this.text())
        _this.addClass('filter-factor-choose');
        $scope.showFilter = false;
    };
    var _search = function($rootScope, $event, $scope, $http, cp) {
        var cp = (cp != undefined && typeof cp == 'number') ? cp : 1;
        var search_fields = $('#js-search-filter-params').val();
        $scope.search_fields = search_fields;
        $scope.keywords = $('#js-search-val').val();
        getListData($scope, $http, $rootScope.url, cp, $scope.mark, $scope.category, search_fields, $scope.keywords);
    };
    var _chooseAllResume = function($event, $scope) {
        var _this = angular.element($event.currentTarget);
        var choose_resume = $('.js-resume');
        var length = choose_resume.length;
        var chooseResumeLength = $scope.chooseResume.length;
        if (!_this.hasClass('check-box-choose')) {
            $scope.chooseResume.splice(0, chooseResumeLength);
            $('.check-box').addClass('check-box-choose');
            $('#js-choose-resume-num').text(length);
            for (var i = 0; i < length; i++) {
                var choose_resume_id = choose_resume.eq(i).attr('id');
                $scope.chooseResume.push(choose_resume_id);
            }
        } else {
            $scope.chooseResume.splice(0, chooseResumeLength);
            $('.check-box').removeClass('check-box-choose');
            $('#js-choose-resume-num').text(0);
        }
    };
    var _chooseCurrentResume = function($event, $scope) {
        var _this = angular.element($event.currentTarget);
        var thisResumeId = _this.parent().parent().parent().attr('id');
        var chooseResumeLength = $scope.chooseResume.length;
        if (!_this.hasClass('check-box-choose')) {
            $scope.chooseResume.push(thisResumeId);
            _this.addClass('check-box-choose');
            $('#js-choose-resume-num').text(chooseResumeLength + 1);
            if ($scope.chooseResume.length >= $('.js-choose-this').length) {
                $('.js-choose-all').addClass('check-box-choose');
            };
        } else {
            _this.removeClass('check-box-choose');
            $('.js-choose-all').removeClass('check-box-choose');
            $('#js-choose-resume-num').text(chooseResumeLength - 1);
            for (var i = 0; i < chooseResumeLength; i++) {
                if (thisResumeId == $scope.chooseResume[i]) {
                    $scope.chooseResume.splice(i, 1);
                    break;
                };
            };
        };
    };
    var _confirmAdd = function($http, $scope) {
        if ($scope.folder_id && $scope.chooseResume && !$('.js-remove-resume').hasClass('remove-resume-choose')) {
            var addFolderResume = postModeData($http, {
                    "record_id": $scope.chooseResume
                },
                '/resume/category_resume/' + $scope.folder_id + '/',
                "",
                function(ret) {
                    if (ret.status == 'ok') {
                        $scope.folder_id = '';
                        $('.check-box').removeClass('check-box-choose');
                        getsideGetData($http, $scope, pbFunc);
                        $('#js-choosed-folder-name').text('添加到自定义文件夹');
                        //document.location.href = '/resume/center/#/f-' + $scope.folder_id + '/1';
                        $('.success-tip').css('display', 'block');
                        $('.js-tip-word').text('添加成功');
                        setTimeout(function() {
                            $('.success-tip').css('display', 'none');
                        }, 4000);
                    }
                }, undefined, function(err) {
                    addFolderResume.abort();
                }, 'json');
        }
        if ($('.js-remove-resume').hasClass('remove-resume-choose')) {
            var addFolderResume = postModeData($http, {
                    "record_id": $scope.chooseResume
                },
                '/resume/category_resume/remove/' + $scope.folderId + '/',
                "",
                function(ret) {
                    if (ret.status == 'ok') {
                        $('.check-box').removeClass('check-box-choose');
                        getsideGetData($http, $scope, pbFunc);
                        $('.js-remove-resume').removeClass('remove-resume-choose');
                        $('#js-choosed-folder-name').text('添加到自定义文件夹');
                        $('.success-tip').css('display', 'block');
                        $('.js-tip-word').text('移除成功');

                        getListData($scope, $http, $scope.url, $scope.cp, $scope.mark, $scope.category);

                        setTimeout(function() {
                            $('.success-tip').css('display', 'none');
                        }, 4000);
                    }
                }, undefined, function(err) {
                    addFolderResume.abort();
                }, 'json');
        }
    };

    app.config([
        '$stateProvider', '$urlRouterProvider',
        function($stateProvider, $urlRouterProvider) {
            var otherwiseUrl = '/';
            $urlRouterProvider.otherwise(otherwiseUrl);
            $stateProvider.state(
                'default', {
                    url: '/',
                    templateUrl: tmpl('resume/resume_center_detail.html'),
                    controller: 'resumeCenter'
                }
            );
            //发送企业名片
            $stateProvider.state(
                'company_card', {
                    url: '/{area:company_card}/{cp:[0-9]+}',
                    templateUrl: tmpl('resume/company_record.html'),
                    controller: 'resumeCenter'
                }
            );
            //我的收藏
            $stateProvider.state(
                'my_favs', {
                    url: '/{area:my_favs}/{cp:[0-9]+}',
                    templateUrl: tmpl('resume/collect.html'),
                    controller: 'resumeCenter'
                }
            );
            //自定义文件夹
            $stateProvider.state(
                'category', {
                    url: '/{area:f\-[0-9]+}/{cp:[0-9]+}',
                    templateUrl: tmpl('resume/resume_center_detail.html'),
                    controller: 'resumeCenter'
                }
            );
            //其他页面
            $stateProvider.state(
                'mark', {
                    url: '/{area:[0-9a-z_]+}/{cp:[0-9]+}',
                    templateUrl: tmpl('resume/resume_center_detail.html'),
                    controller: 'resumeCenter'
                }
            );

        }
    ]);

    app.controller(
        'resumeCenter', ['$rootScope', '$scope', '$http', '$state', '$stateParams',
            function($rootScope, $scope, $http, $state, $stateParams) {

                /*$rootScope.$on('$stateChangeStart',
                    function(event, toState, toParams, fromState, fromParams) {
                        //event.preventDefault();
                        console.log('$stateChangeStart');
                });*/
                //console.log('$stateParams', $stateParams);
                $scope.folderId = 1;
                $scope.sum = 0;
                $scope.pageNum = 0;
                $scope.removeShow = false;
                $scope.startPage = 1;
                $scope.pageDirect = 'next';
                $scope.cp = 1;
                $scope.ep = 10;
                if ($stateParams && $stateParams.cp) $scope.cp = $stateParams.cp.replace(/[^0-9]/ig, "");
                if (parseInt($scope.cp) < 1) $scope.cp = 1;
                $scope.pages = 1;
                $scope.area = '';
                if ($stateParams && $stateParams.area) $scope.area = $stateParams.area.replace(/[^0-9a-z_]/ig, "");
                $scope.sideData = {};
                //有收藏样式
                $scope.haveCollect = false;
                //有数据的选中状态
                $scope.controlNavCurrent = false;
                //有收藏样式
                $scope.nullCollect = true;
                //没有数据的选中状态
                $scope.nullCollectCurrent = false;
                $scope.createFolderState = false;
                $scope.showFolderName = false;
                $scope.showFilter = false;
                $scope.url = "/resume/buy_record/list/";
                $rootScope.url = "/resume/buy_record/list/";
                //默认标记按钮
                $scope.mark = "";
                //自定义文件夹
                $scope.category = "";
                $scope.search_fields = "all";
                $scope.keywords = "";
                $scope.chooseResume = []; //所选择的简历的id。

                //联系方式的样式在收藏夹和名片不同
                $scope.leftFix = false;

                var isInvalidUrl = false;
                $scope.currentFolderId = '';

                var isShowSubMenu = '';
                var showSubMenuName = '';

                var chkRoute = function($rootScope, $scope, $stateParams) {
                    //路由判断
                    if ($stateParams && $stateParams.area) {
                        var trgAreaBtn;
                        $('.control-nav-current').removeClass('control-nav-current');
                        if ($stateParams.area == 'my_favs') {
                            //我的收藏
                            $scope.url = "/resume/follow/list/";
                            $rootScope.url = "/resume/follow/list/";
                            $scope.haveCollect = false;
                            $scope.controlNavCurrent = true;
                            $scope.mark = "";
                            $scope.category = "";
                            if ($scope.sideData.watch_count > 0) {
                                $scope.haveCollect = true;
                                $scope.nullCollect = false;
                            }
                            if ($('#js-collect-num').text() <= 0 && $scope.nullCollectCurrent == false) {
                                $scope.nullCollect = false;
                                $scope.nullCollectCurrent = true;
                            }
                            trgAreaBtn = $('.area-btn-fav');
                            $scope.leftFix = true;
                        } else if ($stateParams.area == 'company_card') {
                            //企业名片
                            $scope.controlNavCurrent = false;
                            $scope.mark = "";
                            $scope.category = "";
                            $scope.url = '/resume/send_record/list/';
                            $rootScope.url = "/resume/send_record/list/";
                            trgAreaBtn = $('.area-btn-company-card');
                            $scope.leftFix = true;
                        } else if ($stateParams.area.match(/^f\-([0-9]+)$/i)) {
                            //自定义文件夹
                            $scope.controlNavCurrent = false;
                            $scope.mark = "";
                            $scope.category = "";
                            $scope.removeShow = true;
                            var fid = RegExp.$1;
                            $scope.currentFolderId = fid;

                            for (var c in $scope.sideData.categories) {
                                if ($scope.sideData.categories[c].id == fid) {
                                    $scope.category = $scope.sideData.categories[c].category_name;
                                    break;
                                }
                            }
                            for (var a in $scope.sideData.categories) {
                                if ($scope.sideData.categories[a].category_name == $scope.category) {
                                    $scope.folderId = $scope.sideData.categories[a].id;
                                    break;
                                }
                            }
                            if ($scope.category == "") {
                                isInvalidUrl = true;
                            }
                            $scope.url = '/resume/buy_record/list/';
                            $rootScope.url = "/resume/buy_record/list/";
                            trgAreaBtn = $('.area-btn-f-' + fid);
                        } else {
                            //默认按钮
                            $scope.controlNavCurrent = false;
                            $scope.mark = $stateParams.area;
                            $scope.category = "";
                            $scope.url = "/resume/buy_record/list/";
                            $rootScope.url = "/resume/buy_record/list/";
                            trgAreaBtn = $('.area-btn-' + $stateParams.area);

                            //console.log('$stateParams.area', $stateParams.area);
                            if ($stateParams.area.match(/^(invite_interview|break_invite|unconfirm)$/i)) {
                                isShowSubMenu = 'interview_stage';
                                showSubMenuName = RegExp.$1;
                            } else if ($stateParams.area.match(/^(send_offer|entry)$/i)) {
                                isShowSubMenu = 'entry_stage';
                                showSubMenuName = RegExp.$1;
                            }
                            //console.log('isShowSubMenu.area', isShowSubMenu);
                        }
                        $('.control-nav').find('a.control-nav-current').removeClass('control-nav-current');
                        trgAreaBtn.addClass('control-nav-current');
                        if (parseInt($('#js-collect-num').text()) > 0) {
                            $scope.haveCollect = true;
                            $scope.controlNavCurrent = false;
                        } else {
                            $scope.nullCollect = true;
                            $scope.nullCollectCurrent = false;
                        }
                        $('#js-interview').css('display', 'none');
                        $('#js-entry').css('display', 'none');

                        if (trgAreaBtn.hasClass('js-show-second-nav')) {
                            if (trgAreaBtn.text().match('录用阶段')) {

                                if ($('#js-entry').css('display') == 'block') {
                                    $('#js-entry').css('display', 'none');
                                } else {
                                    $('#js-entry').css('display', 'block');
                                };
                            } else {

                                if ($('#js-interview').css('display') == 'block') {
                                    $('#js-interview').css('display', 'none');
                                } else {
                                    $('#js-interview').css('display', 'block');
                                }
                            }
                        }
                    }

                    //展示子目录
                    if (isShowSubMenu != '') {
                        $('#js-entry').css('display', 'none');
                        $('#js-interview').css('display', 'none');
                        if (isShowSubMenu == 'interview_stage') {
                            $('.area-btn-interview_stage').addClass('control-nav-current');
                            $('#js-interview').css('display', 'block');
                        } else {
                            $('.area-btn-entry_stage').addClass('control-nav-current');
                            $('#js-entry').css('display', 'block');
                        }
                        $('.area-btn-'+showSubMenuName).addClass('control-subnav-current');
                    }else{

                        $('.area-btn-'+showSubMenuName).removeClass('control-subnav-current');
                    }
                };
                //console.log('isShowSubMenu', isShowSubMenu);

                getsideGetData($http, $scope, pbFunc).then(function() {
                    chkRoute($rootScope, $scope, $stateParams);
                    if (!isInvalidUrl) getListData($scope, $http, $scope.url, $scope.cp, $scope.mark, $scope.category);
                    if (isInvalidUrl) document.location.href = '/resume/center/';
                    return false;
                });

                $rootScope.isHaveCollect = function() {
                    return (parseInt($('#js-collect-num').text()) > 0) ? true : false;
                };

                //跳转
                $scope.go = function(name) {
                    var trgName = '';
                    var params = '';

                    //有子菜单
                    if (name.match(/^(interview_stage|entry_stage)$/i)) {
                        var currentArea = RegExp.$1;
                        var re = RegExp("/" + currentArea + "/", "i");
                        if (document.location.href.toString().match(re)) {
                            if (currentArea == 'entry_stage') {
                                $('#js-interview').css('display', 'none');
                                if ($('#js-entry').css('display') == 'block') {
                                    $('#js-entry').css('display', 'none');
                                } else {
                                    $('#js-entry').css('display', 'block');
                                };
                            } else if (currentArea == 'interview_stage') {
                                $('#js-entry').css('display', 'none');
                                if ($('#js-interview').css('display') == 'block') {
                                    $('#js-interview').css('display', 'none');
                                } else {
                                    $('#js-interview').css('display', 'block');
                                };
                            }
                        }
                    }
                    if (name.match(/^([0-9a-z_]+)$/i)) {
                        trgName = RegExp.$1;
                        params = '/1';
                        //console.log('go', name, trgName, params, '/resume/center/#/' + trgName + params);
                        document.location.href = '/resume/center/#/' + trgName + params;
                        //$state.go('/' + trgName + params);
                    } else if (name.match(/^(f\-[0-9]+)$/i)) {
                        trgName = RegExp.$1;
                        params = '/1';
                        //console.log('go', name, trgName, params, '/resume/center/#/' + trgName + params);
                        document.location.href = '/resume/center/#/' + trgName + params;
                        //$state.go('category',{ area:trgName, cp:1 });
                    } else {
                        document.location.reload();
                        //$state.go('/');
                    }
                };
                //新建文件夹
                $scope.createFolder = function() {
                    _createFolder($scope);

                };
                //点击保存文件夹按钮
                $scope.saveFolder = function() {
                    _saveFolder($http, $scope, pbFunc);
                };
                //编辑自定义文件夹
                $scope.editFolder = function($event) {
                    $event.stopPropagation();
                    _editFolder($event, pbFunc, $, $http, $scope);
                };
                $scope.clickToDetail = function($event) {
                    //$event.stopPropagation();
                    //console.log($event.target);
                    var $this = angular.element( $event.target );
                    if(!$this.hasClass('stop-to-detail')){
                        _clickToDetail($event);
                    }
                }
                $scope.sexMale = function(sex) {
                    if (sex == "男") {
                        return 0;
                    } else if (sex == "女") {
                        return 1;
                    } else if ((sex != "男") && (sex != '女')) {
                        return 2;
                    }
                };
                //点击出现搜索筛选栏
                $scope.showSearchFilter = function() {
                    if ($scope.showFilter == false) {
                        $scope.showFilter = true;
                    } else {
                        $scope.showFilter = false;
                    }
                };
                //点击选择筛选条件
                $scope.chooseSearchFilter = function($event) {
                    $event.stopPropagation();
                    _chooseSearchFilter($event, $scope);
                };
                $scope.search = function($event) {
                    $event.stopPropagation();
                    _search($rootScope, $event, $scope, $http);
                };
                $scope.enterToSearch = function($event) {
                    $event.stopPropagation();
                    var keycode = $event.keyCode;
                    if (keycode == 13) {
                        _search($rootScope, $event, $scope, $http);
                    }
                };
                //全选
                $scope.chooseAllResume = function($event) {
                    $event.stopPropagation();
                    _chooseAllResume($event, $scope);
                };

                //单选
                $scope.chooseCurrentResume = function($event) {
                    $event.stopPropagation();
                    $event.stopPropagation();
                    _chooseCurrentResume($event, $scope);
                }

                //
                $scope.folderAddResume = function() {
                    if ($('#js-foder-choose').css('display') != 'block') {
                        $('#js-foder-choose').css('display', 'block');
                    } else {
                        $('#js-foder-choose').css('display', 'none');
                    }
                }
                $scope.chooseFolderName = function($event) {
                    $event.stopPropagation();
                    var _this = angular.element($event.currentTarget);
                    $scope.folder_id = _this.attr('folder-id');
                    $('#js-choosed-folder-name').text(_this.text());
                    $('#js-foder-choose').css('display', 'none');
                    $('.js-remove-resume').removeClass('remove-resume-choose');
                }
                $scope.chooseRemove = function() {
                    $('.js-remove-resume').toggleClass('remove-resume-choose');
                    $('#js-choosed-folder-name').text('添加到自定义文件夹');
                    $('#js-foder-choose').css('display', 'none');

                }
                $scope.confirmAdd = function() {
                    _confirmAdd($http, $scope);
                };

                $scope.unconfirm = function(current_mark) {
                    if ((current_mark == 'unconfirm') || (current_mark == undefined) || (current_mark == null) || (current_mark == '')) {
                        return true;
                    } else {
                        return false;
                    }
                };
                $scope.redcolor = function(mark_state) {
                    if (mark_state == '待处理' || mark_state == '面试爽约') {
                        return true;
                    } else {
                        return false;
                    }
                };

                $scope.feedback_status_zero = function(feedback_status) {
                    if (feedback_status == 0) {
                        return true;
                    } else {
                        return false;
                    }
                };
                $scope.feedback_status_one = function(feedback_status) {
                    if (feedback_status == 1) {
                        return true;
                    } else {
                        return false;
                    }
                };
                $scope.feedback_status_two = function(feedback_status) {
                    if (feedback_status == 2) {
                        return true;
                    } else {
                        return false;
                    }
                };
                $scope.feedback_status_three = function(feedback_status) {
                    if (feedback_status == 3) {
                        return true;
                    } else {
                        return false;
                    }
                };
            }
        ]
    );

    app.filter('trustHtml', function($sce) {
        //限高最多2行
        var limitLinesTwo = function(str) {
            var lineWidth = 6;
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
            var limitLen = 12;
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

    app.directive('pages', function($http) {
        return {
            restrict: 'E',
            templateUrl: tmpl('resume/pages.html'),
            controller: function($scope, $element) {
                var scope = $scope.$parent;
                $scope.isFirstPage = function($event) {
                    return (scope.cp == 1) ? true : false;
                };
                $scope.isLastPage = function($event) {
                    return (scope.cp == scope.pageNum) ? true : false;
                };
                $scope.prevPage = function($event) {
                    if (scope.cp == 1) return false;
                    if (scope.cp - 1 < 1) {
                        scope.cp = 1;
                    } else {
                        scope.cp -= 1;
                    }
                    scope.pageDirect = 'prev';
                    getListData($scope, $http, $scope.url, scope.cp, $scope.mark, $scope.category, $scope.searchFields, $scope.keywords, true);
                };
                $scope.nextPage = function($event) {
                    if (scope.cp == scope.pageNum) return false;
                    if (scope.cp + 1 > scope.pageNum) {
                        scope.cp = scope.pageNum;
                    } else {
                        scope.cp += 1;
                    }
                    scope.pageDirect = 'next';
                    getListData($scope, $http, $scope.url, scope.cp, $scope.mark, $scope.category, $scope.searchFields, $scope.keywords, true);
                };
                $scope.clickPage = function($event) {
                    var _this = angular.element($event.currentTarget);
                    if (scope.cp == parseInt(_this.text())) return false;
                    scope.cp = parseInt(_this.text());
                    getListData($scope, $http, $scope.url, scope.cp, $scope.mark, $scope.category, $scope.searchFields, $scope.keywords, true);
                };
            },
            scope: {
                cp: '=cp',
                pageNum: '=pageNum',
                pages: '=pages',
                url: '=url',
                mark: '=mark',
                category: '=category',
                searchFields: '=searchFields',
                keywords: '=keywords',
                chooseResume: "=chooseResume"

            }
        };
    });

    //下拉按钮
    app.directive('selectBtns', function($http) {
        return {
            restrict: 'E',
            templateUrl: tmpl('resume/select-btns.html'),
            controller: function($scope, $element) {

                $scope.unconfirm = function(current_mark) {
                    if ((current_mark == 'unconfirm') || (current_mark == undefined) || (current_mark == null) || (current_mark == '')) {
                        return true;
                    } else {
                        return false;
                    }
                };
            },
            scope: {
                resumeMassage: '=resumeMassage'
            }
        };
    });

    //resume_brief.html
    app.directive('resumeBrief', function($http) {
        return {
            restrict: 'E',
            templateUrl: tmpl('resume/resume_brief.html'),
            controller: function($scope, $element) {
                $scope.sexMale = function(sex) {
                    if (sex == "男") {
                        return 0;
                    } else if (sex == "女") {
                        return 1;
                    } else if ((sex != "男") && (sex != '女')) {
                        return 2;
                    }
                };
                $scope.hasContactInfo = function(obj) {
                    ret = !angular.equals(obj, {});
                    return ret;
                };
            },
            scope: {
                resumeMassage: '=resumeMassage',
                leftFix: '=leftFix'
            }
        };
    });

    //meet_time.html
    app.directive('meetTime', function($http) {
        return {
            restrict: 'E',
            templateUrl: tmpl('resume/meet_time.html'),
            controller: function($scope, $element) {
                $scope.showMeetInfo = function(interview) {
                    if (interview.interview_count && interview.interview_count > 0) {
                        return '安排第' + interview.interview_count + '轮面试';
                    } else {
                        return '安排面试';
                    }
                };
                $scope.isInterView = function(mark_state){
                    //console.log('isInterView',mark_state);
                    if (mark_state == 'invite_interview' || mark_state == 'next_interview') {
                        return true;
                    } else {
                        return false;
                    }
                };

            },
            scope: {
                resumeMassage: '=resumeMassage'
            }
        };
    });

})();
