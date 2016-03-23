$(function() {
    var $uncontact = $('#tab_uncontact'),
        $overview = $('#overview_div'),
        $select_job = $('#select_job'),
        $overview_form = $('#overview_form'),
        $job = $('#tab_job'),
        $interview = $('#tab_interview'),
        $offer = $('#tab_offer'),
        $entry = $('#tab_entry'),
        $eliminate = $('#tab_eliminate'),
        $contacted = $('#tab_contacted');

    var select_array = [
        $uncontact,
        $overview,
        $select_job,
        $overview_form,
        $job,
        $interview,
        $offer,
        $entry,
        $eliminate,
        $contacted
    ]

    var load_data = function(e) {
        var api_url = e.data('url');
        e.load(api_url);
    };
    select_array.map(load_data);

    $('#tab_content').on("click", ".job_status", function (event) {
        var $this = $(this),
            job_status = $this.text();
        var resume_id = $this.parent().data("resume_id");
        var record_id = $this.parent().data('record_id');

        $.post(
            "/crm/candidate/update_jobstatus/",
            {
                job_status: job_status,
                resume_id: resume_id
            },
            function(result) {
                if (result.status == 'ok'){
                    $("#show_job_status_"+resume_id).text(job_status);
                }
                else{
                    alert(result.msg);
                }
            }
        );
        $.get(
            "/crm/company/contact/" + record_id + "/",
            function(result){
                if (result.status != 'ok'){
                    alert(result.msg);
                }
            }
        );
    }).on('click', '.overview_list_pager a', function(e) {
        e.preventDefault();
        var $btn = $(this),
            api_url = $btn.attr('href'),
            $container = $btn.parents('.tab-pane');

        if (api_url === '#') {
            return false;
        }
        $container.load(api_url);

    }).on('click', '#query_overview_btn', function(e) {
        var data = $overview_form.serialize(),
            api_url = $(this).data('url');

        $overview.load(api_url+'?'+data);

    }).on('click', '#select_all_btn', function(e) {
        var $check_resume = $('.overview_resume:checked'),
            $uncheck_resume = $('.overview_resume:not(:checked)');
        $check_resume.prop('checked', false);
        $uncheck_resume.prop('checked', true);

    }).on('click', '#export_btn', function(e) {
        $('#export_table').tableExport({
            type: 'csv',
            escape: 'false',
            tableName: '候选人',
            ignoreColumn: [1]
        });

    }).on('change', '.recruit_num_input', function(e) {
        var $input = $(this),
            api_url = $input.data('url'),
            value = $input.val();

        $.getJSON(api_url, {'recruit_num': value}, function(data) {
            alert(data.msg);
        });
    });

    // Change hash for page-reload
    var url = document.location.toString();
    if(url.match('#')){
        $('.nav-tabs a[href=#'+url.split('#')[1]+']').tab('show');
    }
    $('.nav-tabs a').on('shown.bs.tab', function(e){
        window.location.hash = e.target.hash;
    });
    $('#reservation').daterangepicker();

});
