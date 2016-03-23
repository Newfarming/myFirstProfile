/*
    author: 516758517@qq.com
    date:  2014-09-28
    description: 企业名片JS文件
 */

$.CompanyInfo = function( setting ){
    return new $.CompanyInfo.prototype.init( setting );
};
$.CompanyInfo.prototype = {
    constructor: $.CompanyInfo,
    init: function( setting ){
        this.setting = $.extend({
            style: window.infos && window.infos.company && window.infos.company.key_points ? 'info' : 'edit'
        }, setting );

        window.$_companyInfo = this;
        this.appendContent( this.getHtml() );
    },
    getHtml: function( style ){
        style = style || window.$_companyInfo.setting.style;
        var html = '',
            info = window.infos && window.infos.company ? window.infos.company : false,
            company_name = info && info.company_name ? info.company_name : '',
            key_points = info && info.key_points ? info.key_points : '',
            desc = info && info.desc ? info.desc : '',
            company_stage = info && info.company_stage ? info.company_stage : '',
            product_url = info && info.product_url ? info.product_url : '',
            areas = infos && infos.all_company_category ? infos.all_company_category : [],
            getAreaHtml = function( arr , canSelect ){
                var html = '';
                for( var i = 0 , l = arr.length ; i < l ; i++ ){
                    var area = arr[ i ],
                        id = area.id,
                        name = area.category,
                        select = area.select;
                    if( canSelect ){
                        html += '<a data-id="' + id + '" class="area' + ( select ? ' select' : '' ) + '">' + name + '</a>';
                    }else{
                        if( select ){
                            html += '<a data-id="' + id + '" class="area">' + name + '</a>';
                        };
                    };
                };
                return html;
            };
        if( style == 'edit' ){
            html += '<div class="company-card-insert">' +
                    '<form action="" accept-charset="utf-8">' +
                        '<div class="insert-notice">' +
                            '完善企业名片，并在下载简历时选择将企业名片发送给候选人，那么此次简历下载，我们将仅扣除您3个聘宝点数，若候选人通过邮件反馈对您发布的职位感兴趣，我们再扣除您余下9个聘宝点数，若求职者对您发布的职位不感兴趣，将不再扣除您的聘宝点数！' +
                        '</div>' +
                        '<table class="table company-table" width="100%" cellpadding="0" cellspacing="0">' +
                            '<tr>' +
                                '<th><span class="required">企业名称</span></th>' +
                                '<td>' +
                                    '<input type="text" name="company_name" value="' + company_name + '" class="input w526" data-equired data-reg="isNull">' +
                                '</td>' +
                            '</tr>' +
                            '<tr>' +
                                '<th><span class="required">企业亮点</span></th>' +
                                '<td>' +
                                    '<textarea class="textarea w540" placeholder="请尽量精简文字，并适当使用换行，便于候选人阅读哦（140字以内）" name="key_points" maxLength="140" data-lenlimit="140" rows="5" data-equired data-reg="isNull">' + key_points + '</textarea>' +
                                '</td>' +
                            '</tr>' +
                            '<tr>' +
                                '<th><span class="required">企业简介</span></th>' +
                                '<td>' +
                                    '<textarea class="textarea w540" placeholder="请尽量精简文字，并适当使用换行，便于候选人阅读哦（300字以内）" name="desc" maxLength="300" data-lenlimit="300" rows="5">' + desc + '</textarea>' +
                                '</td>' +
                            '</tr>' +
                            '<tr>' +
                                '<th><span class="required">企业发展阶段</span></th>' +
                                '<td>' +
                                    '<input type="text" name="company_stage" value="' + company_stage + '" class="input w526" data-equired data-reg="isNull">' +
                                '</td>' +
                            '</tr>' +
                            '<tr>' +
                                '<th>网址</th>' +
                                '<td>' +
                                    '<input type="text" name="product_url" value="' + product_url + '" class="input w526">' +
                                '</td>' +
                            '</tr>' +
                            '<tr>' +
                                '<th><span class="required">所在领域</span><br><span class="orange">(可选3个)</span></th>' +
                                '<td>' +
                                    '<div class="area-panel clearfix" id="JS_choose_area">' +
                                        getAreaHtml( areas , true ) +
                                    '</div>' +
                                '</td>' +
                            '</tr>' +
                        '</table>' +
                        '<div class="company-submition text-center">';
                            if( window.infos.show_mission ){
                                html += '<a href="javascript:;" title="保存" class="btn btn-large btn-primary" id="JS_save_company">保存并新建定制</a>';
                            }else{
                                html += '<a href="javascript:;" title="保存" class="btn btn-large btn-primary" id="JS_save_company">保 存</a>';
                            };
                            if( company_name ){
                                html += '<a href="javascript:;" title="取消" class="a-blue ml10" id="JS_cancel_edit">取消</a>';
                            };
                            if( window.infos.show_mission ){
                                html += '<p style="color: #666666; line-height:25px; padding-top:10px;"><span class="red simsun">*</span>完成第一个专属定制提交，领取<span style="color:#ff6600;">红包</span><i class="i-envelope"></i></p>';
                            };
                        html +='</div>' +
                    '</form>' +
                '</div>';
        }else{
            desc = desc ? desc : '暂无';
            product_url = product_url ? product_url : '';
            html += '<div class="company-card-show">' +
                        '<h3 class="card-title">' + company_name + '</h3>' +
                        '<ul class="card-details">' +
                            '<li class="clearfix">' +
                                '<strong>企业亮点</strong>' +
                                '<p>' + key_points + '</p>' +
                            '</li>' +
                            '<li class="clearfix">' +
                                '<strong>企业简介</strong>' +
                                '<p>' + desc + '</p>' +
                            '</li>' +
                            '<li class="clearfix">' +
                                '<strong>发展阶段</strong>' +
                                '<p>' + company_stage + '</p>' +
                            '</li>' +
                            '<li class="clearfix">' +
                                '<strong>网址</strong>';
                                if( product_url ){
                                    html += '<p><a href="' + product_url + '" title="" target="_blank" class="a-blue">' + product_url + '</a></p>';
                                }else{
                                    html += '<p>暂无</p>';
                                };

                            html += '</li>' +
                            '<li class="clearfix" style="background-position:31px 13px;">' +
                                '<strong style="margin-top: 4px;">所在领域</strong>' +
                                '<div class="clearfix view">' + getAreaHtml( areas ) + '</div>' +
                            '</li>' +
                        '</ul>' +
                        '<p class="text-right">' +
                            '<a href="javascript:;" title="修改" class="button-default" id="JS_edit_company_info">修改</a>' +
                        '</p>' +
                    '</div>';
        };
        return html;
    },
    saveCompanyAjax: function( data ){
        var url = '/companycard/company/save/',
            that = this,
            updateCategory = function(){
                var cats = data.category,
                    allCats = window.infos.all_company_category,
                    newCats = [];

                    for( var j = 0 , jj = allCats.length ; j < jj ; j++ ){
                        var jCat = allCats[j];
                        jCat.select = false;
                        for( var i = 0 , l = cats.length ; i < l ; i++ ){
                            var id = cats[ i ];
                            if( id == jCat.id ){
                                jCat.select = true;
                            };
                        };
                        newCats.push( jCat );
                    };

                    window.infos.all_company_category = newCats;
            };
        $.post( url , JSON.stringify( data ) , function( res ){
            if( res && res.status == 'ok' ){
                if( window.infos && window.infos.show_mission && res.redirect_url ){
                    location.href = res.redirect_url;
                    return;
                };
                if( !window.infos || !window.infos.company || !window.infos.company.key_points ){
                    that.showAddJob();
                };
                updateCategory();
                window.infos.company = data ;
                window.$_companyInfo.saveAfter();
            }else if( res && res.msg ){
                $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>' + res.msg + '</p>');
            }else{
                $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请求失败，请刷新后再试！</p>');
            };
        }, 'json');
    },
    showAddJob: function(){
        var fun = function(){
            if( $._intentionCard ){
                $._intentionCard.addJob();
                $( '#JS_add_job' ).click();
            }else{
                setTimeout( fun , 100);
            };
        };
        fun();
    },
    saveAfter: function(){
        window.$_companyInfo.appendContent( window.$_companyInfo.getHtml( 'info' ) );
    },
    appendContent: function( html ){
        $('#JS_company_info').html( html );
    }
};
$.CompanyInfo.prototype.init.prototype = $.CompanyInfo.prototype;

