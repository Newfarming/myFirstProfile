(function(angular, undefined) {
    var app = angular.module('feedApp', ['app.config', 'ui.router', 'app.utils', 'app.filter', 'app.django', 'validation', 'validation.rule']),
        $service = angular.injector(['app.django', 'app.utils']),
        id_url = $service.get('id_url'),
        tmpl = $service.get('tmpl');

    app.controller(
        'feedController', [
            '$scope',
            '$validation',
            '$http',
            function($scope, $validation, $http) {
                $scope.feedData = angular.fromJson(angular.element(document.getElementById('JS_container')).attr('data-feedData'));
                //初始化被选关键字
                $scope.feedData.analyze_titles = [];
                $scope.feedData.analyze_keywords = [];

                $scope.isAddNew = true;

                //定制改版
                $scope.loadingMore = false;
                $scope.loadingMoreDone = false;
                $scope.isSyncData = false;

                $scope.isFillAll = true;
                $scope.invalidPanelClassName = '';

                //是否是编辑状态
                for (var i in $scope.feedData.feed) {
                    $scope.isAddNew = false;
                    $scope.loadingMoreDone = true;
                    break;
                };

                //第一步
                $scope.firstStep = true;

                //判断必填提示是否显示
                $scope.feedData.levelDirty = $scope.feedData.levelCity = false;
                $scope.feedData.titleDirty = $scope.feedData.descDirty = false;
                $scope.feedData.jobKeywordDirty = $scope.feedData.keywordDirty = $scope.feedData.catDirty = $scope.feedData.salaryDirty = $scope.preferDirty = $scope.welfareDirty = false;
                $scope.feedData.submiting = false;
                if (!$scope.isAddNew) $scope.feedData.descDirty = true;

                //定制预览
                $scope.showViewDesc = true;
                $scope.viewFeed = false;


                //init data
                $scope.feedData.talent_level = ['初级', '中级', '高级'];
                $scope.feedData.feed = angular.extend({
                    title: '',
                    job_desc: '',
                    expect_area: [],
                    talent_level: [],
                    analyze_titles: [],
                    keywords: [],
                    job_domain: [],
                    company_prefer: [],
                    job_welfare: [],
                    salary_min: '',
                    salary_max: ''
                }, $scope.feedData.feed);

                //兼容老数据没有title显示输入框
                $scope.feedData.title = $scope.feedData.feed.title;

                //判断是否选择了面议
                if ($scope.feedData.feed.salary_min == 0 && $scope.feedData.feed.salary_max == 1000000) {
                    $scope.feedData.feed.salary_min = '';
                    $scope.feedData.feed.salary_max = '';
                    $scope.isNegotiable = true;
                };

                //将公司领域同步到post数据
                $scope.feedData.feed.categorys = $scope.feedData.company.categorys || [];

                $scope.feedData.min_salary = $scope.feedData.max_salary = $scope.feedData.min_num = $scope.feedData.max_num = 0;

                //备份初始数据,在下一步的时候会更新
                $scope.feedData.Databackup = angular.copy($scope.feedData.feed);

                //错误提示信息
                $scope.defaultErrorMsg = '此项为必填项！';
                $scope.reDescErrorMsg = $scope.reTitleErrorMsg = $scope.reLevelErrorMsg = $scope.reAreaErrorMsg = $scope.reKeywordsErrorMsg = $scope.reJobKeywordsErrorMsg = $scope.reCatErrorMsg = $scope.reSalaryErrorMsg = $scope.defaultErrorMsg;
                //$scope.rePreferErrorMsg = $scope.reWelfareErrorMsg =

                //错误变量
                $scope.reDescError = $scope.reTitleError = $scope.reLevelError = $scope.reAreaErrorError = $scope.reKeywordsError = $scope.reCatError = $scope.reJobKeywordsError = $scope.reSalaryError = false;
                //$scope.rePreferError = $scope.reWelfareError =

                //职位领域取消必填
                $scope.reCatErrorMsg = '';
                $scope.reCatError = false;
                $scope.feedData.catDirty = false;

                //过滤空的关键字
                var filterEmptyArr = function(arrName) {
                    //console.log('filterEmptyArr',$scope.feedData.feed,arrName);
                    if ($scope.feedData.feed[arrName].length > 0) {
                        for (var i = 0, imax = $scope.feedData.feed[arrName].length; i < imax; i++) {
                            if ($scope.feedData.feed[arrName][i] == undefined || $scope.feedData.feed[arrName][i].trim() == "") {
                                $scope.feedData.feed[arrName].splice(i, 1);
                            }
                        }
                    }
                };
                if (!$scope.isAddNew) {
                    filterEmptyArr('analyze_titles');
                    filterEmptyArr('keywords');
                }

                //默认关键字可能没有的时候，需要提示错误
                if ($scope.feedData.feed['analyze_titles'].length == 0) {
                    $scope.feedData.jobKeywordDirty = true;
                }
                if ($scope.feedData.feed['keywords'].length == 0) {
                    $scope.feedData.keywordDirty = true;
                }

                //检查提交状态，否则无法新增定制
                var chkSubmitErr = function(nv, trgName) {
                    //console.log('chkSubmitErr', nv, trgName);
                    var hasErr = false;
                    if (typeof nv == 'string') {
                        hasErr = (nv == undefined || nv.trim() == "") ? true : false;
                    } else if (typeof nv == 'object') {
                        hasErr = (nv.length == 0) ? true : false;
                    }
                    if (hasErr) {
                        $scope.invalidPanelClassName = trgName;
                        $scope.isFillAll = false;
                    } else {
                        $scope.isFillAll = true;
                    }
                };

                //标签限制数量
                var maxKeywordLen = 20; //20
                //标签限制总长度1000
                var maxKeywordStrLen = 1000; //1000

                //检查输入框文字长度
                var chkChineseWordsLen = function(val, len) {
                    if (typeof val != 'string') return false;
                    var str = val;
                    if (str.match(/[^\x00-\xff]/i)) str = str.replace(/[^\x00-\xff]/g, '**');
                    //console.log('chkChineseWordsLen',str.length);
                    if (str.length <= len) {
                        return true;
                    } else {
                        return false;
                    }
                };

                //监听职位名称
                $scope.$watchCollection('feedData.feed.title', function(nv, ov) {
                    chkSubmitErr(nv, '#label_job_title_title');
                    $scope.reTitleErrorMsg = $scope.defaultErrorMsg;
                    $scope.reTitleError = false;
                    /*if( !$scope.isPrimaryLevel() ){
                        $scope.isNegotiable = false;
                    };*/
                });

                //监听职位详情
                $scope.$watchCollection('feedData.feed.job_desc', function(nv, ov) {
                    if ($scope.isAddNew) {
                        chkSubmitErr(nv, '#label_job_desc_title');
                    } else {
                        chkSubmitErr(nv, '#label_job_desc_title_edit');
                    }
                    $scope.reDescErrorMsg = $scope.defaultErrorMsg;
                    $scope.reDescError = false;
                    if (nv != "") {
                        if ($scope.invalidPanelClassName == '#label_job_desc_title') $scope.invalidPanelClassName = '';
                        if ($scope.invalidPanelClassName == '#label_job_desc_title_edit') $scope.invalidPanelClassName = '';
                    }
                    if (!chkChineseWordsLen(nv, maxKeywordStrLen)) {
                        $scope.reDescErrorMsg = '职位详情最多为500字';
                        $scope.reDescError = true;
                        if ($scope.isAddNew) {
                            $scope.invalidPanelClassName = '#label_job_desc_title';
                        }else{
                            $scope.invalidPanelClassName = '#label_job_desc_title_edit';
                        }
                    }
                    /*if( !$scope.isPrimaryLevel() ){
                        $scope.isNegotiable = false;
                    };*/
                });

                //监听人才级别
                $scope.$watchCollection('feedData.feed.talent_level', function(nv, ov) {
                    if ($scope.isAddNew) {
                        chkSubmitErr(nv, '#label_level_title');
                    } else {
                        chkSubmitErr(nv, '#label_level_title_edit');
                    }
                    $scope.reLevelErrorMsg = $scope.defaultErrorMsg;
                    $scope.reLevelError = false;
                    /*if (!$scope.isPrimaryLevel()) {
                        $scope.isNegotiable = false;
                    };*/
                    if ($scope.loadingMoreDone) $scope.getAnalyzeRelated();
                });

                //监听工作地
                $scope.$watchCollection('feedData.feed.expect_area', function(nv, ov) {
                    chkSubmitErr(nv, '#label_expect_area_title');
                    $scope.reAreaErrorMsg = $scope.defaultErrorMsg;
                    $scope.reAreaErrorError = false;
                });

                //监控关键字数组变化
                $scope.$watchCollection('feedData.feed.analyze_titles', function(nv, ov) {
                    chkSubmitErr(nv, '#label_job_keywords_title');
                    if ($scope.loadingMoreDone) $scope.getAnalyzeRelated();
                    //$scope.reJobKeywordsErrorMsg = $scope.defaultErrorMsg;
                    $scope.reJobKeywordsErrorMsg = '此项为必填项，试试点击“解析职位详情”帮你填写拓展名';
                    $scope.reJobKeywordsError = false;
                    if (nv.length > 0) {
                        $('.icon-menu-job-keyword').addClass('right-nav-state-current');
                        if ($scope.invalidPanelClassName == '#label_job_keywords_title') $scope.invalidPanelClassName = '';
                        if (nv.length > maxKeywordLen) {
                            $scope.feedData.feed['analyze_titles'].splice(nv.length - 1, 1);
                        }
                    }
                    var str_analyze_titles = $scope.feedData.feed.analyze_titles.join('');
                    if (!chkChineseWordsLen(str_analyze_titles, maxKeywordStrLen)) {
                        //标签限制总长度1000
                        $scope.feedData.feed['analyze_titles'].splice(nv.length - 1, 1);
                    }
                });

                //监控关键字数组变化
                $scope.$watchCollection('feedData.feed.keywords', function(nv, ov) {
                    chkSubmitErr(nv, '#label_skill_keywords_title');
                    if ($scope.loadingMoreDone) $scope.getAnalyzeRelated();
                    $scope.reSkillKeywordsErrorMsg = $scope.defaultErrorMsg;
                    $scope.reSkillKeywordsError = false;
                    if (nv.length > 0) {
                        $('.icon-menu-skill-keyword').addClass('right-nav-state-current');
                        if ($scope.invalidPanelClassName == '#label_skill_keywords_title') $scope.invalidPanelClassName = '';
                        if (nv.length > maxKeywordLen) {
                            $scope.feedData.feed['keywords'].splice(nv.length - 1, 1);
                        }
                    }
                    var str_keywords = $scope.feedData.feed.keywords.join('');
                    if (!chkChineseWordsLen(str_keywords, maxKeywordStrLen)) {
                        //标签限制总长度1000
                        $scope.feedData.feed['keywords'].splice(nv.length - 1, 1);
                    }
                });

                //监控职位领域数组变化
                $scope.$watchCollection('feedData.feed.job_domain', function(nv, ov) {
                    if ($scope.loadingMoreDone) $scope.getAnalyzeRelated();
                    $scope.reCatErrorMsg = $scope.defaultErrorMsg;
                    $scope.reCatError = false;
                });

                //监控公司偏好变化
                $scope.$watchCollection('feedData.feed.company_prefer', function(nv, ov) {
                    if ($scope.loadingMoreDone) $scope.getAnalyzeRelated();
                    $scope.rePreferError = false;
                    $scope.rePreferErrorMsg = $scope.defaultErrorMsg;
                });

                //监控职位诱惑变化
                $scope.$watchCollection('feedData.feed.job_welfare', function(nv, ov) {
                    $scope.reWelfareError = false;
                    $scope.reWelfareErrorMsg = $scope.defaultErrorMsg;
                });

                $scope.salaryMsgs = ['最低薪资为必填项！', '请输入大于1000小于1000000的薪资', '最高薪资应大于最低薪资', '最高薪资不能大于最低薪资的三倍', '最高薪资为必填项！'];

                //监控最低薪资范围变化
                $scope.$watchCollection('feedData.feed.salary_min', function(nv, ov) {

                    if (nv == ov) return;
                    var max = parseInt($scope.feedData.feed.salary_max),
                        msg = '',
                        status = false;
                    nv = parseInt(nv);
                    if (!nv) {
                        msg = $scope.salaryMsgs[0];
                        status = true;
                    } else if (nv < 1000 || nv > 1000000) {
                        msg = $scope.salaryMsgs[1];
                        status = true;
                    } else if (max && nv > max) {
                        msg = $scope.salaryMsgs[2];
                        status = true;
                    } else if (max && max / nv > 3) {
                        status = true;
                        msg = $scope.salaryMsgs[3];
                    } else if (!max) {
                        msg = $scope.salaryMsgs[4];
                        status = true;
                    } else if (max < 1000 || max > 1000000) {
                        msg = $scope.salaryMsgs[1];
                        status = true;
                    };
                    $scope.reSalaryError = status;
                    $scope.reSalaryErrorMsg = msg;
                });

                //监控最高薪资范围变化
                $scope.$watchCollection('feedData.feed.salary_max', function(nv, ov) {
                    if (nv == ov) return;
                    var min = parseInt($scope.feedData.feed.salary_min),
                        msg = '',
                        status = false;
                    nv = parseInt(nv);
                    if (!nv) {
                        msg = $scope.salaryMsgs[4];
                        status = true;
                    } else if (nv < 1000 || nv > 1000000) {
                        msg = $scope.salaryMsgs[1];
                        status = true;
                    } else if (min && min > nv) {
                        msg = $scope.salaryMsgs[2];
                        status = true;
                    } else if (min && nv / min > 3) {
                        msg = $scope.salaryMsgs[3];
                        status = true;
                    } else if (!min) {
                        msg = $scope.salaryMsgs[0];
                        status = true;
                    } else if (min < 1000 || min > 1000000) {
                        msg = $scope.salaryMsgs[1];
                        status = true;
                    };
                    $scope.reSalaryError = status;
                    $scope.reSalaryErrorMsg = msg;
                });

                //右侧菜单按钮显示状态列表
                $scope.isShowList = {};
                //机器人头像状态列表
                $scope.isShowCurrentList = {};
                /*$scope.$watch('isShowCurrentList', function(newVal, oldVal, scope) {
                    //console.log('isShowCurrentList watch', newVal, oldVal);
                    var m = 0;
                    for (var i in $scope.isShowCurrentList) {
                        if ($scope.isShowCurrentList.hasOwnProperty(i)) {
                            if ($scope.isShowCurrentList[i] == false) {
                                if (m <= 1) {
                                    angular.element(document.getElementsByClassName('icon-menu')).removeClass('right-nav-current');
                                    var trg = angular.element(document.getElementsByClassName('icon-menu')[0]);
                                    if (!trg.attr('class').match(/right\-nav/i)) {
                                        trg.addClass('right-nav-state-current');
                                    }
                                    trg = angular.element(document.getElementsByClassName('icon-menu')[1]);
                                    if (!trg.attr('class').match(/right\-nav/i)) {
                                        trg.addClass('right-nav-state-current');
                                    }
                                    angular.element(document.getElementsByClassName('icon-menu')[0]).addClass('right-nav-current');
                                    break;
                                } else {
                                    angular.element(document.getElementsByClassName('icon-menu')).removeClass('right-nav-current');
                                    for (var j = 0, jmax = m - 1; j < jmax; j++) {
                                        var trg = angular.element(document.getElementsByClassName('icon-menu')[m - 1]);
                                        if (!trg.attr('class').match(/right\-nav/i)) {
                                            trg.addClass('right-nav-state-current');
                                        }
                                    }
                                    angular.element(document.getElementsByClassName('icon-menu')[m - 1]).addClass('right-nav-current');
                                    var percent = parseInt(1000 * (m - 1) / 9) / 10;
                                    angular.element(document.getElementsByClassName('progress-width')[0]).css('width', percent + '%');
                                    break;
                                }
                            }
                            m++;
                        }
                    }
                }, true);*/

                //切换菜单图标
                var moveToNameFromIcon = function($event, id) {
                    var trg = angular.element($event.currentTarget);
                    var icons = angular.element(document.getElementsByClassName('icon-menu'));
                    icons.removeClass('right-nav-current');
                    trg.addClass('right-nav-current');
                    if (trg.attr('class').match(/right\-nav\-state\-error/i)) {
                        icons.removeClass('right-nav-current-wrong');
                        trg.addClass('right-nav-current-wrong');
                    }
                };

                //漂移到对应元素
                var jumpToPanel = function(className) {
                    //console.log('jumpToPanel', className);
                    var top = angular.element(eles(className)).offset().top;
                    if (top != undefined && typeof top == 'number') angular.element(window).scrollTop(top);
                };

                //获取元素
                var eles = function(className) {
                    if (className != undefined && typeof className == 'string') {
                        if (className.match(/^#(.+)$/i)) {
                            var id = RegExp.$1;
                            return (document.getElementById(id) != null) ? angular.element(document.getElementById(id))[0] : null;
                        } else {
                            return (document.getElementsByClassName(className) != null) ? angular.element(document.getElementsByClassName(className)[0])[0] : null;
                        }
                    } else {
                        return null;
                    }
                };

                //菜单图标切换
                $scope.moveToPanel = function($event, name) {
                    if ($scope.isAddNew) {
                        if (name == 'city') {
                            moveToNameFromIcon($event, 'label_expect_area_title');
                        } else if (name == 'level') {
                            moveToNameFromIcon($event, 'id');
                        } else if (name == 'job_title') {
                            moveToNameFromIcon($event, 'id');
                        } else if (name == 'job_desc') {
                            moveToNameFromIcon($event, 'id');
                        }
                    } else {
                        if (name == 'city_edit') {
                            moveToNameFromIcon($event, 'id');
                        } else if (name == 'level_edit') {
                            moveToNameFromIcon($event, 'id');
                        } else if (name == 'job_title_edit') {
                            moveToNameFromIcon($event, 'id');
                        } else if (name == 'job_desc_edit') {
                            moveToNameFromIcon($event, 'id');
                        }
                    }
                    if (name == 'keyword') {
                        moveToNameFromIcon($event, 'id');
                    } else if (name == 'job_keyword') {
                        moveToNameFromIcon($event, 'id');
                    } else if (name == 'skill_keyword') {
                        moveToNameFromIcon($event, 'id');
                    } else if (name == 'domain') {
                        moveToNameFromIcon($event, 'id');
                    } else if (name == 'prefer') {
                        moveToNameFromIcon($event, 'id');
                    } else if (name == 'welfare') {
                        moveToNameFromIcon($event, 'id');
                    } else if (name == 'salary') {
                        moveToNameFromIcon($event, 'id');
                    }
                };

                //是否展示菜单关联按钮
                $scope.chkPanel = function(name) {
                    if ($scope.isAddNew) {
                        if (name == 'city' && document.getElementById('JS_city_addnew') != null) {
                            $scope.isShowList['city'] = true;
                            return true;
                        }
                        //level job_title job_desc
                        if (name == 'level' && document.getElementById('JS_level_edit') != null) {
                            $scope.isShowList['level'] = true;
                            return true;
                        }
                        if (name == 'job_title' && document.getElementById('JS_job_title_box') != null) {
                            $scope.isShowList['job_title'] = true;
                            return true;
                        }
                        if (name == 'job_desc' && document.getElementById('JS_job_desc_box') != null) {
                            $scope.isShowList['job_desc'] = true;
                            return true;
                        }
                    } else {
                        //如果是编辑状态 && document.getElementById('JS_city_edit') != null
                        if (name == 'city_edit') {
                            //$scope.isShowList['city_edit'] = true;
                            return true;
                        }
                        //level job_title job_desc
                        if (name == 'level_edit' && document.getElementById('JS_level_edit') != null) {
                            $scope.isShowList['level_edit'] = true;
                            return true;
                        }
                        // && document.getElementById('JS_job_title_edit_box') != null
                        if (name == 'job_title_edit') {
                            //$scope.isShowList['job_title_edit'] = true;
                            return true;
                        }
                        if (name == 'job_desc_edit' && document.getElementById('JS_job_desc_edit_box') != null) {
                            $scope.isShowList['job_desc_edit'] = true;
                            return true;
                        }
                    }
                    if (name == 'keyword' && document.getElementById('JS_skill_keywords_box') != null) {
                        $scope.isShowList['keyword'] = true;
                        return true;
                    }
                    if (name == 'job_keyword' && document.getElementById('JS_job_keywords_box') != null) {
                        $scope.isShowList['job_keyword'] = true;
                        return true;
                    }
                    if (name == 'skill_keyword' && document.getElementById('JS_skill_keywords_box') != null) {
                        $scope.isShowList['skill_keyword'] = true;
                        return true;
                    }
                    if (name == 'domain' && document.getElementById('JS_categorys_box') != null) {
                        $scope.isShowList['domain'] = true;
                        return true;
                    }
                    if (name == 'prefer' && document.getElementById('JS_prefer_box') != null) {
                        $scope.isShowList['prefer'] = true;
                        return true;
                    }
                    if (name == 'welfare' && document.getElementById('JS_welfare_box') != null) {
                        $scope.isShowList['welfare'] = true;
                        return true;
                    }
                    if (name == 'salary' && document.getElementById('JS_salary_box') != null) {
                        $scope.isShowList['salary'] = true;
                        return true;
                    }
                    return false;
                };

                //判断人才级别只为初级
                $scope.isPrimaryLevel = function() {
                    return false;//$scope.feedData.feed.talent_level.length == 1 && $scope.feedData.feed.talent_level[0] == '初级';
                };

                $scope.toLowSalary = function() {
                    if (!$scope.feedData.feed.salary_min || !$scope.feedData.min_salary) return false;
                    return $scope.feedData.feed.salary_min < $scope.feedData.min_salary;
                };

                /* 根据参数返回数组字符串,缺省则返回具体值 */
                $scope.formatArrayParam = function(arr, param) {
                    var txtArr = [];
                    if (!arr || !arr.length) return '';
                    for (var i = 0, l = arr.length; i < l; i++) {
                        if (param) {
                            txtArr.push(arr[i][param]);
                        } else {
                            txtArr.push(arr[i]);
                        };
                    };
                    return txtArr.join(',');
                };

                /* 合并数组 */
                $scope.concat = function(arr, space) {
                    if (!arr || !arr.length) return '';
                    if (space) {
                        return arr.join(space);
                    } else {
                        return arr.join(',');
                    };
                };

                /* 返回一个只包含id的新数组 */
                $scope.returnIdArray = function(arr) {
                    var idArr = [];
                    if (!arr || !arr.length) return '';
                    for (var i = 0, l = arr.length; i < l; i++) {
                        var id = arr[i].id;
                        if (id) {
                            idArr.push(id);
                        };
                    };
                    return idArr;
                };

                /* 判断是否在数组中已存在 */
                $scope.hasInArr = function(arr, val) {
                    // var arr = $scope.feedData.feed.keywords;
                    for (var i = 0, l = arr.length; i < l; i++) {
                        if (arr[i] == val) {
                            return true;
                        };
                    };
                    return false;
                };

                /* 工作地 */
                $scope.toggleCity = function(city, $e) {
                    $scope.feedData.levelCity = true;
                    var cities = $scope.feedData.feed.expect_area,
                        target = angular.element($e.target),
                        active = target.hasClass('active');

                    var cities = $scope.feedData.feed.expect_area || [];
                    if (active) {
                        for (var i = 0, l = cities.length; i < l; i++) {
                            if (cities[i] == city) {
                                $scope.feedData.feed.expect_area.splice(i, 1);
                                break;
                            };
                        };
                    } else {
                        $scope.feedData.feed.expect_area.push(target.text());
                    };
                    target.toggleClass('active');
                };

                $scope.isCityActive = function(city) {
                    var cities = $scope.feedData.feed.expect_area;
                    if (!cities || !cities.length) return false;
                    for (var i = 0, l = cities.length; i < l; i++) {
                        if (cities[i] == city) return 'active';
                    };
                    return false;
                };

                /* 人才级别 */
                $scope.toggleLevel = function(level, $e) {
                    $scope.feedData.levelDirty = true;
                    var levels = $scope.feedData.feed.talent_level,
                        target = angular.element($e.target),
                        id = target.attr('data-id'),
                        active = target.hasClass('active');

                    levels = levels || [];
                    if (active) {
                        for (var i = 0, l = levels.length; i < l; i++) {
                            if (levels[i] == level) {
                                $scope.feedData.feed.talent_level.splice(i, 1);
                                break;
                            };
                        };
                    } else {
                        $scope.feedData.feed.talent_level.push(level);
                    };
                    target.toggleClass('active');
                };

                $scope.isLevelActive = function(level) {
                    var levels = $scope.feedData.feed.talent_level;
                    if (!levels || !levels.length) return false;
                    for (var i = 0, l = levels.length; i < l; i++) {
                        if (levels[i] == level) return 'active';
                    };
                    return false;
                };

                //还原按钮状态
                var resetParseBtn = function() {
                    var btn = angular.element(document.getElementsByClassName('job_desc_parse'));
                    btn.text('解析职位详情');
                    btn.removeAttr('disabled');
                };

                //迁移数组内容 feedData ＝》feedData.feed
                var moveArrVals = function(fromArrName, toArrName, num, keywordName) {
                    if ($scope.feedData[fromArrName].length > 0) {
                        for (var i = 0; i < num; i++) {
                            if ($scope.feedData[fromArrName].length > 0) {
                                var newKw = $scope.feedData[fromArrName].shift();
                                pushWords($scope.feedData.feed[toArrName], newKw, keywordName);
                            } else {
                                break;
                            }
                        }
                    }
                };
                /* 加载小宝推荐数据 */
                $scope.loadAnalyzeData = function(data) {
                    $scope.feedData.analyze_keywords = data.analyze_keywords || [];
                    //前4个关键字放入已选
                    if ($scope.isAddNew){
                        moveArrVals('analyze_keywords', 'keywords', 4, 'keywords');
                    }else{
                        //如果没有关键字
                        if ($scope.feedData.feed['keywords'].length == 0) {
                            moveArrVals('analyze_keywords', 'keywords', 4, 'keywords');
                        }
                    }
                    $scope.feedData.analyze_titles = data.analyze_titles || [];
                    //前8个关键字放入已选
                    if ($scope.isAddNew){
                        moveArrVals('analyze_titles', 'analyze_titles', 8, 'analyze_titles');
                    }else{
                        //如果没有关键字
                        if ($scope.feedData.feed['analyze_titles'].length == 0) {
                            moveArrVals('analyze_titles', 'analyze_titles', 8, 'analyze_titles');
                        }
                    }
                    $scope.feedData.analyze_job_domain = data.analyze_job_domain || [];
                    $scope.feedData.feed.analyze_job_domain = data.analyze_job_domain || [];
                    $scope.feedData.feed_extra_info = data.feed_extra_info || {};
                    $scope.feedData.feed = angular.extend($scope.feedData.feed, $scope.feedData.feed_extra_info);

                    resetParseBtn();
                };

                /* 切换显示小宝推荐 */
                $scope.toggleTip = function() {
                    angular.element(document.getElementById('JS_slideup_btn')).toggleClass('active');
                    $('#JS_on_tip,#JS_off_tip').slideToggle();
                };

                /* 技能关键字 */
                $scope.setKeywords = function(id, keywordName, dirtyName) {
                    var $dom = angular.element(document.getElementById(id)),
                        val = $.trim($dom.val());
                    $dom.val('');
                    if ($scope.feedData.feed[keywordName].length >= 20) return;
                    if (!val || $scope.hasInArr($scope.feedData.feed[keywordName], val)) return;
                    $scope.addAnaKeyword(val, dirtyName, keywordName);
                };

                //截取中文
                var cutChinese = function(str, offsetStart, offsetEnd) {
                    if (typeof str != 'string') return '';

                    //得到字符总数
                    var cn_strlen = function(str) {
                            var i = 0;
                            var c = 0;
                            var unicode = 0;
                            var len = 0;
                            if (str != undefined && typeof str == "string") {
                                str = str.trim();
                                if (str == "") {
                                    return 0;
                                } else {
                                    len = str.length;
                                    for (i = 0; i < len; i++) {
                                        unicode = str.charCodeAt(i);
                                        if (unicode < 127) { //判断是单字符还是双字符
                                            c += 1;
                                        } else { //chinese
                                            c += 2;
                                        }
                                    }
                                    return c;
                                }
                            } else {
                                return 0;
                            }
                        }
                        //截取字符
                    var cn_substr = function(str, startp, endp) {
                        var i = 0;
                        var c = 0;
                        var unicode = 0;
                        var rstr = '';
                        var len = str.length;
                        var sblen = cn_strlen(str);
                        if (startp < 0) {
                            startp = sblen + startp;
                        }
                        if (endp < 1) {
                            endp = sblen + endp; // - ((str.charCodeAt(len-1) < 127) ? 1 : 2);
                        }
                        // 寻找起点
                        for (i = 0; i < len; i++) {
                            if (c >= startp) {
                                break;
                            }
                            var unicode = str.charCodeAt(i);
                            if (unicode < 127) {
                                c += 1;
                            } else {
                                c += 2;
                            }
                        }
                        // 开始取
                        for (i = i; i < len; i++) {
                            var unicode = str.charCodeAt(i);
                            if (unicode < 127) {
                                c += 1;
                            } else {
                                c += 2;
                            }
                            rstr += str.charAt(i);
                            if (c >= endp) {
                                break;
                            }
                        }
                        return rstr;
                    }
                    return cn_substr(str, offsetStart, offsetEnd);
                };
                //添加关键字
                var pushWords = function(obj, val, keywordName) {
                    if (typeof val != 'string') return false;
                    var currentVal = val.trim();
                    var tempArr = [];
                    var removaVal = function(arr, val) {
                        for (var i = 0, imax = arr.length; i < imax; i++) {
                            if (arr[i] == val) {
                                arr.splice(i, 1);
                                break;
                            }
                        }
                    };
                    var pushVal = function($scope, val) {
                        if (!val || $scope.hasInArr(obj, val)) return;
                        if (val.trim() != "" && chkChineseWordsLen(val, 50)) {
                            if (keywordName != undefined) {
                                //删除屏蔽词
                                if (keywordName == 'analyze_titles' || keywordName == 'keywords') {
                                    if ($scope.feedData[keywordName] != undefined) {
                                        removaVal($scope.feedData[keywordName], val);
                                    }
                                }
                            }
                            obj.push(val.trim());
                        }
                    };
                    if (currentVal.match(/([ ,，])/i)) {
                        var splitor = RegExp.$1;
                        tempArr = val.trim().split(splitor);
                        for (var i = 0, imax = tempArr.length; i < imax; i++) {
                            pushVal($scope, tempArr[i]);
                        }
                    } else {
                        pushVal($scope, currentVal);
                    }
                };

                //添加自定义关键字，支持空格，逗号分隔
                $scope.addAnaKeyword = function(val, dirtyName, keywordName) {
                    //console.log('addAnaKeyword', val, dirtyName, keywordName);
                    $scope.feedData[dirtyName] = true;
                    if (typeof val == 'string') {
                        pushWords($scope.feedData.feed[keywordName], val, keywordName);
                    } else {
                        //$scope.feedData.feed[keywordName].push(val);
                    }
                    if (keywordName == 'analyze_titles') {
                        document.getElementById('JS_job_keyword_model').focus();
                    } else if (keywordName == 'keywords') {
                        document.getElementById('JS_keyword_model').focus();
                    }
                };

                $scope.removeAnaKeyword = function(val, arr, $e, addArrName) {

                    if ($($e.target).closest('#JS_skill_keywords_box').length) {
                        $scope.feedData.keywordDirty = true;
                    };

                    if ($($e.target).closest('#JS_job_keywords_box').length) {
                        $scope.feedData.jobKeywordDirty = true;
                    };

                    if ($($e.target).closest('#JS_welfare_box').length) {
                        $scope.feedData.welfareDirty = false;
                    };

                    if (!val || !arr || !arr.length) return;
                    for (var i = 0, l = arr.length; i < l; i++) {
                        if (arr[i] == val) {
                            arr.splice(i, 1);
                            if (addArrName != undefined && typeof addArrName == 'string' && $scope.feedData[addArrName] != undefined && !$scope.hasInArr($scope.feedData[addArrName], val)) {
                                $scope.feedData[addArrName].push(val);
                            }
                            break;
                        };
                    };
                    $e.stopPropagation();
                };

                //限制关键字长度 20
                var watchKwLen = function(id, len) {
                    var trg = eles(id);
                    if (!chkChineseWordsLen(trg.value, len)) {
                        trg.value = cutChinese(trg.value, 0, len);
                    }
                };

                $scope.watchKeyword = function($e, id, keywordName, dirtyName, kwModelId) {
                    watchKwLen(kwModelId, 50);
                    if ($scope.canSave($e)) {
                        $scope.setKeywords(id, keywordName, dirtyName);
                    };
                };

                /* 职位领域 */
                $scope.toggleCat = function(cat, $e) {
                    $scope.feedData.catDirty = false;
                    var cats = $scope.feedData.feed.job_domain,
                        target = angular.element($e.target),
                        id = cat.id,
                        category = cat.category,
                        active = target.hasClass('active');

                    var cats = $scope.feedData.feed.job_domain || [];

                    if (active) {

                        for (var i = 0, l = cats.length; i < l; i++) {
                            if (cats[i].id == id) {
                                $scope.feedData.feed.job_domain.splice(i, 1);
                                break;
                            };
                        };
                    } else {
                        //超过3个不允许再填
                        if (cats.length >= 3) return;
                        $scope.feedData.feed.job_domain.push({
                            id: id,
                            category: category
                        });
                    };
                    target.toggleClass('active');
                };

                $scope.isCatActive = function(cat) {
                    var cats = $scope.feedData.feed.job_domain;
                    if (!cats || !cats.length) return false;
                    for (var i = 0, l = cats.length; i < l; i++) {
                        if (cats[i].id == cat.id) return 'active';
                    };
                    return false;
                };

                /* 公司偏好:单选 */
                $scope.togglePrefer = function(prefer, $e) {
                    $scope.feedData.preferDirty = false;
                    var prefers = $scope.feedData.feed.company_prefer,
                        target = angular.element($e.target),
                        id = prefer.id,
                        category = prefer.name,
                        active = target.hasClass('active');

                    var prefers = $scope.feedData.feed.company_prefer || [];
                    if (active) {
                        for (var i = 0, l = prefers.length; i < l; i++) {
                            if (prefers[i].id == id) {
                                $scope.feedData.feed.company_prefer = [];
                                break;
                            };
                        };
                    } else {
                        $scope.feedData.feed.company_prefer = [{
                            id: id,
                            category: category
                        }];
                    };
                    target.toggleClass('active');
                };

                $scope.isPreferActive = function(prefer) {
                    var prefers = $scope.feedData.feed.company_prefer;
                    if (!prefers || !prefers.length) return false;
                    for (var i = 0, l = prefers.length; i < l; i++) {
                        if (prefers[i].id == prefer.id) return 'active';
                    };
                    return false;
                };

                //判断是否按下空格、分号
                $scope.canSave = function($e) {
                    var target = $e.target,
                        val = target.value,
                        code = $e.keyCode;
                    if (code == 188) {
                        target.value = val.substring(0, val.length - 1);
                        return true;
                    };
                    return false;
                };

                /* 职位诱惑 */
                $scope.setWelfare = function() {
                    var $dom = angular.element(document.getElementById('JS_welfare_model')),
                        val = $.trim($dom.val());
                    $dom.val('');
                    if ($scope.feedData.feed.job_welfare.length >= 20) return;
                    if (!val || $scope.hasInArr($scope.feedData.feed.job_welfare, val)) return;
                    $scope.addWelfare(val);
                };

                $scope.addWelfare = function(val) {
                    $scope.feedData.welfareDirty = false;
                    if (typeof val == 'string') {
                        pushWords($scope.feedData.feed.job_welfare, val);
                    } else {
                        //$scope.feedData.feed.keywords.push(val);
                    }
                };

                $scope.watchWelfare = function($e) {
                    watchKwLen('#JS_welfare_model', 50);
                    if ($scope.canSave($e)) {
                        $scope.setWelfare();
                    };
                };

                //过滤没有显示的职位领域
                $scope.filterJobDomain = function() {
                    var list = $scope.feedData.feed.job_domain || [],
                        cCat = $scope.feedData.company.categorys || [],
                        aCat = $scope.feedData.analyze_job_domain || [],
                        allCat = cCat.concat(aCat),
                        newArr = [];

                    for (var i = 0, l = list.length; i < l; i++) {
                        var lId = list[i].id;
                        for (var j = 0, m = allCat.length; j < m; j++) {
                            jId = allCat[j].id;
                            if (lId == jId) {
                                newArr.push(list[i]);
                                break;
                            };
                        };
                    };

                    $scope.feedData.feed.job_domain = newArr;
                };

                //检查错误，并跳转到对应元素
                var chkErr = function(id, keyName) {
                    var objExist = false;
                    if ($scope.feedData.feed[keyName] != undefined) {
                        if (typeof $scope.feedData.feed[keyName] == 'string' && $scope.feedData.feed[keyName].trim() != '') {
                            objExist = true;
                        } else if (typeof $scope.feedData.feed[keyName] == 'object' && $scope.feedData.feed[keyName].length > 0) {
                            objExist = true;
                        }
                    }
                    if (document.getElementById(id) != null && !objExist) {
                        //console.log('chkErr',id);
                        if (id.match(/^JS_level_edit$/i)) {
                            if ($scope.isAddNew) {
                                jumpToPanel('#label_level_title');
                                $scope.feedData.levelDirty = true;
                            } else {
                                jumpToPanel('#label_level_title_edit');
                            }
                        } else if (id.match(/^JS_job_desc_box/i)) {
                            if ($scope.isAddNew) {
                                jumpToPanel('#label_job_desc_title');
                                $scope.feedData.descDirty = true;
                            } else {
                                jumpToPanel('#JS_job_desc_edit_box');
                            }
                        } else if (id.match(/^JS_city_addnew/i)) {
                            jumpToPanel('#label_expect_area_title');
                            $scope.feedData.levelCity = true;
                        } else if (id.match(/^JS_job_title_box/i)) {
                            jumpToPanel('#label_job_title_title');
                            $scope.feedData.titleDirty = true;
                        } else {
                            var top = angular.element(document.getElementById(id)).offset().top;
                            angular.element(window).scrollTop(top);
                        }
                        return false;
                    } else {
                        var descTooLong = false;
                        if (!chkChineseWordsLen($scope.feedData.feed['job_desc'], maxKeywordStrLen)) {
                            descTooLong = true;
                        }
                        if (descTooLong && id.match(/^JS_job_desc_box/i)) {
                            if ($scope.isAddNew) {
                                jumpToPanel('#label_job_desc_title');
                                $scope.feedData.descDirty = true;
                            } else {
                                jumpToPanel('#label_job_desc_title_edit');
                            }
                            return false;
                        }else{
                            return true;
                        }
                    }
                };

                //解析
                $scope.jobDescParse = function($event, addForm) {
                    if (chkErr('JS_city_addnew', 'expect_area') == false) {
                        return false;
                    }
                    if (chkErr('JS_level_edit', 'talent_level') == false) {
                        return false;
                    }
                    if (chkErr('JS_job_title_box', 'title') == false) {
                        return false;
                    }
                    if (chkErr('JS_job_desc_box', 'job_desc') == false) {
                        return false;
                    }
                    angular.element($event.currentTarget).html('<img src="/static/b_common/img/loading.gif" alt="loading">');
                    angular.element($event.currentTarget).attr('disabled', true);
                    $scope.form.next(addForm);
                };

                /* 验证表单 */
                $scope.form = {
                    //第1步
                    next: function(form) {
                        $scope.feedData.titleDirty = $scope.feedData.descDirty = true;

                        if (form.$error.maxlength != null && form.$error.job_desc != null && form.$error.maxlength != undefined && form.$error.job_desc != undefined) {
                            //console.log('job_desc_message',document.getElementById('job_desc_message'));
                            document.getElementById('job_desc_message').style.display = 'block';
                            document.getElementById('job_desc_message').getElementsByClassName('validation-invalid')[0].innerHTML = '职位详情请控制在1000字以内！';
                            resetParseBtn();
                            return false;
                        }

                        $scope.feedData.levelDirty = $scope.feedData.levelCity = true;
                        var top = 0,
                            validate = $validation.validate(form);

                        if (!$scope.feedData.feed.title) {
                            form.title.$invalid = true;
                            top = angular.element(document.getElementById('JS_job_title')).closest('.form-panel').offset().top;
                            angular.element(window).scrollTop(top);
                            resetParseBtn();
                            return false;
                        };

                        if (!$scope.feedData.feed.talent_level.length) {
                            if ($scope.isAddNew) {
                                top = angular.element(document.getElementById('JS_level_addnew')).offset().top;
                            } else {
                                top = angular.element(document.getElementById('JS_level_edit')).offset().top;
                            };
                            angular.element(window).scrollTop(top);
                            resetParseBtn();
                            return false;
                        };

                        if (!$scope.feedData.feed.expect_area.length) {
                            if ($scope.isAddNew) {
                                top = angular.element(document.getElementById('JS_city_addnew')).offset().top;
                            } else {
                                // top = angular.element( document.getElementById('JS_city_edit') ).offset().top;
                            };
                            angular.element(window).scrollTop(top);
                            resetParseBtn();
                            return false;
                        };

                        if (!$scope.feedData.feed.job_desc) {

                            form.job_desc.$invalid = true;
                            if ($scope.isAddNew) {
                                top = angular.element(document.getElementById('JS_job_desc_addnew')).closest('.form-panel').offset().top;
                            } else {
                                top = angular.element(document.getElementById('JS_job_desc_edit')).closest('.form-panel').offset().top;
                            };
                            angular.element(window).scrollTop(top);
                            resetParseBtn();
                            return false;
                        };
                        $scope.loadingMore = true;

                        validate
                            .success(function() {
                                $scope.loadingMoreDone = true;
                                $scope.loadingMore = false;
                                $scope.next();
                            })
                            .error(function() {

                            });
                    },
                    //第2步验证
                    submit: function(form) {

                        if (!$scope.isAddNew) {
                            //console.log('ok',$scope.isFillAll,$scope.invalidPanelClassName);
                            if ($scope.isFillAll) {} else {
                                if ($scope.invalidPanelClassName != '') {
                                    jumpToPanel($scope.invalidPanelClassName);
                                    return false;
                                }
                            }
                        }

                        $scope.filterJobDomain();

                        $scope.feedData.keywordDirty = $scope.feedData.salaryDirty = true;
                        //$scope.feedData.catDirty =
                        // = $scope.feedData.preferDirty = $scope.feedData.welfareDirty

                        var fastScroll = function(id) {
                            //console.log('fastScroll', id, $scope.feedData.feed);
                            var top = angular.element(document.getElementById(id)).offset().top;
                            angular.element(window).scrollTop(top);
                        };
                        if ($scope.isAddNew) {
                            if (!$scope.feedData.feed.expect_area.length) {
                                fastScroll('label_expect_area_title');
                                return false;
                            };

                            if (!$scope.feedData.feed.talent_level.length) {
                                fastScroll('JS_level_edit');
                                return false;
                            };

                            if ($scope.feedData.feed['title'] == "") {
                                fastScroll('label_job_title_title');
                                return false;
                            };

                            if ($scope.feedData.feed['job_desc'] == "") {
                                fastScroll('label_job_desc_title');
                                return false;
                            };
                        }

                        if (!$scope.feedData.feed.analyze_titles.length) {
                            fastScroll('JS_job_keywords_box');
                            return false;
                        };

                        if (!$scope.feedData.feed.keywords.length) {
                            fastScroll('JS_skill_keywords_box');
                            return false;
                        };

                        var top = 0,
                            validate = $validation.validate(form);

                        //判断是否填写了最高最低薪资
                        if (!$scope.isNegotiable && (!$scope.feedData.feed.salary_min || !$scope.feedData.feed.salary_max)) {
                            $scope.reSalaryError = true;
                        };

                        if (!$scope.isNegotiable) {
                            if (!$scope.feedData.feed.salary_min) {
                                form.salary_min.$invalid = true;
                            };
                            if (!$scope.feedData.feed.salary_max) {
                                form.salary_max.$invalid = true;
                            };
                        };

                        //当有填写公司领域或者有算法推荐的领域，才验证职位领域
                        /*if (($scope.feedData.company.categorys && $scope.feedData.company.categorys.length) || ($scope.feedData.analyze_job_domain && $scope.feedData.analyze_job_domain.length)) {
                            if (!$scope.feedData.feed.job_domain.length) {
                                top = angular.element(document.getElementById('JS_categorys_box')).offset().top;
                                angular.element(window).scrollTop(top);
                                return false;
                            };
                        };*/

                        //如果是中高级别人才，则需验证公司偏好和职位诱惑
                        /*if (!$scope.isPrimaryLevel()) {

                            //公司偏好
                            if (!$scope.feedData.feed.company_prefer.length) {
                                $scope.rePreferError = true;
                                top = angular.element(document.getElementById('JS_prefer_box')).offset().top;
                                angular.element(window).scrollTop(top);
                                return false;
                            };

                            //职位诱惑
                            if (!$scope.feedData.feed.job_welfare.length) {
                                $scope.reWelfareError = true;
                                top = angular.element(document.getElementById('JS_welfare_box')).offset().top;
                                angular.element(window).scrollTop(top);
                                return false;
                            };

                        };*/

                        if (!$scope.isNegotiable && (!$scope.feedData.feed.salary_min || !$scope.feedData.feed.salary_max)) {
                            $scope.reSalaryError = true;
                            $scope.reSalaryErrorMsg = $scope.defaultErrorMsg;
                            if (!$scope.feedData.feed.salary_min) {
                                $('[name="salary_min"]').val('').focus();
                            } else if (!$scope.feedData.feed.salary_max) {
                                $('[name="salary_max"]').val('').focus();
                            };
                            top = angular.element(document.getElementById('JS_salary_box')).offset().top;
                            angular.element(window).scrollTop(top);
                            return false;
                        };

                        //薪资填写，但有误的情况
                        if (!$scope.isNegotiable && $scope.reSalaryError) {
                            top = angular.element(document.getElementById('JS_salary_box')).offset().top;
                            angular.element(window).scrollTop(top);
                            return false;
                        };

                        validate
                            .success(function() {
                                $scope.submit();
                            })
                            .error(function() {
                                console.log('submit error');
                            });

                    }
                };

                /* 返回上一步 */
                $scope.previous = function() {
                    // $scope.feedData.feed = angular.copy( $scope.feedData.Databackup );
                    $scope.firstStep = true;
                };

                // 删除定制
                $scope.deleteFeed = function(id) {
                    $.alert(
                        '<p class="f16 text-center"><i class="i-l-notice"></i>确定删除该定制吗？</p><p class="text-center cf46c62" style="font-size:14px;">删除后不可恢复</p>',
                        function() {
                            location.href = id_url('/feed/delete/', id);
                        }
                    );
                };

                /* 第一步表单验证成功，跳转到第二步 */
                $scope.next = function() {
                    $scope.firstStep = true;
                    //angular.element( window ).scrollTop( 0 );
                    angular.element(document.getElementById('JS_job_keyword_model')).focus();

                    $http.post(
                        '/special_feed/analyze_jd/',
                        JSON.stringify({
                            title: $scope.feedData.feed.title,
                            job_desc: $scope.feedData.feed.job_desc,
                            expect_area: $scope.concat($scope.feedData.feed.expect_area),
                            talent_level: $scope.formatArrayParam($scope.feedData.feed.talent_level)
                        })
                    ).success(function(res) {
                        if (res && res.data) {
                            $scope.loadAnalyzeData(res.data);
                        } else {
                            $scope.loadAnalyzeData({});
                        };
                    }).error(function() {
                        //alert("获取推荐职位关键字失败！");
                        $scope.loadAnalyzeData({});
                    });

                    setTimeout(function() {
                        var topOffest = angular.element(document.getElementById('JS_job_keywords_box')).offset().top;
                        angular.element(window).scrollTop(topOffest);
                    }, 500);

                    $scope.feedData.Databackup = angular.extend($scope.feedData.Databackup, {
                        title: $scope.feedData.feed.title,
                        job_desc: $scope.feedData.feed.job_desc,
                        expect_area: $scope.feedData.feed.expect_area,
                        talent_level: $scope.feedData.feed.talent_level
                    });
                };

                $scope.formatSubmitData = function() {
                    var obj = angular.extend({}, $scope.feedData.feed);
                    obj.job_domain = $scope.returnIdArray(obj.job_domain);
                    obj.company_prefer = $scope.returnIdArray(obj.company_prefer);
                    obj.job_welfare = obj.job_welfare.join(',');
                    obj.keywords = obj.keywords.join(',');
                    obj.analyze_titles = obj.analyze_titles.join(',');
                    obj.talent_level = obj.talent_level.join(',');
                    obj.expect_area = $scope.concat(obj.expect_area);
                    obj.block_titles = $scope.feedData.analyze_titles.join(',');
                    obj.block_keywords = $scope.feedData.analyze_keywords.join(',');
                    obj.__ = new Date().getTime();
                    if ($scope.isNegotiable) {
                        obj.salary_min = 0;
                        obj.salary_max = 1000000;
                    };
                    return obj;
                };

                $scope.submit = function() {
                    var callBackError = function(errors) {
                            var msg = '',
                                carChar = {
                                    salary_max: {
                                        variable: 'reSalaryError',
                                        msg: 'reSalaryErrorMsg',
                                        id: 'label_salary_title'
                                    },
                                    salary_min: {
                                        variable: 'reSalaryError',
                                        msg: 'reSalaryErrorMsg',
                                        id: 'label_salary_title'
                                    },
                                    /*job_desc: {
                                        message: '#job_desc_message',
                                    },*/
                                    job_desc: {
                                        variable: 'reDescError',
                                        msg: 'reDescErrorMsg',
                                        id: 'label_job_desc_title'
                                    },
                                    talent_level: {
                                        variable: 'reLevelError',
                                        msg: 'reLevelErrorMsg',
                                        id: 'label_level_title'
                                    },
                                    title: {
                                        variable: 'reTitleError',
                                        msg: 'reTitleErrorMsg',
                                        id: 'label_job_title_title'
                                    },
                                    expect_area: {
                                        variable: 'reAreaErrorError',
                                        msg: 'reAreaErrorMsg',
                                        id: 'label_expect_area_title'
                                    },
                                    keywords: {
                                        variable: 'reKeywordsError',
                                        msg: 'reKeywordsErrorMsg',
                                        id: 'label_skill_keywords_title'
                                    },
                                    analyze_titles: {
                                        variable: 'reJobKeywordsError',
                                        msg: 'reJobKeywordsErrorMsg',
                                        id: 'label_job_keywords_title'
                                    }
                                    /*,
                                    job_domain: {
                                        variable: 'reCatError',
                                        msg: 'reCatErrorMsg'
                                    }*/
                                    /*,
                                    company_prefer: {
                                        variable: 'rePreferError',
                                        msg: 'rePreferErrorMsg'
                                    },
                                    job_welfare: {
                                        variable: 'reWelfareError',
                                        msg: 'reWelfareErrorMsg'
                                    }*/
                                };

                            for (var i in errors) {
                                var err = carChar[i];
                                if (err) {
                                    if (err.message) {
                                        $(err.message).text(errors[i][0]).show();
                                    } else {
                                        $scope[carChar[i].variable] = true;
                                        $scope[carChar[i].msg] = errors[i][0];
                                        if(document.getElementById(carChar[i].id)!=null){
                                            var top = angular.element(document.getElementById(carChar[i].id)).offset().top;
                                            angular.element(window).scrollTop(top);
                                        }
                                        //break;
                                    };
                                    continue;
                                };
                                msg += errors[i][0] + '\r\n';
                            };

                            if (msg) {
                                $.alert('<p class="f16 text-center"><i class="i-l-notice"></i>' + msg + '</p>');
                            };

                        },
                        func = function() {
                            $scope.feedData.submiting = true;
                            $http.post(
                                '/special_feed/submit_feed/',
                                JSON.stringify($scope.formatSubmitData())
                            ).success(function(res) {
                                if (res && res.status == 'ok') {
                                    if (res.show_mission) {
                                        $('#JS_username').html(res.username);
                                        $('#JS_mission_time').html(res.mission_time);
                                        $('.modal-backdrop-tip,.modal-tip').show();
                                        $('.modal-dialog-tip').css({
                                            marginTop: ($(window).height() - $('.modal-dialog-tip').height()) / 2 + 'px'
                                        });
                                    } else if (res.redirect_url) {
                                        if(res.redirect_url.match(/^\/feed$/i)){
                                            location.href = '/special_feed/page/#/feed_resume/'+res.feed_id+'/';
                                        }else{
                                            location.href = res.redirect_url;
                                        }
                                    } else {
                                        $.alert('<p class="f16 text-center"><i class="i-l-notice"></i>保存成功！</p>');
                                    };
                                } else if (res.errors) {
                                    callBackError(res.errors);
                                } else {
                                    $.alert('<p class="f16 text-center"><i class="i-l-notice"></i>新增定制失败，可能是你的套餐设置问题，请联系我们解决！</p>');
                                };
                                $scope.feedData.submiting = false;
                            }).error(function() {
                                $.alert('<p class="f16 text-center"><i class="i-l-notice"></i>新增定制失败，可能是你的套餐设置问题，请联系我们解决！</p>');
                                $scope.feedData.submiting = false;
                            });
                        };

                    if ($scope.isAddNew) {

                        if ($scope.isFillAll) {
                            var html = '<div style="margin: 0 auto;width: 400px;">' +
                                '<div class="f16 text-center"><i class="i-l-notice"></i>以下内容提交后不可修改</div>' +
                                '<div class="f16 text-left" style="padding: 10px 0 0 135px;">职位名：<span class="cf46c62">' + $scope.feedData.feed.title + '</span></div>' +
                                '<div class="f16 text-left" style="padding: 10px 0 0 135px;">工作地：<span class="cf46c62">' + $scope.concat($scope.feedData.feed.expect_area) + '</span></div>' +
                                '</div>';
                            $.alert(
                                html,
                                '',
                                '', {
                                    handlers: [{
                                        title: '返回修改',
                                        eventType: 'click',
                                        className: 'button button-normal w158 f16',
                                        event: function() {
                                            $._LayerOut.close();
                                        }
                                    }, {
                                        title: '确定',
                                        eventType: 'click',
                                        className: 'button button-primary w158 f16',
                                        event: function() {
                                            func();
                                            $._LayerOut.close();
                                        }
                                    }]
                                }
                            );
                        } else {
                            if ($scope.invalidPanelClassName != '') jumpToPanel($scope.invalidPanelClassName);
                        }

                    } else {
                        if ($scope.invalidPanelClassName != '') {
                            jumpToPanel($scope.invalidPanelClassName);
                        } else {
                            func();
                        }
                    };
                };

                //显示第二个红包
                $scope.toggleEnvelope = function() {
                    $scope.envelope = true;
                };

                //请求推荐数据
                $scope.getAnalyzeRelated = function() {
                    $scope.isSyncData = true;
                    //if (!$scope.loadingMoreDone) return;
                    if (window.__httpAna) {
                        window.__httpAna.abort();
                    };

                    window.__httpAna = $.ajax({
                        type: "POST",
                        url: '/special_feed/analyze_related/',
                        data: JSON.stringify($scope.formatSubmitData()),
                        /*headers: {
                            'Content-Type': 'application/json'
                        },*/
                        success: function(res) {
                            if (res && res.status == 'ok' && res.data) {
                                $scope.synData(res.data);
                            } else {
                                //alert("获取推荐数据失败！");
                            }
                        },
                        //dataType: 'json'
                    });
                };

                //缓存推荐结果
                $scope.synData = function(data) {
                    $scope.animateNumber(data);

                    angular.element(document.getElementById('JS_slideup_btn')).addClass('active');
                    $('#JS_off_tip').slideUp();
                    $('#JS_on_tip').slideDown();

                    $scope.feedData.min_salary = data.salary.min;
                    $scope.feedData.max_salary = data.salary.max;
                    $scope.feedData.min_num = data.num.min;
                    $scope.feedData.max_num = data.num.max;
                };

                //推荐结果数字动画
                $scope.animateNumber = function(data) {

                    var step = 50;

                    var min_salary = $scope.feedData.min_salary,
                        max_salary = $scope.feedData.max_salary,
                        min_num = $scope.feedData.min_num,
                        max_num = $scope.feedData.max_num;

                    var sMin = $('#JS_salary_min'),
                        sMax = $('#JS_salary_max'),
                        nMin = $('#JS_num_min'),
                        nMax = $('#JS_num_max');

                    var csMin = (data.salary.min - min_salary) / step,
                        csMax = (data.salary.max - max_salary) / step,
                        cnMin = (data.num.min - min_num) / step,
                        cnMax = (data.num.max - max_num) / step;

                    var i = 1,
                        formatNumber = function(number, places, symbol, thousand) {
                            number = number || 0;
                            places = !isNaN(places = Math.abs(places)) ? places : 2;
                            symbol = symbol !== undefined ? symbol : "";
                            thousand = thousand || ",";
                            var negative = number < 0 ? "-" : "",
                                i = parseInt(number = Math.abs(+number || 0).toFixed(places), 10) + "",
                                j = (j = i.length) > 3 ? j % 3 : 0;
                            return symbol + negative + (j ? i.substr(0, j) + thousand : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thousand);
                        },
                        func = function() {
                            var num1 = formatNumber(parseInt(csMin * i + min_salary)),
                                num2 = formatNumber(parseInt(csMax * i + max_salary)),
                                num3 = formatNumber(parseInt(cnMin * i + min_num)),
                                num4 = formatNumber(parseInt(cnMax * i + max_num));
                            sMin.text(num1);
                            sMax.text(num2);
                            nMin.text(num3);
                            nMax.text(num4);
                            i++;

                            if (i <= step) {
                                setTimeout(function() {
                                    func();
                                }, 30)
                            };


                        };
                    func();
                };

                //同步薪资
                $scope.synSalary = function() {
                    $scope.isNegotiable = false;
                    $scope.feedData.feed.salary_min = $scope.feedData.min_salary;
                    $scope.feedData.feed.salary_max = $scope.feedData.max_salary;
                    $('[name="salary_min"]').val($scope.feedData.min_salary);
                    $('[name="salary_max"]').val($scope.feedData.max_salary);
                    $('.icon-menu-salary').addClass('right-nav-state-current');
                    jumpToPanel('#label_salary_title');
                };

                //预览定制
                $scope.toggleView = function() {
                    $scope.viewFeed = !$scope.viewFeed;
                    $scope.refresh();
                };

                //切换职位详情
                $scope.toggleDesc = function() {
                    $scope.showViewDesc = !$scope.showViewDesc;
                    $scope.refresh();
                };

                //更新弹窗位置
                $scope.refresh = function() {
                    if (!$scope.viewFeed) return;
                    setTimeout(function() {
                        $('.modal-dialog-view').css({
                            marginTop: ($(window).height() - $('.modal-dialog-view').height()) / 2 + 'px'
                        });
                    }, 0);
                };

            }
        ]
    );

    app.directive('ngEnter', function() {
        return function(scope, element, attrs) {
            element.bind("keydown keypress", function(event) {
                if (event.which === 13) {
                    scope.$apply(function() {
                        scope.$eval(attrs.ngEnter);
                    });

                    event.preventDefault();
                }
            });
        };
    });

    //工作地按钮
    app.directive('locationButton', function() {
        return {
            restrict: 'E',
            replace: true,
            template: '<a class="button button-normal f16" data-id="{- city -}" ng-class="isCityActive( city )" ng-click="toggleCity( city , $event )" ng-repeat="city in expectArea">{- city -}</a>',
            controller: function($scope, $element) {
                //console.log('locationButton controller',$scope, $element);

            },
            link: function(scope, elem, attrs) {},
            scope: {
                expectArea: "="
            }
        }
    });

    //人才级别按钮
    app.directive('talentButton', function() {
        return {
            restrict: 'E',
            replace: true,
            template: '<a class="button button-normal f16" data-level="{- level -}" ng-class="isLevelActive( level )" ng-click="toggleLevel( level , $event )" ng-repeat="level in talentLevel">{- level -}</a>',
            controller: function($scope, $element) {
                //console.log('talentButton controller',$scope, $element);

            },
            link: function(scope, elem, attrs) {},
            scope: {
                talentLevel: "="
            }
        }
    });

    //详情输入框
    app.directive('detailTextarea', function() {
        return {
            restrict: 'E',
            replace: true,
            template: '<textarea name="job_desc" id="JS_job_desc_addnew" rows="10" class="textarea full" ng-model="jobDescInfo" validator="jobDesc" ng-maxlength="1000" message-id="job_desc_message">{- jobDescInfo -}</textarea>',
            controller: function($scope, $element) {
                //console.log('locationButton controller',$scope, $element);

            },
            link: function(scope, elem, attrs) {},
            scope: {
                jobDescInfo: "="
            }
        }
    });

    app.filter('maxlen', function() {
        //截取中文
        var cutChinese = function(str, offsetStart, offsetEnd) {
            if (typeof str != 'string') return '';

            //得到字符总数
            var cn_strlen = function(str) {
                    var i = 0;
                    var c = 0;
                    var unicode = 0;
                    var len = 0;
                    if (str != undefined && typeof str == "string") {
                        str = str.trim();
                        if (str == "") {
                            return 0;
                        } else {
                            len = str.length;
                            for (i = 0; i < len; i++) {
                                unicode = str.charCodeAt(i);
                                if (unicode < 127) { //判断是单字符还是双字符
                                    c += 1;
                                } else { //chinese
                                    c += 2;
                                }
                            }
                            return c;
                        }
                    } else {
                        return 0;
                    }
                }
                //截取字符
            var cn_substr = function(str, startp, endp) {
                var i = 0;
                var c = 0;
                var unicode = 0;
                var rstr = '';
                var len = str.length;
                var sblen = cn_strlen(str);
                if (startp < 0) {
                    startp = sblen + startp;
                }
                if (endp < 1) {
                    endp = sblen + endp; // - ((str.charCodeAt(len-1) < 127) ? 1 : 2);
                }
                // 寻找起点
                for (i = 0; i < len; i++) {
                    if (c >= startp) {
                        break;
                    }
                    var unicode = str.charCodeAt(i);
                    if (unicode < 127) {
                        c += 1;
                    } else {
                        c += 2;
                    }
                }
                // 开始取
                for (i = i; i < len; i++) {
                    var unicode = str.charCodeAt(i);
                    if (unicode < 127) {
                        c += 1;
                    } else {
                        c += 2;
                    }
                    rstr += str.charAt(i);
                    if (c >= endp) {
                        break;
                    }
                }
                return rstr;
            }
            return cn_substr(str, offsetStart, offsetEnd);
        };
        //检查输入框文字长度
        var chkChineseWordsLen = function(val, len) {
            if (typeof val != 'string') return false;
            var str = val;
            if (str.match(/[^\x00-\xff]/i)) str = str.replace(/[^\x00-\xff]/g, '**');
            if (str.length <= len) {
                return true;
            } else {
                return false;
            }
        };
        return function(str) {
            var len = 16;
            if(!str.match(/[^\x00-\xff]/i)){
                len = 12;
            }
            if (!chkChineseWordsLen(str, len)) {
                return cutChinese(str, 0, len) + '...';
            }else{
                return str;
            }
        };
    });

    //职位扩展名自定义按钮
    app.directive('customizedTitleButton', function() {
        return {
            restrict: 'E',
            replace: true,
            templateUrl: '/static/special_feed/customized_title_button.html',
            controller: function($scope, $element) {
                $scope.isShowNew = false;
                $scope.watchKeyword = function($event, id, keywordName, dirtyName, kwModelId) {
                    $scope.$parent.watchKeyword($event, id, keywordName, dirtyName, kwModelId);
                };
                $scope.hasInArr = function(arr, val) {
                    return $scope.$parent.hasInArr(arr, val);
                };
                $scope.setKeywords = function(id, keywords, dirtyName, keywordName) {
                    /* 技能关键字 */
                    var $dom = angular.element(document.getElementById(id));
                    var val = $.trim($dom.val());
                    if (val == undefined || val.trim() == "") {
                        return;
                    } else if (!val || (keywords != undefined && typeof keywords == 'object' && $scope.hasInArr(keywords, val))) {
                        return;
                    } else {
                        $dom.val('');
                        $scope.$parent.addAnaKeyword(val, dirtyName, keywordName);
                    }
                };
                $scope.setKeywordsEnter = function($event, id, keywordName, dirtyName) {
                    $scope.$parent.setKeywords(id, keywordName, dirtyName);
                };
                $scope.addAnaKeyword = function(val, dirtyName, keywordName) {
                    //console.log('addAnaKeyword',val);
                    $scope.$parent.addAnaKeyword(val, dirtyName, keywordName);
                };
                $scope.removeAnaKeyword = function(anaKeyword, keywords, $event, addArrName) {
                    $scope.$parent.removeAnaKeyword(anaKeyword, keywords, $event, addArrName);
                };
                $scope.$watch('isShowNew', function(newValue, oldValue, scope) {
                    if (newValue == true) {
                        window.setTimeout(function() {
                            document.getElementById('JS_job_keyword_model').focus();
                        }, 200);
                    }
                });

            },
            link: function(scope, elem, attrs) {},
            scope: {
                keywords: "=",
                useRecommand: "=",
                recommandKeywords: "=",
                kwt: "=",
                selectTitle: "="
            }
        }
    });

    //技能关键字自定义按钮
    app.directive('customizedButton', function() {
        return {
            restrict: 'E',
            replace: true,
            templateUrl: '/static/special_feed/customized_button.html',
            controller: function($scope, $element) {
                $scope.isShowNew = false;
                $scope.watchKeyword = function($event, id, keywordName, dirtyName, kwModelId) {
                    $scope.$parent.watchKeyword($event, id, keywordName, dirtyName, kwModelId);
                };
                $scope.hasInArr = function(arr, val) {
                    return $scope.$parent.hasInArr(arr, val);
                };
                $scope.setKeywords = function(id, keywords, dirtyName, keywordName) {
                    /* 技能关键字 */
                    var $dom = angular.element(document.getElementById(id));
                    var val = $.trim($dom.val());
                    if (val == undefined || val.trim() == "") {
                        return;
                    } else if (!val || (keywords != undefined && typeof keywords == 'object' && $scope.hasInArr(keywords, val))) {
                        return;
                    } else {
                        $dom.val('');
                        $scope.$parent.addAnaKeyword(val, dirtyName, keywordName);
                    }
                };
                $scope.setKeywordsEnter = function($event, id, keywordName, dirtyName) {
                    $scope.$parent.setKeywords(id, keywordName, dirtyName);
                };
                $scope.addAnaKeyword = function(val, dirtyName, keywordName) {
                    $scope.$parent.addAnaKeyword(val, dirtyName, keywordName);
                };
                $scope.removeAnaKeyword = function(anaKeyword, keywords, $event, addArrName) {
                    $scope.$parent.removeAnaKeyword(anaKeyword, keywords, $event, addArrName);
                };
                /*$scope.$watch('isShowNew', function(newValue, oldValue, scope) {
                    if (newValue == true) {
                        window.setTimeout(function() {
                            document.getElementById('JS_keyword_model').focus();
                        }, 200);
                    }
                });*/

            },
            link: function(scope, elem, attrs) {},
            scope: {
                keywords: "=",
                useRecommand: "=",
                recommandKeywords: "=",
                kwt: "=",
                selectTitle: "="
            }
        }
    });

    //职位诱惑自定义按钮
    app.directive('welfareButton', function() {
        return {
            restrict: 'E',
            replace: true,
            templateUrl: '/static/special_feed/welfare_button.html',
            controller: function($scope, $element) {
                $scope.isShowNew = false;
                $scope.watchWelfare = function($event) {
                    $scope.$parent.watchWelfare($event);
                };
                $scope.hasInArr = function(arr, val) {
                    return $scope.$parent.hasInArr(arr, val);
                };
                $scope.setWelfare = function() {
                    return $scope.$parent.setWelfare();
                };
                $scope.setKeywords = function(id, keywords) {
                    /* 技能关键字 */
                    var $dom = angular.element(document.getElementById(id));
                    var val = $.trim($dom.val());
                    if (val == undefined || val.trim() == "") {
                        return;
                    } else if (!val || (keywords != undefined && typeof keywords == 'object' && $scope.hasInArr(keywords, val))) {
                        return;
                    } else {
                        $dom.val('');
                        $scope.$parent.addWelfare(val);
                    }
                };
                $scope.addWelfare = function(val) {
                    //console.log('addWelfare',val);
                    $scope.$parent.addWelfare(val);
                };
                $scope.removeAnaKeyword = function(anaKeyword, keywords, $event, addArrName) {
                    $scope.$parent.removeAnaKeyword(anaKeyword, keywords, $event, addArrName);
                };
                $scope.$watch('isShowNew', function(newValue, oldValue, scope) {
                    if (newValue == true) {
                        window.setTimeout(function() {
                            document.getElementById('JS_welfare_model').focus();
                        }, 200);
                    }
                });
            },
            link: function(scope, elem, attrs) {},
            scope: {
                keywords: "=",
                recommandKeywords: "="
            }
        }
    });

    //职位领域按钮
    app.directive('domainButton', function() {
        return {
            restrict: 'E',
            replace: true,
            template: '<a class="button button-normal" ng-repeat="cat in categorys" data-cat="{- cat.id -}" ng-class="isCatActive( cat )" ng-click="toggleCat( cat , $event )">{- cat.category -}</a>',
            controller: function($scope, $element) {
                //console.log('talentButton controller',$scope, $element);

            },
            link: function(scope, elem, attrs) {},
            scope: {
                categorys: "="
            }
        }
    });

    //公司偏好按钮
    app.directive('preferButton', function() {
        return {
            restrict: 'E',
            replace: true,
            template: '<a class="button button-normal" ng-repeat="prefer in companyPrefer" ng-class="isPreferActive( prefer )" ng-click="togglePrefer( prefer , $event )">{- prefer.name -}</a>',
            controller: function($scope, $element) {
                //console.log('talentButton controller',$scope, $element);

            },
            link: function(scope, elem, attrs) {},
            scope: {
                companyPrefer: "="
            }
        }
    });

    //定制标题头
    app.directive('feedLabel', function() {
        return {
            restrict: 'E',
            replace: true,
            template: '<div><p id="{- forId -}" class="form-label alert-label-ok text-center c607d8b" ng-class="{\'alert-label-error\':isShowErr}"><label for="{- forId -}" class="relative"><span class="sumsun cf46c62" ng-if="star">*</span><span class="info">{- title -}</span></label></p><div class="wrong-tip ng-hide" ng-show="isShowErr"><span ng-bind="errorMsg"></span><span class="arrow"><em></em></span></div></div>',
            controller: function($scope, $element) {
                var addErr = function(forId, className) {
                    if ($scope.forId == forId && document.getElementsByClassName(className) != null) {
                        //console.log('addErr',forId, className,$scope);
                        if ($scope.$parent.isShowCurrentList && $scope.$parent.isShowCurrentList.hasOwnProperty(className)) $scope.$parent.isShowCurrentList[className] = false;
                        var trg = angular.element(document.getElementsByClassName(className)[0]);
                        if (trg.attr('class') && trg.attr('class').match(/right\-nav\-current/i)) {
                            trg.removeClass('right-nav-current');
                            trg.addClass('right-nav-current-wrong');
                            trg.addClass('right-nav-state-error');
                        } else if (trg.attr('class') && trg.attr('class').match(/right\-nav\-state\-current/i)) {
                            trg.removeClass('right-nav-state-current');
                            trg.addClass('right-nav-state-error');
                        } else {
                            trg.addClass('right-nav-state-error');
                        }
                        return false;
                    }

                };
                var removeErr = function(forId, className, newVal, oldVal) {
                    if ($scope.forId == forId && document.getElementsByClassName(className) != null) {
                        //console.log('removeErr',forId, className,$scope);
                        if ($scope.$parent.isShowCurrentList && $scope.$parent.isShowCurrentList.hasOwnProperty(className)) $scope.$parent.isShowCurrentList[className] = true;
                        var trg = angular.element(document.getElementsByClassName(className)[0]);
                        if (trg.attr('class') && trg.attr('class').match(/right\-nav\-current/i)) {
                            trg.removeClass('right-nav-current-wrong');
                            trg.removeClass('right-nav-state-error');
                            trg.addClass('right-nav-current');
                        } else if (trg.attr('class') && trg.attr('class').match(/right\-nav\-state\-error/i)) {
                            trg.removeClass('right-nav-state-error');
                            trg.addClass('right-nav-state-current');
                        } else {
                            trg.addClass('right-nav-state-current');
                        }
                        if (oldVal != newVal && oldVal == true) {
                            angular.element(document.getElementsByClassName('icon-menu')).removeClass('right-nav-current');
                            trg.addClass('right-nav-current right-nav-state-current');
                        }
                        return false;
                    }

                };
                $scope.$watch('isShowErr', function(newVal, oldVal, scope) {
                    //if (newVal != oldVal) {
                    if (newVal == true) {
                        addErr('label_expect_area_title', 'icon-menu-city');
                        addErr('label_level_title', 'icon-menu-level');
                        addErr('label_job_title_title', 'icon-menu-job-title');
                        addErr('label_job_desc_title', 'icon-menu-job-desc');
                        //addErr('label_keywords_title', 'icon-menu-keyword');
                        addErr('label_job_keywords_title', 'icon-menu-job-keyword');
                        addErr('label_skill_keywords_title', 'icon-menu-skill-keyword');
                        //addErr('label_domain_title', 'icon-menu-domain');
                        //addErr('label_prefer_title', 'icon-menu-prefer');
                        //addErr('label_welfare_title', 'icon-menu-welfare');
                        addErr('label_salary_title', 'icon-menu-salary');
                    } else {
                        removeErr('label_expect_area_title', 'icon-menu-city', newVal, oldVal);
                        removeErr('label_level_title', 'icon-menu-level', newVal, oldVal);
                        removeErr('label_job_title_title', 'icon-menu-job-title', newVal, oldVal);
                        removeErr('label_job_desc_title', 'icon-menu-job-desc', newVal, oldVal);
                        //removeErr('label_keywords_title', 'icon-menu-keyword', newVal, oldVal);
                        removeErr('label_job_keywords_title', 'icon-menu-job-keyword', newVal, oldVal);
                        removeErr('label_skill_keywords_title', 'icon-menu-skill-keyword', newVal, oldVal);
                        //removeErr('label_domain_title', 'icon-menu-domain', newVal, oldVal);
                        //removeErr('label_prefer_title', 'icon-menu-prefer', newVal, oldVal);
                        //removeErr('label_welfare_title', 'icon-menu-welfare', newVal, oldVal);
                        removeErr('label_salary_title', 'icon-menu-salary', newVal, oldVal);
                    }
                    //}
                });

            },
            link: function(scope, elem, attrs) {},
            scope: {
                title: "=",
                forId: "=",
                isShowErr: "=",
                errorMsg: "=",
                star: "="
            }
        }
    });

})(angular);