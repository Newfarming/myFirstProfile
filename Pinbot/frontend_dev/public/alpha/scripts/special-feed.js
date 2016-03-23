function minusOne(e) {
    e.each(function() {
        var e = $(this),
            t = parseInt(e.html(), 10) - 1;
        0 >= t && (t = "", $(this).parents("li").removeClass("latest-count")), e.html(t)
    })
}

function setNum(e, t) {
    /*
    e.each(function() {
        0 >= t ? t = "" : $(this).parents("li").addClass("latest-count"), $(this).html(t)
    })
    */
    return;
}
var feedApp = angular.module("feedApp", []);
feedApp.config(["$interpolateProvider",
    function(e) {
        e.startSymbol("{[{"), e.endSymbol("}]}")
    }
]), feedApp.config(["$routeProvider",
    function(e) {
        var t = $("#template-feeditem").html();
        e.when("/group/:id", {
            template: t,
            controller: "feedPage"
        });
        var n = $(".feed-group-link").first(),
            r = "/";
        n.length && (r = n.attr("href").substr(1)), e.otherwise({
            redirectTo: r
        })
    }
]), feedApp.factory("Feed", ["$http",
    function(e) {
        var t = window.location.pathname || "",
            n = "user";
        return "/statis/feed_result/" === t && (n = "cached"), {
            group: function(t, n, r, o, i) {
                return e.get("/special_feed/feed_list/" + t + "?start=" + n + "&latest=" + r + "&limit=5&view=" + o + "&t=" + +new Date).then(function(e) {
                    return e.data
                }).then(i)
            },
            current: {
                id: "",
                view: n,
                start: 0,
                latest: 0,
                total_count: 0,
                total_recommend_count: 0,
                scope: {}
            }
        }
    }
]), feedApp.filter("gender", function() {
    return function(e) {
        return "female" == e ? "女" : "男";
    }
}).filter("nospace", function() {
    return function(e) {
        return e.split(/\s+/)[0]
    }
}).filter("default", function() {
    return function(values, default_value) {
        return value ? value : default_value;
    }
}).filter("checkFeedOpen", function() {
    return function(e) {
        return e == 'read' ? "" : "feed-unread"
    }
}).filter("checkFeedLatest", function() {
    return function(e) {
        return e ? "feed-latest" : ""
    }
}).filter("manual_status", function() {
    return function(e) {
        if(item.is_manual) {
            return item.admin;
        }
        return "";
    }
}).filter("chop", function() {
    return function(e) {
        return e.length > 150 && (e = e.substr(0, 147) + "</br>..."), e
    }
}), feedApp.directive("fixedtop", function() {
    return {
        restrict: "A",
        link: function(e, t, n) {
            var r = n.fixedtop || 0,
                o = $(t).offset().top,
                i = $(t),
                a = $(window),
                s = i.css("position");
            a.on("scroll", function() {
                a.scrollTop() >= o - r ? i.css({
                    position: "fixed",
                    top: r + "px"
                }) : i.css({
                    position: s,
                    top: "auto"
                })
            })
        }
    }
});
var $more = $(".load-more");
feedApp.controller("aside", ["$scope", "$location",
    function(e, t) {
        e.isActive = function(e) {
            return -1 != t.path().indexOf(e)
        }
    }
]).controller("feedApp", ["$scope", "Feed", "$timeout",
    function(e, t, n) {
        e.current = t.current, e.toggleLatest = function() {
            e.current.latest = e.current.latest ? 0 : 1, n(function() {
                var e = $(".feed-nav .curr").find("a"),
                    t = e.attr("href");
                window.location.replace(t.split("?")[0] + "?" + Math.random().toString(16).substr(2))
            })
        }, e.toggleView = function(t) {
            return e.current.view == t ? !1 : (e.current.view = t || "user", n(function() {
                var e = $(".feed-nav .curr").find("a"),
                    t = e.attr("href");
                window.location.replace(t.split("?")[0] + "?" + Math.random().toString(16).substr(2))
            }), void 0)
        }
    }
]).controller("feedPage", ["$scope", "Feed", "$timeout", "$routeParams", "$rootScope",
    function(e, t, n, r) {

        var li =$('li[data-id="' + r.id + '"]');

        //7天定制激活提示
        if( li.attr('data-continue_url') ){
            var last_date = li.attr('data-last_date'),
                last_msg = last_date ? '(上次查看：' + li.attr('data-last_date') + ')' : '';
            t.current.total_count = 0;
            t.current.total_recommend_count = 0;
            $('#JS_recruit_job').html( li.find('.recruit_job').html() );
            $('#JS_last_date').html( last_msg );
            $('.subscribe-expire').hide();
            $('#JS_end_feed').hide();
            $('#JS_over_date').show();
            return false;
        }else{
            $('#JS_over_date').hide();
        };

        //定制服务到期
        if( li.attr('data-subscribe_expire') ){
            e.initLoading = !0;
            t.current.total_count = 0;
            t.current.total_recommend_count = 0;
            $('.subscribe-expire').hide();
            $('#JS_over_date').hide();
            $('#JS_end_feed').hide();
            checkHasNullFeed( li );
            return;
        }else{
            $('.subscribe-expire').hide();
        };

        t.current.id = r.id, t.current.start = 0, t.current.limit = 5, e.fetch = function() {
            e.loadmore = !0, e.hasmore = !1, t.group(t.current.id, t.current.start, t.current.latest, t.current.view, function(r) {
                n(function() {
                    e.feeditems.push.apply(e.feeditems, r.data), t.current.start = r.next_start, e.loadmore = !1, "-1" != r.next_start && (e.hasmore = !0), e.current.latest ? setNum($(".feed-nav li.curr").find(".feed-latest-count"), r.newest_recommend_count) : r.newest_recommend_count && _.filter(r.data || [], function(e) {
                        return !!e.latest
                    }).length && setNum($(".feed-nav li.curr").find(".feed-latest-count"), r.newest_recommend_count)
                })
            })
        }, n(function() {
            e.initLoading = !0;
            e.loadmore = !1;
            e.hasmore = !1;
            e.waiting = !1;
        }), t.current.id && t.group(t.current.id, t.current.start, t.current.latest, t.current.view, function(r) {
            n(function() {
                e.feeditems = r.data, e.initLoading = !1, t.current.total_count = r.total_count, t.current.total_recommend_count = r.total_recommend_count, t.current.start = r.next_start, "-1" != r.next_start && (e.hasmore = !0), r.count && r.data.length || (e.waiting = !0, e.hasmore = !1), e.current.latest ? setNum($(".feed-nav li.curr").find(".feed-latest-count"), r.newest_recommend_count) : r.newest_recommend_count && _.filter(r.data || [], function(e) {
                    return !(!e || !e.latest)
                }).length && setNum($(".feed-nav li.curr").find(".feed-latest-count"), r.newest_recommend_count)
            })
        }), e.openFeed = function(t) {
            e.feeditems[t].latest && minusOne($('span[data-count-group="' + e.feeditems[t].feed_id + '"], span[data-count-group="all"]')), e.feeditems[t].latest = !1, e.feeditems[t].opened = !0
        }, e.dislike = function(t) {
            $.get("/feed/modify_feed_result", {
                feed_id: e.feeditems[t].feed.id,
                resume_id: e.feeditems[t].resume.id,
                reco_index: "-150"
            }), n(function() {
                e.feeditems[t].dislike = !0, e.feeditems[t].latest = !1, e.feeditems[t].opened = !0
            })
        }
    }
]), $(function() {
    function e(e) {
        $("html, body").stop().animate({
            scrollTop: e
        }, "normal")
    }
    var t = $("#feed-submit-form");
    t.find(".options").each(function() {
        var e = $(this),
            t = e.data("name"),
            n = $('input[name="' + t + '"]');
        e.find("span").on("click", function() {
            e.hasClass("op-multi") ? $(this).toggleClass("selected") : e.hasClass("op-single") && ($(this).parents("li").find(".selected").removeClass("selected"), $(this).addClass("selected")), n.val(e.find(".selected").map(function() {
                return $.trim($(this).html())
            }).toArray().join(","))
        })
    }), $(".suggested-keywords").on("click", "span", function() {
        var e = $(this).html();
        $('input[name="keywords"]').val(e).focus()
    });
    var n = !1;
    t.on("submit", function() {
        return n ? !1 : $('input[name="job_type"]').val() ? $('input[name="keywords"]').val() ? $('input[name="talent_level"]').val() ? $('input[name="expect_area"]').val() ? (n = !0, $("#btn-feed-submit").val("正在提交.."), void 0) : (e(t.find("li").eq(3).offset().top), !1) : (e(t.find("li").eq(2).offset().top), !1) : (e(t.find("li").eq(1).offset().top), !1) : (e(t.find("li").eq(0).offset().top), !1)
    }), $(".select-btn-more>a").on("click", function(e) {
        e.preventDefault();
        var t = $(this);
        $(".select-expect-area").toggleClass("expect-area-span").find(".op-multi").slideToggle(200);
        var n = $.trim(t.html());
        t.html(t.data("text-span")), t.data("text-span", n)
    }), $('p[data-name="job_type"]>span').on("click", function() {
        var e = $(this).data("suggest");
        e && $(".suggested-keywords").html($.map(e.split("|"), function(e) {
            return "<span>" + e + "</span>"
        }).join(""))
    }), $('a[href^="/feed/delete"]').on("click", function() {
        var e = window.confirm("删除订阅条件将清除此订阅下的所有简历！是否继续？");
        return e ? void 0 : !1
    }), $(".feed-edit-jd >form").on("submit", function(e) {
        e.preventDefault();
        var t = $(this),
            n = t.attr("action"),
            r = t.find('textarea[name="job_desc"]').val();
        if (r == window.feed_edit_jd_old) return t.find('textarea[name="job_desc"]').focus(), !1;
        var o = t.find('button[type="submit"]').html("正在保存");
        o.addClass("submitting"), $.post(n, {
            job_desc: r
        }, function(e) {
            o.removeClass("submitting"), o.html("保存"), e && e.status ? (window.feed_edit_jd_old = r, o.prev().remove(), $('<span style="margin-right: 10px; color:green;">已保存!</span>').insertBefore(o).fadeOut(1500, function() {
                $(this).remove()
            })) : (o.prev().remove(), $('<span style="margin-right: 10px; color:red;">保存失败，请重试!</span>').insertBefore(o).fadeOut(3e3, function() {
                $(this).remove()
            }))
        })
    });
    var r;
    $("body").on("mouseover", ".resume-tags-hook", function() {
        clearTimeout(r), $(this).parents(".item-header").find(".item-action-keywords").fadeIn()
    }).on("mouseout", ".resume-tags-hook, .item-action-keywords", function() {
        r = setTimeout(function() {
            $(".item-action-keywords").hide()
        }, 400)
    }).on("mouseover", ".item-action-keywords", function() {
        clearTimeout(r)
    }),
    function() {
        var e = $(document);
        $(window).on("scroll", function() {
            var t = $('a[ng-show="hasmore"]');
            if (!t.length) return !1;
            if (!t.is(":hidden")) {
                var n = e.height() - e.scrollTop() - $(window).height();
                100 > n && t.get(0).click()
            }
        })
    }()
}),
function() {
    var e;
    $(".profile-rss").find("li>a").on("click", function() {
        clearTimeout(e);
        var t = $(this);
        if (t.hasClass("selected")) return !1;
        t.parents("ul").find(".selected").removeClass("selected"), t.addClass("selected");
        var n = t.data("selected");
        return $(".selected-tip").remove(), e = setTimeout(function() {
            $.post("/feed/modify_frequency", {
                frequency: n
            }, function(e) {
                if ("success" == e.status) {
                    var n = $('<p class="selected-tip">设置成功！</p>').appendTo(t.parent());
                    n.fadeOut(2e3, function() {
                        n.remove()
                    })
                }
            })
        }, 1e3), !1
    })
}();

