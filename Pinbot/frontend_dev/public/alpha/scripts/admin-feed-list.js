$(function(o) {

    window.confirmBox = (function() {
        var $box = $('.confirm-box');

        function preZero(n) {
            return (n = +n) < 10 ? '0' + n : n;
        };

        function today() {
            var d = new Date();
            return ([
                d.getFullYear(), preZero(d.getMonth() + 1), preZero(d.getDate())
            ]).join('-')
        }

        function nextDay() {
            var str = today();
            var date = new Date(str);
            date.setDate((+str.split('-')[2] + 1));
            return date.toJSON().split('T')[0];
        }
        $box.find('input[type="date"]').val(today());
        var isHidden = true;
        var lasttype = '';
        return {
            show: function(type) {
                var number = $('.selected-item').length || 0;
                $box.show().find('span.selected-num').html(number);
                $('.confirm-action').hide();
                $('.action-' + type).show();
                isHidden = false;
                lasttype = type;
            },
            toggle: function(type) {
                if (isHidden) {
                    this.show(type);
                } else {
                    if (lasttype != type) {
                        this.show(type);
                    } else {
                        this.hide();
                    }
                }
            },
            hide: function() {
                $box.hide();
                isHidden = true;
            }
        }
    }());

    var opts = $.extend({}, {
            html: '',
            style: 'preview-info-default',
            width: '650px',
            height: '450px'
        }, o || {}),
        $w = $(window);
    var timer;
    var hoverInterval = 600;
    var div = $('<div class="preview-info-default"><div style="margin:0;padding:0;position:ralative;width:100%;height:100%" class="info_wrapper"><b style="margin:0;padding:0;background-position:5px center; background-repeat:no-repeat;position:absolute;left:-15px;top:8%;width:15px;height:17px;" class="info_arrow"></b><div style="margin:0;padding:0;" class="info_content"></div></div></div>');
    var initTimer;
    var $dummy = $('<div/>').appendTo('body').hide();

    function Int(val) {
        return parseInt(val, 10);
    };
    $('.feed-page').on('xmouseenter', '.feed-item', function() {
        var elem = $(this),
            w = Int(opts.width),
            h = Int(opts.height),
            gap = 12,
            left, top, ll, tt, ww, hh, arrow;
        if (elem.find('.control-pending').length) {
            clearTimeout(initTimer);
            return false;
        }
        initTimer = setTimeout(function() {
            if (timer) {
                clearTimeout(timer);
            }
            if (elem.find('.control-pending').length)
                return false;
            div.appendTo('body').css({
                position: 'absolute',
                'z-index': 100000
            }).width(w - Int(div.css('padding-left')) - Int(div.css('padding-right')) - Int(div.css('border-left-width')) - Int(div.css('border-right-width'))).height(h - Int(div.css('padding-top')) - Int(div.css('padding-bottom')) - Int(div.css('border-top-width')) - Int(div.css('border-bottom-width')));
            arrow = div.find('.info_arrow');
            left = (ll = elem.offset().left) + elem.outerWidth() + gap;
            if (left + (ww = div.outerWidth()) > $w.width()) {
                arrow.css({
                    'background-position': '-20px 0',
                    'left': '',
                    'right': '-15px'
                });
                left = ll - ww - gap;
            }
            top = tt = elem.offset().top;
            if (top + (hh = div.outerHeight()) - $w.scrollTop() > $w.height()) {
                arrow.css({
                    'top': '',
                    'bottom': '8%'
                });
                top = tt - hh + elem.outerHeight();
            }
            div.css({
                top: top,
                left: left
            }).find('.info_content').html(opts.html).end().hover(function() {
                timer && clearTimeout(timer);
            }, function() {
                timer = setTimeout(function() {
                    div.remove();
                }, 300);
            });
            setTimeout(function() {
                var loadUrl = elem.find('.item-body>a').attr('href');
                $dummy.load(loadUrl + ' #main', function() {
                    $dummy.find('#main').removeAttr('id').removeAttr('class');
                    $dummy.find('.contact-info').remove();
                    $dummy.find('#resume-detail-header').remove();
                    $dummy.find('.contact-info').remove();
                    $dummy.find('.aside').remove();
                    $dummy.find('.btn-toggle').remove();
                    div.find('.info_content').html($dummy.html());
                });
            }, 100);
        }, $('.preview-info-default').length && 400 || hoverInterval);
    });
    $('.feed-page').on('mouseleave', '.feed-item', function() {
        clearTimeout(initTimer);
        timer = setTimeout(function() {
            div.remove();
        }, 400);
    });
});
$(document).keyup(function(e) {
    if (e.keyCode == 27) {
        if ($('.preview-info-default').length) {
            $('.preview-info-default').remove();
        }
    }
});


