$.SetKeyword = (function($, undefined) {
    var keyword = function(params) {
        return new keyword.prototype.init(params);
    };
    keyword.prototype = {
        init: function(params) {
            this.setting = params;
            __setKeyword = this;
            this.addHtml();
            this.bindEvent();
        },
        escEvent: function(e) {
            if (e.keyCode == 27) {
                __setKeyword.close();
            };
        },
        bindEvent: function() {
            $(window).on('keyup', window, __setKeyword.escEvent);
        },
        add: function() {
            html = '<tr>' +
                '<td class="flag-td">' + ($('.editbox-table tbody tr').length + 1) + '</td>' +
                '<td title="主题词进行分词后，每个词进行同义词扩展得到若干同义词集合, 简历中必须包含每个集合中至少一个词。"><div><input class="latent_semantic_keywords"></div></td>' +
                '<td title="简历中必须包含所有必含词."><div><input class="necessary_keywords" ></div></td>' +
                '<td title="简历中不能包含任意一个屏蔽词."><div><input class="exclude_job_keywords"></div></td>' +
                '<td class="action-td"><div><a href="javascript:;" onclick="__setKeyword.remove( this );">删除</a></div></td>' +
                '</tr>';
            return html;
        },
        addNew: function() {
            var html = this.add();
            $('.editbox-table tbody').append(html);
        },
        //修改定制
        editFeed: function() {
            $('.feed-nav li').each(function(i){
                if($(this).attr('class').match(/curr/i)){
                    if($(this).find('a').attr('href').match(/^#\/group\/([0-9a-z]+)/i)){
                        window.open('http://da.pinbot.me/admin/feed/edit/?url=%2Fadmin%2Ffeed%2F&id=' + RegExp.$1);
                        return false;
                    }
                }
            });
            return false;
        },
        remove: function(dom) {
            $(dom).closest('tr').remove();
            this.order();
        },
        order: function() {
            var list = $('.flag-td');
            list.each(function(i, v) {
                this.innerHTML = i + 1;
            });
        },
        addHtml: function() {
            var list = function(arr) {
                    var html = '';

                    if (!list.length) {
                        html = this.add();
                        return html;
                    };

                    for (var i = 0, l = arr.length; i < l; i++) {
                        var item = arr[i];

                        html += '<tr data-op_time="' + (item.op_time || '') + '" data-username="' + (item.username || '') + '">' +
                            '<td class="flag-td">' + (i + 1) + '</td>' +
                            '<td title="主题词进行分词后，每个词进行同义词扩展得到若干同义词集合, 简历中必须包含每个集合中至少一个词。"><div><input class="latent_semantic_keywords" value="' + (typeof item.latent_semantic_keywords == 'object' ? item.latent_semantic_keywords.join(' ') : item.latent_semantic_keywords) + '"></div></td>' +
                            '<td title="简历中必须包含所有必含词."><div><input class="necessary_keywords" value="' + (typeof item.necessary_keywords == 'object' ? item.necessary_keywords.join(' ') : item.necessary_keywords) + '"></div></td>' +
                            '<td title="简历中不能包含任意一个屏蔽词."><div><input class="exclude_job_keywords" value="' + (typeof item.exclude_job_keywords == 'object' ? item.exclude_job_keywords.join(' ') : item.exclude_job_keywords) + '"></div></td>' +
                            '<td class="action-td"><div><a href="javascript:;" onclick="__setKeyword.remove( this );">删除</a></div></td>' +
                            '</tr>';
                    };
                    return html;
                },
                html = '<div class="wp-popup">' +
                '<div class="popup popup-enter">' +
                '<div class="popup-loading" id="JS_loading_img" style="display:none;"></div>' +
                '<div class="popup-hd clearfix">' +
                '<h3 class="popup-title">添加备注(多个词间用空格隔开)</h3>' +
                '<span class="span-switch">' +
                '<input type="checkbox" id="switch1" name="switch1" class="switch" ' + (this.setting.ignored.toString() == 'true' ? 'checked="checked"' : '') + '>' +
                '<label for="switch1">点击绿色后屏蔽用户填写的关键词</label>' +
                ' </span>' +
                '</div>' +
                '<div class="popup-bd">' +
                '<div id="editbox">' +
                '<div class="editbox-table"><div style="float:right;width:200px;text-align:right;">? <a href="https://tower.im/s/8cOFt" target=_blank>帮助文档</a></div>1、一行为一个条件,条件内为"且"关系,条件间为"或"关系;<br>2、以下关键词过滤逻辑：分别为"同义词扩展过滤"、"强过滤"、"强过滤"。<br>' +
                '<table>' +
                '<thead>' +
                '<tr>' +
                '<th class="flag-th">◊</th>' +
                '<th title="主题词进行分词后，每个词进行同义词扩展得到若干同义词集合, 简历中必须包含每个集合中至少一个词。"><span>主题词 <strong></strong></span></th>' +
                '<th title="简历中必须包含所有必含词."><span>必含词 <strong></strong></span></th>' +
                '<th title="简历中不能包含任意一个屏蔽词."><span>屏蔽词 <strong></strong></span></th>' +
                '<th class="action-th">操作</th>' +
                '</tr>' +
                '</thead>' +
                '<tbody>' +
                list(this.setting.remarks) +
                '</tbody>' +
                '</table>' +
                '</div>' +
                '</div> ' +
                '</div>' +
                '<div class="popup-action" style="display: block;">' +
                '<a href="javascript:;" class="action-add" onclick="__setKeyword.addNew();">+ 新增条件</a> ' +
                '<a href="javascript:;" class="action-edit-feed" onclick="__setKeyword.editFeed();">修改定制</a> ' +
                '<a href="javascript:;" class="action-ok" onclick="__setKeyword.save();">保存</a> ' +
                '<a href="javascript:;" class="action-cancel" onclick="__setKeyword.close();">取消</a> ' +
                '</div>' +
                '</div> ' +
                '</div>';
            $('body').append(html);
        },
        save: function() {
            var list = $('.editbox-table tbody tr'),
                obj = {
                    remarks: []
                },
                that = this;
            obj.ignored = $('#switch1').prop('checked');
            for (var i = 0, l = list.length; i < l; i++) {
                var tr = list.eq(i),
                    keyObj = {},
                    op_time = tr.attr('data-op_time') || '',
                    username = tr.attr('data-username') || '';
                var necessary_keywords = tr.find('.necessary_keywords')[0].value,
                    latent_semantic_keywords = tr.find('.latent_semantic_keywords')[0].value,
                    exclude_job_keywords = tr.find('.exclude_job_keywords')[0].value;
                keyObj.necessary_keywords = necessary_keywords;
                keyObj.latent_semantic_keywords = latent_semantic_keywords;
                keyObj.exclude_job_keywords = exclude_job_keywords;
                keyObj.op_time = op_time;
                keyObj.username = username;
                obj.remarks.push(keyObj);
                //console.log('obj.remarks',obj.remarks);
            };
            obj.___ = new Date().getTime();
            var str = JSON.stringify(obj);

            var tempRemarks = [];
            for (var i in obj.remarks) {
                if (obj.remarks.hasOwnProperty(i)) {
                    if (obj.remarks[i].necessary_keywords.trim() !== "" || obj.remarks[i].latent_semantic_keywords.trim() !== "" || obj.remarks[i].exclude_job_keywords.trim() !== "") {
                        tempRemarks.push(obj.remarks[i]);
                    }else{
                        alert('请至少填写一项关键词');
                        return false;
                    }
                }
            }
            /*if(tempRemarks.length==0){
                alert('无数据保存');
                return false;
            }*/
            //console.log('tempRemarks', tempRemarks);

            if (tempRemarks.length >= 0) {
                obj.remarks = tempRemarks;
                str = JSON.stringify(obj);

                $.post('/feed/edit_remarks/' + that.setting.feed_id + '/', str, function(res) {
                    $('#JS_loading_img').hide();
                    if (res && res.status == 'ok') {
                        var $doms = $('.JS_set_keyword');
                        $doms.each(function(index, value) {
                            var $dom = $doms.eq(index);
                            if ($dom.attr('data-feedid') == that.setting.feed_id) {
                                delete obj.__;
                                delete obj.feed_id;
                                $dom.attr('data-remarks', JSON.stringify(obj));
                                return false;
                            };
                        });
                        // alert('保存成功！');
                        that.close();
                    } else if (res && res.msg) {
                        alert(res.msg);
                    } else {
                        alert('请求失败！');
                    };
                }, 'json').fail(function() {
                    alert('请求失败！');
                    $('#JS_loading_img').hide();
                });
                $('#JS_loading_img').show();
            } else {
                this.close();
            }

        },
        close: function() {
            $('.wp-popup').remove();
            $(window).off('keyup', __setKeyword.escEvent);
            __setKeyword = null;
        }
    };
    keyword.prototype.init.prototype = keyword.prototype;
    return function(params) {
        keyword(params);
    };
})(jQuery);