//分页插件
/**
2014-08-05 ch
**/
(function($) {
    var ms = {
        init: function(obj, args) {
            return (function() {
                ms.fillHtml(obj, args);
                ms.bindEvent(obj, args);
            })();
        },
        //填充切换样式
        fillHtml: function(obj, args) {
            return (function() {
                obj.empty();
                if (args.pageCount > 1) {
                    var pageStr = '';
                    if (args.current > 1) {
                        pageStr += ('<a href="javascript:;" class="prev-page noselect">&nbsp;</a>');
                    } else {
                        pageStr += ('<a class="prev-page-disabled noselect">&nbsp;</a>');
                    }
                    if (args.current != 1 && args.current >= 4 && args.pageCount != 4) {
                        pageStr += ('<a href="javascript:;" class="page-num noselect">' + 1 + '</a>');
                    }
                    if (args.current - 2 > 2 && args.current <= args.pageCount && args.pageCount > 5) {
                        pageStr += ('<span>...</span>');
                    }
                    var start = args.current - 2,
                        end = args.current + 2;
                    if ((start > 1 && args.current < 4) || args.current == 1) {
                        end++;
                    }
                    if (args.current > args.pageCount - 4 && args.current >= args.pageCount) {
                        start--;
                    }
                    for (; start <= end; start++) {
                        if (start <= args.pageCount && start >= 1) {
                            if (start != args.current) {
                                pageStr += ('<a href="javascript:;" class="page-num noselect">' + start + '</a>');
                            } else {
                                pageStr += ('<span class="current">' + start + '</span>');
                            }
                        }
                    }
                    if (args.current + 2 < args.pageCount - 1 && args.current >= 1 && args.pageCount > 5) {
                        pageStr += ('<span>...</span>');
                    }
                    if (args.current != args.pageCount && args.current < args.pageCount - 2 && args.pageCount != 4) {
                        pageStr += ('<a href="javascript:;" class="page-num noselect">' + args.pageCount + '</a>');
                    }

                    if (args.current < args.pageCount) {
                        pageStr += ('<a href="javascript:;" class="next-page noselect">&nbsp;</a>');
                    } else {
                        pageStr += ('<a class="next-page-disabled noselect">&nbsp;</a>');
                    }
                    obj.append(pageStr);
                }

            })();
        },
        //添加事件
        bindEvent: function(obj, args) {
            return (function() {
                obj.off('click', "a.page-num");
                obj.on("click", "a.page-num", function() {
                    var current = parseInt($(this).text());
                    ms.fillHtml(obj, {
                        "current": current,
                        "pageCount": args.pageCount
                    });
                    if (typeof(args.backFn) == "function") {
                        args.backFn(current);
                    }
                });
                obj.off('click', "a.prev-page");
                obj.on("click", "a.prev-page", function() {
                    var current = parseInt(obj.children("span.current").text());
                    ms.fillHtml(obj, {
                        "current": current - 1,
                        "pageCount": args.pageCount
                    });
                    if (typeof(args.backFn) == "function") {
                        args.backFn(current - 1);
                    }
                });
                obj.off('click', "a.next-page");
                obj.on("click", "a.next-page", function() {
                    var current = parseInt(obj.children("span.current").text());
                    ms.fillHtml(obj, {
                        "current": current + 1,
                        "pageCount": args.pageCount
                    });
                    if (typeof(args.backFn) == "function") {
                        args.backFn(current + 1);
                    }
                });
            })();
        }
    }
    $.fn.createPage = function(options) {
        var args = $.extend({
            pageCount: 1,
            current: 1,
            backFn: function() {}
        }, options);
        ms.init(this, args);
    }
})(jQuery);

