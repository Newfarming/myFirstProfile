var signResult = function( res ){
    $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>激活邮件已发至您的邮箱，请尽快激活账号！</p>');
	$('#JS_register_form').find('input.input').val('').find('.drop-down li').eq(0).click();

};
var beforeSubmit = function(){
	var form = $('#JS_register_form'),
		pwd = form.find( '[name="password"]' ).val(),
		rePwd = form.find( '[name="confirm_password"]' ).val();
	if( pwd != rePwd ){
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
	if( /(邮箱)|(用户名)/.test( msg ) ){
		form.find( '[name="user_email"]' ).addClass('tip-error');
	};
	if( /密码/.test( msg ) ){
		form.find( '[name="password"]' ).addClass('tip-error');
		form.find( '[name="confirm_password"]' ).addClass('tip-error');
	};
	if( /姓名/.test( msg ) ){
		form.find( '[name="name"]' ).addClass('tip-error');
	};
	if( /电话/.test( msg ) ){
		form.find( '[name="phone"]' ).addClass('tip-error');
	};
	if( /qq/i.test( msg ) ){
		form.find( '[name="qq"]' ).addClass('tip-error');
	};
	if( /角色/.test( msg ) ){
		form.find( '[name="role"]' ).siblings('.button').addClass('tip-error');
	};
	if( /企业名称/.test( msg ) ){
		form.find( '[name="company_name"]' ).addClass('tip-error');
	};
	if( /公司网站/.test( msg ) ){
		form.find( '[name="url"]' ).addClass('tip-error');
	};
    $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + tip + '</p>');

};
$(function(){
    $( document ).on( 'click' , '#JS_sign_parter' , function(){
        var $this = $( this );
        if( $this.attr('disabled') ) return false;
        $.commonAjax.call(this);
    });
});