$.intentionCard = function( setting ){
    return new $.intentionCard.prototype.init( setting );
};
$.intentionCard.prototype = {
    constructor: $.intentionCard,
    init: function( setting ){
        this.setting = $.extend({
            list: [],
            allowSend: false,  //简历详情页
            synOnly: false,     //新增定制
            contentDom: '#JS_jobs_list',
            callback: null
        }, setting);
        $._intentionCard = this;
        this.appendList( this.getList() );
        if( window.infos && window.infos.company && window.infos.company.key_points && !this.setting.allowSend ){
            if( !window.infos.jobs || $.isEmptyObject(infos.jobs) ){
                this.addJob();
            };
        };
        if( typeof this.setting.callback == 'function' ){
            this.setting.callback();
        };
    },
    templates: function( type , card ){
        var html = '',
            companyName = window.infos && window.infos.company && window.infos.company.company_name ? window.infos.company.company_name : '',
            title = '',
            id = '',
            salary_low = '',
            salary_high = '',
            address = '',
            work_years = '',
            workYearText = {
                '0' : '不限',
                '1' : '一年以上',
                '3' : '三年以上',
                '5' : '五年以上'
            },
            degree = '',
            desc = '',
            skill_desc = '',
            degreeText = {
                '0' : '不限',
                '3' : '专科',
                '4' : '本科',
                '7' : '硕士',
                '10' : '博士'
            };
        if( card ){
            id = card.id;
            title = card.title;
            salary_low = +card.salary_low / 1000;
            salary_high = +card.salary_high / 1000;
            address = card.address;
            work_years = card.work_years;
            degree = card.degree;
            desc = card.desc;
            skill_desc = card.skill_desc;
        };
        switch( type ){
            case 'new':
                html += '<div class="job-panel">' +
                            '<div class="border"></div>' +
                            '<div class="job-info">' +
                                '<a href="javascript:;" title="新增岗位" class="add-job-btn" id="JS_add_job">新增岗位</a>' +
                            '</div>' +
                        '</div>';
                break;
            case 'edit':
                desc = desc == '暂无' ? '' : desc;
                skill_desc = skill_desc == '暂无' ? '' : skill_desc;
                html += '<div class="job-panel">' +
                            '<div class="border"></div>' +
                            '<div class="job-info">' +
                                '<h3 class="card-title arr">' + companyName + '</h3>' +
                                '<div class="job-details">' +
                                    '<form action="" method="get" accept-charset="utf-8">' +
                                        '<table class="table company-table job-table" width="100%" cellpadding="0" cellspacing="0">' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>职位名称</th>' +
                                            '<td>' +
                                                '<input type="text" name="title" value="' + title + '" class="input w220" data-equired data-reg="isNull">' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>薪资范围</th>' +
                                            '<td>' +
                                                '<input type="text" name="salary_low" value="' + salary_low + '" class="input w70 inline" data-equired data-reg="price"> K&nbsp;&nbsp;-&nbsp;&nbsp;<input type="text" name="salary_high" value="' + salary_high + '" class="input w70 inline" data-equired data-reg="price"> K' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>工作地点</th>' +
                                            '<td>' +
                                                '<input type="text" name="address" value="' + address + '" class="input w220" data-equired data-reg="isNull">' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>最低工作年限</th>' +
                                            '<td>' +
                                                '<div class="drop-select left w246" style="*z-index:190">' +
                                                    '<button class="button" type="button" data-toggle="dropdown">' + ( work_years ? workYearText[work_years] : '不限' ) + '<i class="i-barr"></i></button>' +
                                                    '<div class="drop-box">' +
                                                        '<ul class="drop-down">' +
                                                            '<li>' +
                                                                '<a ' + ( work_years == '0' ? 'class="active"' : '' ) + '>不限</a>' +
                                                            '</li>' +
                                                            '<li>' +
                                                                '<a ' + ( work_years == '1' ? 'class="active"' : '' ) + '>一年以上</a>' +
                                                            '</li>' +
                                                            '<li>' +
                                                                '<a ' + ( work_years == '3' ? 'class="active"' : '' ) + '>三年以上</a>' +
                                                            '</li>' +
                                                            '<li>' +
                                                                '<a ' + ( work_years == '5' ? 'class="active"' : '' ) + '>五年以上</a>' +
                                                            '</li>' +
                                                        '</ul>' +
                                                    '</div>' +
                                                    '<select name="work_years" class="JS_proficiency">' +
                                                        '<option value="0" ' + ( work_years == '0' ? 'selected' : '' ) + '>不限</option>' +
                                                        '<option value="1" ' + ( work_years == '1' ? 'selected' : '' ) + '>一年以上</option>' +
                                                        '<option value="3" ' + ( work_years == '3' ? 'selected' : '' ) + '>三年以上</option>' +
                                                        '<option value="5" ' + ( work_years == '5' ? 'selected' : '' ) + '>五年以上</option>' +
                                                    '</select>' +
                                                '</div>' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>最低学历</th>' +
                                            '<td>' +
                                                '<div class="drop-select left w246" style="*z-index:190">' +
                                                    '<button class="button" type="button" data-toggle="dropdown">' + ( degree ? degreeText[degree] : '不限' ) + '<i class="i-barr"></i></button>' +
                                                    '<div class="drop-box">' +
                                                        '<ul class="drop-down">' +
                                                            '<li>' +
                                                                '<a ' + ( degree == '0' ? 'class="active"' : '' ) + '>不限</a>' +
                                                            '</li>' +
                                                            '<li>' +
                                                                '<a ' + ( degree == '3' ? 'class="active"' : '' ) + '>专科</a>' +
                                                            '</li>' +
                                                            '<li>' +
                                                                '<a ' + ( degree == '4' ? 'class="active"' : '' ) + '>本科</a>' +
                                                            '</li>' +
                                                            '<li>' +
                                                                '<a ' + ( degree == '7' ? 'class="active"' : '' ) + '>硕士</a>' +
                                                            '</li>' +
                                                            '<li>' +
                                                                '<a ' + ( degree == '10' ? 'class="active"' : '' ) + '>博士</a>' +
                                                            '</li>' +
                                                        '</ul>' +
                                                    '</div>' +
                                                    '<select name="degree" class="JS_proficiency">' +
                                                        '<option value="0" ' + ( degree == '0' ? 'selected' : '' ) + '>不限</option>' +
                                                        '<option value="3" ' + ( degree == '3' ? 'selected' : '' ) + '>专科</option>' +
                                                        '<option value="4" ' + ( degree == '4' ? 'selected' : '' ) + '>本科</option>' +
                                                        '<option value="7" ' + ( degree == '7' ? 'selected' : '' ) + '>硕士</option>' +
                                                        '<option value="10" ' + ( degree == '10' ? 'selected' : '' ) + '>博士</option>' +
                                                    '</select>' +
                                                '</div>' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th>职位描述</th>' +
                                            '<td>' +
                                                '<textarea class="textarea w275" name="desc">' + desc + '</textarea>' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th>岗位要求</th>' +
                                            '<td>' +
                                                '<textarea class="textarea w275" name="skill_desc">' + skill_desc + '</textarea>' +
                                            '</td>' +
                                        '</tr>' +
                                    '</table>' +
                                    '<p class="job-handles" data-id="' + id + '">' +
                                        '<a href="javascript:;" title="保存" class="button-active JS_save_job">保存</a> ' +
                                        '<a href="javascript:;" title="取消" class="button-default JS_cancel_save">取消</a>' +
                                    '</p>' +
                                    '</form>' +
                                '</div>' +
                            '</div>' +
                        '</div>';
                break;
            case 'info':
                desc = desc == '' ? '暂无' : desc;
                skill_desc = skill_desc == '' ? '暂无' : skill_desc;
                html += '<div class="job-panel">' +
                            '<div class="border"></div>' +
                            '<div class="job-info">' +
                                '<h3 class="card-title arr">' + companyName;
                                if( !this.setting.allowSend && !this.setting.synOnly ){
                                    html += '<a href="javascript:;" class="i-del JS_delete_job" data-id="' + id + '"></a>';
                                };
                                html += '</h3><div class="job-details">' +
                                    '<table class="table company-table job-table" width="100%" cellpadding="0" cellspacing="0">' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>职位名称</th>' +
                                            '<td>' +
                                                '<span>' + title + '</span>' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>薪资范围</th>' +
                                            '<td>' +
                                                '<span>' + salary_low + 'K - ' + salary_high + 'K</span>' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>工作地点</th>' +
                                            '<td>' +
                                                '<span>' + address + '</span>' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>最低工作年限</th>' +
                                            '<td>' +
                                                '<span>' + workYearText[work_years] + '</span>' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th><span class="red simsun">*</span>最低学历</th>' +
                                            '<td>' +
                                                '<span>' + degreeText[degree] + '</span>' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th>职位描述</th>' +
                                            '<td>' +
                                                '<span>' + desc + '</span>' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<th>岗位要求</th>' +
                                            '<td>' +
                                                '<span>' + skill_desc + '</span>' +
                                            '</td>' +
                                        '</tr>' +
                                    '</table>' +
                                    '<p class="job-handles mt31" data-id="' + id + '">';
                                    if( this.setting.allowSend ){
                                        html += '<a href="javascript:;" title="发送" class="button-default JS_send_job_to_user">发送</a> ';
                                    };
                                    if( !this.setting.synOnly ){
                                        html += '<a href="javascript:;" title="修改" class="button-default JS_edit_job_btn">修改</a> ' +
                                        '<a href="/companycard/job/preview/' + id + '/" title="预览" class="button-default" target="_blank">预览</a>';
                                    }else{
                                        html += '<a href="javascript:;" title="同步" class="button-default JS_syn_job_btn">同步</a> ';
                                    };
                                    html += '</p>' +
                                '</div>' +
                            '</div>' +
                        '</div>';
                break;
        };
        return html;
    },
    getList: function(){
        var setting = this.setting,
            list = setting.list,
            page = setting.page,
            html = '',
            obj = {};
        if( !list.length ){
            window.infos.jobs = obj;
            return html;
        };
        for( var i = 0, l = list.length ; i < l ; i++ ){
            var card = list[i],
                id = card.id;
            html += this.templates( 'info' , card );
            obj[ id ] = card;
        };
        window.infos.jobs = obj;
        if( !this.setting.allowSend && !this.setting.synOnly ){
            html += this.templates( 'new' );
        };
        return html;
    },
    saveSuccess: function( $obj , card ){
        var parent = $obj.closest('.job-panel');
        parent.before( this.templates( 'info' , card ) ).remove();
        if( !$('#JS_add_job').length && !this.setting.allowSend ){
            $( this.setting.contentDom ).append( $._intentionCard.templates('new') );
        };
    },
    jobShowEdit: function( $obj , id ){
        var parent = $obj.closest('.job-panel'),
            html = '';
        html = $._intentionCard.templates( 'edit' , window.infos.jobs[id] );
        parent.after( html ).remove();
    },
    cancelEdit: function( $obj , id ){
        var parent = $obj.closest('.job-panel'),
            html = '';
        if( id ){
            html = $._intentionCard.templates( 'info' , window.infos.jobs[id] );
        }else{
            html = $._intentionCard.templates('new');
        };
        parent.after( html ).remove();
    },
    addJob: function(){
        $._intentionCard.appendList( $._intentionCard.templates('new') );
    },
    insertJob: function(){
        $._intentionCard.appendList( $._intentionCard.templates('edit') );
    },
    deleteJob: function( $obj , id ){
        if( !id ) return;
        var url = '/companycard/job/delete/' + id + '/',
            func = function(){
                $.get( url , {} , function(res){
                    if( res && res.status == 'ok' ){
                        $obj.closest('.job-panel').remove();
                        delete window.infos.jobs[id];
                        if( $.isEmptyObject(infos.jobs) && !$('#JS_add_job').length ){
                            $._intentionCard.addJob();
                        };
                    }else if( res && res.msg ){
                        $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>' + res.msg + '</p>');
                    }else{
                        $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请求失败，请刷新后再试！</p>');
                    };
                });
            };
        if( $( '.JS_delete_job').length == 1 ){
            $.confirm( '<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>您只有一条岗位信息了，删除后无法生成企业名片，确认要删除吗？</p>', func  );
        }else{
            func();
        };
    },
    appendList: function( html ){
        $( this.setting.contentDom ).html( html );
    }
};
$.intentionCard.prototype.init.prototype = $.intentionCard.prototype;

