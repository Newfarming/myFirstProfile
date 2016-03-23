/*
    author: 516758517@qq.com
    date:  2014-07-30
    description: 简历录入JS
 */

$.placeholderHandle = function(){
    $('#JS_resume_content [placeholder]').each(function(){
        var $this = $( this ),
            holder = $this.attr('placeholder');
        if( !$this.val() ){
            $this.val( holder );
        };
    });
};

$.loadResume = function( json ){
    var html = '<div class="personal-info mt20">' +
                    '<fieldset class="fieldset" id="JS_contact_info">' +
                        '<h3>个人信息 <span>(必填)</span></h3>' +
                        '<div class="field-box">' +
                            '<table width="90%" cellspacing="0" cellpadding="0">' +
                                '<tr>' +
                                    '<td width="340">' +
                                        '<span class="red">*</span><input type="text" class="input w268" name="name" value="' + ( json && json.contact_info && json.contact_info.name ? json.contact_info.name : '' ) + '" placeholder="姓名" data-equired data-reg="isNull">' +
                                    '</td>' +
                                    '<td><span class="red">*</span>';
                                        if( json && json.contact_info && json.contact_info.gender ){
                                            html += '<label><input type="radio" name="gender" ' + ( json.contact_info.gender == '男' ? 'checked' : '' ) + ' value="男">男</label>' +
                                        '<label><input type="radio" name="gender" value="女" ' + ( json.contact_info.gender == '女' ? 'checked' : '' ) + '>女</label>';
                                        }else{
                                            html += '<label><input type="radio" name="gender" value="男">男</label><label><input type="radio" name="gender" checked value="女">女</label>';
                                        };
                                    html += '</td>' +
                                '</tr>' +
                                '<tr>' +
                                    '<td>' +
                                        '<span class="red">*</span><input maxLength="11" type="text" value="' + ( json && json.contact_info && json.contact_info.phone ? json.contact_info.phone : '' ) + '" class="input w268" data-equired data-reg="number" name="phone" placeholder="电话">' +
                                    '</td>' +
                                    '<td colspan="2">' +
                                        '<span class="red">*</span><input type="text" name="email" value="' + ( json && json.contact_info && json.contact_info.email ? json.contact_info.email : '' ) + '" data-equired data-reg="email" class="input w268" placeholder="邮箱">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr>' +
                                    '<td>' +
                                        '<span class="red">*</span><input type="text" class="input w268" data-reg="number" value="' + ( json && json.resume && json.resume.work_years ? json.resume.work_years : '' ) + '" name="work_years" data-equired placeholder="工作年限:例 5">' +
                                    '</td>' +
                                    '<td width="340">' +
                                        '<span class="red">*</span><input type="text" value="' + ( json && json.resume && json.resume.job_target && json.resume.job_target.expectation_area ? json.resume.job_target.expectation_area : '' ) + '" name="expectation_area" class="input w268" data-equired data-reg="isNull" placeholder="意向工作地">' +
                                    '</td>' +
                                '</tr>' +
                                '<tr>' +
                                    '<td colspan="2">' +
                                        '<span class="red">*</span><input type="text" class="input w268" data-reg="number" value="' + ( json && json.contact_info && json.contact_info.age ? json.contact_info.age : '' ) + '" name="age" data-equired placeholder="年龄">' +
                                    '</td>' +
                                '</tr>' +
                            '</table>' +
                            '<hr class="hr hr-solid mt20">' +
                            '<p class="mt20">' +
                                '<a href="javascript:;" title="保存" class="btn btn-primary noradius ml50 JS_save_someone">保存</a>' +
                                '<a href="javascript:;" class="btn btn-primary noradius ml50 disabled">已保存<i class="i-bingo"></i></a>' +
                            '</p>' +
                        '</div>' +
                    '</fieldset>' +
                '</div>' +
                '<div class="personal-info mt20">' +
                    '<fieldset class="fieldset" id="JS_work_info">' +
                        '<h3>工作经历 <span>(必填)</span></h3>';
                        if( json && json.resume && json.resume.works && json.resume.works.length ){
                            var works = json.resume.works;
                            for( var i = 0 , l = works.length ; i < l ; i++ ){
                                html += $.getWorkHtml( works[i] , ( i == l -1 ? 'last' : '' ) );
                            };
                        }else{
                            html += $.getWorkHtml();
                        };
                    html += '</fieldset>' +
                '</div>' +
                '<div class="personal-info mt20">' +
                    '<fieldset class="fieldset" id="JS_education_info">' +
                        '<h3>教育经历 <span>(必填)</span></h3>';
                    if( json && json.resume && json.resume.educations && json.resume.educations.length ){
                            var education = json.resume.educations;
                            for( var i2 = 0 , l2 = education.length ; i2 < l2 ; i2++ ){
                                html += $.getEducationHtml( education[i2] , ( i2 == l2 -1 ? 'last' : '' ) );
                            };
                        }else{
                            html += $.getEducationHtml();
                        };
                    html += '</fieldset>' +
                '</div>';

                //管理员显示
                if( $('body').attr('data-admin_edit') ){

                    html += '<div class="personal-info mt20">' +
                        '<fieldset class="fieldset" id="JS_project_info">' +
                            '<h3>项目经历</h3>';
                            if( json && json.resume && json.resume.projects && json.resume.projects.length){
                                var project = json.resume.projects;
                                for( var i1 = 0 , l1 = project.length ; i1 < l1 ; i1++ ){
                                    html += $.getProjectHtml( project[i1] , ( i1 == l1 -1 ? 'last' : '' ) );
                                };
                            };
                            html += '<p class="text-center" style="display:' + ( json && json.resume && json.resume.projects && json.resume.projects.length ? 'none' : 'block' ) + '">' +
                                '<a href="javascript:;" class="btn btn-large btn-white noradius" onclick="$(this).parent().hide().closest(\'fieldset\').append( $.getProjectHtml() );"><i class="i-add"></i><strong>添加项目经历</strong></a>' +
                            '</p>';
                        html += '</fieldset>' +
                    '</div>' +
                    '<div class="personal-info mt20">' +
                        '<fieldset class="fieldset" id="JS_train_info">' +
                            '<h3>培训经历</h3>';
                            if( json && json.resume && json.resume.trains && json.resume.trains.length ){
                                var trin = json.resume.trains;
                                for( var i3 = 0 , l3 = trin.length ; i3 < l3 ; i3++ ){
                                    html += $.getTrinHtml( trin[i3] , ( i3 == l3 -1 ? 'last' : '' ) );
                                };
                            };
                            html += '<p class="text-center" style="display:' + ( json && json.resume && json.resume.trains && json.resume.trains.length ? 'none' : 'block' ) + '">' +
                                '<a href="javascript:;" class="btn btn-large btn-white noradius" onclick="$(this).parent().hide().closest(\'fieldset\').append( $.getTrinHtml() );"><i class="i-add"></i><strong>添加培训经历</strong></a>' +
                            '</p>';
                        html += '</fieldset>' +
                    '</div>' +
                    '<div class="personal-info mt20">' +
                        '<fieldset class="fieldset" id="JS_evaluation_info">' +
                            '<h3>自我评价</h3>';
                            if( json && json.resume && json.resume.self_evaluation ){
                                var evaluation = json.resume.self_evaluation;
                                html += $.getEvaluationHtml( evaluation );
                            };
                            html += '<p class="text-center" style="display:' + ( json && json.resume && json.resume.self_evaluation ? 'none' : 'block' ) + '">' +
                                '<a href="javascript:;" class="btn btn-large btn-white noradius" onclick="$(this).parent().hide().closest(\'fieldset\').append( $.getEvaluationHtml() );"><i class="i-add"></i><strong>添加自我评价</strong></a>' +
                            '</p>';
                        html += '</fieldset>' +
                    '</div>' +
                    '<div class="personal-info mt20">' +
                        '<fieldset class="fieldset" id="JS_skill_info">' +
                            '<h3>专业技能</h3>';
                            if( json && json.resume && json.resume.professional_skills && json.resume.professional_skills.length ){
                                var skills = json.resume.professional_skills;
                                for( var i4 = 0 , l4 = skills.length ; i4 < l4 ; i4++ ){
                                    html += $.getSkillHtml( skills[i4] , ( i4 == l4 -1 ? 'last' : '' ) );
                                };
                            };
                            html += '<p class="text-center" style="display:' + ( json && json.resume && json.resume.professional_skills && json.resume.professional_skills.length ? 'none' : 'block' ) + '">' +
                                '<a href="javascript:;" class="btn btn-large btn-white noradius" onclick="$(this).parent().hide().closest(\'fieldset\').append( $.getSkillHtml() );"><i class="i-add"></i><strong>添加专业技能</strong></a>' +
                            '</p>';
                        html += '</fieldset>' +
                    '</div>';
                };

                html += '<div class="personal-info mt20">' +
                    '<fieldset class="fieldset" id="JS_other_info">' +
                        '<h3>其他</h3>';
                        if( json && json.resume && json.resume.other_info ){
                            var content = json.resume.other_info.content;
                            html += $.getOtherHtml( content );
                        };
                        html += '<p class="text-center" style="display:' + ( json && json.resume && json.resume.other_info ? 'none' : 'block' ) + '">' +
                            '<a href="javascript:;" class="btn btn-large btn-white noradius w124" onclick="$(this).parent().hide().closest(\'fieldset\').append( $.getOtherHtml() );"><i class="i-add"></i><strong>添加其他</strong></a>' +
                        '</p>';
                    html += '</fieldset>' +
                '</div>';

    $('#JS_resume_content').html(html);
};