//本地存储
function setLocalData(storageKey, storageValue) {
    //if (pbDebug) console.log('setLocalData', storageKey);
    try {
        window.localStorage.setItem(storageKey, JSON.stringify(storageValue));
        return true;
    } catch (localStorageError) {
        console.log('Storage数据失败! [' + localStorageError.toString() + ']');
        return false;
    }
    //return false;
}
//获取本地存储数据
function getLocalData(storageKey) {
    //if (pbDebug) console.log('getLocalData', storageKey);
    try {
        if (storageKey in window.localStorage) {
            return $.parseJSON(window.localStorage.getItem(storageKey));
        }
    } catch (localStorageError) {
        //if (isLoging) throw new Error('Storage数据失败! [' + localStorageError.toString() + ']');
        return false;
    }
    //return null;
}
//删除本地存储数据
function delLocalData(storageKey, cb) {
    //if (pbDebug) console.log('delLocalData', storageKey);
    try {
        if (storageKey in window.localStorage) {
            window.localStorage.removeItem(storageKey);
            if (typeof cb == 'function') {
                cb();
            }
        } else if (storageKey in localStorage) {
            localStorage.removeItem(storageKey);
            if (typeof cb == 'function') {
                cb();
            }
        } else {
            localStorage.removeItem(storageKey);
            if (typeof cb == 'function') {
                cb();
            }
        }
    } catch (localStorageError) {
        //if (isLoging) throw new Error('Storage数据失败! [' + localStorageError.toString() + ']');
        //return false;
    }
}
//页面加载开始，发送请求是否有完成任务的状态。
function getTaskState() {
    $.ajax({
        url: '/task/task_status/',
        type: 'get',
        datatype: 'json',
        success: function(data) {
            if ((data.status == "ok") && (data.msg == 'reward_to_receive')) {
                $('#js-task-state').removeClass('task-state-undo').addClass('task-state-finish');
            };
            if (data.status == "ok" && data.msg == 'task_to_do') {
                $('#js-task-state').removeClass('task-state-finish').addClass('task-state-undo');
            };
            if (data.status == 'ok' && data.msg == 'all_finished') {
                $('#js-task-state').removeClass('task-state-finish').addClass('task-state-all-finish');
            };
        }
    })
};
//显示清除loading.gif
function showLoading(obj, loadingState) {
    if (!loadingState) {
        $(obj).append('<span class="data-loading"></span>');
    } else {
        $(obj).find('span.data-loading').remove();
    }
};

//获取任务数据
function getTaskData() {
    var taskNum = 5; //一页里面装多少个任务
    var loadingState = false;
    $('.black-bg,#js-task-content').show();
    showLoading('#js-task-content',loadingState);
    $.ajax({
        url: '/task/',
        type: 'get',
        datatype: 'json',
        success: function(data) {
            if (data.status == 'ok') {
                fillSpeaker(data);
                growTaskHtml(1, 5, data);
                //生成分页
                $(".js-task-page").createPage({
                    pageCount: Math.ceil(data.task_count / taskNum),
                    current: 1,
                    backFn: function(p) {
                        var loadingState = false;
                        showLoading('#js-all-task',loadingState);
                        growTaskHtml(p, 5, data);
                    }
                });
            }
        }
    })
}
var ualert = 0;
var urgent_alert = document.getElementById('urgent_alert');
if(urgent_alert != null){
    setInterval(function(){
        urgent_alert.style.left = ualert + 'px';
        ualert -= 1;
        if (ualert < -1600) {
            ualert = 500;
        }
    }, 20);
}

