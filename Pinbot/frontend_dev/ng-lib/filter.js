(function() {
    var app = angular.module('app.filter', []);

    app.filter('as_html', ['$sce',
        function($sce) {
            return function(text) {
                if (!text) return '';
                var safe_text = text.replace(/<script>/g, '').replace(/<script \/>/g, '').replace(/\r\n/g, '<br>').replace(/\n/g, '<br>')
                return $sce.trustAsHtml(safe_text);
            };
        }
    ]);

    app.filter('moneyFilter', function() {
        return function(i) {
            return parseInt(i / 1000);
        };
    });

    app.filter('formatMoney', function() {
        return function(min, max) {
            var txt = '',
                m = 1000000,
                filterFun = function(i) {
                    return parseInt(i / 1000);
                };
            if ((min == 0 && max == m) || (min == 0 && max == 0)) {
                txt = '面议';
            } else if (min > 0 && max == m) {
                txt = (filterFun(min)) + 'K以上';
            } else if (min > 0 && max < m) {
                txt = (filterFun(min)) + 'K - ' + (filterFun(max)) + 'K';
            } else if (min == 0 && max < m) {
                txt = (filterFun(max)) + 'K以下';
            } else {
                txt = '面议';
            };
            return txt;
        };
    });

    app.filter('filterYear', function() {
        return function(i) {
            var str = '';
            str = i ? i + '年工作经验' : '经验不限';
            return str;
        };
    });

    app.filter('filterDegree', function() {
        return function(i) {
            var obj = {
                0: '不限',
                3: '大专',
                4: '本科',
                7: '硕士',
                10: '博士'
            };
            return obj[i];
        };
    });

    app.filter('textSendStatus', function() {
        return function(str) {
            return {
                waiting: '等待企业反馈',
                download: '面试邀请中',
                no_reply: '企业无回复',
                unfit: '不合适'
            }[str];
        };
    });

    app.filter('textCardStatus', function() {
        return function(str) {
            return {
                waiting: '等待你的反馈',
                accept: '面试邀请中',
                reject: '已拒绝该企业',
                expire: '职位已过期',
                chat_expire: '会话已过期'
            }[str];
        };
    });

    app.filter('formartJobCategory', function() {
        return function(list) {
            var arr = [];
            for (var i = 0, l = list.length; i < l; i++) {
                arr.push('#' + list[i] + '#');
            };
            return arr.join('  ');
        };
    });

    //格式化任务领域
    app.filter('formatTaskDomain', function() {
        return function(job_domain, task_domain) {
            var arrLight = [],
                arrDedault = [],
                job_domain = job_domain || [],
                task_domain = task_domain || [];

            //如果没有设置领域就默认返回职位领域集合
            if (!task_domain.length && job_domain.length) {
                return job_domain.join(',');
            };

            //如果有，则检索出相同的领域，高亮，剩下的排后面
            for (var i = 0, l = job_domain.length; i < l; i++) {

                var jd = job_domain[i],
                    isIn = false;

                for (var j = 0, jj = task_domain.length; j < jj; j++) {
                    var td = task_domain[j];
                    if (td == jd) {
                        isIn = true;
                        break;
                    };
                };

                if (isIn) {
                    arrLight.push('<span class="task-area">' + jd + '</span>');
                } else {
                    arrDedault.push('<span class="task-area-default">' + jd + '</span>');
                };

            };

            return arrLight.join() + (arrDedault.length && arrLight.length ? '，' : '') + arrDedault.join(',');

        };
    });

    app.filter('mergeCity', function() {
        return function(arr) {
            var newArr = [];
            for (var i = 0, l = arr.length; i < l; i++) {
                newArr.push(arr[i].name);
            };
            return newArr.join(',');
        };
    });

    app.filter('joinCity', function() {
        return function(arr) {
            return arr.join(',');
        };
    });

    app.filter('joinCat', function() {
        return function(arr) {
            if (!arr || !arr.length) return '';
            var newArr = [];
            for (var i = 0, l = arr.length; i < l; i++) {
                newArr.push(arr[i].category);
            };
            return newArr.join(',');
        };
    });

    //格式化月薪范围
    app.filter('mode_salary_range', function($sce) {
        //"5,20"
        return function(salary_str) {
            if (typeof salary_str != "string") salary_str = "";
            if (salary_str.match(/([0-9]+),([0-9]+)/i)) {
                var min = RegExp.$1;
                var max = RegExp.$2;
                if(parseInt(max)>=100){
                    return min + "K 以上";
                }else{
                    return min + "~" + max + "K";
                }
            }
            return "";
        }
    });






})();