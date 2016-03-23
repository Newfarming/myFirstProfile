$(function() {
    __admin_utils.show_params($('#search_form'));
    __admin_utils.clear_btn($('#clear_query_btn'), $('#search_form'));
    // 添加下拉列表查找
    $(".select2").select2();
});
