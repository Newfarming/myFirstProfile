
var useragent=navigator.userAgent.toString();
var isMobile=useragent.match(/ mobile/i);
if(1==1){
    //修复placeholder动画效果
    $("input.big-placeholder").focus(function() {
        if ($(this).parent().find('label:nth-child(1)').length == 1) {
            var label = $(this).parent().find('label:nth-child(1)');
            $(label).removeClass('pc-hide');
        }
    });
    $("input.big-placeholder").blur(function() {
        if ($(this).parent().find('label:nth-child(1)').length == 1) {
            var label = $(this).parent().find('label:nth-child(1)');
            if (!$(label).hasClass('pc-hide') && $(this).prop("value") == "") {
                $(label).addClass('pc-hide');
            }
        }
    });
    $("input.big-placeholder").change(function() {
        if ($(this).parent().find('label:nth-child(1)').length == 1) {
            var label = $(this).parent().find('label:nth-child(1)');
            if (!$(label).hasClass('pc-hide') && $(this).prop("value") == "") {
                $(label).addClass('pc-hide');
            } else if ($(this).prop("value") != "") {
                if($(label).hasClass('pc-hide')) $(label).removeClass('pc-hide');
            } else {
                if(!$(label).hasClass('pc-hide')) $(label).addClass('pc-hide');
            }
        }
    });
    $("input.big-placeholder").keydown(function() {
        if ($(this).parent().find('label:nth-child(1)').length == 1) {
            var label = $(this).parent().find('label:nth-child(1)');
            if ($(this).prop("value") == "") {
                if(!$(label).hasClass('pc-hide')) $(label).addClass('pc-hide');
            } else if ($(this).prop("value") != "") {
                if($(label).hasClass('pc-hide')) $(label).removeClass('pc-hide');
            } else {
                if(!$(label).hasClass('pc-hide')) $(label).addClass('pc-hide');
            }
        }
    });
}



$(document).ready(function() {
    
});