$(function() {

    //删除评价
    $(".table").undelegate(".delete_remark").delegate(".delete_remark", "click", function(){
        var delete_remark_id = $(this).attr("remark_id")
        var csrf = document.cookie.match('(^|;) ?' + 'csrftoken' + '=([^;]*)(;|$)');
        $.post('/crm/delete_remark/',{'csrfmiddlewaretoken': csrf, 'remark_id': delete_remark_id}, function(result){
            location.reload();
        })
    })

    //修改求职状态
    $("#sleect_job_status").on("click", "li", function (event) {
        var $this = $(this),
        job_status = $this.text();
        $.post("/crm/candidate/update_jobstatus/",{
            job_status: job_status,
            resume_id: $("#resume_id").val()
        },
               function(result) {
                   if (result.status == 'ok'){
                       $("#show_job_status").text(job_status);
                   }
                   else{
                       alert(result.msg);
                   }
               });
    });

    //删除候选人标签
    $(".tag a").on("click", function (event) {
        var names = [];
        var ids = [];
        var $this = $(this);
        names.push($this.attr('data-name'));
        ids.push($this.attr('data-id'));

        $.post("/crm/candidate/del_tag/",{
            tag_names: names,
            tag_ids: ids,
            resume_id: $("#resume_id").val()
        },
               function(result) {
                   if (result.status == 'ok'){
                       $this.parent().remove();
                   }
                   else{
                       alert(result.msg);
                   }
               });
    });
    //添加候选人标签
    var tag_names = [];
    var tag_ids = [];
    $("#btn_post_tags").on("click", function (event) {
        $('#sys_tags_span .btn-primary').each(function(){
            var $this = $(this),
            id = $this.attr('data-id'),
            name = $this.attr('data-name');
            tag_names.push(name);
            tag_ids.push(id);
        });
        $("#btn_post_tags").attr('disabled',"true");

        $.post("/crm/candidate/add_tag/", {
            tag_names: tag_names,
            tag_ids: tag_ids,
            resume_id: $("#resume_id").val()
        },
        function(result) {
            if (result.status == 'ok'){
                alert('添加标签成功!');
                $("#add_tag").modal('hide');
                window.location.reload();
            }
            else{
                alert(result.msg);
            }
        });
        tag_names = [];
        tag_ids = [];
    });

    $("#add_tag").on("click", "button", function (event) {
        var toggled = $(this).data('toggled');
        $(this).data('toggled', !toggled);
        if (!toggled) {
            $(this).removeClass("btn-default");
            $(this).addClass("btn-primary");
        }
        else {
            $(this).removeClass("btn-primary");
            $(this).addClass("btn-default");
        }
    });

    // 发布推荐定制
    __admin_utils.request_api($('.pub_feed_btn'));

    // 屏蔽推荐定制
    __admin_utils.request_api($('.block_feed_btn'));

    // Change hash for page-reload
    var url = document.location.toString();
    if(url.match('#')){
        $('.nav-tabs a[href=#'+url.split('#')[1]+']').tab('show');
    }
    $('.nav-tabs a').on('shown.bs.tab', function(e){
        window.location.hash = e.target.hash;
    });
});
