$(function() {
    __admin_utils.show_params($('#search_form'));

    $('.cancel_assign').on('click', function() {
        var client_id = $(this).attr('data-client_id');
        $.post('/crm/company/cancel_assign/', {'client_id': client_id}, function(data){
            if (data.status == 'ok'){
                window.location.reload();
            }
        });
    });

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
});
