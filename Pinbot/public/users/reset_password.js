var signResult = function( res ){
    location.href = '/special_feed/page/';
};
var beforeSubmit = function(){
	var form = $('#JS_resetpassword_form'),
		pwd = form.find( '[name="password"]' ).val(),
		rePwd = form.find( '[name="confirm_password"]' ).val();
	if( !pwd || !rePwd || pwd != rePwd ){
        $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>两次输入密码不一致！</p>');
		form.find( '[name="password"]' ).addClass('tip-error');
		form.find( '[name="confirm_password"]' ).addClass('tip-error');
		return false;
	};
	return true;
};
var signErrorResult = function( res ){
	var msg = res.msg,
		form = $('#JS_register_form'),
		tip = msg.substring( msg.indexOf( ':' ) + 1 );
	if( /密码/.test( msg ) ){
		form.find( '[name="password"]' ).addClass('tip-error');
		form.find( '[name="confirm_password"]' ).addClass('tip-error');
	};
    $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + tip + '</p>');
};
$(function(){
    $( document ).on( 'click' , '#JS_reset_password' , function(){
        $.commonAjax.call(this);
    });
});