$.uploadResume = function( val ){
    var progress = $('.progress').find('span:first'),
        code = $('.progress').next('code'),
        fileName = val.split('\\');
    progress[0].style.width = '0%';
    code.html('0%');
    var width = 0,
        countdown = function(){
            if( width < 99 ){
                width++;
                progress.css({
                    width: width + '%'
                });
                code.html( width + '%' );
                t1 = setTimeout( function(){
                    countdown();
                }, 50);
            };
        };
    $('.entry-progress').show().siblings().hide();

    countdown();

};

$.getWorkHtml = function( work , isLast ){
    var html ='';
    html = '<div class="field-box">' +
                '<table width="90%" cellspacing="0" cellpadding="0">' +
                    '<tr>' +
                        '<td>' +
                            '<span class="red">*</span><input type="text" class="input w268 JS_company_name" data-reg="isNull" data-equired value="' + ( work && work.company_name ? work.company_name : '' ) + '" placeholder="公司名称">' +
                        '</td>' +
                        '<td>' +
                            '<span class="red">*</span><input type="text" class="input w268 JS_position_title" data-reg="isNull" data-equired value="' + ( work && work.position_title ? work.position_title : '' ) + '" placeholder="职位名称">' +
                        '</td>' +
                    '</tr>' +
                    '<tr>' +
                        '<td>' +
                            '<div>' +
                                '<span class="red left">*</span>';

                                if( work && work.start_time ){
                                    var star = work.start_time.split('-');
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + star[0] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始年份</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="work_start_year" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getYear( 'option' , star[0] ) +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + star[1] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始月份</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="work_start_month" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getMonth( 'option' , star[1] ) +
                                        '</select>' +
                                    '</div>';
                                }else{
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">开始年份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始年份</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="work_start_year" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getYear() +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">开始月份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始月份</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="work_start_month" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getMonth() +
                                        '</select>' +
                                    '</div>';
                                };
                                html += '<div class="clearBoth"></div>' +
                            '</div>' +
                        '</td>' +
                        '<td>' +
                            '<div>' +
                                '<span class="red left">*</span>';
                                if( work && work.end_time ){
                                    var end = work.end_time.split('-');
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + end[0] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束年份</a></li>' +
                                                '<li class="now"><a>至今</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="work_end_year" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今" ' + ( end[0] == '至今' ? 'selected' : '' ) + '>至今</option>' +
                                            $.getYear( 'option' , end[0] ) +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" ' + ( end[0] == '至今' ? 'disabled' : '' ) + ' style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + ( end[1] ? end[1] : '至今' ) + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束月份</a></li>' +
                                                '<li class="nowMonth"><a>至今</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="work_end_month" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今" ' + ( end[0] == '至今' ? 'selected' : '' ) + '>至今</option>' +
                                            $.getMonth( 'option' , end[1] ) +
                                        '</select>' +
                                    '</div>';
                                }else{
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">结束年份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束年份</a></li>' +
                                                '<li class="now"><a>至今</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="work_end_year" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今">至今</option>' +
                                            $.getYear() +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">结束月份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束月份</a></li>' +
                                                '<li class="nowMonth"><a>至今</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="work_end_month" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今">至今</option>' +
                                            $.getMonth() +
                                        '</select>' +
                                    '</div>';
                                };
                                html += '<div class="clearBoth"></div>' +
                            '</div>' +
                        '</td>' +
                    '</tr>' +
                    '<tr>' +
                        '<td colspan="2" style="vertical-align:top">' +
                            '<span class="red" style="vertical-align:top">*</span><textarea maxLength="500" style="vertical-align:top" rows="5" class="textarea JS_job_desc w609" placeholder="工作描述" data-reg="isNull" data-equired data-lengthlimit="500">' + ( work && work.job_desc ? $.wrapToggle( work.job_desc , 'toR' ) : '' ) + '</textarea><br>' +
                            '<p class="limit-count"><span>500</span>字</p>' +
                        '</td>' +
                    '</tr>' +
                '</table>' +
                '<p class="mt10 multiterm">' +
                    '<a href="javascript:;" title="保存" class="btn btn-primary noradius ml50 JS_save_someone">保存</a>' +
                    '<a href="javascript:;" class="btn btn-primary noradius ml50 disabled">已保存<i class="i-bingo"></i></a>';
                    if( $('#JS_work_info').length ){
                        html += '<a href="javascript:;" class="JS_delete a-default ml10" onclick="$.Delete( this , true )">删除</a>';
                    };
                    html += '<a href="javascript:;" class="JS_add_new a-default ml10" onclick="$.addNew( this , \'work\')">新增一条</a>' +
                '</p>' +
            '</div>';
            if( work && !isLast ){
                html += '<hr class="hr mt50">';
            };

    return html;
};