var pbDebug = false;
var feedApp = angular.module('feedApp', ['app.utils']);
var $funcs = angular.injector(['app.utils']);
var pbLib = $funcs.get('pbLib');
var pbFunc = $funcs.get('pbFunc');
var getModeData = $funcs.get('getModeData');
feedApp.config([
    '$interpolateProvider',
    function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    }
]);
feedApp.config([
    '$routeProvider',
    function($routeProvider) {
        var $feedTemplate = $('#template-feeditem').html();

        $routeProvider.when('/group/:id', {
            template: $feedTemplate,
            controller: 'feedPage'
        });

        var other = $('.feed-group-link').first();
        var url = '/';
        if (other.length) {
            url = other.attr('href').substr(1);
        }

        $routeProvider.otherwise({
            redirectTo: url
        });
    }
]);
feedApp.factory('Feed', [
    '$http',
    function($http) {
        var pathname = window.location.pathname || '';
        var default_view = 'cached';
        if (pathname === '/statis/feed_result/') {
            default_view = 'cached';
        }

        var ckCurrentView = pbLib.getCookie('xadmin_feed_current.view');
        var ckCurrentLatest = pbLib.getCookie('xadmin_feed_current.latest');
        var ckCurrentOdbJob = pbLib.getCookie('xadmin_feed_current.order_by_job');
        var ckCurrentIsManual = pbLib.getCookie('xadmin_feed_current.is_manual');
        var ckCurrentOrderby = pbLib.getCookie('xadmin_feed_current.orderby');

        return {
            group: function(id, start, latest, view, orderby, order_by_job, is_manual, fn) {
                if (id === 'all') {
                    var other = $('.feed-group-link').first();
                    var url = '/';
                    if (other.length) {
                        url = other.attr('href').substr(1);
                    }
                    window.location = '#' + url;
                    return;
                }
                return $http.get('/special_feed/verify_list/' + id + '?start=' + start + '&latest=' + latest + '&orderby=' + orderby + '&order_by_job=' + order_by_job + '&is_manual=' + is_manual + '&limit=10&view=' + view + '&t=' + +new Date()).then(function(response) {
                    //return $http.get('/data/items-all.json?start=' + start + '&latest=' + latest + '&limit=9&t=' + +new Date()).then(function (response) {
                    return response.data;
                }).then(fn);
            },
            current: {
                id: '',
                view: (ckCurrentView == null) ? default_view : ckCurrentView,
                start: 0,
                latest: (ckCurrentLatest == null) ? 1 : ckCurrentLatest,
                total_count: 0,
                orderby: (ckCurrentOrderby == null) ? 'resume_update_time' : ckCurrentOrderby,
                order_by_job: (ckCurrentOdbJob == null) ? '-job_related' : ckCurrentOdbJob,
                is_manual: (ckCurrentIsManual == null) ? 'no' : ckCurrentIsManual,
                total_recommend_count: 0,
                scope: {}
            }
        };
    }
]).factory('Auto', ['$http',
    function($http) {
        return function(fn) {
            return $http.get('/resumes/all_tags').then(function(response) {
                return response.data;
            }).then(fn)
        }
    }
]);

function minusOne($elems) {
    $elems.each(function() {
        var $this = $(this);
        var count = parseInt($this.html(), 10) - 1;
        if (count <= 0)
            count = '';
        $this.html(count);
    });
}

