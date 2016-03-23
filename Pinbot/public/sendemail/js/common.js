//数据初始化
var tpl_id = 1;
var tpl_content = '';
var tag_id = '';
var post_data = {};
var tmp_category_id = '';

//预览邮件
function preview_email(content){
    $("#preview_content").html($('#id_content').code());
    $("#preview_modal").modal('show');
};

//加载邮件模板内容 根据id
function load_template(tplId){
    $.getJSON("/email/get_tpl/"+tplId, function( data ) {
        //change template
        tpl_content = data.template_content;
        $('#id_content').code(tpl_content);
        $('#send_email_title').val(data.template_title);
        tmp_category_id =data.category_id;
    });
};


//检查用户选择
function check_select_user(){
    post_data['test_users'] = false;
    post_data['b_user'] = false;
    post_data['c_user'] = false;
    post_data['b_unactive_user'] = false;
    if ($("#test_users").is(":checked")){
        post_data['test_users'] = true;
    }
    if ($("#b_user").is(":checked")){
        post_data['b_user'] = true;
    }
    if ($("#c_user").is(":checked")){
        post_data['c_user'] = true;
    }
    if ($("#b_unactive_user").is(":checked")){
        post_data['b_unactive_user'] = true;
    }
}


$("#tpl_id").change(function() {
    tpl_id = $(this).find(':selected')[0].id;
    load_template(tpl_id);
});

$('input[name="tag"]').click(function() {
  tag_id =  $('input[name="tag"]:checked').val();
});

//发送邮件
function send_email(){
    post_data['tpl_id'] = tpl_id;
    post_data['tpl_content'] = $('#id_content').code();
    post_data['tag_id'] = tag_id;
    post_data['sendto'] = $("#sendto").val();
    post_data['email_title'] = $("#send_email_title").val();
    check_select_user();
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/email/send/",
        data: JSON.stringify(post_data),
        success: function(result){
          if (result.message == 'success')
          {
            alert('send success!');
          }
          else
          {
            alert(result.message);
          }
        },
        error: function(msg){
          alert("error");
        }
    });
  };

//添加标签
function add_tag(){
    $.post("/email/add_tag/",{ tag_name: $("#tag_name").val()},
    function(result) {
      if (result.status == 'ok'){
        console.log(result);
        $("#add_tag_modal").modal('hide');
          $(".tags_choice").append(
            '<span id="tag_'+result.tag_id+'">'+
            '<input type="radio" checked="checked" name="tag" value="'+result.tag_id+'" />'+result.tag_name+
            '<a class="btn btn-xs btn-danger remove_fields" onclick="delete_tag('+result.tag_id+');">'+
            '<i class="glyphicon glyphicon-remove"></i></a>'+
            '&nbsp;&nbsp;</span>'
          );
          tag_id = result.tag_id;
      }
      else{
        alert(result.msg);
      }
    });
};

//ajax save template
function save_email_tpl(tplid){

    var tplID = tplid
    if (tplid == ''){
        tplID = tpl_id;
    }

    post_data = {
        'name':$("#send_email_title").val(),
        'content':$('#id_content').code(),
        'category':tmp_category_id
    }
    console.log(post_data);
    console.log(tplID);
    $.post("/email/edit_tpl/"+tplID+'/', post_data,
    function(result) {
        alert(result.msg);
    });
};

//ajax add template
function add_email_tpl(){
    post_data = {
        'category':$("#id_category").val(),
        'name':$("#send_email_title").val(),
        'content':$('#id_content').code(),
    }
    console.log(post_data);

    $.post("/email/add_tpl/", post_data,
    function(result) {
        alert(result.msg);
    });
};

//ajax delete tag
function delete_tag(tag_id){

    var r = confirm("您确定删除此标签吗!");
    if (r == true) {
        post_data = {
            'tag_id':tag_id
        }
        console.log(post_data);
        $.post("/email/del_tag/", post_data,
        function(result) {
            if (result.status == 'ok'){
                $('#tag_'+tag_id).remove();
            }
            else
            {
                alert('删除失败');
            }
        });
    }
};