//填充任务系统获奖信息
function fillSpeaker(data) {
    var speakerHtml = '';
    var speakerData = data.recent;
    for (var i = 0; i < speakerData.length; i++) {
        speakerHtml += '<li>' + speakerData[i] + '</li>'
    }
    $('.js-speaker').empty().append(speakerHtml);
}
// 滚动获奖信息
function AutoScroll(obj, liHeight) {
    if ($(obj).find("li").length > 1) {
        $(obj).find("ul:first").animate({
            marginTop: liHeight
        }, 500, function() {
            $(this).css({
                marginTop: "0px"
            }).find("li:first").appendTo(this);
        });
    };
};
//渲染一级页面模版
function growTaskHtml(p, liNum, data) {
    var allTaskHtml = '<li><div class="task-name-title float-left task-name-title-public align-left">任务名称</div><div class="task-number-title float-left task-name-title-public">完成度</div><div class="task-gift-title float-left task-name-title-public">奖励</div></li>';
    var taskData = data;
    var rewardData = getLocalData('rewardData');
    var forLength = 0;

    if (liNum * p <= taskData.data.length) {
        forLength = liNum * p;
    } else {
        forLength = taskData.data.length;
    };
    for (var i = liNum * (p - 1); i < forLength; i++) {
        var taskType = '';
        if (taskData.data[i].task_type == 1) {
            taskType += '【新手】';
        };
        allTaskHtml += '<li class="task-one" reward-type="' + taskData.data[i].reward_type + '"><div class="task-name float-left align-left"><a><em>' + taskData.data[i].task_name + '</em><span class="cf76a58">' + taskType + '</span></a><span class="task-descript">' + taskData.data[i].description + '<em></em></span></div><div class="task-number float-left"><span>' + taskData.data[i].current_process + '</span>/' + taskData.data[i].task_count + '</div><p class="task-gift float-left">' + taskData.data[i].task_reward + '</p>';

        if (taskData.data[i].finished_status == 3) {
            allTaskHtml += '<a class="task-go float-left bcF76A58 js-receiv-reward" href="javascript:void(0)" reward-type="' + taskData.data[i].reward_type + '" task-code="' + taskData.data[i].task_code + '">领取奖励</a></li>';
        } else if (taskData.data[i].finished_status == 1) {
            allTaskHtml += '<a class="task-go float-left bcCFD8DD" href="javascript:void(0)">已完成</a></li>';
        } else if (taskData.data[i].finished_status == 2) {
            allTaskHtml += '<a class="task-go float-left bcffd254 js-to-do-task" href="javascript:void(0);" data-href="' + taskData.data[i].task_url + '" >前往任务</a></li>';
        };
    }
    $('#js-all-task').empty().append(allTaskHtml);
    loadingState = true;
    showLoading('#js-task-content',loadingState);
    $('.task-one').delegate('a.js-to-do-task', 'click', function() {
        $('.task-contain').hide();
        $('.black-bg').hide();
        var data_href = $(this).attr('data-href');
        window.location.href = data_href;
    })
    showDescript();
    receivReward();
};
//获取奖品数据
function getRewardData() {
    var taskNum = 5; //一页里面装多少个任务
    var loadingState = false;
    showLoading('#js-my-reward',loadingState);
    $.ajax({
        url: '/task/finished/',
        type: 'get',
        datatype: 'json',
        success: function(data) {
            if (data.status == 'ok') {
                //生成分页
                growRewardHtml(1, 5, data);
                $(".js-reward-page").createPage({
                    pageCount: Math.ceil(data.finished_count / taskNum),
                    current: 1,
                    backFn: function(p) {
                        var loadingState = false;
                        showLoading('#js-my-reward',loadingState);
                        growRewardHtml(p, 5, data);
                    }
                });
            }
        }
    })
}
// 处理时间
function dealDate(now) {
    var time = new Date(now);
    var year = time.getFullYear().toString();
    var month = (time.getMonth() + 1).toString();
    var date = time.getDate().toString();
    if (month.length == 1) {
        month = '0' + month;
    };
    if (date.length == 1) {
        date = '0' + date;
    }
    return year.toString() + '-' + month.toString() + '-' + date.toString();
}

function growRewardHtml(p, liNum, data) {
    var myRewardHtml = '';
    var rewardData = data;
    var forLength = 0;
    if (liNum * p <= rewardData.data.length) {
        forLength = liNum * p;
    } else {
        forLength = rewardData.data.length;
    };
    if ((rewardData.data.length < 1) || (rewardData.data.length == null)) {
        myRewardHtml += '<li><div class="gift-null"><div class="gift-instrction">你还没有获得任何奖品哦<br>快去<a href="javascript:void(0)" class="c44b5e8" id="js-turn-to-task">所有任务</a>中和我一起做任务吧!</div></div></li>';
    } else {
        var myRewardHtml = '<li><div class="task-gift-name float-left task-name-title-public align-left">任务名称</div><div class="task-gift-gift float-left task-name-title-public">奖品</div><div class="task-time-gift float-left task-name-title-public">领取时间</div><div class="task-time-gift float-left task-name-title-public">使用时间</div><div class="task-time-gift float-left task-name-title-public">过期时间</div></li>';
        for (var i = liNum * (p - 1); i < forLength; i++) {
            var taskType = '';
            var reward_time = rewardData.data[i].reward_time;
            var coupon_used_time = rewardData.data[i].coupon_used_time;
            var reward_due_time = rewardData.data[i].reward_due_time;

            if (reward_time == null) {
                reward_time = '-';
            } else {
                reward_time = dealDate(parseInt(reward_time.$date));
            };
            if (coupon_used_time == null) {
                coupon_used_time = '-';
            } else {
                coupon_used_time = dealDate(coupon_used_time.$date);
            };
            if (reward_due_time == null) {
                reward_due_time = '-';
            } else {
                reward_due_time = dealDate(reward_due_time.$date);
            };
            if (rewardData.data[i].task_type == 1) {
                taskType += '【新手】';
            };
            myRewardHtml += '<li class="task-one"><div class="task-gift-name task-name float-left align-left"><a><em>' + rewardData.data[i].task_name + '</em><span class="cf76a58">' + taskType + '</span></a><span class="task-descript">' + rewardData.data[i].description + '<em></em></span></div><p class="task-gift-gift task-gift float-left">' + rewardData.data[i].task_reward + '</p><p class="task-time-gift float-left c999999">' + reward_time + '</p><p class="task-time-gift float-left c999999">' + coupon_used_time + '</p><p class="task-time-gift float-left cf76a58">' + reward_due_time + '</p></li>';
        }
    }
    $('#js-my-reward').empty().append(myRewardHtml);
    loadingState = true;
    showLoading('#js-task-content', loadingState);
    $('.gift-instrction').delegate('a#js-turn-to-task', 'click', function() {
        $('.js-my-gift').removeClass('task-tab-current').siblings('a').addClass('task-tab-current')
        $('.task-slide-contain').hide().eq(0).show();

    });
    showDescript();
}