function checkHasNullFeed( li ){
    var url = li.attr('data-rest_url');
    $.get( url , {} , function( res ){
        $('.feed-loading ').hide();
        $('.JS_recruit_feed').html( li.find('.recruit_job').text() );
        if( res.status == 'ok' ){
            $('#JS_end_feed').show();
        }else{
            if( !li.attr('data-partner_feed') ){    //不是人才伙伴赠送的专属定制
                $('.subscribe-expire-info').html('你好！你于<span class="JS_bought_date"></span>购买的专属定制已于今天到期。<br>你可以再次购买一段时间的专属定制，继续获得人才推荐。');
            }else{   //人才伙伴赠送的专属定制
                $('.subscribe-expire-info').html('你好！你于<span class="JS_bought_date"></span>获得的人才伙伴赠送定制已被关闭，<br>您可以再次上传简历以重新使用专属定制，也可以购买一段时间的专属定制，继续获得人才推荐。');
            };
            $('.subscribe-expire').show();
        };
        $('.JS_bought_date').html( li.attr('data-order_date') );
    },'json').fail(function(){
        $.alert('请求失败了！');
    });
};

$(function(){
    $(document).on( 'click' , '#JS_recruit_again' , function(){
        var _this = $( '.feed-nav li.curr' ),
            url = _this.attr('data-continue_url');
        $.get( url , {} , function( res ){
            if( res.status == 'ok' ){
                $('#JS_over_date').hide();
                $('.activate-success').show();
                _this.removeAttr('data-continue_url');
                _this.find( 'a:first').click();
                _this.find('.i-over-date').hide();
            }else{
                $.alert('<p class="alert-notice-center"><span>请求失败，请稍后再试！</span></p>');
            }
        }, 'json').fail(function(){
            $.alert('<p class="alert-notice-center"><span>请求失败，请稍后再试！</span></p>');
        });
    });

    $(document).on( 'click' , '.JS_recruit_end' , function(){
        var _this = $( '.feed-nav li.curr' ),
            url = _this.attr('data-delete_url');
        $.confirm( '<p class="alert-notice-center"><span>恭喜！我们将为你删除该条定制服务，你可以立即开始创建新的定制。</span></p>', function(){
            window.location.href = url;
        });
    });

    $(document).on( 'click' , '#JS_view_history' , function(){
        var li = $( '.feed-nav li.curr' );
        li.removeAttr('data-subscribe_expire').find('a:first').click();
    });

    $(document).on( 'click' , '#JS_feed_again' , function(){
        var li = $( '.feed-nav li.curr' ),
            url = li.attr('data-renewal_url');
        $.get( url , {} , function( res ){
            if( res.status == 'ok' ){
                $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>定制成功,点击确定刷新页面就看见啦！</p>' , function(){
                    window.location.reload();
                });
            }else{
                $.alert('请求失败了！');
            };
        },'json').fail(function(){
            $.alert('请求失败了！');
        });
    });

})