var cardScroll = function( setting ){
    setting = $.extend({
        boxDom: '#JS_jobs_ajax_content',
        tagClass: 'job-panel',
        leftBtn: '#JS_left_btn',
        rightBtn: '#JS_right_btn',
        stepCount: 2,
        present: 0,
        step: 870
    },setting);
    var scroll = function(){
        if( setting.present <= 0 ){
            setting.present = 0;
            $( setting.leftBtn ).hide();
        };
        if( setting.present >= setting.len ){
            setting.present = setting.len;
            $( setting.rightBtn ).hide();
        };
        if( setting.present > 0 ){
            $( setting.leftBtn ).show();
        };
        if( setting.present < setting.len ){
            $( setting.rightBtn ).show();
        };
        $( setting.boxDom ).animate({
            left: -setting.step * setting.present + 'px'
        },'slow');
    },
    len = null,
    num = $( setting.boxDom ).find('.' + setting.tagClass ).length;

    if( !num ) return;
    len = Math.ceil( num / 2 );
    $( setting.boxDom ).css( 'width' , setting.step * len + 'px' );
    setting.len = len - 1;
    if( setting.len == 0 ){
        $( setting.rightBtn ).hide();
    };
    $( setting.leftBtn ).hide();
    $( setting.rightBtn ).on( 'click' , function(){
        setting.present++;
        scroll();
    });
    $( setting.leftBtn ).on( 'click' , function(){
        setting.present--;
        scroll();
    });
};