//鼠标到达任务名称时，出现任务描述
function showDescript() {
    $('.task-name').delegate('a', 'mouseover', function() {
        $('.task-descript').hide();
        $(this).siblings('.task-descript').fadeIn(300);
        $('.task-descript').on('mouseout', function() {
            $(this).hide();
        })
    });
}
var reward = [{
    taskType: 1,
    templateClass: 'gift-pindian'
}, {
    taskType: 2,
    templateClass: 'gift-gold'
}, {
    taskType: 3,
    templateClass: 'gift-juan'
}, {
    taskType: 4,
    templateClass: 'gift-hongbao',
    templateClass_error: 'gift-hongbao-error'
}, {
    taskType: 5,
    templateClass: 'gift-real-gift'
}];

//领取奖励
var getCookie = function(key) {
    var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
    return keyValue ? keyValue[2] : null;
}

function receivReward() {
    $('.task-one').delegate('a.js-receiv-reward', 'click', function() {
        var _this = $(this);
        var rewardType = _this.attr('reward-type');
        var task_code = _this.attr('task-code');
        var task_reward = _this.siblings('.task-gift').text();
        var loadingState = false;
        showLoading('#js-all-task',loadingState);
        if (rewardType == 5) {
            var templateClass = "." + reward[4].templateClass;
            $('#js-task-content').hide();
            $('#js-reward-content').show();
            $(templateClass).show().siblings().hide();
            $('.js-task-reward').text(task_reward);
            getAdress();
            submitAddress(task_code);
        } else if (rewardType != 5) {
            receiveAjax(task_code, rewardType, task_reward);
        }
    });
}

function receiveAjax(task_code, rewardType, task_reward) {
    $.ajax({
        url: '/task/receive_reward/',
        type: 'POST',
        datatype: 'json',
        data: {
            'task_data': task_code
        },
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        success: function(data) {
            var loadingState = true;
            showLoading('#js-all-task',loadingState);
            $('#js-task-content').hide();
            $('#js-reward-content').show();
            if (data.status == "ok") {
                for (var i = 0, rewardLength = reward.length; i < rewardLength; i++) {
                    if (rewardType == reward[i].taskType) {
                        var templateClass = "." + reward[i].templateClass;
                        $(templateClass).show().siblings().hide();
                        $('.js-task-reward').text(task_reward);
                        break;
                    }
                }
            } else if ((data.status == "error") && (data.msg == 'weixin bind required')) {
                var templateClass = "." + reward[3].templateClass_error;
                $(templateClass).show().siblings().hide();
                $('.js-task-reward').text(task_reward);
            }
        }
    });

};
getTaskState();
//弹框位置
var windowWidth = $(window).width();
var windowHeight = $(window).height();
$('#js-task-content,#js-reward-content').css({
    'left': (windowWidth - 600) / 2,
    'top': (windowHeight - 550) / 2
});
$('.js-task-tip-contain').css({
    'left': (windowWidth - 600) / 2,
    'top': (windowHeight - 400) / 2
})
$('.task-close-tip').css({
        'left': (windowWidth - 600) / 2,
        'top': (windowHeight - 200) / 2
    })
    //控制小机器人的位置
