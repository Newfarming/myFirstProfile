var report_name = $("#report_name").val();

var report_type = $("#report_type").val();
var data_url = '/dash/report/'+report_type+'/get_data/'+report_name+'/';
var data_block = $("#data_block_"+report_name);
var data_table = $("#data_table_"+report_name);

console.log(data_url);
function init_data(){
    data_block.show();
    data_table.attr("data-url", data_url);
}

$(function() {
    $('input[name="daterange"]').daterangepicker({
        format: 'YYYY-MM-DD',
        dateLimit: { days: 180 },
        showDropdowns: true,
        locale: {
            applyLabel: '确定',
            cancelLabel: '取消',
            fromLabel: '开始日期',
            toLabel: '截止日期',
            customRangeLabel: '自定义',
            daysOfWeek: ['周日', '周一', '周二', '周三', '周四', '周五','周六'],
            monthNames: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
            firstDay: 1
        }
    });


});
function export_csv(){
    data_table.tableExport({type:'csv'});
}

function filter_data(){

    var date_range = $("#daterange").val();
    date_range = date_range.replace(/\s/g, '');
    console.log( data_url + date_range)
    data_table.bootstrapTable('refresh', {
        url: data_url + date_range
    });
}

init_data();