/* CRM 通用JS组件 */

__admin_utils = {

    // 查询表单参数回填
    show_params: function(q_form) {
        var q_args_json = q_form.attr('q_args_json');
        var get_args = $.parseJSON(q_args_json);
        if($.isEmptyObject(get_args)){
            $('.default_active').addClass('active');
        }
        else{
            _.each(get_args, function(val, name) {
                var $field = q_form.find('[name='+name+']');
                var field_type = $field.attr('type');
                if(field_type === 'checkbox') {
                    _.each(val, function(v) {
                        _.each($field, function(el) {
                            var $el = $(el);
                            if($el.attr('value') == v) {
                                $el.attr('checked', true);
                            }
                        });
                    });
                }
                else {
                    $field.val(val[0]);
                    var $btn_field = q_form.find('[field_name='+name+']');
                    if($btn_field.length > 0) {
                        $btn_field.removeClass('active');
                        $btn_field.siblings('[value='+val[0]+']').addClass('active');
                    }
                }
            });
        }
    },

    // form clear
    form_clear: function(form) {
        form.find('input[type=text]').val('');
        form.find('input[type=hidden][need_clear]').val('');
        form.find('select').val('');
        form.find('input[type=checkbox]').attr('checked', false);
        form.find('button[field_name]').removeClass('active');
        form.find('button[field_name][value=""]').addClass('active');
    },

    // 清空按钮
    clear_btn: function(btn, form) {
        var a_utils = this;
        btn.click(function(e) {
            e.preventDefault();
            a_utils.form_clear(form);
            form.submit();
        });
    },

    // 通用按钮提交
    request_api: function($btn, callback) {
        $btn.on('click', function(e) {
            var $this = $(this),
            confirm_msg = $this.data('confirm_msg') || '请确定执行？',
            method = $this.data('method') || 'get',
            request_data = $this.data(),
            api_url = $this.data('api_url'),
            confirm_result = confirm(confirm_msg);

            if (!confirm_result) {
                return false;
            }

            if (method === 'get') {
                $.getJSON(api_url, request_data, function(ret) {
                    alert(ret.msg || '操作成功');
                    if (ret.status === 'ok' && typeof(callback) === 'function') {
                        callback()
                    } else if (res.status === 'ok') {
                        window.location.reload();
                    }
                });
            }

            if (method === 'post') {
                $.post(api_url, request_data, function(ret) {
                    alert(ret.msg || '操作成功');
                    if (ret.status === 'ok' && typeof(callback) === 'function') {
                        callback()
                    } else if (res.status === 'ok') {
                        window.location.reload();
                    }
                });
            }
        });
    }
};
