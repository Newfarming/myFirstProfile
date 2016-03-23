$(function(){
	//获取url，更改feed_status check框
	var url = window.location.href;
	if (url.indexOf('waiting') != -1) {
		$('.waiting').find('input')[0].checked = true;
	};
	//tr行点击
	$('tr.hover-layer').each(function(){
		var $this = $(this);
		var url = $($this.find('td')[1]).find('a').attr('url');
		$this.on('click', function(e){
			window.location.href = url;
		});
	});
	//会话点击
	$('.chat').on('click', function(e){
		e.stopPropagation();
	});
	//还未反馈的简历
	$('.waiting').find('input').on('click', function(){
		var static_url = window.location.origin;
		var $this = $(this);
		if($this[0].checked){
			window.location.href = static_url + '/feed/receive_resume/?feed_status=waiting';
		} else {
			window.location.href = static_url + '/feed/receive_resume/?feed_status=';
		}
	});
});