$.getProjectHtml = function( project , isLast ){
    var html = '<div class="field-box">' +
                '<table width="90%" cellspacing="0" cellpadding="0">' +
                    '<tr>' +
                        '<td>' +
                            '<span class="red">*</span><input type="text" data-equired data-reg="isNull" class="input w268 JS_project_name" value="' + ( project && project.project_name ? project.project_name : '' ) + '" placeholder="项目名称">' +
                        '</td>' +
                        '<td>' +
                            '<input type="text" class="input w268 ml12 JS_job_title" value="' + ( project && project.job_title ? project.job_title : '' ) + '" placeholder="担任职位">' +
                        '</td>' +
                    '</tr>' +
                    '<tr>' +
                        '<td>' +
                            '<div>' +
                                '<span class="red left">*</span>';

                                if( project && project.start_time ){
                                    var star = project.start_time.split('-');
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + star[0] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始年份</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select data-equ class="project_start_year">' +
                                            '<option value=""></option>' +
                                            $.getYear( 'option' , star[0] ) +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + star[1] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始月份</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select data-equ class="project_start_month">' +
                                            '<option value=""></option>' +
                                            $.getMonth( 'option' , star[1] ) +
                                        '</select>' +
                                    '</div>';
                                }else{
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">开始年份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始年份</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select data-equ class="project_start_year">' +
                                            '<option value=""></option>' +
                                            $.getYear() +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">开始月份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始月份</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select data-equ class="project_start_month">' +
                                            '<option value=""></option>' +
                                            $.getMonth() +
                                        '</select>' +
                                    '</div>';
                                };
                                html += '<div class="clearBoth"></div>' +
                            '</div>' +
                        '</td>' +
                        '<td>' +
                            '<div>' +
                                '<span class="red left">*</span>';
                                if( project && project.end_time ){
                                    var end = project.end_time.split('-');
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + end[0] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束年份</a></li>' +
                                                '<li class="now"><a>至今</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select data-equ class="project_end_year">' +
                                            '<option value=""></option>' +
                                            '<option value="至今" ' + ( end[0] == '至今' ? 'selected' : '' ) + '>至今</option>' +
                                            $.getYear( 'option' , end[0] ) +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" ' + ( end[0] == '至今' ? 'disabled' : '' ) + ' style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + ( end[1] ? end[1] : '至今' ) + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束月份</a></li>' +
                                                '<li class="nowMonth"><a>至今</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select data-equ class="project_end_month">' +
                                            '<option value=""></option>' +
                                            '<option value="至今" ' + ( end[0] == '至今' ? 'selected' : '' ) + '>至今</option>' +
                                            $.getMonth( 'option' , end[1] ) +
                                        '</select>' +
                                    '</div>';
                                }else{
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">结束年份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束年份</a></li>' +
                                                '<li class="now"><a>至今</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select data-equ class="project_end_year">' +
                                            '<option value=""></option>' +
                                            '<option value="至今">至今</option>' +
                                            $.getYear() +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">结束月份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束月份</a></li>' +
                                                '<li class="nowMonth"><a>至今</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select data-equ class="project_end_month">' +
                                            '<option value=""></option>' +
                                            '<option value="至今">至今</option>' +
                                            $.getMonth() +
                                        '</select>' +
                                    '</div>';
                                };
                                html += '<div class="clearBoth"></div>' +
                            '</div>' +
                        '</td>' +
                    '</tr>' +
                    '<tr>' +
                        '<td colspan="2" style="vertical-align:top">' +
                            '<span class="red" style="vertical-align:top">*</span><textarea maxLength="500" data-reg="isNull" data-equired style="vertical-align:top" rows="5" class="textarea w609 JS_project_desc" placeholder="项目描述" data-lengthlimit="500">' + ( project && project.project_desc ? $.wrapToggle( project.project_desc , 'toR' ) : '' ) + '</textarea><br>' +
                            '<p class="limit-count"><span>500</span>字</p>' +
                        '</td>' +
                    '</tr>' +
                '</table>' +
                '<p class="mt10 multiterm">' +
                    '<a href="javascript:;" title="保存" class="btn btn-primary noradius ml50 JS_save_someone">保存</a>' +
                    '<a href="javascript:;" class="btn btn-primary noradius ml50 disabled">已保存<i class="i-bingo"></i></a>' +
                    '<a href="javascript:;" class="JS_delete a-default ml10" onclick="$.Delete( this )">删除</a>' +
                    '<a href="javascript:;" class="JS_add_new a-default ml10" onclick="$.addNew( this , \'project\')">新增一条</a>' +
                '</p>' +
            '</div>';
            if( project && !isLast ){
                html += '<hr class="hr mt50">';
            };

    return html;
};

