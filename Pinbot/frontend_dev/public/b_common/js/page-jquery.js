// jQuery分页插件
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

//如何调用
/*$(obj).createPage({
    pageCount:pageCount,
    current: 1,
    backFn: function(p) {
        //p为当前页数
    }
});*/
