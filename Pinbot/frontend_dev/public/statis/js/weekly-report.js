// Run the script on DOM ready:
$(function(){
	$('table##userInfo').visualize({type: 'line',colFilter: ':not(:first-child)',rowFilter: ':not(:last-child)'});
                         
});