$.getEducationHtml = function( education , isLast ){
    var html = '<div class="field-box">' +
                    '<table width="90%" cellspacing="0" cellpadding="0">' +
                    '<tr>' +
                        '<td>' +
                            '<span class="red">*</span><input type="text" data-reg="isNull" data-equired class="input w268 JS_school" value="' + ( education && education.school ? education.school : '' ) + '" placeholder="学校名称">' +
                        '</td>' +
                        '<td>' +
                            '<span class="red">*</span><input type="text" data-reg="isNull" data-equired class="input w268 JS_major" value="' + ( education && education.major ? education.major : '' ) + '" placeholder="专业名称">' +
                        '</td>' +
                    '</tr>' +
                    '<tr>' +
                        '<td colspan="2">' +
                            '<span class="red">*</span><input type="text" class="input w268 JS_degree" value="' + ( education && education.degree ? education.degree : '' ) + '" placeholder="学历" data-equired data-reg="isNull">' +
                        '</td>' +
                    '</tr>' +
                    '<tr>' +
                        '<td>' +
                            '<div>' +
                                '<span class="red left">*</span>';

                                if( education && education.start_time ){
                                    var star = education.start_time.split('-');
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + star[0] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始年份</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="edu_start_year" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getYear( 'option' , star[0] ) +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + star[1] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始月份</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="edu_start_month" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getMonth( 'option' , star[1] ) +
                                        '</select>' +
                                    '</div>';
                                }else{
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">开始年份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始年份</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="edu_start_year" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getYear() +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">开始月份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始月份</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="edu_start_month" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getMonth() +
                                        '</select>' +
                                    '</div>';
                                };
                                html += '<div class="clearBoth"></div>' +
                            '</div>' +
                        '</td>' +
                        '<td>' +
                            '<div>' +
                                '<span class="red left">*</span>';
                                if( education && education.end_time ){
                                    var end = education.end_time.split('-');
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + end[0] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束年份</a></li>' +
                                                '<li class="now"><a>至今</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="edu_end_year" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今" ' + ( end[0] == '至今' ? 'selected' : '' ) + '>至今</option>' +
                                            $.getYear( 'option' , end[0] ) +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" ' + ( end[0] == '至今' ? 'disabled' : '' ) + ' style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + ( end[1] ? end[1] : '至今' ) + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束月份</a></li>' +
                                                '<li class="nowMonth"><a>至今</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="edu_end_month" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今" ' + ( end[0] == '至今' ? 'selected' : '' ) + '>至今</option>' +
                                            $.getMonth( 'option' , end[1] ) +
                                        '</select>' +
                                    '</div>';
                                }else{
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">结束年份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束年份</a></li>' +
                                                '<li class="now"><a>至今</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="edu_end_year" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今">至今</option>' +
                                            $.getYear() +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">结束月份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束月份</a></li>' +
                                                '<li class="nowMonth"><a>至今</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="edu_end_month" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今">至今</option>' +
                                            $.getMonth() +
                                        '</select>' +
                                    '</div>';
                                };
                                html += '<div class="clearBoth"></div>' +
                            '</div>' +
                        '</td>' +
                        '</tr>' +
                    '</table>' +
                    '<p class="mt10 multiterm">' +
                        '<a href="javascript:;" title="保存" class="btn btn-primary noradius ml50 JS_save_someone">保存</a>' +
                        '<a href="javascript:;" class="btn btn-primary noradius ml50 disabled">已保存<i class="i-bingo"></i></a>';
                        if( $('#JS_education_info').length ){
                            html += '<a href="javascript:;" class="JS_delete a-default ml10" onclick="$.Delete( this , \'leastOne\')">删除</a>';
                        };
                        html += '<a href="javascript:;" class="JS_add_new a-default ml10" onclick="$.addNew( this , \'education\')">新增一条</a>' +
                    '</p>' +
                '</div>';
            if( education && !isLast ){
                html += '<hr class="hr mt50">';
            };

    return html;
};

