function minusOne(e) {
    e.each(function() {
        var e = $(this),
            t = parseInt(e.html(), 10) - 1;
        0 >= t && (t = "", $(this).parents("li").removeClass("latest-count")), e.html(t)
    })
}

function setNum(e, t) {
    e.each(function() {
        0 >= t ? t = "" : $(this).parents("li").addClass("latest-count"), $(this).html(t)
    })
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
                return e.get("/feed/group/" + t + "?start=" + n + "&latest=" + r + "&limit=5&view=" + o + "&t=" + +new Date).then(function(e) {
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
        return "female" == e ? "女" : "男"
    }
}).filter("nospace", function() {
    return function(e) {
        return e.split(/\s+/)[0]
    }
}).filter("checkFeedOpen", function() {
    return function(e) {
        return e ? "" : "feed-unread"
    }
}).filter("checkFeedLatest", function() {
    return function(e) {
        return e ? "feed-latest" : ""
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
        t.current.id = r.id, t.current.start = 0, t.current.limit = 5, e.fetch = function() {
            e.loadmore = !0, e.hasmore = !1, t.group(t.current.id, t.current.start, t.current.latest, t.current.view, function(r) {
                n(function() {
                    e.feeditems.push.apply(e.feeditems, r.data), t.current.start = r.next_start, e.loadmore = !1, "-1" != r.next_start && (e.hasmore = !0), e.current.latest ? setNum($(".feed-nav li.curr").find(".feed-latest-count"), r.newest_recommend_count) : r.newest_recommend_count && _.filter(r.data || [], function(e) {
                        return !!e.latest
                    }).length && setNum($(".feed-nav li.curr").find(".feed-latest-count"), r.newest_recommend_count)
                })
            })
        }, n(function() {
            e.initLoading = !0, e.loadmore = !1, e.hasmore = !1, e.waiting = !1
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
                feed_id: e.feeditems[t].feed_id,
                resume_id: e.feeditems[t].resume_id,
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
    $(".select-btn-more>a").on("click", function(e) {
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
            salary_min = t.find('input[name="salary_min"]').val(),
            salary_max = t.find('input[name="salary_max"]').val(),
            r = t.find('textarea[name="job_desc"]').val(),
            skill_required = t.find('textarea[name="skill_required"]').val();
        if (r == window.feed_edit_jd_old) return t.find('textarea[name="job_desc"]').focus(), !1;
        var o = t.find('button[type="submit"]').html("正在保存");
        o.addClass("submitting"), $.post(n, {
            salary_min: salary_min,
            salary_max: salary_max,
            job_desc: r,
            skill_required: skill_required
        }, function(e) {
            o.removeClass("submitting"), o.html("保存"), e && e.status === true ? (window.feed_edit_jd_old = r, o.prev().remove(), $('<span style="margin-right: 10px; color:green;">已保存!</span>').insertBefore(o).fadeOut(1500, function() {
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
    $('#show_knowed').on('click', function(e){
        e.preventDefault();
        var $this = $(this),
            $knowed = $('#knowed');
        $this.css('display', 'none');
        $knowed.css('display', 'block');
    });
}),

window.subscribe = function( res ){
    if( res && res.status == 'ok' ){
        if( res.show_mission ){
            $('#JS_username').html( res.username );
            $('#JS_mission_time').html( res.mission_time );
            $('.modal-backdrop-tip,.modal-tip').show();
            $('.modal-dialog-tip').css({
                marginTop: ( $(window).height() - $('.modal-dialog-tip').height() ) / 2 + 'px'
            });
        }else if( res.redirect_url ){
            $.alert( '<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>操作成功！</p>' , function(){
                location.href = res.redirect_url;
            } , '' , {
                confirmByShadow: true
            });
        };
    };
},

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
    });

    $('#btn-feed-submit').on( 'click' , $.commonAjax);

}();
