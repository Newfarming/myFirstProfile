$.Health = (function( $ , undefined ){
    if( !$ ) return;

    var health = function( setting ){
        return new health.prototype.init( setting );
    };

    health.prototype = {
        constructor: health,
        init: function( setting ) {
            this.setting = $.extend({
                triggerSelector: '#JS_trigger_health',
                contentSelector: '#JS_health_content',
                loadingSelector: '#loading',
                url: '/partner/level_state/',
                data: {
                    download_level: {
                        bonus_coin: 0,
                        exp: 0,
                        is_max_level: false,
                        level: 1,
                        level_type: 0,
                        next_bonus_coin: 4,
                        next_exp: 10,
                        next_level: 2,
                        user_exp: 0
                    },
                    interview_level: {
                        bonus_coin: 0,
                        exp: 0,
                        is_max_level: false,
                        level: 1,
                        level_type: 0,
                        next_bonus_coin: 12,
                        next_exp: 3,
                        next_level: 2,
                        user_exp: 0
                    },
                    taking_work_level: {
                        bonus_coin: 0,
                        exp: 0,
                        is_max_level: false,
                        level: 1,
                        level_type: 0,
                        next_bonus_coin: 20,
                        next_exp: 3,
                        next_level: 2,
                        user_exp: 0
                    },
                    flowerpot: "sick"
                },
                unit: '金币/次'
            }, setting);
            window.__Health = this;
            this.bindTriggerHealth();
            this.getHealthData(window.__Health.renderingPotOnly);
            this.scroll();
        },
        /**
         * [bindTriggerHealth 绑定点击侧边栏事件]
         * @return {[type]} [description]
         */
        bindTriggerHealth: function() {
            var setting = this.setting,
                $trigger = $(setting.triggerSelector),
                $content = $(setting.contentSelector);
            $trigger.on('click', function(){
                if($content.hasClass('show')){
                    window.__Health.hideHealth();
                } else {
                    window.__Health.showHealth();
                }
            });
            // 点击空白处，收起
            $('.inner-content, #JS_container, .main-subnav, .regular, .panel, .home-foot').on('click', function(){
                if($content.hasClass('show')){
                    window.__Health.hideHealth();
                }
            });
        },
        /**
         * [getHealthData 获取健康度数据]
         * @return {[type]} [description]
         */
        getHealthData: function(fn) {
            var setting = this.setting;
            $(setting.loadingSelector).show();
            $.ajax({
                method: 'get',
                url: setting.url,
                success: fn,
                error: function(){
                    $.alert('数据请求失败，请关闭后重新点击打开奖励规则...');
                }
            });
        },
        /**
         * [renderingData 渲染数据到页面]
         * @return {[type]} [description]
         */
        renderingData: function() {
            var setting = this.setting,
                data = setting.data;

            for(var key in data) {
                if (key != 'taking_work_level') {
                    setting.unit = '金币/次';
                } else {
                    setting.unit = '%佣金/次';
                }
                var $key = $('#' + key),
                    $level = $key.find('.level'),                           //当前等级
                    $next_bonus_coin = $key.find('.i-next-award'),          //下阶段奖励
                    $bonus_coin = $key.find('.i-curr-award'),               //当前奖励
                    $ratio = $key.find('.ratio'),                           //进度条
                    $user_exp = $key.find('.curr-num'),                     //当前数量
                    $next_exp = $key.find('.next-num'),                     //下阶段数量
                    $number = $key.find('.number'),
                    key_item = data[key],
                    ratio = key_item.user_exp / key_item.next_exp * 100;
                $level.html('lv.' + key_item.level);
                $number.find('b.max').remove();
                if(key_item.bonus_coin === 0){
                    $bonus_coin.hide();
                } else {
                    $bonus_coin.html(key_item.bonus_coin + setting.unit).css('left', ratio-12 + '%');
                };
                if (key_item.is_max_level) {
                    // 满级情况
                    $bonus_coin.hide();
                    $next_bonus_coin.html(key_item.bonus_coin + setting.unit).addClass('max');
                    $user_exp.html(key_item.user_exp);
                    $next_exp.html(key_item.exp);
                    $number.append('<b class="max">MAX!!</b>');
                    $ratio.css('width', 100 + '%').addClass('max');
                } else {
                    $user_exp.html(key_item.user_exp);
                    $next_exp.html(key_item.next_exp);
                    $next_bonus_coin.html(key_item.next_bonus_coin + setting.unit);
                    $ratio.css('width', ratio + '%');
                }
                $(setting.loadingSelector).hide();
                $('#content_detail').css({'opacity':'0'}).stop().animate({'opacity':'1'}, 500);
            }
        },
        /**
         * [renderingPot 渲染花盆及提示文字]
         * @return {[type]} [description]
         */
        renderingPot: function() {
            var setting = this.setting,
                data = setting.data,
                $trigger_pot = $('#small-pot'),
                $dynamic_pot = $('#dynamic-pot'),
                $pot_word = $('#pot-word');

            switch(data.flowerpot){
                case 'ordinary':
                    $trigger_pot.attr('class', 'i-small-pot pot-ordinary');
                    $dynamic_pot.attr('class', 'dynamic-pot dynamic-pot-ordinary');
                    $pot_word.html('提高简历被下载数量，有机会拿到1.5~2倍的金币奖励！');
                    break;
                case 'sick':
                    $trigger_pot.attr('class', 'i-small-pot pot-sick');
                    $dynamic_pot.attr('class', 'dynamic-pot dynamic-pot-sick');
                    $pot_word.html('你还没有任何简历被下载，推荐优质又匹配的候选人有助简历被下载喔！');
                    break;
                case 'sunlight':
                    $trigger_pot.attr('class', 'i-small-pot pot-sunlight');
                    $dynamic_pot.attr('class', 'dynamic-pot dynamic-pot-sunlight');
                    $pot_word.html('候选人进入面试，可获得更高奖励！快去我的任务里跟进简历吧！');
                    break;
                case 'unusual_interview':
                    $trigger_pot.attr('class', 'i-small-pot pot-unusual');
                    $dynamic_pot.attr('class', 'dynamic-pot dynamic-pot-unusual');
                    $pot_word.html('推进候选人完成入职，可获得更高奖励！快去我的任务里跟进简历吧！');
                    break;
                case 'unusual_taking_work':
                    $trigger_pot.attr('class', 'i-small-pot pot-unusual');
                    $dynamic_pot.attr('class', 'dynamic-pot dynamic-pot-unusual');
                    $pot_word.html('候选人进入面试，可获得更高奖励！快去我的任务里跟进简历吧！');
                    break;
                case 'unbelievable':
                    $trigger_pot.attr('class', 'i-small-pot pot-unbelievable');
                    $dynamic_pot.attr('class', 'dynamic-pot dynamic-pot-unbelievable');
                    $pot_word.html('你正处于无敌状态，可享受最高额度金币奖励，保持喔！');
                    break;
                default:
                    break;
            }
        },
        /**
         * [renderingPotOnly ajax请求success回调函数，只渲染花盆（针对页面刚加载）]
         * @return {[type]} [description]
         */
        renderingPotOnly: function(data) {
            var setting = window.__Health.setting;
            if (data.status === 'ok') {
                setting.data = $.extend(setting.data, data.data);
                window.__Health.renderingPot();
            };
        },
        /**
         * [renderingAll ajax请求success回调函数，渲染全部数据]
         * @return {[type]} [description]
         */
        renderingAll: function(data) {
            var setting = window.__Health.setting;
            if (data.status === 'ok') {
                setting.data = $.extend(setting.data, data.data);
                window.__Health.renderingPot();
                window.__Health.renderingData();
            };
        },
        scroll: function() {
            $(window).on('scroll', function(e){
                var top = $(document).scrollTop(),
                    $content = $('.health-content');
                if (top > 60) {
                    $content.css('padding-top', '0');
                } else {
                    $content.css('padding-top', 60 - top + 'px');
                }
            });
        },
        hideHealth: function() {
            var setting = this.setting;
            $(setting.contentSelector).removeClass('show').addClass('hide');
            $('#content_detail').animate({'opacity':'0'}, 500);
        },
        showHealth: function() {
            var setting = this.setting;
            $(setting.contentSelector).removeClass('hide').addClass('show');
            window.__Health.getHealthData(window.__Health.renderingAll);
        }
    };

    health.prototype.init.prototype = health.prototype;
    return health;
})(jQuery);

$(function(){
    $.Health();
});
