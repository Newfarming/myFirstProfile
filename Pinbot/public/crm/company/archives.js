$(function() {
    $('#clear_query_btn').click(function() {
       $('#select_admin').val('-1');
       $('#search_form').submit();
   });

   $('#export_all').click(function() {
       var $admin_id = $('#select_admin').find("option:selected").val();
       if ($admin_id == -1) {
           $admin_id = 0;
       }
       window.open('/crm/company/export_all/' + $admin_id + '/');
   });
   // 添加下拉列表查找
    $(".select2").select2();
    $('.change_status').click(function() {
        var the_id = $(this).attr("the_id");
        var order_id = $(this).attr("order_id");
        var type = $(this).prev().val();
        var csrftoken = document.cookie.match('(^|;) ?' + 'csrfmiddlewaretoken' + '=([^;]*)(;|$)');
        switch(type) {
            case ("success"):
                var url = '/vip/apply_user_manual_service/' + the_id +'/';
                var data = 'sucess';
                break;
            case ("continue"):
                var url =  '/vip/apply_user_manual_service/' + the_id + '/';
                var data = {'pay_status': 'continue'};
                break;
            case ("refunded"):
                var url =  '/vip/order/confirm_refund/' + order_id + '/';
                var data = '';
                break;
            case ("finished"):
                var url =  '/vip/manual_service/finished_form/' + the_id + '/';
                var data = '';
                break;
        }
        $.post(url, data, function(result){
            location.reload();
        });
    });
});