var chooseSynCard = function(){
    var html = $('#JS_syn_cards').html(),
        jobs = jobList || [],
        width = 925;

    if( jobs.length == 1 ){
        width = 490;
    };

    $.LayerOut({
        html: html,
        closeByShadow: false,
        dialogCss: 'width:' + width + 'px; height:610px;'
    });

    $.intentionCard({
        list: jobs,
        synOnly: true,
        allowSend: false,
        contentDom: '#JS_jobs_ajax_content',
        callback: cardScroll
    });

};

$(function(){

    //保存公司信息
    $( document ).on( 'click' , '#JS_save_company' , function(){
        var $this = $( this ),
            form = $this.closest( 'form' ),
            data = form.serializeObject(),
            isOk = true,
            cats = $('#JS_choose_area .select');
        if( !data.company_name ){
            //$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>公司名称不能为空</p>');
            form.find('input[name="company_name"]').addClass('tip-error');
            isOk = false;
        };
        if( !data.key_points || data.key_points == form.find('textarea[name="key_points"]').attr('placeholder') ){
            form.find('textarea[name="key_points"]').addClass('tip-error');
            isOk = false;
        };
        if( !data.company_stage ){
            form.find('input[name="company_stage"]').addClass('tip-error');
            isOk = false;
        };
        form.find('[maxLength]').each(function(){
            var $that = $( this ),
                len = $that.attr('maxLength'),
                val = $that.val(),
                msg = '请控制在' + len + '字以内，精简的文字更便于候选人阅读哦！',
                name = $that.attr('name');
            if( val.length > len ){
                if( name == 'key_points' ){
                    msg = '企业亮点' + msg;
                }else if( name == 'desc' ){
                    msg = '企业简介' + msg;
                };
                $that.addClass('tip-error');
                isOk = false;
                $.alert( msg );
                return false;
            };
        });
        if( !cats.length ){
            $.alert( '<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请选择所在领域！</p>' );
            isOk = false;
        }else{
            var category = [];
            for( var i = 0 , l = cats.length ; i < l ; i++ ){
                var cat = cats.eq( i );
                    id = cat.attr( 'data-id' );
                category.push( id );
            };
            data.category = category;
        };
        if( !isOk ){
            return false;
        };
        if( data.desc == form.find('textarea[name="desc"]').attr('placeholder') ){
            data.desc = '';
        };
        window.$_companyInfo.saveCompanyAjax( data );
    });

    $( document ).on( 'click' , '#JS_cancel_edit' , function(){
        window.$_companyInfo.appendContent( window.$_companyInfo.getHtml( 'info' ) );
    });

    //编辑公司信息
    $( document ).on( 'click' , '#JS_edit_company_info' , function(){
        window.$_companyInfo.appendContent( window.$_companyInfo.getHtml( 'edit' ) );
    });

    //添加岗位
    $( document ).on( 'click' , '#JS_add_job' , function(){
        $( '.JS_cancel_save' ).click();
        $( this ).closest( '.job-panel' ).before( $._intentionCard.templates('edit') ).remove();
    });

    //保存岗位信息
    $( document ).on( 'click' , '.JS_save_job' , function(){
        if( window.sockJob ) return false;
        window.sockJob = true;
        var $this = $( this ),
            id = $this.parent().attr('data-id'),
            form = $this.closest( 'form' ),
            data = form.serializeObject(),
            isOk = true;
        if( !data.title ){
            form.find('input[name="title"]').addClass('tip-error');
            isOk = false;
        };
        if( !data.salary_low || !regs.price.test( data.salary_low ) ){
            form.find('input[name="salary_low"]').addClass('tip-error');
            isOk = false;
        };
        if( !data.salary_high || !regs.price.test( data.salary_high ) ){
            form.find('input[name="salary_high"]').addClass('tip-error');
            isOk = false;
        };
        if( +data.salary_high <= +data.salary_low ){
            form.find('input[name="salary_low"]').addClass('tip-error');
            form.find('input[name="salary_high"]').addClass('tip-error');
            isOk = false;
        };
        if( !data.work_years ){
            form.find('select[name="work_years"]').addClass('tip-error');
            isOk = false;
        };
        if( !data.address ){
            form.find('input[name="address"]').addClass('tip-error');
            isOk = false;
        };
        if( !data.degree ){
            form.find('select[name="degree"]').siblings('button').addClass('tip-error');
            isOk = false;
        };
        if( !isOk ){
            window.sockJob = false;
            return false;
        };
        if( id ){
            data.id = id;
        };
        data.salary_high = +data.salary_high * 1000;
        data.salary_low = +data.salary_low * 1000;
        $.post( '/companycard/job/save/' , JSON.stringify( data ) , function( res ){
            if( res && res.status == 'ok' ){
                if( !data.id ) data.id = res.id;
                window.infos.jobs[res.id] = data;
                window.$._intentionCard.saveSuccess( $this , data );
            }else if( res && res.msg ){
                $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>' + res.msg + '</p>');
            }else{
                $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请求失败，请刷新后再试！</p>');
            };
            window.sockJob = false;
        },'json').fail(function(){
            window.sockJob = false;
        });
    });

    //取消修改岗位信息
    $( document ).on( 'click' , '.JS_cancel_save' , function(){
        var $this = $( this ),
            id = $this.parent().attr( 'data-id' );
        window.$._intentionCard.cancelEdit( $this , id );
    });

    //修改岗位信息
    $( document ).on( 'click' , '.JS_edit_job_btn' , function(){
        var $this = $( this ),
            id = $this.parent().attr( 'data-id' );
        $( '.JS_cancel_save' ).click();
        window.$._intentionCard.jobShowEdit( $this , id );
    });

    //删除岗位信息
    $( document ).on( 'click' , '.JS_delete_job' , function(){
        var $this = $( this ),
            id = $this.attr( 'data-id' );
        window.$._intentionCard.deleteJob( $this , id );
    });

    //发送企业名片
    $( document ).on( 'click' , '.JS_send_job_to_user' , function(){
        var url = '/companycard/card/send/',
            resume_id = $('#main').attr('data-resumeid'),
            $this = $( this ),
            feed_id = $( '#main' ).attr( 'data-feed_id' ),
            job_id = $this.parent().attr('data-id');
        if( !job_id || !resume_id ){
            $.alert( '缺少数据' );
            return false;
        };
        if( $this.attr('disabled') ) return false;
        $this.attr('disabled', true);
        $.post( url , {
            feed_id: feed_id,
            resume_id: resume_id,
            job_id: job_id
        }, function( res ){
            $this.attr('disabled', false);
            if( res && res.status == 'ok' ){
                var setCookie=function(key, value) {
                   var expires = new Date();
                   expires.setTime(expires.getTime() + 864000);
                   document.cookie = key + '=' + value + ';expires=' + expires.toUTCString() + ';path=/;';
                }
                setCookie("isSendCompanyCard"+resume_id, 1);
                $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>企业名片发送成功！稍后请在“简历中心”中查看候选人的反馈信息。</p>' , function(){
                    location.reload();
                } );
            }else if( res && res.msg ){
                $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>' + res.msg + '</p>');
            }else{
                $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请求失败，请刷新后再试！</p>');
            };
        }, 'json');
    });

    //选择同步的企业名片
    $( document ).on( 'click' , '#JS_syn_btn' , chooseSynCard);

    //同步企业名片
    $( document ).on( 'click' , '.JS_syn_job_btn', function(){
        var $dom = $( this ).closest('.job-panel'),
            job_detail = $dom.find('tr').eq(5).find('span').html(),
            requirement = $dom.find('tr').eq(6).find('span').html(),
            val = job_detail + '\r\n\r\n' + requirement;
        $( 'textarea[name="job_desc"]' ).val( val );
        $._LayerOut.close();
    });

    $( document ).on( 'click' , '#JS_choose_area a' , function(){
        var $this = $( this ),
            select = $this.hasClass( 'select' );
        if( $('#JS_choose_area a.select').length >= 3 && !select ){
            return false;
        };
        $this.toggleClass( 'select' );
    });

});
