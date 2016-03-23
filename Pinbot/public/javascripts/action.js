
$(function() {

	var href = window.location.href.split('/');               
 	var id = href[(href.indexOf('display') + 1)] || '';

	var text = {
		add: '<i class="icon-star-empty"></i>关注',
		remove: '<i class="icon-star-empty"></i>取消关注'
	};

	var cname = {
		add: 'btn_add_watch',
		remove: 'btn_remove_watch'
	}

	var $comments = $('.comment');
	var $textarea = $comments.find('textarea');
	var get_comments = function() {
		return $.trim($textarea.val());
	}
	

	$('.btn_add_watch, .btn_remove_watch').on('click', function() {
		var $thisButton = $(this);
		if ($thisButton.hasClass(cname.add)) {
			$.get('/resumes/add_watch/' + id, function(result) {
				if (result && result.status) {
					$thisButton.removeClass(cname.add).addClass(cname.remove).html(text.remove);
				}
			});
		} else if ($thisButton.hasClass(cname.remove)) {
			$.get('/resumes/remove_watch/' + id, function(result) {
				if (result && result.status) {
					$thisButton.removeClass(cname.remove).addClass(cname.add).html(text.add)
				}
			});

		}
 	});


	$('.btn_discard_resume').on('click', function() {          
		$.get('/resumes/discard_resume/' + id, function(result) {
			if (result && result.status) {
				window.location.href = '/resumes/all'; 
			}
		})
	});

	$('.comment').find('input[type="submit"]').on('click', function() {
		var content = get_comments() || '';
		if (content.length) {
			$.post('/resumes/add_comment/' + id, { comment:content}, function(result) {
				if (result && result.status) {
					window.location.reload();	
				} else {
					alert('提交失败，请重试!');
				}
			});
		} else {
			alert('请填写好备注!')
		}
	});
});

        
