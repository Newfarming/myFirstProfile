/**
 * 彩蛋活动插件
 * @param  {[type]} $         [description]
 * @param  {[type]} undefined ){              if( !$ ) return;    var eggs [description]
 * @return {[type]}           [description]
 * @author llp
 * @date 2015-06-25
 */

//扩展jQuery animate的easing参数
jQuery.extend(jQuery.easing, {
    def: 'easeOutQuad',

    easeInCubic: function(x, t, b, c, d) {
        return c * (t /= d) * t * t + b;
    },
    easeOutCubic: function(x, t, b, c, d) {
        return c * ((t = t / d - 1) * t * t + 1) + b;
    },
    easeInOutCubic: function(x, t, b, c, d) {
        if ((t /= d / 2) < 1) return c / 2 * t * t * t + b;
        return c / 2 * ((t -= 2) * t * t + 2) + b;
    }
});

$.Eggs = (function($, undefined) {
    if (!$) return;

    var eggs = function(setting) {
        return new eggs.prototype.init(setting);
    };

    eggs.prototype = {
        debug: false,
        constructor: eggs,
        eggCookieName: (this.debug) ? 'isShowEggNewDebug' : 'isShowEggNew',
        countDayByDayTime: function(offsetNum) {
            var getDateObj = function(t) {
                var dt;
                if (t != undefined) {
                    if (typeof t == 'string' || typeof t == 'number') {
                        dt = new Date(t);
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
                    h: 0, //dt.getHours(),
                    i: 0, //dt.getMinutes(),
                    s: 0, //dt.getSeconds()
                };
            };
            var monthStartObj = getDateObj();
            var monthEnd = new Date(monthStartObj.y, monthStartObj.m - 1, monthStartObj.d + offsetNum, monthStartObj.h, monthStartObj.i, monthStartObj.s);
            return monthEnd.getFullYear() + '-' + (monthEnd.getMonth() + 1) + '-' + monthEnd.getDate() + ' 00:00:00';
        },
        getTimeStamp: function(t) {
            var dt = new Date();
            if (typeof t == 'string' || typeof t == 'number') {
                dt = new Date(t);
            }
            return Math.round(dt / 1000);
        },
        getTimeStampM: function(t) {
            var dt = new Date();
            //注意safari下直接字符串返回new date会得到NaN，否则必须是个标准dateString
            if (typeof t == 'string') {
                t = t.trim();
                if (t.match(/^([0-9]{4})\-([0-9]{1,2})\-([0-9]{1,2}) ([0-9]{1,2}):([0-9]{1,2}):([0-9]{1,2})$/i)) {
                    dt = new Date(RegExp.$1, parseInt(RegExp.$2) - 1, RegExp.$3, RegExp.$4, RegExp.$5, RegExp.$6);
                } else if (t.match(/^([0-9]{4})\-([0-9]{1,2})\-([0-9]{1,2})/i)) {
                    dt = new Date(RegExp.$1, parseInt(RegExp.$2) - 1, RegExp.$3);
                } else {
                    dt = new Date(t);
                }
            } else if (typeof t == 'number') {
                dt = new Date(t);
            }
            return dt.getTime();
        },
        setCookieToday: function(key, value) {
            var ckTime = 86400000;
            var tomorrow = this.countDayByDayTime(1);
            var expires = new Date();
            var deadline = this.getTimeStampM(tomorrow);
            expires.setTime(deadline);
            document.cookie = key + '=' + value + ';expires=' + expires.toUTCString() + ';path=/;';
        },
        setCookie: function(key, value, day) {
            var ckTime = (day != undefined && typeof day == 'number') ? parseInt(day) * 86400000 : 86400000;
            var expires = new Date();
            expires.setTime(expires.getTime() + ckTime);
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
        init: function(setting) {
            this.setting = $.extend({
                reqUrl: ' /activity/find_egg/',
                reqCloseUrl: '/activity/close_easter/',
                reqLogUrl: '/activity/user_need/',
                selector: '.eggs', //彩蛋功能
                eggPopupSelector: '#JS_egg', //彩蛋弹窗
                eggSelector: '#JS_drop_egg', //彩蛋图片
                popupSelector: '#JS_egg',
                closeSelector: '.close',
                randomImg: '',
                eggLeftPadding: '',
                giftName: '',
                giftType: '',
                giftImgSelector: '',
                giftWordSelector: '',
                realGift: {
                    'jd_shopping_card_50': {
                        imgUrl: '/static/partner/eggs/img/JD.gif',
                        word: '50元京东购物卡' //'好运当头！50元京东购物卡拿去随便花～'
                    },
                    /*'condom': {
                        imgUrl: '/static/partner/eggs/img/condom.gif',
                        word: '在这个特殊的节日，希望你能用得到！'//'开箱后惊呆了，竟然有一盒TT！'
                    },*/
                    'christmas_cake': {
                        imgUrl: '/static/partner/eggs/img/snow.gif?t=151211',
                        word: '圣诞玛德琳蛋糕礼盒'
                    },
                    'starbuck': {
                        imgUrl: '/static/partner/eggs/img/starbuck.gif',
                        word: 'Starbucks星礼卡' //'哇！聘宝真宠你，砸中Starbucks星礼卡。'
                    },
                    'mask': {
                        imgUrl: '/static/partner/eggs/img/Masks.gif',
                        word: '3M防霾口罩' //'聘宝不仅关心你的工作，也关心你的身体。'
                    },
                    'pillow': {
                        imgUrl: '/static/partner/eggs/img/pillow.gif',
                        word: '聘宝多功能抱枕' //'工作辛苦了，送你一个抱枕靠着它好好休息。'
                    },
                    'pinbot_note': {
                        imgUrl: '/static/partner/eggs/img/notebook.gif',
                        word: '限量版聘宝江湖纪念本' //'限量版聘宝江湖纪念本，居然被你砸到了！'
                    },
                    'hongbao_1': {
                        imgUrl: '/static/partner/eggs/img/hongbao.gif',
                        word: '1元微信红包' //'运气不错！砸中1元微信红包。'
                    },
                    'hongbao_3': {
                        imgUrl: '/static/partner/eggs/img/hongbao.gif',
                        word: '3元微信红包' //'好像在下红包雨！砸中3元微信红包。'
                    },
                    'hongbao_3.8': {
                        imgUrl: '/static/partner/eggs/img/hongbao.gif',
                        word: '3.8元微信红包' //'运气不错！砸中3.8元微信红包。'
                    },
                    'hongbao_5': {
                        imgUrl: '/static/partner/eggs/img/hongbao.gif',
                        word: '5元微信红包' //'财神到！砸中5元微信红包。'
                    },
                    'hongbao_8': {
                        imgUrl: '/static/partner/eggs/img/hongbao.gif',
                        word: '8元微信红包' //'这是要发的节奏！砸中8元微信红包。'
                    },
                    'hongbao_38': {
                        imgUrl: '/static/partner/eggs/img/hongbao.gif',
                        word: '38元微信红包' //'运气不错！砸中38元微信红包。'
                    },
                    'hongbao_48': {
                        imgUrl: '/static/partner/eggs/img/hongbao.gif',
                        word: '48元微信红包' //'运气不错！砸中48元微信红包。'
                    },
                    'hongbao_58': {
                        imgUrl: '/static/partner/eggs/img/hongbao.gif',
                        word: '58元微信红包' //'运气不错！砸中58元微信红包。'
                    },
                    'hongbao_68': {
                        imgUrl: '/static/partner/eggs/img/hongbao.gif',
                        word: '68元微信红包' //'运气不错！砸中68元微信红包。'
                    },
                    'apple': {
                        imgUrl: '/static/partner/eggs/img/apple.gif',
                        word: '精品红富士苹果礼盒' //'这是要发的节奏！砸中8元微信红包。'
                    },
                    'kiwi': {
                        imgUrl: '/static/partner/eggs/img/kiwi.gif',
                        word: '意大利绿奇异果礼盒' //'这是要发的节奏！砸中8元微信红包。'
                    },
                    'lemon': {
                        imgUrl: '/static/partner/eggs/img/lemon.gif',
                        word: '进口尤立克柠檬礼盒' //'这是要发的节奏！砸中8元微信红包。'
                    },
                    'orange': {
                        imgUrl: '/static/partner/eggs/img/orange.gif',
                        word: '美国新奇士脐橙礼盒' //'这是要发的节奏！砸中8元微信红包。'
                    },
                    'xiaweiyiguo': {
                        imgUrl: '/static/partner/eggs/img/xiaweiyiguo.gif',
                        word: '夏威夷果坚果1份'
                    },
                    'bigenguo': {
                        imgUrl: '/static/partner/eggs/img/bigenguo.gif',
                        word: '碧根果坚果1份'
                    },
                    'badanmu': {
                        imgUrl: '/static/partner/eggs/img/badanmu.gif',
                        word: '巴旦木坚果1份'
                    },
                    'book1': {
                        imgUrl: '/static/partner/eggs/img/book1.gif',
                        word: '《招聘面试新法》1本'
                    },
                    'book2': {
                        imgUrl: '/static/partner/eggs/img/book2.gif',
                        word: '《拆掉思维的墙》1本'
                    }
                },
                unrealGift: {
                    /*'shit': {
                        imgUrl: '/static/partner/eggs/img/shit.gif',
                        word: '这次运气差了点，居然是一坨便便。<br>下一个彩蛋随时可能出现，爱聘宝人品更棒喔！'
                    },*/
                    'pinot_point_10': {
                        imgUrl: '/static/partner/eggs/img/10pindian.gif',
                        word: '10聘点'
                    },
                    'smile': {
                        imgUrl: '/static/partner/eggs/img/smile.gif',
                        word: '差一点就砸到奖品啦！'
                    },
                    /*'dog': {
                        imgUrl: '/static/partner/eggs/img/dog.gif',
                        word: '你单身吗？双11小狗驾到。<br>下一个彩蛋随时可能出现，汪汪！'
                    },*/
                    'cup': {
                        imgUrl: '/static/partner/eggs/img/Trophy.gif',
                        word: '奖你一个水晶杯，最佳HR的荣耀一定非你莫属。'
                    },
                    /*'meat': {
                        imgUrl: '/static/partner/eggs/img/Meat.gif',
                        word: '要小鲜肉不要做光棍<br>下一个彩蛋随时可能出现，试试再看几封简历！'
                    },*/
                    'black_card': {
                        imgUrl: '/static/partner/eggs/img/card.gif',
                        word: '获得一张“百约百中”黑卡，大牛从此不再难约。'
                    },
                    'medicine': {
                        imgUrl: '/static/partner/eggs/img/Drug.gif',
                        word: '送你一瓶速效招人胶囊，按需服用效果更佳。'
                    },
                    'new_year_xin': {
                        imgUrl: '/static/partner/eggs/img/xin.gif',
                        word: '【新】'
                    },
                    'new_year_nian': {
                        imgUrl: '/static/partner/eggs/img/nian.gif',
                        word: '【年】'
                    },
                    'new_year_kuai': {
                        imgUrl: '/static/partner/eggs/img/kuai.gif',
                        word: '【快】'
                    },
                    'new_year_le': {
                        imgUrl: '/static/partner/eggs/img/le.gif',
                        word: '【乐】'
                    }

                }
            }, setting);
            if (this.debug) {
                this.randomImg();
            } else {
                if (this.getCookie(this.eggCookieName) === null) {
                    /*$(this.setting.selector).show();
                    $(this.setting.eggPopupSelector).show();*/
                    this.randomImg();
                }
            }
            window.__Eggs = this;
        },
        queryBonus: function() {
            var _this = this;
            var setting = this.setting,
                setPos = this.setPos;
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: setting.reqUrl,
                success: function(data) {
                    _this.setCookieToday(_this.eggCookieName, 1, 1);
                    $('.egg-click-btn').html('砸开看看');
                    /**
                     *redpack_send_fail:红包发放失败,
                     *redpack_send_success:红包已经发送至聘宝招聘版服务号
                     *unbind:您还未绑定微信服务号
                     */
                    if (data.status.match(/^(ok|unbind|redpack_send_fail|redpack_send_success)$/i)) {
                        _this.showBonus(data);
                    } else {
                        _this.showBonus(data, 'smile', 0);
                    }
                },
                error: function(data) {
                    _this.setCookieToday(_this.eggCookieName, 1, 1);
                    $('.egg-click-btn').html('砸开看看');
                    console.log(data);
                    _this.showBonus(data, 'smile', 0);
                }
            });
        },
        showBonus: function(data, gift, giftType) {
            var _this = this;
            var setting = this.setting,
                setPos = this.setPos;

            setting.giftName = (gift != undefined && typeof gift == 'string') ? gift : data.gift;
            setting.giftType = (giftType != undefined && typeof giftType == 'string') ? giftType : data.gift_type;
            if (data.gift == 'pinot_point_10') {
                setting.giftType = 0;
            }
            setting.gift_id = data.gift_id;
            if (data.status === 'ok' && data.gift.match(/^new_year_/i)) {
                setting.giftType = 1;
            }
            if (setting.giftType === undefined) setting.giftType = 0;
            //console.log('setting',setting.giftType,setting.giftName);
            //$(setting.selector).show();
            //$(setting.eggPopupSelector).show();
            //window.__Eggs.randomImg(data.gift);
            //window.__Eggs.setPos();
            window.__Eggs.bindCloseEvent();
            switch (setting.giftType) {
                case 0:
                    setting.popupSelector = '#JS_unreal';
                    setting.giftImgSelector = '#JS_unreal_img';
                    setting.giftWordSelector = '#JS_unreal_word';
                    //window.__Eggs.bindEggClickEvent();
                    break;
                case 1:
                    setting.popupSelector = '#JS_real';
                    setting.giftImgSelector = '#JS_real_img';
                    setting.giftWordSelector = '#JS_real_word';
                    //window.__Eggs.bindEggClickEvent();
                    break;
                default:
                    break;
            }
            $('.eggs-popup').css('top', '-100px');
            $(setting.eggPopupSelector).hide();
            if (setting.giftType == 1) {
                var tmpTop = parseInt($(setting.popupSelector).css('top'));
                tmpTop -= 50;
                $(setting.popupSelector).css('top', tmpTop + 'px');
            }

            $(setting.popupSelector).show();
            window.__Eggs.setHtml();

            /* update Html */
            //img.code-img
            var defaultRealGiftQrcodeSrc = '/static/partner/eggs/img/ass_code.jpg';
            //barcode-info-more
            var defaultRealGiftTextLine1 = '1. 拍下此弹窗（或截图）';
            //get-gift-desc-more
            var defaultRealGiftTextLine2 = '2. 扫码加小助手并发送图片领奖';
            //gift-title-more
            var defaultRealGiftTextLineSpace = $('#JS_real .gift-title-more').html();
            $('#JS_real img.code-img').attr('src', defaultRealGiftQrcodeSrc);

            if (setting.giftName.match(/^hongbao_/i)) {
                //红包自动发放
                if (data.status == 'unbind') {
                    //未绑定
                    //$('#JS_real img.code-img').attr('src', '/static/b_common/img/qrcode_for_pinbot_wx.jpg');
                    $('#JS_real img.code-img').attr('src', '/hr/qrcode_redpack/');
                    $('#JS_real p.barcode-info-more').html('您还未绑定聘宝服务号，请您扫码绑定后');
                    $('#JS_real p.get-gift-desc-more').html('红包将通过微信<span class="c44b5e8">聘宝招聘版</span>服务号自动完成发放！');
                    $('#JS_real .gift-title-more').html('<br>');
                } else if (data.status == 'redpack_send_fail') {
                    //红包发放失败
                    $('#JS_real p.barcode-info-more').html('<span class="cf46c62">红包发放失败！</span><br>请拍下此弹窗（或截图）');
                    $('#JS_real p.get-gift-desc-more').html('扫码加聘宝小助手并发送图片领奖');
                    $('#JS_real .gift-title-more').html('');
                } else if (data.status == 'redpack_send_success') {
                    //红包已经发送至聘宝招聘版服务号
                    $('#JS_real p.barcode-info-more').html('红包已发送至<span class="c44b5e8">聘宝招聘版</span>服务号！');
                    $('#JS_real p.get-gift-desc-more').html('关注聘宝小助手 更多好玩的活动进行中');
                    $('#JS_real .gift-title-more').html('<br>');
                }
            } else if (setting.giftType == 1) {
                //如果是实物礼品，需要提醒填写收货地址
                $('#JS_real p.barcode-info-more').html('请至<a href="/users/profile/#person-info" class="c44b5e8" target="_blank">个人设置</a>确认您的收货地址，没有地址无法领奖');
                $('#JS_real p.get-gift-desc-more').html('<br>');
                $('#JS_real .gift-title-more').html('<br>');
                $('#JS_real .img-p').html('小助手会在<span class="cf46c62">每周五</span>统一邮寄<br>本周所有中奖并确认地址的实物奖品<br>请耐心等待');
                $('#JS_real .footer-p').html('<a href="javascript:void(0);" class="egg-btn egg-btn-red goto-want">我想要</a> <a href="javascript:void(0);" class="egg-btn egg-btn-blue goto-deny">我不想要</a>');
                $("#JS_real").undelegate(".goto-want").delegate(".goto-want", "click", function(e) {
                    $(this).removeClass('goto-want');
                    $(this).removeClass('egg-btn-red');
                    $(this).addClass('egg-btn-dark-blue');
                    $(this).addClass('goto-confirm');
                    $(this).text('去确认地址');
                    $.ajax({
                        type: 'post',
                        dataType: 'json',
                        data: JSON.stringify({
                            gift_id: setting.gift_id,
                            need_status: 1
                        }),
                        headers: {
                            "X-CSRFToken": _this.getCookie('csrftoken'),
                            'Content-Type': 'application/json'
                        },
                        url: _this.setting.reqLogUrl,
                        success: function(data) {},
                        error: function(data) {
                            console.log(data);
                        }
                    });
                    $("#JS_real").undelegate(".goto-confirm").delegate(".goto-confirm", "click", function(e) {
                        document.location.href='/users/profile/#person-info';
                        $(setting.selector).hide();
                    });
                });

                $("#JS_real").undelegate(".goto-deny").delegate(".goto-deny", "click", function(e) {
                    $.ajax({
                        type: 'post',
                        dataType: 'json',
                        data: JSON.stringify({
                            gift_id: setting.gift_id,
                            need_status: 0
                        }),
                        headers: {
                            "X-CSRFToken": _this.getCookie('csrftoken'),
                            'Content-Type': 'application/json'
                        },
                        url: _this.setting.reqLogUrl,
                        success: function(data) {},
                        error: function(data) {
                            console.log(data);
                        }
                    });
                    $(setting.selector).hide();
                });

            }

            window.__Eggs.bindCloseEvent();
            $('.eggs-layer').show();
            window.__Eggs.setPos();
        },
        closeEgg: function() {
            var _this = this;
            $.ajax({
                type: 'get',
                dataType: 'json',
                url: _this.setting.reqCloseUrl,
                success: function(data) {
                    if (data.status === 'ok') {
                        _this.setCookieToday(_this.eggCookieName, 1, 1);
                    };
                },
                error: function(data) {
                    console.log(data);
                }
            });
        },
        loadImage: function(url) {
            var loadImage = function(deferred) {
                var image = new Image();
                image.onload = loaded;
                image.onerror = errored;
                image.onabort = errored;
                image.src = url;

                function loaded() {
                    unbindEvents();
                    deferred.resolve(image);
                }

                function errored() {
                    unbindEvents();
                    deferred.reject(image);
                }

                function unbindEvents() {
                    image.onload = null;
                    image.onerror = null;
                    image.onabort = null;
                }
            };
            return $.Deferred(loadImage).promise();
        },
        waitSeconds: function() {
            var deferred = jQuery.Deferred();
            var randomSecond = 1000 * Math.ceil(Math.random() * 3)
            setTimeout(function() {
                deferred.resolve();
            }, randomSecond);
            return deferred.promise();
        },
        countDayByDay: function(offsetNum) {
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
        },
        getDay: function(str) {
            if (typeof str == 'string' && str.match(/^([0-9]{4})\-([0-9]{1,2})\-([0-9]{1,2})/i)) {
                var y = parseInt(RegExp.$1);
                var m = parseInt(RegExp.$2);
                var d = parseInt(RegExp.$3);
                return y + '-' + m + '-' + d;
            }
            return '';
        },
        randomImg: function() {
            var _this = this;
            var setting = this.setting;
            //圣诞就是截止到14-20号  元旦彩蛋：12月21日-25日
            var christStart = this.getDay('2015-12-14'); //'2015-12-14'
            var christEnd = this.getDay('2015-12-19'); //'2015-12-20'
            var newYearStart = this.getDay('2015-12-20'); //'2015-12-21'
            var newYearEnd = this.getDay('2015-12-25');
            var fruitStart = this.getDay('2016-1-4'); //'2015-12-21'
            var fruitEnd = this.getDay('2016-1-25');
            var random_num = Math.ceil(Math.random() * 10);

            if (1 == 2 && this.countDayByDay(0) >= christStart && this.countDayByDay(0) <= christEnd) {
                setting.randomImg = '/static/partner/eggs/img/s5_100_c.png';
                setting.eggLeftPadding = '35%';
            } else if (this.countDayByDay(0) >= newYearStart && this.countDayByDay(0) <= newYearEnd) {
                setting.randomImg = '/static/partner/eggs/img/s4_140_c.png';
                setting.eggLeftPadding = '35%';
            } else if (this.countDayByDay(0) >= fruitStart && this.countDayByDay(0) <= fruitEnd) {
                setting.randomImg = '/static/partner/eggs/img/s6_140_c.png';
                setting.eggLeftPadding = '35%';
            } else {
                switch (random_num) {
                    case 1:
                        setting.randomImg = '/static/partner/eggs/img/L2_220_c.png';
                        setting.eggLeftPadding = '25%';
                        break;
                    case 2:
                        setting.randomImg = '/static/partner/eggs/img/m1_140_c.png';
                        setting.eggLeftPadding = '35%';
                        break;
                    case 3:
                        setting.randomImg = '/static/partner/eggs/img/m2_140_c.png';
                        setting.eggLeftPadding = '35%';
                        break;
                    case 4:
                        setting.randomImg = '/static/partner/eggs/img/m3_140_c.png';
                        setting.eggLeftPadding = '35%';
                        break;
                    case 5:
                        setting.randomImg = '/static/partner/eggs/img/m4_140_c.png';
                        setting.eggLeftPadding = '35%';
                        break;
                    case 6:
                        setting.randomImg = '/static/partner/eggs/img/s1_100_c.png';
                        setting.eggLeftPadding = '40%';
                        break;
                    case 7:
                        setting.randomImg = '/static/partner/eggs/img/s2_100_c.png';
                        setting.eggLeftPadding = '40%';
                        break;
                    case 8:
                        setting.randomImg = '/static/partner/eggs/img/s3_100_c.png';
                        setting.eggLeftPadding = '40%';
                        break;
                    case 9:
                        setting.randomImg = '/static/partner/eggs/img/L1_220_c.png';
                        setting.eggLeftPadding = '25%';
                        break;
                        /*case 10: //christmas cacke
                        setting.randomImg = '/static/partner/eggs/img/s5_100_c.png';
                        break;*/
                    default:
                        setting.randomImg = '/static/partner/eggs/img/s1_100_c.png';
                        setting.eggLeftPadding = '40%';
                        break;
                }
            }

            var randomImg = setting.randomImg;
            var a_randomImg = randomImg; //.replace(/c\.png/, 'a.gif');
            var b_randomImg = randomImg; //.replace(/c\.png/, 'b.gif');
            var giftImg = '';
            var _this = this;
            var p1 = this.loadImage(setting.randomImg);
            p1.then(function(image) {
                $(setting.eggSelector).attr('src', setting.randomImg);
                return _this.loadImage(a_randomImg);
            }).then(function(image) {
                return _this.loadImage(b_randomImg);
            }).then(function(image) {
                return _this.loadImage(b_randomImg);
            }).done(function(image) {
                var ddd = _this.waitSeconds();
                ddd.then(function() {
                    window.__Eggs.animation();
                });
            });
            //.fail(function(image) {});
        },
        //暂时隐藏的弹窗id/Class
        hideModalList: '',
        chkOtherModals: function() {
            //任务系统弹窗
            if ($('.black-bg').length && $('.black-bg').css('display') == 'block') {
                if ($('.js-task-tip-contain').css('display') == 'block') {
                    this.hideModalList = '.js-task-tip-contain';
                } else if ($('.task-close-tip').css('display') == 'block') {
                    this.hideModalList = '.task-close-tip';
                } else if ($('#js-task-content').css('display') == 'block') {
                    this.hideModalList = '#js-task-content';
                } else if ($('#js-reward-content').css('display') == 'block') {
                    this.hideModalList = '#js-reward-content';
                }
                return true;
            } else {
                return false;
            }
        },
        showOtherModals: function() {
            if (typeof this.hideModalList == 'string' && this.hideModalList != '') {
                $(this.hideModalList).show();
            }
        },
        hideOtherModals: function() {
            if (typeof this.hideModalList == 'string' && this.hideModalList != '') {
                $(this.hideModalList).hide();
            }
        },
        animation: function() {
            var _this = this;
            var setting = this.setting;

            //检查是否有其他弹窗，有就先隐藏
            if (_this.chkOtherModals()) {
                _this.hideOtherModals();
            }

            $(setting.selector).show();
            $(setting.eggPopupSelector).show();
            var $eggSelector = $(setting.eggSelector);
            var randomImg = setting.randomImg;
            var $popup = $(setting.popupSelector);
            var marginTop = (($(window).height() - $('#JS_egg').height()) / 2 + 70) + 'px';
            $('.eggs-popup-layer').addClass('half-dark');
            $('.egg-box img').css('left', setting.eggLeftPadding);
            $('#JS_egg').animate({
                top: marginTop
            }, 500, 'easeInCubic');
            setTimeout(function() {
                var a_randomImg = randomImg; //.replace(/c.png/, 'a.gif');
                $(setting.eggSelector).attr('src', a_randomImg);
            }, 1000);
            /*setTimeout(function() {
                var b_randomImg = randomImg.replace(/c.png/, 'b.gif');
                $(setting.eggSelector).attr('src', b_randomImg);
            }, 2000);*/
            //setTimeout(function() {
            _this.bindCloseEvent();
            //关闭彩蛋
            $('.egg-close').on('click', function() {
                //关闭彩蛋，恢复之前弹窗
                _this.showOtherModals();
                _this.closeEgg();
            });

            //开奖
            $('.egg-click').on('click', function() {
                $('.egg-click-btn').html('<img src="/static/b_common/img/loading.gif" border="0">');
                _this.queryBonus();
            });


            //}, 10);

        },
        /**
         * [setPos 设置弹窗居中]
         */
        setPos: function() {
            var setting = this.setting,
                $popup = $(setting.popupSelector);
            $('#JS_real').css({
                marginTop: (($(window).height() - $('#JS_real').height()) / 2 + 70) + 'px'
            });
            $('#JS_unreal').css({
                marginTop: (($(window).height() - $('#JS_unreal').height()) / 2) + 'px'
            });
        },
        /**
         * [bindEggClickEvent 彩蛋点击事件]
         * @return {[type]} [description]
         */
        /*bindEggClickEvent: function() {
            var _this = this,
                setting = _this.setting;
            $(setting.eggSelector).on('click', function(){
                $(setting.eggPopupSelector).hide();
                $(setting.popupSelector).show();
                _this.setHtml();
                $(setting.giftImgSelector).load(function(){
                    // 图片加载完成后更新位置
                    _this.setPos();
                });
                _this.bindCloseEvent();
            })
        },*/
        bindCloseEvent: function() {
            var _this = this,
                setting = _this.setting;
            $(setting.closeSelector).on('click', function() {
                $(setting.selector).hide();
                //关闭彩蛋，恢复之前弹窗
                _this.showOtherModals();
            });
        },
        /**
         * [setHtml 设置奖品HTML]
         */
        setHtml: function() {
            var _this = this,
                setting = _this.setting,
                $img = $(setting.giftImgSelector),
                $word = $(setting.giftWordSelector);
            var newText = '2. 扫码加小助手并发送图片领奖';
            var currentKey = '';
            var isReal = false;
            for (var key in setting.unrealGift) {
                if (key === setting.giftName) {
                    isReal = false;
                    if(key.match(/^(black_card|medicine|cup|smile)$/i)){
                        key = 'smile';
                        $('.unreal_footer').html('<span class="c607d8b">请不要灰心，明天继续努力哟！</span><br><a href="javascript:void(0);" class="egg-btn egg-btn-dark-blue close">知道了</a>');
                    }else{
                        $('.unreal_footer').html('明天还来聘宝招人，彩蛋天天有喔！<br><a href="javascript:void(0);" class="egg-btn egg-btn-dark-blue close">知道了</a>');
                    }
                    // 图片
                    $img.attr('src', setting.unrealGift[key].imgUrl);
                    // 文字
                    $word.html(setting.unrealGift[key].word);
                    currentKey = key;
                    break;
                };
            }
            for (var key in setting.realGift) {
                if (key === setting.giftName) {
                    if (key == 'pinot_point_10') {
                        isReal = false;
                    } else if (key.match(/^new_year_/i)) {
                        isReal = true;
                    } else {
                        isReal = true;
                    }
                    // 图片
                    $img.attr('src', setting.realGift[key].imgUrl);
                    // 文字
                    $word.html(setting.realGift[key].word);
                    currentKey = key;
                    break;
                };
            }
            //调整描述
            if (currentKey.match(/^(self|manual)_service_/i)) {
                $('.eggs-popup .blue-reel').css('padding', '32px 0');
                if (currentKey == 'self_service_111') {
                    newText = '2、扫码加小助手为微信好友，把图发给小助手；<br>3、2015年内购买任意自助型套餐可<span style="color:#fff;">减免111</span>元；<br><span style="color:#fff;">4、一个套餐只能使用一张抵用券。</span>';
                } else if (currentKey == 'manual_service_500') {
                    newText = '2、扫码加小助手为微信好友，把图发给小助手；<br>3、2015年内购买任意省心型套餐可<span style="color:#fff;">减免500</span>元；<br><span style="color:#fff;">4、一个套餐只能使用一张抵用券。</span>';
                } else if (currentKey == 'manual_service_1111') {
                    newText = '2、扫码加小助手为微信好友，把图发给小助手；<br>3、2015年内购买任意省心型套餐可<span style="color:#fff;">减免1111</span>元；<br><span style="color:#fff;">4、一个套餐只能使用一张抵用券。</span>';
                }
            } else if (currentKey == 'pinot_point_10') {
                $('#JS_unreal_word').html('<span class="small-title">恭喜你获得</span><span class="barcode-info-red barcode-info-gift gift-title" style="color:#f66b5d;">10聘点</span>');
                $('.eggs-popup .blue-reel').css('padding', '21px 0');
            } else {
                $('.eggs-popup .blue-reel').css('padding', '32px 0');
            }
            if (isReal) {
                $('.i-red-close').addClass('i-red-close-new');
            } else {
                $('.i-red-close').removeClass('i-red-close-new');
            }
            if (currentKey.match(/^new_year_/i)) {
                $('.eggs-popup .gift-title-more').html('快与分舵伙伴凑齐“新年快乐”领取Sounder蓝牙音响！<br><br>');
                $('.eggs-popup .barcode-info-more').text('1. 拍下此弹窗（或截图）凑齐 “新年快乐”');
                $('.eggs-popup .get-gift-desc-more').text('2. 扫码加小助手并发送4张截图领奖');
            } else {
                $('.eggs-popup .gift-title-more').html('<br><br>');
                $('.eggs-popup .barcode-info-more').text('1. 拍下此弹窗（或截图）');
                $('.eggs-popup .get-gift-desc-more').text('2. 扫码加小助手并发送图片领奖');
            }

            $('.eggs-popup .get-gift-desc').html(newText);

            /*if(setting.giftName=='christmas_cake'){
                $('.barcode .small-title').css('display','block');
            }else{
                $('.barcode .small-title').css('display','none');
            }*/
        }
    };

    eggs.prototype.init.prototype = eggs.prototype;
    return eggs;
})(jQuery);

$(function() {
    $.Eggs();
});