function countDown(secs, surl) {
    var jumpTo = $('.jumpTo')[0];
    if(jumpTo.innerHTML != null){
    	jumpTo.innerHTML = secs;
	    if (--secs > 0) {
	        setTimeout("countDown(" + secs + ",'" + surl + "')", 1000);
	    }
	    else {
	        window.location.href = surl;
	    }
    }
}
$(function(){
	//点击发送激活邮件
	$('.send_active').on('click', function(){
        var $this = $(this);
        var email = $this.attr('email');
        $.ajax({
            type: 'get',
            dataType: 'json',
            url: '/account/send_active_email/' + email,
            success: function(data){
                if (data && data.status && data.status == 'ok'){
                    $('label').html(data.msg).css('display', 'block');
                } else if(data && data.status && data.status == 'malice'){
                    $('label').html(data.msg).css('display', 'block');
                }
            }
        });
    });
	countDown(5, '/account/login');
});