$.getTrinHtml = function( trin , isLast ){
    var html = '<div class="field-box">' +
                    '<table width="90%" cellspacing="0" cellpadding="0">' +
                        '<tr>' +
                        '<td>' +
                            '<div>' +
                                '<span class="red left">*</span>';

                                if( trin && trin.start_time ){
                                    var star = trin.start_time.split('-');
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + star[0] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始年份</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="train_start_year" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getYear( 'option' , star[0] ) +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + star[1] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始月份</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="train_start_month" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getMonth( 'option' , star[1] ) +
                                        '</select>' +
                                    '</div>';
                                }else{
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">开始年份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始年份</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="train_start_year" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getYear() +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">开始月份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>开始月份</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="train_start_month" data-equ>' +
                                            '<option value=""></option>' +
                                            $.getMonth() +
                                        '</select>' +
                                    '</div>';
                                };
                                html += '<div class="clearBoth"></div>' +
                            '</div>' +
                        '</td>' +
                        '<td>' +
                            '<div>' +
                                '<span class="red left">*</span>';
                                if( trin && trin.end_time ){
                                    var end = trin.end_time.split('-');
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + end[0] + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束年份</a></li>' +
                                                '<li class="now"><a>至今</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="train_end_year" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今" ' + ( end[0] == '至今' ? 'selected' : '' ) + '>至今</option>' +
                                            $.getYear( 'option' , end[0] ) +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" ' + ( end[0] == '至今' ? 'disabled' : '' ) + ' style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">' + ( end[1] ? end[1] : '至今' ) + '<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束月份</a></li>' +
                                                '<li class="nowMonth"><a>至今</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="train_end_month" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今" ' + ( end[0] == '至今' ? 'selected' : '' ) + '>至今</option>' +
                                            $.getMonth( 'option' , end[1] ) +
                                        '</select>' +
                                    '</div>';
                                }else{
                                    html += '<div class="drop-select w142 left" style="*z-index:2000">' +
                                        '<button class="button" type="button" data-toggle="dropdown">结束年份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束年份</a></li>' +
                                                '<li class="now"><a>至今</a></li>' +
                                                $.getYear('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="train_end_year" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今">至今</option>' +
                                            $.getYear() +
                                        '</select>' +
                                    '</div>' +
                                    '<div class="drop-select ml10 left w142" style="*z-index:1999">' +
                                        '<button class="button" type="button" data-toggle="dropdown">结束月份<i class="i-barr"></i></button>' +
                                        '<div class="drop-box">' +
                                            '<ul class="drop-down">' +
                                                '<li><a>结束月份</a></li>' +
                                                '<li class="nowMonth"><a>至今</a></li>' +
                                                $.getMonth('li') +
                                            '</ul>' +
                                        '</div>' +
                                        '<select class="train_end_month" data-equ>' +
                                            '<option value=""></option>' +
                                            '<option value="至今">至今</option>' +
                                            $.getMonth() +
                                        '</select>' +
                                    '</div>';
                                };
                                html += '<div class="clearBoth"></div>' +
                            '</div>' +
                        '</td>' +
                    '</tr>' +
                    '<tr>' +
                        '<td colspan="2" style="vertical-align:top">' +
                            '<span class="red" style="vertical-align:top">*</span><textarea maxLength="500" style="vertical-align:top" data-reg="isNull" data-equired rows="5" class="textarea w609 JS_train_desc" placeholder="培训详情" data-lengthlimit="500">' + ( trin && trin.train_desc ? $.wrapToggle( trin.train_desc , 'toR' ) : '' ) + '</textarea><br>' +
                            '<p class="limit-count"><span>500</span>字</p>' +
                        '</td>' +
                    '</tr>' +
                    '</table>' +
                    '<p class="mt10 multiterm">' +
                        '<a href="javascript:;" title="保存" class="btn btn-primary noradius ml50 JS_save_someone">保存</a>' +
                        '<a href="javascript:;" class="btn btn-primary noradius ml50 disabled">已保存<i class="i-bingo"></i></a>' +
                        '<a href="javascript:;" class="JS_delete a-default ml10" onclick="$.Delete( this )">删除</a>' +
                        '<a href="javascript:;" class="JS_add_new a-default ml10" onclick="$.addNew( this , \'train\')">新增一条</a>' +
                    '</p>' +
                '</div>';
            if( trin && !isLast ){
                html += '<hr class="hr mt50">';
            };

    return html;
};

$.getEvaluationHtml = function( evaluation ){
    var html = '<div class="field-box">'+
            '<table width="90%" cellspacing="0" cellpadding="0">' +
            '<tr>' +
                '<td colspan="2" style="vertical-align:top">' +
                    '<textarea maxLength="500" style="vertical-align:top" rows="5" class="textarea w609" id="JS_evaluation" placeholder="自我评价" data-lengthlimit="500">' + ( evaluation ? $.wrapToggle( evaluation , 'toR' ) : '' ) + '</textarea><br>' +
                    '<p class="limit-count"><span>500</span>字</p>' +
                '</td>' +
            '</tr>' +
            '</table>' +
            '<p class="mt10">' +
                '<a href="javascript:;" title="保存" class="btn btn-primary noradius ml50 JS_save_someone">保存</a>' +
                '<a href="javascript:;" class="btn btn-primary noradius ml50 disabled">已保存<i class="i-bingo"></i></a>' +
                '<a href="javascript:;" class="JS_delete a-default ml10" onclick="$.Delete( this )">删除</a>' +
            '</p>' +
            '</div>';
    return html;
};

$.getSkillHtml = function( skill , isLast ){
    var html = '<div class="field-box">'+
            '<table width="90%" cellspacing="0" cellpadding="0">' +
            '<tr>' +
                '<td width="340">' +
                    '<input type="text" class="input w268 ml12 JS_skill_desc" value="' + ( skill && skill.skill_desc ? skill.skill_desc : '' ) + '" placeholder="技能名称">' +
                '</td>' +
                '<td>' +
                    '<div class="drop-select left w142" style="*z-index:1999">' +
                        '<button class="button" type="button" data-toggle="dropdown">' + ( skill && skill.proficiency ? skill.proficiency : '技能水平' ) + '<i class="i-barr"></i></button>' +
                        '<div class="drop-box">' +
                            '<ul class="drop-down">' +
                                '<li><a>请选择</a></li>' +
                                '<li><a>一般</a></li>' +
                                '<li><a>良好</a></li>' +
                                '<li><a>熟练</a></li>' +
                                '<li><a>精通</a></li>' +
                            '</ul>' +
                        '</div>' +
                        '<select class="JS_proficiency">' +
                            '<option value="">请选择</option>' +
                            '<option value="一般" ' + ( skill && skill.proficiency && skill.proficiency == '一般' ) + '>一般</option>' +
                            '<option value="良好" ' + ( skill && skill.proficiency && skill.proficiency == '良好' ) + '>良好</option>' +
                            '<option value="熟练" ' + ( skill && skill.proficiency && skill.proficiency == '熟练' ) + '>熟练</option>' +
                            '<option value="精通" ' + ( skill && skill.proficiency && skill.proficiency == '精通' ) + '>精通</option>' +
                        '</select>' +
                    '</div>' +
                '</td>' +
            '</tr>' +
            '</table>' +
            '<p class="mt10 multiterm">' +
                '<a href="javascript:;" title="保存" class="btn btn-primary noradius ml50 JS_save_someone">保存</a>' +
                '<a href="javascript:;" class="btn btn-primary noradius ml50 disabled">已保存<i class="i-bingo"></i></a>' +
                '<a href="javascript:;" class="JS_delete a-default ml10" onclick="$.Delete( this )">删除</a>' +
                '<a href="javascript:;" class="JS_add_new a-default ml10" onclick="$.addNew( this , \'skill\')">新增一条</a>' +
            '</p>' +
            '</div>';
    if( skill && !isLast ){
        html += '<hr class="hr mt50">';
    };
    return html;
};

$.getOtherHtml = function( other ){
    var html = '<div class="field-box">'+
            '<table width="90%" cellspacing="0" cellpadding="0">' +
            '<tr>' +
                '<td colspan="2" style="vertical-align:top">' +
                    '<textarea maxLength="2000" style="vertical-align:top" rows="5" class="textarea w609" id="JS_other_text" placeholder="其他" data-lengthlimit="2000">' + ( other ? $.wrapToggle( other , 'toR' ) : '' ) + '</textarea><br>' +
                    '<p class="limit-count"><span>2000</span>字</p>' +
                '</td>' +
            '</tr>' +
            '</table>' +
            '<p class="mt10">' +
                '<a href="javascript:;" title="保存" class="btn btn-primary noradius ml50 JS_save_someone">保存</a>' +
                '<a href="javascript:;" class="btn btn-primary noradius ml50 disabled">已保存<i class="i-bingo"></i></a>' +
                '<a href="javascript:;" class="JS_delete a-default ml10" onclick="$.Delete( this )">删除</a>' +
            '</p>' +
            '</div>';
    return html;
};

$.Delete = function( obj , leastOne ){
    var $obj = $( obj ),
        dom = $obj.closest('.field-box'),
        prev = dom.prev();
    if( dom.parent().find('.field-box').length == 1 ){
        if( leastOne ){
            alert('该分类至少需要一条信息!');
            $obj.hide();
            return;
        }else{
            dom.siblings('p').show();
        };
    };
    if( prev[0].tagName.toLowerCase() == 'hr' ){
        prev.remove();
    };
    dom.remove();
};

$.addNew = function( obj , type ){
    var html = '<hr class="hr mt50">';
    switch( type ){
        case "work":
            html += $.getWorkHtml();
            break;
        case "project":
            html += $.getProjectHtml();
            break;
        case "train":
            html += $.getTrinHtml();
            break;
        case "education":
            html += $.getEducationHtml();
            break;
        case 'skill':
            html += $.getSkillHtml();
            break;
    };

    $( obj ).closest('.fieldset').append( html );
};


$.wrapToggle = function( desc , type ){
    if( type == 'toR' ){
        desc = desc.replace( /\<br \/\>|\<br\>/g , '\r\n' );
    }else{
        desc = desc.replace( /\r\n/g , '<br>' );
    };
    return desc;
};

$.UploadResumeFile = function(){
    var bar = $('.progress span');
    var percent = $('.progress code');
    var progress = $(".progress");
    var files = $(".files");
    var upElement = $(".upload-file");
    for( var i = 0 , l = upElement.length ; i < l ; i++){
        var item = upElement.eq(i),
            url = item.attr('data-url');
        item.wrap('<form action="' + url + '" method="POST" enctype="multipart/form-data"></form>');
        item.change(function(){ //选择文件
            $(this).closest('form').ajaxSubmit({
                dataType:  'json', //数据格式为json
                beforeSend: function() { //开始上传
                    //progress.show(); //显示进度条
                    //var percentVal = '0%'; //开始进度为0%
                    //bar.width(percentVal); //进度条的宽度
                    //percent.html(percentVal); //显示进度为0%
                },
                uploadProgress: function(event, position, total, percentComplete) {
                    //var percentVal = percentComplete + '%'; //获得进度
                    //bar.width(percentVal); //上传进度条宽度变宽
                    //percent.html(percentVal); //显示上传进度百分比
                },
                success: function(data) { //请求成功
                    $('.entry-progress .progress span').css( 'width','100%');
                    $('.entry-progress code').text('100%');
                    var completeFunc = function(){
                        if( window.t1 ){
                            clearTimeout( t1 );
                        };
                        $('.entry-notice').show();
                        $('.entry-progress').hide();
                        $('.re-entry').hide();
                        $('.upload-file').val('');
                    };
                    if( data && data.status == 'ok' ){

                        $.alert('<p class="alert-notice" style="margin-left: 77px;">简历上传成功，我们将会对您上传的简历进行审核，若审核通过，<br>您将会得到<span style="color:#FC7524">5</span>个聘点的奖励，请稍后登录录入记录查看。</p>' , function(){
                            window.location.href = '/resumeupload/uploadlist/';
                        } , '' , {
                            confirmByShadow: true
                        });

                    }else if( data && data.status == 'phone_error' ){

                        $.confirm('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + data.msg + '</p>' , '' , '' , '' ,{
                            handlers: [
                                {
                                    title: '再试一次',
                                    eventType: 'click',
                                    className: 'layer-button grey-button',
                                    event: function(){
                                        $._LayerOut.close();
                                    }
                                },
                                {
                                    title: '手动录入',
                                    eventType: 'click',
                                    className: 'layer-button blue-button',
                                    event: function(){
                                        window.ResumeData = data;
                                        $('#JS_user_tab a').eq(1).click();
                                        if( data && data.upload_file ){
                                            $('#JS_upload_file').val( data.upload_file );
                                        }else{
                                            $('#JS_upload_file').val();
                                        };
                                        $._LayerOut.close();
                                    }
                                }
                            ]
                        });

                    }else{

                        var msg = data && data.msg || '上传失败了！';
                        $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + msg + '</p>');

                    };
                    completeFunc();
                },
                error:function(){ //请求失败
                    if( !window.stopByUser){
                        $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>上传失败！</p>');
                    };
                    if( window.t1 ){
                        clearTimeout( t1 );
                    };
                    $('.entry-notice').show();
                    $('.entry-progress').hide();
                    $('.re-entry').hide();
                    $('.upload-file').val('');
                }
            });
        });
    };
};

