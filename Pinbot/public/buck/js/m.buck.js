$(function(){
    var resize = function(){
            var wHeight = $( window ).height();
            $('.fullscreen').css({
                height: wHeight + 'px'
            });
        };
    resize();
    $( window ).on( 'resize' , window , resize );

    $('.message,.sign-btn').addClass('active');
});