if (window.location.href.match('feed/feedFrequency')) {
    var stateHtml = '<div class="task-state-parent"><div class="task-state task-state-undo bd-trace" id="js-task-state" trace-title="任务系统"></div></div>';
    var taskStateLeft = ((windowWidth - 1140) / 2 + 160) + 'px';
    $('#js-task-state').remove();
    $('body').append(stateHtml);
    $('#js-task-state').css('right', taskStateLeft);
} else {
    var taskStateLeft = ((windowWidth - 1140) / 2 + 160) + 'px';
    $('#js-task-state').css('right', taskStateLeft);
}
//点击页面顶部，弹出任务系统
$('.task-state-parent').delegate('div.task-state', 'click', function() {
    setLocalData('task_tip', 'ture');
    getTaskData();
});
//关闭任务系统
function closeTask() {
    var noTip = getLocalData('no-tip');
    if ($('#js-task-tip').css('display') == 'block') {
        $('#js-task-tip').hide();
        $('.task-close-tip').show();
    };
    if (($('#js-task-content').css('display') == 'block') || ($('#js-reward-content').css('display') == 'block')) {
        if (!noTip) {
            $('.task-contain').hide();
            $('.task-close-tip').show();
        } else if (noTip) {
            $('.task-contain').hide();
            $('.black-bg').hide();
        }
    };
};
$('.black-bg').on('click', function() {
    closeTask();
});
$('.js-close-task').click(function() {
    closeTask();
});

$('.task-start-confirm,.js-close-task-tip').click(function() {
    setLocalData('no-tip', 'ture');
    $('.task-close-tip').hide();
    $('.black-bg').hide();
});


//滚动显示中奖用户
setInterval('AutoScroll(".task-notice-one","-32px")', 3000);
setInterval('AutoScroll(".task-notice-two","-32px")', 3000);
setInterval('AutoScroll(".task-notice-three","-32px")', 3000);
//左右切换
$('.task-tab a').click(function() {
    var tabIndex = $(this).index();
    $(this).addClass('task-tab-current').siblings('a').removeClass('task-tab-current');
    $('.task-slide-contain').hide().eq(tabIndex).show();
    if ($(this).hasClass('js-my-gift')) {
        getRewardData();
    }
})

$('.js-task-return').click(function() {
    if ($('.gift-real-gift').css('display') == 'block') {
        $('#js-task-content').show();
        $('#js-reward-content').hide();
    } else {
        $('#js-task-content').show();
        $('#js-reward-content').hide();
        getTaskData();
        getTaskState();
    }
});
$('.js-confirm').click(function() {
    $('#js-task-content').show();
    $('#js-reward-content').hide();
    getTaskData();
    getTaskState();
})

//获取地址
function getAdress() {
    $.ajax({
        url: '/task/address/',
        type: 'get',
        datatype: 'json',
        success: function(data) {
            $('#js-task-reward-name').prop('value', data.name);
            $('#js-task-provice').prop('value', data.province);
            $('#js-task-city').prop('value', data.city);
            $('#js-task-street').prop('value', data.city);
        }
    });
}
//提交地址
function submitAddress(task_code) {
    $('#js-submit-task-form').click(function() {
        var name = $('#js-task-reward-name').prop('value');
        var province = $('#js-task-provice').prop('value');
        var city = $('#js-task-city').prop('value');
        var street = $('#js-task-street').prop('value');
        var submitState = true;
        if (name.length == 0) {
            $('#js-task-reward-name').siblings('span.task-error-tip').show();
            submitState = false;
        };
        if (province.length == 0 || city.length == 0) {
            $('#js-task-city').siblings('span.task-error-tip').show();
            submitState = false;
        };
        if (street.length == 0) {
            $('#js-task-street').siblings('span.task-error-tip').show();
            submitState = false;
        };
        if (submitState) {
            var loadingState = false;
            showLoading('.gift-real-gift',loadingState);
            $.ajax({
                url: '/task/address/',
                type: 'POST',
                datatype: 'json',
                data: {
                    'name': name,
                    'province': province,
                    'city': city,
                    'street': street
                },
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                },
                success: function(data) {
                    if (data.status == 'ok') {
                        var loadingState = true;
                        showLoading('.gift-real-gift',loadingState);
                        $('.submit-sucess').show();
                        $('.gift-real-gift').hide();
                        $.ajax({
                            url: '/task/receive_reward/',
                            type: 'POST',
                            datatype: 'json',
                            data: {
                                'task_data': task_code
                            },
                            headers: {
                                "X-CSRFToken": getCookie('csrftoken')
                            },
                            success: function(data) {}
                        });
                    }
                }
            });
        }
    });
}

;
(function() {
    var taskTip = getLocalData('task_tip');
    //delLocalData('task_tip');
    if (!taskTip) {
        $('.js-task-tip-contain').show();
        $('.black-bg').show();
        $.ajax({
            url: '/task/',
            type: 'get',
            datatype: 'json',
            success: function(data) {
                if (data.status == 'ok') {
                    fillSpeaker(data);
                }
            }
        })
        $('.js-start-task').click(function() {
            setLocalData('task_tip', 'ture');
            $('.js-task-tip-contain').hide();
            $('#js-task-content').show();
            getTaskData();
        })
    }
})();