$.Serialize = function(){
    var isOk = true,
        data = window.ResumeData || {
            contact_info: {},
            resume: {
                job_target: {},
                professional_skills: [],
                educations: [],
                projects: [],
                trains: [],
                works: [],
                other_info: {
                    content: ''
                }
            }
        },
        checkForm = function( dom , val , isMust , isSelectMust , rule , placeholder ){

            if( typeof isMust != 'undefined' ){
                if( !val || !regs[rule].test( val ) || ( val == placeholder ) ){
                    dom.addClass('tip-error');
                    isOk = false;
                };
            };

            if( typeof isSelectMust != 'undefined' ){
                if( !val ){
                    dom.siblings('.button').addClass('tip-error');
                    isOk = false;
                };
            };

        },
        getContantInfo = function(){
            var forms = $('#JS_contact_info').find('input[type="text"],select'),
                contactInfo = {},
                gender = $('#JS_contact_info').find('[name="gender"]:checked').val(),
                political_landscape = $('#JS_contact_info').find('[name="political_landscape"]:checked').val(),
                highest_degree = $('#JS_contact_info').find('[name="highest_degree"]').val(),
                age = $('#JS_contact_info').find('[name="age"]').val();

            contactInfo.gender = gender;
            contactInfo.political_landscape = political_landscape;
            contactInfo.highest_degree = highest_degree;
            contactInfo.age = age;

            for( var i = 0 , l = forms.length ; i < l ; i++ ){
                var dom = forms.eq(i),
                    val = dom.val(),
                    isMust = dom.attr('data-equired'),
                    isSelectMust = dom.attr('data-equ'),
                    rule = dom.attr('data-reg'),
                    placeholder = dom.attr('placeholder'),
                    name = dom.attr('name');

                checkForm( dom , val , isMust , isSelectMust , rule , placeholder );
                if( val == placeholder ){
                    val = '';
                }
                contactInfo[name] = val;
            };

            return contactInfo;
        },
        getWorkInfo = function(){
            var list = $('#JS_work_info').find('.field-box'),
                workList = [];

            for(  var i = 0 , l = list.length ; i < l ; i++ ){

                var dom = list.eq(i),
                    company = dom.find('.JS_company_name'),
                    position = dom.find('.JS_position_title'),
                    start_year = dom.find('.work_start_year'),
                    end_year = dom.find('.work_end_year'),
                    start_month = dom.find('.work_start_month'),
                    end_month = dom.find('.work_end_month'),
                    job_desc = dom.find('.JS_job_desc'),
                    arr = [],
                    workInfo = {};
                arr.push(company,position,start_year,end_year,start_month,end_month,job_desc);

                for( var ii = 0 , ll = arr.length ; ii < ll ; ii++ ){
                    var dom = arr[ii],
                        val = dom.val(),
                        isMust = dom.attr('data-equired'),
                        isSelectMust = dom.attr('data-equ'),
                        rule = dom.attr('data-reg'),
                        placeholder = dom.attr('placeholder'),
                        name = dom.attr('name');

                    checkForm( dom , val , isMust , isSelectMust , rule , placeholder );
                    if( val == placeholder ){
                        val = '';
                    }

                    if( dom.hasClass('JS_company_name') ){
                        workInfo['company_name'] = val;
                    };
                    if( dom.hasClass('JS_position_title') ){
                        workInfo['position_title'] = val;
                    };
                    if( dom.hasClass('JS_job_desc') ){
                        workInfo['job_desc'] = val;
                    };
                    if( dom.hasClass('work_start_year') ){
                        workInfo['start_year'] = val;
                    };
                    if( dom.hasClass('work_start_month') ){
                        workInfo['start_month'] = val;
                    };
                    if( dom.hasClass('work_end_year') ){
                        workInfo['end_year'] = val;
                    };
                    if( dom.hasClass('work_end_month') ){
                        workInfo['end_month'] = val;
                    };
                };
                workList.push({
                    company_name: workInfo.company_name,
                    position_title: workInfo.position_title,
                    job_desc: workInfo.job_desc,
                    start_time: workInfo.start_year + '-' + workInfo.start_month,
                    end_time: ( workInfo.end_year != '至今' ? workInfo.end_year + '-' + workInfo.end_month : '至今')
                });
            };

            return workList;
        },
        getProjectInfo = function(){
            var list = $('#JS_project_info').find('.field-box'),
                itemList = [];

            for(  var i = 0 , l = list.length ; i < l ; i++ ){

                var dom = list.eq(i),
                    company = dom.find('.JS_project_name'),
                    position = dom.find('.JS_job_title'),
                    start_year = dom.find('.project_start_year'),
                    end_year = dom.find('.project_end_year'),
                    start_month = dom.find('.project_start_month'),
                    end_month = dom.find('.project_end_month'),
                    job_desc = dom.find('.JS_project_desc'),
                    arr = [],
                    info = {};
                arr.push(company,position,start_year,end_year,start_month,end_month,job_desc);

                for( var ii = 0 , ll = arr.length ; ii < ll ; ii++ ){
                    var dom = arr[ii],
                        val = dom.val(),
                        isMust = dom.attr('data-equired'),
                        isSelectMust = dom.attr('data-equ'),
                        rule = dom.attr('data-reg'),
                        placeholder = dom.attr('placeholder'),
                        name = dom.attr('name');

                    checkForm( dom , val , isMust , isSelectMust , rule , placeholder );
                    if( val == placeholder ){
                        val = '';
                    }

                    if( dom.hasClass('JS_project_name') ){
                        info['project_name'] = val;
                    };
                    if( dom.hasClass('JS_job_title') ){
                        info['job_title'] = val;
                    };
                    if( dom.hasClass('JS_project_desc') ){
                        info['project_desc'] = val;
                    };
                    if( dom.hasClass('project_start_year') ){
                        info['start_year'] = val;
                    };
                    if( dom.hasClass('project_start_month') ){
                        info['start_month'] = val;
                    };
                    if( dom.hasClass('project_end_year') ){
                        info['end_year'] = val;
                    };
                    if( dom.hasClass('project_end_month') ){
                        info['end_month'] = val;
                    };
                };
                itemList.push({
                    project_name: info.project_name,
                    job_title: info.job_title,
                    project_desc: info.project_desc,
                    start_time: info.start_year + '-' + info.start_month,
                    end_time: ( info.end_year != '至今' ? info.end_year + '-' + info.end_month : '至今')
                });
            }
            return itemList;
        },
        getEducationInfo = function(){
            var list = $('#JS_education_info').find('.field-box'),
                itemList = [];

            for(  var i = 0 , l = list.length ; i < l ; i++ ){

                var dom = list.eq(i),
                    company = dom.find('.JS_school'),
                    position = dom.find('.JS_major'),
                    start_year = dom.find('.edu_start_year'),
                    end_year = dom.find('.edu_end_year'),
                    start_month = dom.find('.edu_start_month'),
                    end_month = dom.find('.edu_end_month'),
                    job_desc = dom.find('.JS_degree'),
                    arr = [],
                    info = {};
                arr.push(company,position,start_year,end_year,start_month,end_month,job_desc);

                for( var ii = 0 , ll = arr.length ; ii < ll ; ii++ ){
                    var dom = arr[ii],
                        val = dom.val(),
                        isMust = dom.attr('data-equired'),
                        isSelectMust = dom.attr('data-equ'),
                        rule = dom.attr('data-reg'),
                        placeholder = dom.attr('placeholder'),
                        name = dom.attr('name');

                    checkForm( dom , val , isMust , isSelectMust , rule , placeholder );
                    if( val == placeholder ){
                        val = '';
                    }

                    if( dom.hasClass('JS_school') ){
                        info['school'] = val;
                    };
                    if( dom.hasClass('JS_major') ){
                        info['major'] = val;
                    };
                    if( dom.hasClass('JS_degree') ){
                        info['degree'] = val;
                    };
                    if( dom.hasClass('edu_start_year') ){
                        info['start_year'] = val;
                    };
                    if( dom.hasClass('edu_start_month') ){
                        info['start_month'] = val;
                    };
                    if( dom.hasClass('edu_end_year') ){
                        info['end_year'] = val;
                    };
                    if( dom.hasClass('edu_end_month') ){
                        info['end_month'] = val;
                    };
                };
                itemList.push({
                    school: info.school,
                    major: info.major,
                    degree: info.degree,
                    start_time: info.start_year + '-' + info.start_month,
                    end_time: ( info.end_year != '至今' ? info.end_year + '-' + info.end_month : '至今')
                });
            };

            return itemList;
        },
        getTrainInfo = function(){
            var list = $('#JS_train_info').find('.field-box'),
                itemList = [];

            for(  var i = 0 , l = list.length ; i < l ; i++ ){

                var dom = list.eq(i),
                    train_desc = dom.find('.JS_train_desc'),
                    start_year = dom.find('.train_start_year'),
                    end_year = dom.find('.train_end_year'),
                    start_month = dom.find('.train_start_month'),
                    end_month = dom.find('.train_end_month'),
                    arr = [],
                    info = {};
                arr.push(train_desc,start_year,end_year,start_month,end_month);

                for( var ii = 0 , ll = arr.length ; ii < ll ; ii++ ){
                    var dom = arr[ii],
                        val = dom.val(),
                        isMust = dom.attr('data-equired'),
                        isSelectMust = dom.attr('data-equ'),
                        rule = dom.attr('data-reg'),
                        placeholder = dom.attr('placeholder'),
                        name = dom.attr('name');

                    checkForm( dom , val , isMust , isSelectMust , rule , placeholder );
                    if( val == placeholder ){
                        val = '';
                    }

                    if( dom.hasClass('JS_train_desc') ){
                        info['train_desc'] = val;
                    };
                    if( dom.hasClass('train_start_year') ){
                        info['start_year'] = val;
                    };
                    if( dom.hasClass('train_start_month') ){
                        info['start_month'] = val;
                    };
                    if( dom.hasClass('train_end_year') ){
                        info['end_year'] = val;
                    };
                    if( dom.hasClass('train_end_month') ){
                        info['end_month'] = val;
                    };
                };
                itemList.push({
                    train_desc: info.train_desc,
                    start_time: info.start_year + '-' + info.start_month,
                    end_time: ( info.end_year != '至今' ? info.end_year + '-' + info.end_month : '至今')
                });
            };

            return itemList;
        },
        getSkillInfo = function(){
            var list = $('#JS_skill_info').find('.field-box'),
                itemList = [];

            for(  var i = 0 , l = list.length ; i < l ; i++ ){

                var dom = list.eq(i),
                    skill_desc = dom.find('.JS_skill_desc'),
                    proficiency = dom.find('.JS_proficiency'),
                    arr = [],
                    info = {};
                arr.push(skill_desc,proficiency);

                for( var ii = 0 , ll = arr.length ; ii < ll ; ii++ ){
                    var dom = arr[ii],
                        val = dom.val(),
                        isMust = dom.attr('data-equired'),
                        isSelectMust = dom.attr('data-equ'),
                        rule = dom.attr('data-reg'),
                        placeholder = dom.attr('placeholder'),
                        name = dom.attr('name');

                    checkForm( dom , val , isMust , isSelectMust , rule , placeholder );
                    if( val == placeholder ){
                        val = '';
                    }

                    if( dom.hasClass('JS_skill_desc') ){
                        info['skill_desc'] = val;
                    };
                    if( dom.hasClass('JS_proficiency') ){
                        info['proficiency'] = val;
                    };
                };
                itemList.push({
                    skill_desc: info.skill_desc,
                    proficiency: info.proficiency
                });
            };

            return itemList;
        };

    var contactInfo = getContantInfo();
    if( !isOk ){
        alert('个人信息输入有误！');
        return false;
    }else{

        if( $.isEmptyObject( data.contact_info ) ){
            data.contact_info = {};
        };

        data.contact_info.name = contactInfo.name;
        data.contact_info.phone = contactInfo.phone;
        data.contact_info.email = contactInfo.email;
        data.contact_info.age = contactInfo.age;
        data.contact_info.highest_degree = contactInfo.highest_degree;
        data.contact_info.gender = contactInfo.gender;

        if( $.isEmptyObject( data.resume ) ){
            data.resume = {};
        };

        data.resume.work_years = contactInfo.work_years;

        if( $.isEmptyObject( data.resume.job_target ) ){
            data.resume.job_target = {};
        };
        data.resume.job_target.expectation_area = contactInfo.expectation_area;
    };

    var workInfo = getWorkInfo();
    if( !isOk ){
        alert('工作经历输入有误！');
        return false;
    }else{
        data.resume.works = workInfo;
    };

    var educationInfo = getEducationInfo();
    if( !isOk ){
        alert('教育经历输入有误！');
        return false;
    }else{
        data.resume.educations = educationInfo;
    };

    //管理员保存
    if( $('body').attr('data-admin_edit') ){

        var projectInfo = getProjectInfo();
        if( !isOk ){
            alert('项目经历输入有误！');
            return false;
        }else{
            data.resume.projects = projectInfo;
        };

        

        var trainInfo = getTrainInfo();
        if( !isOk ){
            alert('培训经历输入有误！');
            return false;
        }else{
            data.resume.trains = trainInfo;
        };

        var skillInfo = getSkillInfo();
        if( !isOk ){
            alert('专业技能输入有误！');
            return false;
        }else{
            data.resume.professional_skills = skillInfo;
        };

        var evaluation = $('#JS_evaluation').val();
        data.resume.self_evaluation = evaluation || '';

    };

    var otherText = $('#JS_other_text').val();
    if( !data.resume.other_info ){
        data.resume.other_info = {};
    };

    data.resume.other_info.content = otherText || '';
    data.upload_file = $('#JS_upload_file').val();

    return data;
};