function setNum($elems, num) {
    $elems.each(function() {
        if (num <= 0)
            num = '';
        $(this).html(num);
    });
}
feedApp.filter('gender', function() {
    return function(text) {
        return text == 'female' ? '女' : '男';
    };
}).filter("default", function() {
    return function(values, default_value) {
        return value ? value : default_value;
    }
}).filter('checkFeedOpen', function() {
    return function(input) {
        return input === 'read' ? '' : 'feed-unread';
    };
}).filter('checkFeedLatest', function() {
    return function(input) {
        return input ? 'feed-latest' : '';
    };
}).filter('searchKeyword', function() {
    return function(input) {
        return typeof(input) === 'string' ? input : '';
    };
}).filter("manual_status", function() {
    return function(item) {
        if (item.admin) {
            return item.admin;
        }
        return "";
    }
}).filter('chop', function() {
    return function(text) {
        if (text && text.length > 150) {
            text = text.substr(0, 147) + '</br>...';
        }
        return text;
    }
});
feedApp.directive('clickedit', function() {
    return {
        restrict: 'A',
        transclude: true,
        scope: true,
        template: [
            '<span ng-hide="editing" ng-transclude style="padding-right:10px;line-height:23px">',
            '<i class="prop-action" ng-click="editing=true"></i>',
            '</span>',
            '<span ng-show="editing" style="line-height:31px;display: inline-block;position:relative;top: -4px;" class="clickdit">',
            '<input autofocus type="text" list="tagHistory" ng-model="_text" style="border: 0; padding: 5px; background:f5f5f5; border: 1px solid #eee; width:100px;box-shadow: inset 0px 1px rgba(0,0,0,.1)"/>',
            //'<label style="color: #111;margin-left: 5px;">\u5e94\u7528\u5168\u90e8</label><input ng-checked="isAll(_scope)" type="checkbox" style="margin-right: 10px"/>',
            '<a href="" style="color:#111; margin-left:5px;" ng-click="ok($event)">\u786e\u5b9a</a><a href="" style="color:#111;margin-left:5px;" ng-click="cancel()">\u53d6\u6d88</a>',
            '</span>'
        ].join(''),
        link: function(scope, element, attrs) {
            scope.text = attrs.clickedit;
            //scope.scopevalue = attrs.scope;
            scope.feed_id = attrs.feed_id;
            scope.resume_id = attrs.resume_id;
        },
        controller: [
            '$scope',
            '$timeout',
            function($scope, $timeout) {
                $scope.$watch('editing', function() {
                    if ($scope.editing) {
                        $scope._text = '' //$scope.item.recommended_words[$scope.text];
                        //$scope._scope = $scope.item.recommended_words[$scope.scopevalue] || 'feed';
                    }
                });
                $scope.isAll = function(val) {
                    return $scope.isall = (val == 'resume');
                };

                $scope.ok = function($event) {
                    var input = $($event.target).parent().find('input');
                    //$scope.item.recommended_words[$scope.text] = $scope._text;
                    //$scope.item.recommended_words[$scope.scopevalue] = input.is(':checked') ? 'resume' : 'feed';
                    $scope.editing = false;
                    if (!$scope._text) {
                        return false;
                    }

                    if (!$scope.item.tags) {
                        $scope.item.tags = [];
                    }

                    for (var i = 0; i < $scope.item.tags.length; ++i) {
                        if ($scope.item.tags[i].tag.toLowerCase() == $.trim($scope._text).toLowerCase()) {
                            alert('标签已存在');
                            return false;
                        }
                    }

                    $.post('/resumes/add_tag_resume', {
                        tag_id: window.autoHistoryMap[$scope._text] || '',
                        tag: $scope._text,
                        resume_id: $scope.item.resume.id
                    }, function(ret) {
                        if (!ret) return false;
                        if (ret && ret.status == "success") {
                            $timeout(function() {
                                if (!$scope.item.tags) {
                                    $scope.item.tags = [];
                                }
                                $scope.item.tags.push({
                                    tag_id: ret.tag_id,
                                    tag: $scope._text
                                });

                                if (!window.autoHistoryMap[$scope._text]) {
                                    $scope.autoHistory.push({
                                        tag_id: ret.tag_id,
                                        tag: $scope._text
                                    });
                                }

                                window.autoHistoryMap[$scope._text] = ret.tag_id;
                                $scope._text = '';
                            });
                        } else {
                            alert('添加失败，请联系开发!');
                            $timeout(function() {
                                $scope.item.tags.pop();
                            });
                        }
                    });
                };
                $scope.cancel = function() {
                    $scope.editing = false;
                };
            }
        ]
    };
});
feedApp.directive('fixedtop', function() {
    return {
        restrict: 'A',
        link: function(scope, elem, attrs) {
            var offset = attrs.fixedtop || 0;
            var top = $(elem).offset().top;
            var $el = $(elem);
            var $win = $(window);
            var pos = $el.css('position');
            $win.on('scroll', function() {
                if ($win.scrollTop() >= top - offset) {
                    $el.css({
                        'position': 'fixed',
                        top: offset + 'px'
                    });
                } else {
                    $el.css({
                        'position': pos,
                        top: 'auto'
                    });
                }
            });
        }
    };
});
var $more = $('.load-more');
feedApp.controller('aside', [
    '$scope',
    '$location',
    function($scope, $location) {
        $scope.isActive = function(route) {
            return $location.path().indexOf(route) != -1;
        };
    }
]).controller('resumeTag', [
    '$scope',
    '$location',
    '$timeout',
    function($scope, $location, $timeout) {
        $scope.delTag = function(tag, resume_id) {
            $.post('/resumes/del_tag_resume', {
                tag_id: tag.tag_id,
                resume_id: resume_id
            }, function(ret) {
                if (ret && ret.status == "success") {
                    $timeout(function() {
                        for (var i = 0; i < $scope.item.tags.length; ++i) {
                            if ($scope.item.tags[i].tag_id == tag.tag_id) {
                                $scope.item.tags.splice(i, 1);
                            }
                        }
                    });
                } else {
                    alert('操作失败了，请联系瑶哥');
                }
            });
        }
    }
]).controller('feedApp', [
    '$scope',
    'Feed',
    'Auto',
    '$timeout',
    '$http',
    function($scope, Feed, Auto, $timeout, $http) {
        Auto(function(data) {
            $scope.autoHistory = data.data || [];
            window.autoHistoryMap = {};
            angular.forEach($scope.autoHistory, function(d) {
                window.autoHistoryMap[d.tag] = d.tag_id;
            });
        });

        //管理员发送实时推荐任务
        $scope.sendRealCo = function($event) {
            var trg = angular.element($event.target);
            trg[0].innerHTML = '<img width="15" src="/static/partner/images/loading.gif" border="0">';
            var feedid = trg.attr('data-feedid');
            //console.log('feedid2',feedid);
            var submit = getModeData($http,
                '/special_feed/admin/send_reco_task/' + feedid + '/',
                "",
                function(ret) {
                    //console.log('ret',ret);
                    if (ret.status == "ok") {
                        console.log('sendRealCo', 'ok');
                        trg[0].innerHTML = '<span style="color:#008000;">成功</span>';
                        setTimeout(function() {
                            trg[0].innerHTML = '实时推荐';
                        }, 2000);
                    } else {
                        trg[0].innerHTML = '<span style="color:#ff3000;">失败</span>';
                        setTimeout(function() {
                            trg[0].innerHTML = '实时推荐';
                        }, 2000);
                    }
                }, undefined, function(err) {
                    submit.abort();
                });
        };

        $scope.current = Feed.current;

        $scope.ckCurrentView = pbLib.getCookie('xadmin_feed_current.view');
        $scope.ckCurrentLatest = pbLib.getCookie('xadmin_feed_current.latest');
        console.log('xadmin_feed_current.latest', pbLib.getCookie('xadmin_feed_current.latest'));
        $scope.ckCurrentOdbJob = pbLib.getCookie('xadmin_feed_current.order_by_job');
        $scope.ckCurrentIsManual = pbLib.getCookie('xadmin_feed_current.is_manual');
        $scope.ckCurrentOrderby = pbLib.getCookie('xadmin_feed_current.orderby');

        var updatePage = function() {
            var link = $('.feed-nav .curr').find('a.feed-group-link');
            var href = link.attr('href') || '';
            if (href == '') {
                alert('当前定制不存在啦～');
            } else {
                window.location.replace(href.split('?')[0] + '?' + Math.random().toString(16).substr(2));
            }
        };

        $scope.toggleLatest = function($event) {
            if (!$scope.current.latest) {
                $scope.current.latest = 1;
            } else {
                $scope.current.latest = 0;
            }
            pbLib.setCookie('xadmin_feed_current.latest', $scope.current.latest, 365 * 86400);
            $scope.ckCurrentLatest = $scope.current.latest;
            setTimeout(function() {
                updatePage();
            }, 800);
        };

        $scope.toggleOrderJob = function($event) {
            if (!/^\-/.test($scope.current.order_by_job)) {
                $scope.current.order_by_job = '-job_related';
            } else {
                $scope.current.order_by_job = 'job_related';
            }
            pbLib.setCookie('xadmin_feed_current.order_by_job', $scope.current.order_by_job, 365 * 86400);
            $scope.ckCurrentOdbJob = $scope.current.order_by_job;
            setTimeout(function() {
                updatePage();
            }, 800);
        };

        $scope.toggleManual = function($event) {
            if (/^yes/.test($scope.current.is_manual)) {
                $scope.current.is_manual = 'no';
            } else {
                $scope.current.is_manual = 'yes';
            }
            pbLib.setCookie('xadmin_feed_current.is_manual', $scope.current.is_manual, 365 * 86400);
            $scope.ckCurrentIsManual = $scope.current.is_manual;
            setTimeout(function() {
                updatePage();
            }, 800);
        };

        $scope.toggleOrderby = function($event) {
            if (!/^\-/.test($scope.current.orderby)) {
                $scope.current.orderby = '-resume_update_time';
            } else {
                $scope.current.orderby = 'resume_update_time';
            }
            pbLib.setCookie('xadmin_feed_current.orderby', $scope.current.orderby, 365 * 86400);
            $scope.ckCurrentOrderby = $scope.current.orderby;
            setTimeout(function() {
                updatePage();
            }, 800);
        };

        $scope.toggleView = function(view, $event) {
            //if ($scope.current.view == view) return false;
            $scope.current.view = view || 'user';
            pbLib.setCookie('xadmin_feed_current.view', $scope.current.view, 365 * 86400);
            $scope.ckCurrentView = $scope.current.view;
            setTimeout(function() {
                updatePage();
            }, 800);
        };
        $scope.chkCurrentView = function(name) {
            if ($scope.ckCurrentView == null) {
                if ($scope.current.view == name) {
                    return true;
                }
            } else {
                if ($scope.ckCurrentView == name) {
                    return true;
                }
            }
        };
        $scope.chkCurrentSelect = function(trg, value) {
            var defaultTrg = null;
            var defaultCkTrg = null;
            if (trg == 'latest') {
                defaultTrg = $scope.current.latest;
                defaultCkTrg = $scope.ckCurrentLatest;
            } else if (trg == 'orderby') {
                defaultTrg = $scope.current.orderby;
                defaultCkTrg = $scope.ckCurrentOrderby;
            } else if (trg == 'orderby') {
                defaultTrg = $scope.current.orderby;
                defaultCkTrg = $scope.ckCurrentOrderby;
            } else if (trg == 'order_by_job') {
                defaultTrg = $scope.current.order_by_job;
                defaultCkTrg = $scope.ckCurrentOdbJob;
            } else if (trg == 'is_manual') {
                defaultTrg = $scope.current.is_manual;
                defaultCkTrg = $scope.ckCurrentIsManual;
            }
            if (defaultCkTrg == null) {
                if (defaultTrg == value) {
                    return true;
                }
            } else {
                if (defaultCkTrg == value) {
                    return true;
                }
            }
        };
        $scope.publishAll = function(idx) {
            var email = $.trim($('.feed-aside').find('h2[data-username]>span').html());
            var pub_time = $('.confirm-box').find('input[type="date"]').val() || '';
            confirmBox.hide();
            if (!email) return alert('没有获取到用户名，请联系开发');
            $.post('/special_feed/publish_feed/', {
                'username': email,
                'publish_all': true,
                'pub_time': pub_time,
                'published': true
            }, function(ret) {
                if (ret) {
                    alert(ret.msg);
                } else {
                    alert('oh no! 联系开发');
                }
            });
        };
        $scope.publishFeed = function() {
            var feed_id = $('.feed-nav').find('.curr>span').data('count-group');
            var pub_time = $('.confirm-box').find('input[type="date"]').val() || '';

            confirmBox.hide();
            var resume_ids = [];
            $('.selected-item').each(function() {
                resume_ids.push($(this).data('resume_id'));
            });
            if (!resume_ids.length) {
                return alert('请先选择要推荐的简历！');
            }
            $.post('/special_feed/publish_feed/', {
                'feed_id': feed_id,
                'pub_time': pub_time,
                'resume_ids': resume_ids,
                'published': true
            }, function(ret) {
                if (ret) {
                    alert(ret.msg);
                } else {
                    alert('oh no! 联系开发');
                }
            });
        };
    }
]).controller('feedPage', [
    '$scope',
    'Feed',
    'Auto',
    '$timeout',
    '$routeParams',
    '$rootScope',
    function($scope, Feed, Auto, $timeout, $routeParams, $rootScope) {
        Feed.current.id = $routeParams.id;
        if (Feed.current.id.match(/^([^&]+)&/i)) {
            Feed.current.id = RegExp.$1;
        }
        Feed.current.start = 0;
        Feed.current.limit = 5;

        $scope.fetch = function($event) {
            $scope.loadmore = true;
            $scope.hasmore = false;
            Feed.group(Feed.current.id, Feed.current.start, Feed.current.latest, Feed.current.view, Feed.current.orderby, Feed.current.order_by_job, Feed.current.is_manual, function(data) {
                $timeout(function() {
                    $scope.feeditems.push.apply($scope.feeditems, data.data);
                    Feed.current.start = data.next_start;
                    $scope.loadmore = false;
                    if (data.next_start != '-1') {
                        $scope.hasmore = true;
                    }
                    if ($('.feed-nav li.curr').find('.feed-latest-count').data('count-group') == 'all') {
                        return false;
                    }
                    if ($scope.current.latest) {
                        setNum($('.feed-nav li.curr').find('.feed-latest-count'), data.newest_recommend_count);
                    } else if (data.newest_recommend_count) {
                        if (_.filter(data.data || [], function(d) {
                            return !!d.latest;
                        }).length) {
                            setNum($('.feed-nav li.curr').find('.feed-latest-count'), data.newest_recommend_count);
                        }
                    }
                });
            });
        };
        $timeout(function() {
            $scope.initLoading = true;
            $scope.loadmore = false;
            $scope.hasmore = false;
            $scope.waiting = false;
        });
        if (Feed.current.id) {
            Feed.group(Feed.current.id, Feed.current.start, Feed.current.latest, Feed.current.view, Feed.current.orderby, Feed.current.order_by_job, Feed.current.is_manual, function(data) {
                $timeout(function() {
                    $scope.feeditems = data.data;
                    $scope.initLoading = false;
                    Feed.current.total_count = data.total_count;
                    Feed.current.total_recommend_count = data.total_recommend_count;
                    Feed.current.start = data.next_start;
                    if (data.next_start != '-1') {
                        $scope.hasmore = true;
                    }
                    if (!data.count || !data.data.length) {
                        $scope.waiting = true;
                        $scope.hasmore = false;
                    }
                    if ($('.feed-nav li.curr').find('.feed-latest-count').data('count-group') == 'all') {
                        return false;
                    }
                    if ($scope.current.latest) {
                        setNum($('.feed-nav li.curr').find('.feed-latest-count'), data.newest_recommend_count);
                    } else if (data.newest_recommend_count) {
                        if (_.filter(data.data || [], function(d) {
                            return !!d.latest;
                        }).length) {
                            setNum($('.feed-nav li.curr').find('.feed-latest-count'), data.newest_recommend_count);
                        }
                    }
                });
            });
        }

        $scope.openFeed = function(idx, group) {};
        $scope.dislike = function(idx) {
            $.get('/feed/modify_feed_result', {
                feed_id: $scope.feeditems[idx].feed.id,
                resume_id: $scope.feeditems[idx].resume.id,
                reco_index: '-100'
            });
            $timeout(function() {
                $scope.feeditems[idx].dislike = true;
                $scope.feeditems[idx].latest = false;
                $scope.feeditems[idx].opened = true;
            });
        };

        $scope.adminVote = function(idx, $event) {
            var $elem = $($event.target);
            if ($('.preview-info-default').length) {
                $('.preview-info-default').remove();
            };

            if ($('.preview-info-default').length) {
                $('.preview-info-default').remove();
            }
            $elem.parent().addClass('control-pending');
            if ($elem.parent().hasClass('control-voted')) {
                $.get('/feed/modify_feed_result', {
                    feed_id: $scope.feeditems[idx].feed.id,
                    resume_id: $scope.feeditems[idx].resume.id,
                    reco_index: '-150'
                }, function() {
                    $elem.parent().removeClass('control-pending').removeClass('control-voted');
                });
            } else {
                $.get('/feed/modify_feed_result', {
                    feed_id: $scope.feeditems[idx].feed.id,
                    resume_id: $scope.feeditems[idx].resume.id,
                    reco_index: '150'
                }, function() {
                    $elem.parent().removeClass('control-pending').addClass('control-voted');
                });
            }
        };

        var array_deal = function(array, match) {
            for (var i = 0, imax = array.length; i < imax; i++) {
                if (array[i] == match) {
                    array.splice(i, 1);
                    break;
                };
            };
        };

        $scope.adminBlock = function(idx, $event) {

        };

        $scope.hoverBlock = function(idx, $event) {
            var $elem = $($event.target);
            var html_suit = '<div class="admin-custom-control-public admin-custom-control-refuse"><p>告诉我们不准的原因，下次会更准哦～</p><div class="clearfix js-choose-box"><a href="javascript:void(0)" data_conflict="0" data-value="salary_high">薪资偏高</a><a href="javascript:void(0)" data_conflict="0" data-value="salary_low">薪资偏低</a><a href="javascript:void(0)" data_conflict="1" data-value="level_low" class="admin-custom-control-margin">级别太低</a><a href="javascript:void(0)" data_conflict="1" data-value="level_high" class="admin-custom-control-margin">级别太高</a></div><p>还可以选择其他原因(可多选):</p><div class="clearfix js-choose-box"><a href="javascript:void(0)" data_conflict="2" data-value="degree_high">学历太高</a><a href="javascript:void(0)" data_conflict="2" data-value="degree_low">学历太低</a><a href="javascript:void(0)" data-value="title_not_match">职位名称不符</a><a href="javascript:void(0)" data-value="industry_not_match">行业不准</a><a href="javascript:void(0)" class="admin-custom-control-submit js-vote-submit">一键屏蔽</a></div><div class="admin-custom-control-opacity"></div></div>';
            var suit_array = [];
            var parent = $elem.parents('.item-footer');
            if ($('.admin-custom-control-refuse', parent).length == 0) {
                parent.append(html_suit);
                $('.admin-custom-control-refuse', parent).on('mouseleave', function() {
                    $('.admin-custom-control-refuse', parent).remove();
                });
                $('.admin-custom-control-suit').remove();
                $('.js-choose-box a').not($('.js-vote-submit')).on('click', function() {
                    var data_value = $(this).attr('data-value');
                    var data_conflict = $(this).attr('data_conflict');
                    if (!$(this).hasClass('admin-custom-control-choose')) {
                        var data_conflict_same = 'a[data_conflict="' + data_conflict + '"]';
                        var data_conflict_same_value_one = $(data_conflict_same).eq(0).attr('data-value');
                        var data_conflict_same_value_two = $(data_conflict_same).eq(1).attr('data-value');
                        $(data_conflict_same).removeClass('admin-custom-control-choose');
                        $(this).addClass('admin-custom-control-choose');
                        $('.js-vote-submit').text('提交');
                        array_deal(suit_array, data_conflict_same_value_one);
                        array_deal(suit_array, data_conflict_same_value_two);
                        suit_array.push(data_value);
                    } else {
                        $(this).removeClass('admin-custom-control-choose');
                        array_deal(suit_array, data_value);
                        if (suit_array.length <= 0) {
                            $('.js-vote-submit').text('一键屏蔽');
                        }
                    };
                });
                $('.js-vote-submit').on('click', function() {
                    var feed_id = $elem.attr('feed-id');
                    var resume_id = $elem.attr('resume-id');
                    var index_id = $elem.attr('index-id');
                    $.get('/feed/modify_feed_result', {
                        feed_id: feed_id,
                        resume_id: resume_id,
                        reco_index: '-100',
                        feedback: suit_array
                    }, function() {
                        $elem.parent().removeClass('control-pending').addClass('control-voted');
                        $('.admin-custom-control-suit').remove();
                        $elem.parent().removeClass('control-pending');
                        $elem.parents('.feed-item').addClass('shrink');
                        setTimeout(function() {
                            var feed_item_parent = '.feed-item-' + index_id;
                            $(feed_item_parent).remove();
                            if ($('.feed-item').length <= 0) {
                                $('.feed-waiting').show();
                            }
                        }, 400);
                    });
                });
            } else {
                $('.admin-custom-control-refuse', parent).show();
            };
            if ($('.preview-info-default').length) {
                $('.preview-info-default').remove();
            };
        };
    }
]);
$(function() {
    var $submitForm = $('#feed-submit-form');
    $submitForm.find('.options').each(function() {
        var $options = $(this);
        var name = $options.data('name');
        var input = $('input[name="' + name + '"]');
        $options.parent().find('span').on('click', function() {
            if ($options.hasClass('op-multi')) {
                $(this).toggleClass('selected');
            } else if ($options.hasClass('op-single')) {
                $(this).parents('li').find('.selected').removeClass('selected');
                $(this).addClass('selected');
            }
            input.val($options.parent().find('.selected').map(function() {
                return $.trim($(this).html());
            }).toArray().join(','));
        });
    });
    $('.select-btn-more>a').on('click', function(e) {
        e.preventDefault();
        var $a = $(this);
        $('.select-expect-area').toggleClass('expect-area-span').find('.op-multi').slideToggle(200);
        var text = $.trim($a.html());
        $a.html($a.data('text-span'));
        $a.data('text-span', text);
    });
    $('a[href^="/feed/delete"]').on('click', function(e) {
        var choice = window.confirm('\u5220\u9664\u8ba2\u9605\u6761\u4ef6\u5c06\u6e05\u9664\u6b64\u8ba2\u9605\u4e0b\u7684\u6240\u6709\u7b80\u5386\uff01\u662f\u5426\u7ee7\u7eed\uff1f');
        if (!choice)
            return false;
    });
    $('#give-me-feed').on('click', function() {
        $submitForm.submit();
    });
    $('.feed-edit-jd >form').on('submit', function(e) {
        e.preventDefault();
        var $form = $(this);
        var action = $form.attr('action');
        var job_desc = $form.find('textarea[name="job_desc"]').val();
        if (job_desc == window.feed_edit_jd_old) {
            $form.find('textarea[name="job_desc"]').focus();
            return false;
        }
        var $btn = $form.find('button[type="submit"]').html('\u6b63\u5728\u4fdd\u5b58');
        $btn.addClass('submitting');
        $.post(action, {
            job_desc: job_desc
        }, function(ret) {
            $btn.removeClass('submitting');
            $btn.html('\u4fdd\u5b58');
            if (ret && ret.status) {
                window.feed_edit_jd_old = job_desc;
                $btn.prev().remove();
                $('<span style="margin-right: 10px; color:green;">\u5df2\u4fdd\u5b58!</span>').insertBefore($btn).fadeOut(1500, function() {
                    $(this).remove();
                });
            } else {
                $btn.prev().remove();
                $('<span style="margin-right: 10px; color:red;">\u4fdd\u5b58\u5931\u8d25\uff0c\u8bf7\u91cd\u8bd5!</span>').insertBefore($btn).fadeOut(3000, function() {
                    $(this).remove();
                });
            }
        });
    });
    var hovertimer;
    $('body').on('mouseover', '.resume-tags-hook', function() {
        clearTimeout(hovertimer);
        $(this).parents('.item-header').find('.item-action-keywords').fadeIn();
    }).on('mouseout', '.resume-tags-hook, .item-action-keywords', function() {
        hovertimer = setTimeout(function() {
            $('.item-action-keywords').hide();
        }, 400);
    }).on('mouseover', '.item-action-keywords', function() {
        clearTimeout(hovertimer);
    });

    ;
    (function() {
        var $doc = $(document);
        var times = 0;
        $(window).on('scroll', function() {
            var more = $('a[ng-show="hasmore"]');
            if (!more.is(':hidden')) {
                var offset = $doc.height() - $doc.scrollTop() - $(window).height();
                if (offset < 100) {
                    more.get(0).click();
                }
            }
        });
    }());


    $('.btn-unselect').on('click', function() {
        $(this).parent().find('input').val(0);
        $('.selected-item').removeClass('selected-item');
        $('.selectBox').removeAttr('checked');
    });

    $('.sub-control input[type="number"]').on('change', function(e) {
        var num = parseInt($(this).val(), 10);
        $('.selected-item').removeClass('selected-item');
        $('.feed-item').each(function(idx, el) {
            if (idx < num) {
                $(this).addClass('selected-item');
                $(this).find('.selectBox').attr('checked', 'checked');
            }
        });
    });

    $('.toggleConfirm').on('click', function() {
        var type = $(this).data('type');
        confirmBox.toggle(type);
    });
    $("body").on('change', '.selectBox', function() {
        $(this).parents('.feed-item').toggleClass('selected-item');
    });

    $('.js-choose-box').undelegate('a').delegate('a', 'click', function() {});

    $('.js-choose-box').click(function() {
        var _this = $(this);
        var suit_array = [],
            refuse_array = [];

        if (_this.closest('div.admin-custom-control-public').hasClass('admin-custom-control-suit')) {
            if (!_this.hasClass('admin-custom-control-choose')) {
                _this.addClass('admin-custom-control-choose')
            }
        }
    });




});