$(function(){

    $( document ).on( 'change' , 'input[type="text"],textarea' , function(){
        $( this ).closest('.field-box.saved').removeClass('saved').find('.JS_save_someone').show().end().find('.disabled').hide();
    });

    $('.upload-file').change(function(){
        var $this = $( this ),
            val = $this.val();
        if( !val ) return;
        $.uploadResume( val );
    });

    $( document ).on( 'click' , '#JS_cancel_upload' , function(){
        if( window.__jqxhr__ ){
            window.stopByUser = true;
            window.__jqxhr__.abort();
            window.__jqxhr__ = null;
            window.stopByUser = null;
        };
        if( window.t1 ){
            clearTimeout( t1 );
        };
        $('.entry-progress').hide();
        $('.entry-notice').show();
    });

    $(document).on('click', '.JS_save_someone' , function(){
        var $this = $(this),
            field = $this.closest('.field-box'),
            inputs = field.find('[data-equired]'),
            selects = field.find('select[data-equ]');

        var isOk = true;
        for( var i = 0, l = inputs.length ; i < l ; i++ ){
            var input = inputs.eq(i),
                reg = input.attr('data-reg'),
                val = $.trim( input.val() ),
                placeholder = input.attr('placeholder');

            if( !regs[reg].test( val ) || placeholder == val ){
                input.addClass('tip-error');
                isOk = false;
            };
        };
        for( var j = 0 , jj = selects.length ; j < jj ; j++ ){
            var select = selects.eq(j),
                val = select.val();
            if( !val ){
                select.siblings('.button').addClass('tip-error');
                isOk = false;
            };
        };
        if( !isOk ) return;

        $this.hide().siblings('.btn.disabled').show();
        if( $this.parent().hasClass('multiterm') ){
            $this.siblings('.JS_add_new').show();
        };
        $this.siblings('.JS_delete').show();
        field.addClass('saved');
    });

    //默认组装页面
    $.loadResume( ResumeData );

    //绑定输入框
    $.placeholderHandle();

    //绑定上传组建
    $.UploadResumeFile();

    $( document ).on( 'focus' , '#JS_resume_content [placeholder]' , function(){
        var $this = $( this ),
            holder = $this.attr('placeholder'),
            val = $this.val();
        if( val == holder ){
            $this.val('');
        };
    });

    $( document ).on( 'blur' , '#JS_resume_content [placeholder]' , function(){
        var $this = $( this ),
            holder = $this.attr('placeholder'),
            val = $this.val();
        if( val == '' && !$this.hasClass( 'data-fixholder' )){
            $this.val( holder );
        };
    });

});
