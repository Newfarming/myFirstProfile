/**
 * 打印后台返回的错误内容
 * @param  {[type]} obj [description]
 * @return {[type]}     [description]
 */
function alertErrors(obj){
    var output = "";
    for(var i in obj){
        var property = obj[i];
        for(var key in property){
            if (typeof(property[key]) != 'function') {
                if (isNaN(parseInt(key))) {
                    output += i + " = {" + key + ':' + property[key] + '}<br>';
                } else {
                    var newObj = property[key].errors;
                    for(var j in newObj){
                        var sub_property = newObj[j];
                        output += i + " = {" + j + ':' + sub_property[0] + '}<br>';
                    }
                }
            };
        }
    }
    $.alert(output + '若看到此弹框请截图下来并联系聘宝管理员，谢谢！');
}
/**
 * 扩展数组对象，添加方法，根据索引删除元素
 * @param  {[type]} dx [description]
 * @return {[type]}    [description]
 */
Array.prototype.remove=function(dx)
{
    if(isNaN(dx)||dx > this.length)
        return false;
    for(var i = 0,n = 0;i < this.length;i++)
    {
        if(this[i] != this[dx])
        {
            this[n++] = this[i]
        }
    }
    this.length -= 1;
};
(function(angular,undefined){

    //根据自定义select获取所选值
    var degree_list = ['专科','本科','硕士','博士'];
    var degree_list_values = ['hnd','bachelor','master','phd'];
    var setDegreeValue=function(degree,trg){
        for(var i=0,imax=degree_list.length;i<imax;i++){
            if(degree_list[i]==degree){
                if(degree!='候选人最高学历（请选择）') $(trg).val(degree_list_values[i]);
                break;
            }
        }
    };
    //不做转换，直接用中文
    var setDegreeValue2=function(degree,trg){
        for(var i=0,imax=degree_list.length;i<imax;i++){
            if(degree_list[i]==degree){
                if(degree!='候选人最高学历（请选择）') $(trg).val(degree);
                break;
            }
        }
    };
    var getDegreeValue=function(degree){
        var result='';
        for(var i=0,imax=degree_list.length;i<imax;i++){
            if(degree_list[i]==degree){
                result=degree_list_values[i];
                break;
            }
        }
        return result;
    };
    var getReverseDegreeValue=function(degreeValue){
        var result='';
        for(var i=0,imax=degree_list_values.length;i<imax;i++){
            if(degree_list_values[i]==degreeValue){
                result=degree_list[i];
                break;
            }
        }
        return result;
    };

    var appModules=[
        'app.config' , 'ui.router' , 'app.utils' , 'app.filter' ,
        'app.django' , 'validation', 'validation.rule', 'ngRaven'
    ];
    var app = angular.module( 'uploadApp' , appModules ),
        $service = angular.injector( [ 'app.django' , 'app.utils' ] ),
        id_url = $service.get('id_url'),
        tmpl = $service.get('tmpl');
        //,
        //open_select = $service.get('open_select');

    app.controller(
        'uploadController',
        [
            '$scope',
            '$validation',
            '$http',
            '$injector',
            function( $scope , $validation , $http , $injector ){
                var $validationProvider = $injector.get('$validation'),
                    resumeData = JSON.parse($('#JS_container').attr('data-resumeData')),
                    task_id = $('#JS_container').attr('task-id');
                resumeData.task_id = task_id;
                $scope.isSubmiting = false;
                $scope.resume = angular.extend({
                    name: '',
                    gender: '',
                    phone: '',
                    email: '',
                    qq: '',
                    address: '',
                    work_years: '',
                    expect_work_place: $('#JS_expect_work_place').val(),
                    age: '',
                    expect_position: '',
                    target_salary: '',
                    degree: '',
                    self_evaluation: '',
                    works: [
                    ],
                    educations: [
                    ],
                    projects: [
                    ],
                    skills: [
                    ],
                    job_hunting_state: '',
                    last_contact: '',
                    hr_evaluate: '',
                    task_id: ''
                }, resumeData);
                $scope.works = 1;
                $scope.education = 2;
                $scope.projects = 3;
                $scope.skills = 4;

                // toggle icon status
                $scope.h_step_1 = false;
                $scope.h_step_2 = false;

                $scope.toggleSth = function (key, i_key){
                    $('#' + key).toggle();
                    var $i_key = $('#' + i_key);
                    $i_key.hasClass('i-toggle-90') ? $i_key.removeClass('i-toggle-90') : $i_key.addClass('i-toggle-90');
                }

                $scope.upload_form = {
                    submit: function (form) {
                        $('#JS_resume, #JS_status').show();
                        $validation.validate(form)
                            .success($scope.success)
                            .error($scope.error);
                    }
                };

                // 任务接受成功弹窗
                var html =  '<div class="mission-success">' +
                                '<h3 class="text-center"><i class="i-ms"></i>恭喜！任务接受成功！</h3>' +
                                '<p class="mt20 text-center">' +
                                    '<a class="btn red-btn" href="/partner/reco_task/#/list">继续认领任务</a>' +
                                    '<a class="btn blue-btn" href="/partner/task_manage/">查看我的任务</a>' +
                                '</p>' +
                            '</div>',
                    //简历录入成功信息
                    html2 = function(id){return '<div class="mission-success">' +
                                '<h3 class="text-center"><i class="i-ms"></i>恭喜，简历录入成功！</h3>' +
                                '<p class="c607d8b f14 text-center">请等待系统为您的简历推荐匹配的任务</p>' +
                                '<p class="mt20 text-center">' +
                                    //'<a class="btn red-btn" href="/partner/resume_manage/">我知道了</a>' +
                                    '<a class="btn red-btn" href="/partner/edit_resume/">继续录入简历</a>' +
                                    '<a class="btn blue-btn" href="/partner/edit_resume/'+id+'/">查看我的简历</a>' +
                                '</p>' +
                            '</div>';
                        },
                    //简历编辑成功信息
                    html3 = function(id){return '<div class="mission-success">' +
                                '<h3 class="text-center"><i class="i-ms"></i>简历编辑成功！</h3>' +
                                //'<p class="c607d8b f14 text-center">请等待系统为您的简历推荐匹配的任务</p>' +
                                '<p class="mt20 text-center">' +
                                    //'<a class="btn red-btn" href="/partner/resume_manage/">我知道了</a>' +
                                    '<a class="btn red-btn" href="/partner/edit_resume/">录入新的简历</a>' +
                                    '<a class="btn blue-btn" href="/partner/edit_resume/'+id+'/">继续编辑我的简历</a>' +
                                '</p>' +
                            '</div>';
                        },
                    //显示是否匹配信息
                    htmlForMatch = function(reason_name,task_id){
                        var title="";
                        if(typeof reason_name == 'string' && reason_name=='salary'){
                            //薪资不匹配
                            title="您上传的简历与任务薪资不匹配！";
                        }else{
                            //地点不匹配
                            title="您上传的简历与任务地点不匹配！";
                        }
                        return '<div class="mission-success">' +
                                '<h3 class="text-center"><i class="i-ms"></i>'+title+'</h3>' +
                                '<p class="caaa f14 text-center">(PS. 您录入的简历已保存至<a href="/partner/resume_manage/#/manage_detail/"><span class="c44b5e8">我的简历</span></a>中，系统将为您的简历匹配合适的任务)</p>' +
                                '<p class="mt20 text-center">' +
                                    //'<a class="btn red-btn" href="/partner/resume_manage/">我知道了</a>' +
                                    '<a class="btn red-btn" href="/partner/edit_resume/?task_id='+task_id+'">重新录入简历</a>' +
                                '</p>' +
                            '</div>';
                        };

                var postResume=function($scope,$http){

                    //如果候选人意向地为空，错误提示
                    if($('#JS_expect_work_place').prop('value')==""){
                        $('.search-city .search-city-field').addClass('searchCityInvalid');
                        $('#expect_work_place_message').html('<p class="validation-invalid">此项为必填项！</p>');
                        $('#JS_expect_work_place').focus();
                        return false;
                    }

                    if (!$scope.isSubmiting) {
                        $scope.isSubmiting = true;
                        // 验证成功，提交
                        $http.post(
                            '.',
                            JSON.stringify($scope.resume)
                        ).success(function(data) {
                            $scope.isSubmiting = false;
                            var task_id=$('#JS_container').attr('task-id');
                            if (data.status === 'ok') {
                                var msg = data.msg,
                                    resume_source = data.resume_source;
                                if (resume_source === 'add_task') {
                                    $.LayerOut({html: html});
                                } else if (resume_source === 'edit_resume') {
                                    $.LayerOut({html: html3(data.resume_id)});
                                } else if (resume_source === 'add_resume') {
                                    $.LayerOut({html: html2(data.resume_id)});
                                }
                                $('.JS_close_layerout').unbind('click').hide();
                                $('#myModal').unbind('click');
                            } else if (data.status === 'city_unfit') {
                                //city_unfit 简历期望工作地和任务的工作地不匹配
                                $.LayerOut({
                                    html: htmlForMatch('location',task_id),
                                    afterClose: function(){
                                        document.location.href='/partner/edit_resume/'+data.resume_id+'/?task_id='+task_id+'';
                                    }
                                });
                            } else if (data.status === 'salary_unfit') {
                                //salary_unfit 简历的期望薪资和任务的薪资不匹配
                                $.LayerOut({
                                    html: htmlForMatch('salary',task_id),
                                    afterClose: function(){
                                        document.location.href='/partner/edit_resume/'+data.resume_id+'/?task_id='+task_id+'';
                                    }
                                });
                            } else if (data.status === 'form_error') {
                                var errors = data.errors;
                                // 错误信息弹出
                                alertErrors(errors);
                            }
                        }).error(function(data) {
                            $scope.isSubmiting = false;
                            $.alert('请求失败！请重新提交...');
                        });
                    };
                };

                // Callback method
                $scope.success = function (message) {
                    postResume($scope,$http);
                    /*if (!$scope.isSubmiting) {
                        $scope.isSubmiting = true;
                        // 验证成功，提交
                        $http.post(
                            '.',
                            JSON.stringify($scope.resume)
                        ).success(function(data) {
                            $scope.isSubmiting = false;
                            if (data.status === 'ok') {
                                var msg = data.msg,
                                    resume_source = data.resume_source;
                                if (resume_source === 'add_task') {
                                    $.LayerOut({html: html});
                                } else if (resume_source === 'edit_resume') {
                                    $.LayerOut({html: html2(data.resume_id)});
                                };
                                $('.JS_close_layerout').unbind('click').hide();
                                $('#myModal').unbind('click');
                            } else if (data.status === 'form_error') {
                                var errors = data.errors;
                                // 错误信息弹出
                                alertErrors(errors);
                            }
                        }).error(function(data) {
                            $scope.isSubmiting = false;
                            $.alert('请求失败！请重新提交...');
                        });
                    };*/
                };

                $scope.error = function (message) {
                    // 验证失败

                    //如果候选人意向地不为空，自动取消错误提示
                    /*if($('#JS_expect_work_place').prop('value')!=""){
                        $('.search-city .search-city-field').removeClass('searchCityInvalid');
                        $('#expect_work_place_message').html('');
                    }*/

                    //如果候选人意向地为空，错误提示
                    if($('#JS_expect_work_place').prop('value')==""){
                        $('.search-city .search-city-field').addClass('searchCityInvalid');
                        $('#expect_work_place_message').html('<p class="validation-invalid">此项为必填项！</p>');
                        //$('#JS_expect_work_place').focus();
                        return false;
                    }

                    console.log(message);
                    return;

                };

                // 邮箱和电话号码后台查重规则
                var expression = {
                    email_recheck: function (value) {
                        var result = true,
                            options = {
                                type: 'get',
                                url: '/partner/check_exist_email?info=' + value + '&id=' + $scope.resume.id,
                                async:false,
                                success: function (data) {
                                    if (data.status === 'ok') {
                                        result = true;
                                    } else {
                                        result = false;
                                    }
                                },
                                error: function (result) {
                                }
                            };
                        $.ajax(options);
                        return result;
                    },
                    phone_recheck: function (value) {
                        var result = true,
                            options = {
                                type: 'get',
                                url: '/partner/check_exist_phone?info=' + value + '&id=' + $scope.resume.id,
                                async:false,
                                success: function (data) {
                                    if (data.status === 'ok') {
                                        result = true;
                                    } else {
                                        result = false;
                                    }
                                },
                                error: function (result) {
                                }
                            };
                        $.ajax(options);
                        return result;
                    }
                },
                defaultMsg = {
                    email_recheck: {
                        error: '该候选人已被推荐，请重新录入！'
                    },
                    phone_recheck: {
                        error: '该候选人已被推荐，请重新录入！'
                    }
                }

                // 添加邮箱和电话号码后台查重
                 $validationProvider
                .setExpression(expression)
                .setDefaultMsg(defaultMsg);

            }
        ]
    );
    app.controller(
        'editBaseInfo',
        [ '$scope' , '$http' , '$element' , 'id_url' , function( $scope , $http , $element , id_url ){

            // 获取本地存储对象
            var storage = window.localStorage;

            $scope.isMale = false;
            $scope.isFemale = false;
            if($scope.resume.gender === 'male'){
                $scope.isMale = true;
            }
            if($scope.resume.gender === 'female'){
                $scope.isFemale = true;
            }

            $scope.city_list = JSON.parse($('#JS_container').attr('data-all_citys'));
            $scope.showCityList = false;
            $scope.showCityListAlert = false;

            //用于监听城市列表是否该隐藏
            $scope.isCanHideCityList = false;

            // 已选择的城市
            $scope.selected_city = [];
            //storage.getItem('selected_city') ? storage.getItem('selected_city').split(',') : [];
            if($scope.resume.expect_work_place!="" && $scope.resume.expect_work_place != undefined){
                $scope.selected_city = $scope.resume.expect_work_place.split(",");
            }

            // toggle city list
            $scope.toggleCity = function(bool){
                if($('.search-city .search-city-field').hasClass('searchCityInvalid')){
                    if($('#expect_work_place_message').text() != ""){
                        $('.search-city .search-city-field').removeClass('searchCityInvalid');
                        $('#expect_work_place_message').html('')
                    }
                }
                $scope.showCityList = !bool;
                if($scope.showCityList){
                    $scope.isCanHideCityList = true;
                }
            }

            // 判断城市是否已选中
            $scope.isSelected = function(city) {
                for (var i = $scope.selected_city.length - 1; i >= 0; i--) {
                    if($scope.selected_city[i] === city){
                        return true;
                    }
                };
                return false;
            }

            //是否显示无效样式
            $scope.invalidSearchCity = function() {
                if($('#expect_work_place_message').text() != ""){
                    return true;
                }else{
                    return false;
                }
            }

            $scope.setCity = function(city, e) {
                var $target = $(e.target);
                if ($target.hasClass('selected')) {
                    $scope.showCityListAlert = false;
                    $target.removeClass('selected');
                    for(var i = 0,n = 0;i < $scope.selected_city.length;i++)
                    {
                        if($scope.selected_city[i] != city)
                        {
                            $scope.selected_city[n++] = $scope.selected_city[i]
                        }
                    }
                    $scope.selected_city.length -= 1;
                    storage.setItem('selected_city', $scope.selected_city);
                    //arr.join(',')
                } else {
                    if($scope.selected_city.length>=3){
                        $scope.showCityListAlert = true;
                        //console.log('showCityListAlert',$scope.showCityListAlert);
                    }else{
                        $scope.showCityListAlert = false;
                        $target.addClass('selected');
                        $scope.selected_city.push(city);
                    }

                }
                $scope.resume.expect_work_place=$scope.selected_city.join(',');
            };

            // 保存已选城市到本地存储
            $scope.saveCity = function() {
                storage.setItem('selected_city', $scope.selected_city);
                $scope.resume.expect_work_place=$scope.selected_city.join(',');
                $scope.showCityList = false;
            };

            //点击自定义select，弹出下拉
            $scope.toggleSelectDegree = function() {
                //open_select('.JS_degree_info');
            };

            /* start degree select*/
            $scope.degree_list = degree_list;
            $scope.showDegree = false;
            //用于监听列表是否该隐藏
            $scope.isCanHideDegreeList = false;

            // 已选择的 degree
            $scope.selected_degree = '候选人最高学历（请选择）';
            if($scope.resume.degree!="" && $scope.resume.degree != undefined){
                $scope.selected_degree = getReverseDegreeValue($scope.resume.degree);
            }

            // toggle list
            $scope.toggleDegree = function(bool){
                if($('.degree .degree-field').hasClass('searchDegreeInvalid')){
                    if($('#degree_message').text() != ""){
                        $('.degree .degree-field').removeClass('searchDegreeInvalid');
                        $('#degree_message').html('')
                    }
                }
                $scope.showDegree = !bool;
                if($scope.showDegree){
                    $scope.isCanHideDegreeList = true;
                }

            }

            // 判断是否已选中
            $scope.isSelectedOne = function(what) {
                if($scope.selected_degree === what){
                    return true;
                }
                return false;
            }

            //是否显示无效样式
            $scope.invalidShowDegree = function() {
                if($('#degree_message').text() != ""){
                    return true;
                }else{
                    return false;
                }
            }

            $scope.setDegree = function(what, e) {
                var $target = $(e.target);
                if ($target.hasClass('selected')) {
                    $target.removeClass('selected');
                    $scope.selected_degree = '候选人最高学历（请选择）';
                    storage.setItem('selected_degree', $scope.selected_degree);
                } else {
                    $target.addClass('selected');
                    $scope.selected_degree=what;
                    $scope.showDegree = false;

                }
                $scope.resume.degree=getDegreeValue($scope.selected_degree);

            };

            // 保存已选到本地存储
            $scope.saveDegree = function() {
                storage.setItem('selected_degree', $scope.selected_degree);
                $scope.resume.degree=getDegreeValue($scope.selected_degree);
                $scope.showDegree = false;
            };

            //点击自定义select，弹出下拉
            $scope.toggleSelectDegree = function() {
                //open_select('.JS_degree_info');
            };

            /* end degree select */

            //下拉框打开状态下，鼠标点击其他空白网页区域，默认收起下拉框
            $scope.hideCitySelectList = function(event) {
                var classDotStr=function(trgClassArr){
                    var trgClassDot='';
                    for(var i=0,imax=trgClassArr.length;i<imax;i++){
                        if(!trgClassArr[i].match(/^ng\-/i)){
                            trgClassDot+=' .'+trgClassArr[i];
                        }
                    }
                    return trgClassDot;
                };
                if($scope.isCanHideCityList===true){
                    var trgClass=$(event.target).attr('class');
                    if(trgClass!=undefined){
                        var trgClassArr=trgClass.split(' ');
                        var trgClassDot=classDotStr(trgClassArr);
                        if(trgClassDot!=''){
                            //console.log('trgClass',trgClass,trgClassDot,$('.city-list').find(trgClassDot).length);
                            if($('.city-list').find(trgClassDot).length
                                || trgClass.match(/(city\-list|search\-city\-field|i\-arr\-down)/i)) {
                                //console.log('not hide');
                            }else{
                                //console.log('hide');
                                $scope.showCityList = false;
                                $scope.isCanHideCityList = false;
                            }
                        }
                    }
                }
                if($scope.isCanHideDegreeList===true){
                    var trgClass=$(event.target).attr('class');
                    if(trgClass!=undefined){
                        var trgClassArr=trgClass.split(' ');
                        var trgClassDot=classDotStr(trgClassArr);
                        if(trgClassDot!=''){
                            //for degree
                            if($('.degree').find(trgClassDot).length
                                || trgClass.match(/(degree|degree\-field|i\-arr\-down)/i)) {
                                //console.log('degree not hide');
                            }else{
                                //console.log('degree hide');

                                $scope.showDegree = false;
                                $scope.isCanHideDegreeList = false;
                            }
                        }
                    }
                }
            };

            // 选择性别
            $scope.selectGender = function(value) {
                if (value == '1') {
                    $scope.isMale = true;
                    $scope.isFemale = false;
                    $scope.resume.gender = 'male';
                } else{
                    $scope.isMale = false;
                    $scope.isFemale = true;
                    $scope.resume.gender = 'female';
                };
            }
        }]
    ).filter( 'formatCity' , function(){
        return function( arr ){
            var newArr = [];
            if(arr.length === 0) {
                $('#JS_expect_work_place').val('');
                return '';//请选择';
            } else if(arr.length < 3) {
                $('#JS_expect_work_place').val(arr.join(','));
                return '：'+arr.join(',');
            } else {
                $('#JS_expect_work_place').val(arr.join(','));
                for (var i = 0; i < 2; i++) {
                    newArr.push(arr[i]);
                };
                return '：'+newArr.join(',') + '...';
            }
        }
    }).filter( 'formatCityForInput' , function(){
        return function( arr ){
            return arr.join(',');
        }
    }).filter( 'syncDegreeInfo' , function(){
        //同步到hidden元素
        return function( degree ){
            setDegreeValue(degree,'.JS_degree_info');
            return degree;
        }
    });

    app.controller(
        'additionController',
        ['$scope', '$http', '$validation', '$element', '$controller', '$timeout', function($scope, $http, $validation, $element, $controller, $timeout) {

            //教育经历的select保存值必须为中文，需做对应转换。比如：专科不能保存为hnd

            // init temp object
            $scope.temp = new Object();

            var experience_length = 0;
            if ($scope.experience != undefined) {
                experience_length = $scope.experience.length;
            };
            $scope.curr_edit = -1;
            $scope.isOpenItem = ( experience_length === 0 ? true : false );
            $scope.isDeleteShow = false;

            // 新增经历item
            $scope.add_item = function() {
                if (!$scope.isOpenItem) {
                    // 清空临时数组
                    $scope.temp = {};
                    $scope.curr_edit = -2;
                    $scope.isOpenItem = true;
                    $scope.isDeleteShow = false;
                };
            }

            // 编辑经历item
            $scope.edit_item = function(item, $index) {
                if (!$scope.isOpenItem) {

                    item._index = $index;
                    // 临时数组赋值
                    $scope.temp = angular.copy(item);

                    $scope.curr_edit = item._index;
                    $scope.isOpenItem = true;
                    $scope.isDeleteShow = ( experience_length === 1 ? false : true );

                    // 已选择的 degree
                    $scope.selected_degree = '候选人最高学历（请选择）';
                    if($scope.temp.degree!="" && $scope.temp.degree != undefined){
                        $scope.selected_degree = $scope.temp.degree;
                        //$scope.selected_degree = getReverseDegreeValue($scope.temp.degree);
                    }

                    $('.add-handle-title').text('编辑［'+$scope.temp.school+'］');

                }else{
                    $('.add-handle-title').text('新增一条');
                }
            }

            //点击自定义select，弹出下拉
            $scope.toggleSelectDegreeEdu = function() {
                //open_select('.JS_degree_edu');
            };

            // 保存经历item
            $scope.info_form = {
                submit: function (form) {
                    $('.add-handle-title').text('新增一条');
                    $validation.validate(form)
                        .success(function(message){
                            if($scope.temp._index != undefined){
                                //修改
                                $scope.experience.remove($scope.temp._index);
                            }
                            $scope.experience.push($scope.temp);
                            $scope.temp = {};
                            $scope.curr_edit = -1;
                            $scope.isOpenItem = false;
                            experience_length += 1;
                        })
                        .error(function(message){
                        });
                },
                reset: function(form, id, i_id) {
                    $('.add-handle-title').text('新增一条');
                    $validation.reset(form);
                    $scope.temp = {};
                    $scope.curr_edit = -2;
                    $scope.isOpenItem = false;
                    if (experience_length === 0) {
                        $('#' + id).hide();
                        $('#' + i_id).removeClass('i-toggle-90');
                    }
                }
            };

            // 取消编辑经历item
            $scope.cancelItem = function() {
                $('.add-handle-title').text('新增一条');
                if (experience_length === 0) {
                    return;
                } else {
                    $scope.temp = {};
                    $scope.curr_edit = -1;
                    $scope.isOpenItem = false;
                }
            }

            // 删除经历item
            $scope.deleteItem = function(item) {
                $('.add-handle-title').text('新增一条');
                if (experience_length === 0 && ( $scope.workForm || $scope.eduForm )) {
                    return;
                }
                $scope.experience.remove(item._index);
                $scope.curr_edit = -1;
                $scope.isOpenItem = false;
                experience_length === 0 ? experience_length = 0 : experience_length -= 1;
                $scope.temp = {};
            }

            //判断经历是否展示预览
            $scope.isPreview = function(item) {
                return item._index === $scope.curr_edit ? false : true;
            }


            /* start degree select*/
            $scope.degree_list=degree_list;
            $scope.degree_list_values=degree_list_values;
            $scope.getReverseDegreeValue=function(degreeValue){
                var result='';
                for(var i=0,imax=$scope.degree_list_values.length;i<imax;i++){
                    if($scope.degree_list_values[i]==degreeValue){
                        result=$scope.degree_list[i];
                        break;
                    }
                }
                return result;
            };
            $scope.showDegree = false;
            //用于监听列表是否该隐藏
            $scope.isCanHideDegreeList = false;

            // 已选择的 degree
            $scope.selected_degree = '候选人最高学历（请选择）';
            if($scope.temp.degree!="" && $scope.temp.degree != undefined){
                $scope.selected_degree = $scope.temp.degree;
                //$scope.selected_degree = getReverseDegreeValue($scope.temp.degree);
            }

            // toggle list
            $scope.toggleDegree = function(bool){
                if($('.degree .degree-field').hasClass('searchDegreeInvalid')){
                    if($('#edu_degree_message').text() != ""){
                        $('.degree .degree-field').removeClass('searchDegreeInvalid');
                        $('#edu_degree_message').html('')
                    }
                }
                $scope.showDegree = !bool;
                if($scope.showDegree){
                    $scope.isCanHideDegreeList = true;
                }

            }

            // 判断是否已选中
            $scope.isSelected = function(what) {
                if($scope.selected_degree === what){
                    return true;
                }
                return false;
            }

            //是否显示无效样式
            $scope.invalidShowDegree = function() {
                if($('#edu_degree_message').text() != ""){
                    return true;
                }else{
                    return false;
                }
            }

            $scope.setDegree = function(what, e) {
                var $target = $(e.target);
                if ($target.hasClass('selected')) {
                    $target.removeClass('selected');
                    $scope.selected_degree = '候选人最高学历（请选择）';
                    //storage.setItem('selected_degree', $scope.selected_degree);
                } else {
                    $target.addClass('selected');
                    $scope.selected_degree=what;
                    $scope.showDegree = false;

                }
                $scope.temp.degree=$scope.selected_degree;
                //$scope.temp.degree=getDegreeValue($scope.selected_degree);

            };

            // 保存已选到本地存储
            $scope.saveDegree = function() {
                //storage.setItem('selected_degree', $scope.selected_degree);
                $scope.temp.degree=$scope.selected_degree;
                //$scope.temp.degree=getDegreeValue($scope.selected_degree);
                $scope.showDegree = false;
            };

            //点击自定义select，弹出下拉
            $scope.toggleSelectDegree = function() {
                //open_select('.JS_degree_info');
            };

            /* end degree select */

            //下拉框打开状态下，鼠标点击其他空白网页区域，默认收起下拉框
            $scope.hideCitySelectList = function(event) {
                var classDotStr=function(trgClassArr){
                    var trgClassDot='';
                    for(var i=0,imax=trgClassArr.length;i<imax;i++){
                        if(!trgClassArr[i].match(/^ng\-/i)){
                            trgClassDot+=' .'+trgClassArr[i];
                        }
                    }
                    return trgClassDot;
                };
                if($scope.isCanHideDegreeList===true){
                    var trgClass=$(event.target).attr('class');
                    if(trgClass!=undefined){
                        var trgClassArr=trgClass.split(' ');
                        var trgClassDot=classDotStr(trgClassArr);
                        if(trgClassDot!=''){
                            //for degree
                            if($('.degree').find(trgClassDot).length
                                || trgClass.match(/(degree|degree\-field|i\-arr\-down)/i)) {
                                //console.log('degree not hide');
                            }else{
                                //console.log('degree hide');

                                $scope.showDegree = false;
                                $scope.isCanHideDegreeList = false;
                            }
                        }
                    }
                }
            };

            // 子表单与父表单分离验证
            $scope.$watch('workForm', function(form) {
              if(form) {
                // Do a copy of the controller
                var ctrlCopy = {};
                angular.copy(form, ctrlCopy);
                var parent_form = form.$$parentForm;
                parent_form.$removeControl(form);
                var isolatedFormCtrl = {
                    $setValidity: function (validationToken, isValid, control) {
                        ctrlCopy.$setValidity(validationToken, isValid, control);
                        parent_form.$setValidity(validationToken, true, form);
                    },
                    $setDirty: function () {
                        form.$dirty = true;
                        form.$pristine = false;
                    },
                };
                angular.extend(form, isolatedFormCtrl);
              }
            });

            $scope.$watch('eduForm', function(form) {
              if(form) {
                // Do a copy of the controller
                var ctrlCopy = {};
                angular.copy(form, ctrlCopy);
                var parent_form = form.$$parentForm;
                parent_form.$removeControl(form);
                var isolatedFormCtrl = {
                    $setValidity: function (validationToken, isValid, control) {
                        ctrlCopy.$setValidity(validationToken, isValid, control);
                        parent_form.$setValidity(validationToken, true, form);
                    },
                    $setDirty: function () {
                        form.$dirty = true;
                        form.$pristine = false;
                    },
                };
                angular.extend(form, isolatedFormCtrl);
              }
            });

            $scope.$watch('projectForm', function(form) {
              if(form) {
                // Do a copy of the controller
                var ctrlCopy = {};
                angular.copy(form, ctrlCopy);
                var parent_form = form.$$parentForm;
                parent_form.$removeControl(form);
                var isolatedFormCtrl = {
                    $setValidity: function (validationToken, isValid, control) {
                        ctrlCopy.$setValidity(validationToken, isValid, control);
                        parent_form.$setValidity(validationToken, true, form);
                    },
                    $setDirty: function () {
                        form.$dirty = true;
                        form.$pristine = false;
                    },
                };
                angular.extend(form, isolatedFormCtrl);
              }
            });

            $scope.$watch('skillForm', function(form) {
              if(form) {
                // Do a copy of the controller
                var ctrlCopy = {};
                angular.copy(form, ctrlCopy);
                var parent_form = form.$$parentForm;
                parent_form.$removeControl(form);
                var isolatedFormCtrl = {
                    $setValidity: function (validationToken, isValid, control) {
                        ctrlCopy.$setValidity(validationToken, isValid, control);
                        parent_form.$setValidity(validationToken, true, form);
                    },
                    $setDirty: function () {
                        form.$dirty = true;
                        form.$pristine = false;
                    },
                };
                angular.extend(form, isolatedFormCtrl);
              }
            });

        }]
    ).filter( 'syncDegreeEdu' , function(){
        //同步到hidden元素
        return function( degree ){
            setDegreeValue2(degree,'.JS_degree_edu');
            return degree;
        }
    });

    app.controller(
        'candidateStatus',
        ['$scope', function($scope) {

            $scope.job_hunting_state = null;
            if( $scope.$parent.resume.job_hunting_state === '目前正在找工作')
                $scope.job_hunting_state = 1;
            if( $scope.$parent.resume.job_hunting_state === '我目前在职，正考虑换个环境')
                $scope.job_hunting_state = 2;
            if( $scope.$parent.resume.job_hunting_state === '我目前处于离职状态，可立即上岗')
                $scope.job_hunting_state = 3;
            if( $scope.$parent.resume.job_hunting_state === '观望有好的机会再考虑')
                $scope.job_hunting_state = 4;
            $scope.last_contact = $scope.$parent.resume.last_contact;

            // 选择求职意愿
            $scope.selectStatus = function(value) {
                switch (value){
                    case 1:
                        $scope.job_hunting_state = 1;
                        $scope.$parent.resume.job_hunting_state = '目前正在找工作';
                        break;
                    case 2:
                        $scope.job_hunting_state = 2;
                        $scope.$parent.resume.job_hunting_state = '我目前在职，正考虑换个环境';
                        break;
                    case 3:
                        $scope.job_hunting_state = 3;
                        $scope.$parent.resume.job_hunting_state = '我目前处于离职状态，可立即上岗';
                        break;
                    case 4:
                        $scope.job_hunting_state = 4;
                        $scope.$parent.resume.job_hunting_state = '观望有好的机会再考虑';
                        break;
                    default:
                        break;
                }
            }

            // 选择最近联系时间
            $scope.selectLastContact = function(value) {
                switch (value){
                    case 1:
                        $scope.last_contact = 1;
                        $scope.$parent.resume.last_contact = 1;
                        break;
                    case 2:
                        $scope.last_contact = 2;
                        $scope.$parent.resume.last_contact = 2;
                        break;
                    case 3:
                        $scope.last_contact = 3;
                        $scope.$parent.resume.last_contact = 3;
                        break;
                    default:
                        break;
                }
            }

        }]
    );

    app.controller(
        'taskInfo',
        [
            '$scope',
            '$http',
            function($scope, $http){

                $scope.task_id = $scope.resume.task_id;

                // 定制预览
                $scope.feedData = null;
                $scope.viewFeed = false;
                $scope.showViewDesc = true;

                if ($scope.task_id != 0) {
                    // 获取任务数据
                    $http.get('/partner/task_info/' + $scope.task_id + '/')
                        .success(function(data){
                            if (data.status === 'ok') {
                                $scope.feedData = data.data;
                                $scope.feedData.company = data.data.feed.company;
                            } else {
                                $.alert('该任务无效！');
                                $scope.task_id = 0;
                            }
                        }).error(function(data){
                            $.alert('请求失败，请刷新页面！');
                        });
                }

                $scope.show_feed = function(feed) {
                    $scope.viewFeed = true;
                    $scope.refresh();
                }

                //切换职位详情
                $scope.toggleDesc = function(){
                    $scope.showViewDesc = !$scope.showViewDesc;
                    $scope.refresh();
                };

                //更新弹窗位置
                $scope.refresh = function(){
                    if( !$scope.viewFeed ) return;
                    setTimeout( function(){
                        $('.modal-dialog-view').css({
                            marginTop: ( $(window).height() - $('.modal-dialog-view').height() ) / 2 + 'px'
                        });
                    }, 0);
                };

                //定制显示开关
                $scope.toggleView = function( bool ){
                    $scope.viewFeed = bool;
                };
            }
        ]
    );

    app.directive('calendarWrapper', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/calendar_wrapper.html'),
            link: function(scope, elem, attrs) {

                // init 验证所需的 message-id
                scope.start_time_message = 'start_time_message' + scope.belong;
                scope.end_time_message =  'end_time_message' + scope.belong;

                scope.start_year = [];
                scope.end_year = ['至今'];
                scope.month = ['01月','02月','03月','04月','05月','06月','07月','08月','09月','10月','11月','12月'];

                // init time list
                scope.time_list = '';

                // init start_time & end_time
                scope.start_time_year = '开始年份';
                scope.start_time_month = '开始月份';
                scope.end_time_year = '结束年份';
                scope.end_time_month = '结束月份';

                if(scope.temp.start_time != undefined){
                    var start_time = scope.temp.start_time.split('.'),
                        end_time = scope.temp.end_time.split('.');
                    scope.start_time_year = start_time[0] + '年';
                    scope.start_time_month = start_time[1] + '月';
                    scope.start_time = scope.start_time_year + scope.start_time_month;
                    if(end_time[0] != '2100') {
                        scope.end_time_year = end_time[0] + '年';
                        scope.end_time_month = end_time[1] + '月';
                        scope.end_time = scope.end_time_year + scope.end_time_month;
                    } else {
                        scope.end_time_year = '至今';
                        scope.end_time_month = '至今';
                        scope.end_time = '至今';
                    }
                }

                var thisYear = new Date().getFullYear();
                for( var i = thisYear ; i > 1989 ; i--){
                    var year = i + '年';
                    scope.start_year.push(year);
                    scope.end_year.push(year);
                };

                scope.toggleList = function(value, e) {
                    var node_name = e.target.nodeName,
                        $target = $(e.target),
                        $pre_node = $target.parent().siblings().children()[0];
                    if (node_name == 'I') {
                        $target.siblings()[0].focus();
                    };
                    if (value === 'start_month') {
                        if(scope.start_time_year === '开始年份'){
                            scope.time_list = '';
                            $pre_node.focus();
                            return;
                        }
                    };
                    if(value === 'end_month') {
                        if(scope.end_time_year === '结束年份' || scope.end_time_year === '至今'){
                            scope.time_list = '';
                            $pre_node.focus();
                            return;
                        }
                    };
                    if(scope.time_list != value){
                        scope.time_list = value;
                        setTimeout(function() {
                            var $list = $target.next().next().length === 0 ? $target.next() : $target.next().next();
                            if(value === 'start_year') {
                                if(scope.start_time_year != '开始年份') {
                                    var top = $('#' + scope.start_time_year)[0].offsetTop,
                                        height = $list.height();
                                    if( top > (height/2) ){
                                        $list.scrollTop(Math.abs(top - height/3));
                                    }
                                }
                            };
                            if (value === 'end_year') {
                                if(scope.end_time_year != '结束年份') {
                                    var top = $('#' + scope.end_time_year)[0].offsetTop,
                                        height = $list.height();
                                    if( top > (height/2) ){
                                        $list.scrollTop(Math.abs(top - height/3));
                                    }
                                }
                            };
                            if (value === 'start_month') {
                                if(scope.start_time_month != '开始月份') {
                                    var top = $('#' + scope.start_time_month)[0].offsetTop,
                                        height = $list.height();
                                    if( top > (height/2) ){
                                        $list.scrollTop(Math.abs(top - height/3));
                                    }
                                }
                            };
                            if(value === 'end_month') {
                                if(scope.end_time_month != '结束月份') {
                                    var top = $('#' + scope.end_time_month)[0].offsetTop,
                                        height = $list.height();
                                    if( top > (height/2) ){
                                        $list.scrollTop(Math.abs(top - height/3));
                                    }
                                }
                            };
                        }, 0);
                        return;
                    };
                    scope.time_list = '';
                }

                $('body').click(function(e){
                    e.stopPropagation();
                    var $target = $(e.target),
                        target_type = $target.attr('target_type');
                    if (target_type != undefined){
                        return false;
                    } else {
                        $('.calendar-wrap-list').hide();
                        scope.time_list = '';
                    }
                });

                scope.setStartYear = function(value, e) {
                    if(!scope.isDisabled(value, 'start_year')){
                        scope.start_time_year = value;
                        scope.start_time = scope.start_time_year + scope.start_time_month;
                    } else {
                        scope.time_list = 'start_year';
                    }
                }

                scope.setStartMonth = function(value, e) {
                    if (scope.start_time_year != '开始年份' && !scope.isDisabled(value, 'start_month')) {
                        scope.start_time_month = value;
                        scope.start_time = scope.start_time_year + scope.start_time_month;
                        scope.temp.start_time = scope.start_time.replace('年', '.').replace('月', '');
                    } else {
                        scope.time_list = 'start_month';
                    }
                }

                scope.setEndYear = function(value, e) {
                    if(!scope.isDisabled(value, 'end_year')){
                        scope.end_time_year = value;
                        if (value === '至今') {
                            scope.end_time_month = '至今';
                            scope.temp.end_time = '2100.01';
                            return;
                        } else if (scope.end_time_month === '至今') {
                            scope.end_time_month = '结束月份';
                            scope.temp.end_time = '';
                        }
                        scope.end_time = scope.end_time_year + scope.end_time_month;
                    } else {
                        scope.time_list = 'end_year';
                    }
                }

                scope.setEndMonth = function(value, e) {
                    if (scope.end_time_year != '结束年份' && !scope.isDisabled(value, 'end_month')) {
                        scope.end_time_month = value;
                        scope.end_time = scope.end_time_year + scope.end_time_month;
                        scope.temp.end_time = scope.end_time.replace('年', '.').replace('月', '');
                    } else {
                        scope.time_list = 'end_month';
                    }
                }

                // 判断当前列表项是否选中
                scope.isSelected = function(item, type) {
                    if (type === 'start_year') {
                        return item === scope.start_time_year ? true : false;
                    };
                    if (type === 'start_month') {
                        return item === scope.start_time_month ? true : false;
                    };
                    if (type === 'end_year') {
                        return item === scope.end_time_year ? true : false;
                    };
                    if (type === 'end_month') {
                        return item === scope.end_time_month ? true : false;
                    };
                }

                // 判断当前列表项是否可选
                scope.isDisabled = function(item, type) {
                    if (type === 'start_year') {
                        if (scope.end_time != undefined){
                            if(scope.end_time_year != '至今') {
                                var item_year = parseInt(item.split('年')[0]),
                                    curr_end_year = parseInt(scope.end_time_year.split('年')[0]);
                                return item_year > curr_end_year ? true : false;
                            } else {
                                return false;
                            }
                        } else {
                            return false;
                        }
                    };
                    if (type === 'start_month') {
                        if (scope.end_time != undefined) {
                            if(scope.end_time != '至今') {
                                if (scope.end_time.split('年')[1].length != 0){
                                    var curr_end_year = parseInt(scope.end_time_year.split('年')[0]),
                                        curr_start_year = parseInt(scope.start_time_year.split('年')[0]);
                                    if (curr_end_year === curr_start_year) {
                                        var item_month = parseInt(item.split('月')[0]),
                                            curr_end_month = parseInt(scope.end_time_month.split('月')[0]);
                                        return item_month > curr_end_month ? true : false;
                                    } else {
                                        return false;
                                    }
                                } else {
                                    return false;
                                }
                            } else {
                                return false;
                            }
                        } else {
                            return false;
                        }
                    };
                    if (type === 'end_year') {
                        if (scope.start_time != undefined){
                            var item_year = parseInt(item.split('年')[0]),
                                curr_start_year = parseInt(scope.start_time_year.split('年')[0]);
                            return item_year < curr_start_year ? true : false;
                        } else {
                            return false;
                        }
                    };
                    if (type === 'end_month') {
                        if (scope.start_time != undefined) {
                            if (scope.start_time.split('年')[1].length != 0){
                                var curr_end_year = parseInt(scope.end_time_year.split('年')[0]),
                                    curr_start_year = parseInt(scope.start_time_year.split('年')[0]);
                                if (curr_end_year === curr_start_year) {
                                    var item_month = parseInt(item.split('月')[0]),
                                        curr_start_month = parseInt(scope.start_time_month.split('月')[0]);
                                    return item_month < curr_start_month ? true : false;
                                } else {
                                    return false;
                                }
                            } else {
                                return false;
                            }
                        } else {
                            return false;
                        }
                    };
                    return false;
                }
            },
            scope: {
                // 包含开始时间和结束时间的temp对象
                temp: '=',
                belong: '='
            }
        }
    });

    //为了保证样式统一，单选select也使用下拉日期的样式
    app.directive('selectWrapper', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/select_wrapper.html'),
            link: function(scope, elem, attrs) {

                // init 验证所需的 message-id
                scope.start_time_message = 'start_time_message' + scope.belong;
                scope.end_time_message =  'end_time_message' + scope.belong;

                scope.start_year = [];
                scope.end_year = ['至今'];
                scope.month = ['01月','02月','03月','04月','05月','06月','07月','08月','09月','10月','11月','12月'];

                // init time list
                scope.time_list = '';

                // init start_time & end_time
                scope.start_time_year = '开始年份';
                scope.start_time_month = '开始月份';
                scope.end_time_year = '结束年份';
                scope.end_time_month = '结束月份';

                if(scope.temp.start_time != undefined){
                    var start_time = scope.temp.start_time.split('.'),
                        end_time = scope.temp.end_time.split('.');
                    scope.start_time_year = start_time[0] + '年';
                    scope.start_time_month = start_time[1] + '月';
                    scope.start_time = scope.start_time_year + scope.start_time_month;
                    if(end_time[0] != '2100') {
                        scope.end_time_year = end_time[0] + '年';
                        scope.end_time_month = end_time[1] + '月';
                        scope.end_time = scope.end_time_year + scope.end_time_month;
                    } else {
                        scope.end_time_year = '至今';
                        scope.end_time_month = '至今';
                        scope.end_time = '至今';
                    }
                }

                var thisYear = new Date().getFullYear();
                for( var i = thisYear ; i > 1989 ; i--){
                    var year = i + '年';
                    scope.start_year.push(year);
                    scope.end_year.push(year);
                };

                scope.toggleList = function(value, e) {
                    var node_name = e.target.nodeName,
                        $target = $(e.target),
                        $pre_node = $target.parent().siblings().children()[0];
                    if (node_name == 'I') {
                        $target.siblings()[0].focus();
                    };
                    if (value === 'start_month') {
                        if(scope.start_time_year === '开始年份'){
                            scope.time_list = '';
                            $pre_node.focus();
                            return;
                        }
                    };
                    if(value === 'end_month') {
                        if(scope.end_time_year === '结束年份' || scope.end_time_year === '至今'){
                            scope.time_list = '';
                            $pre_node.focus();
                            return;
                        }
                    };
                    if(scope.time_list != value){
                        scope.time_list = value;
                        setTimeout(function() {
                            var $list = $target.next().next().length === 0 ? $target.next() : $target.next().next();
                            if(value === 'start_year') {
                                if(scope.start_time_year != '开始年份') {
                                    var top = $('#' + scope.start_time_year)[0].offsetTop,
                                        height = $list.height();
                                    if( top > (height/2) ){
                                        $list.scrollTop(Math.abs(top - height/3));
                                    }
                                }
                            };
                            if (value === 'end_year') {
                                if(scope.end_time_year != '结束年份') {
                                    var top = $('#' + scope.end_time_year)[0].offsetTop,
                                        height = $list.height();
                                    if( top > (height/2) ){
                                        $list.scrollTop(Math.abs(top - height/3));
                                    }
                                }
                            };
                            if (value === 'start_month') {
                                if(scope.start_time_month != '开始月份') {
                                    var top = $('#' + scope.start_time_month)[0].offsetTop,
                                        height = $list.height();
                                    if( top > (height/2) ){
                                        $list.scrollTop(Math.abs(top - height/3));
                                    }
                                }
                            };
                            if(value === 'end_month') {
                                if(scope.end_time_month != '结束月份') {
                                    var top = $('#' + scope.end_time_month)[0].offsetTop,
                                        height = $list.height();
                                    if( top > (height/2) ){
                                        $list.scrollTop(Math.abs(top - height/3));
                                    }
                                }
                            };
                        }, 0);
                        return;
                    };
                    scope.time_list = '';
                }

                $('body').click(function(e){
                    e.stopPropagation();
                    var $target = $(e.target),
                        target_type = $target.attr('target_type');
                    if (target_type != undefined){
                        return false;
                    } else {
                        $('.calendar-wrap-list').hide();
                        scope.time_list = '';
                    }
                });

                scope.setStartYear = function(value, e) {
                    if(!scope.isDisabled(value, 'start_year')){
                        scope.start_time_year = value;
                        scope.start_time = scope.start_time_year + scope.start_time_month;
                    } else {
                        scope.time_list = 'start_year';
                    }
                }

                scope.setStartMonth = function(value, e) {
                    if (scope.start_time_year != '开始年份' && !scope.isDisabled(value, 'start_month')) {
                        scope.start_time_month = value;
                        scope.start_time = scope.start_time_year + scope.start_time_month;
                        scope.temp.start_time = scope.start_time.replace('年', '.').replace('月', '');
                    } else {
                        scope.time_list = 'start_month';
                    }
                }

                scope.setEndYear = function(value, e) {
                    if(!scope.isDisabled(value, 'end_year')){
                        scope.end_time_year = value;
                        if (value === '至今') {
                            scope.end_time_month = '至今';
                            scope.temp.end_time = '2100.01';
                            return;
                        } else if (scope.end_time_month === '至今') {
                            scope.end_time_month = '结束月份';
                            scope.temp.end_time = '';
                        }
                        scope.end_time = scope.end_time_year + scope.end_time_month;
                    } else {
                        scope.time_list = 'end_year';
                    }
                }

                scope.setEndMonth = function(value, e) {
                    if (scope.end_time_year != '结束年份' && !scope.isDisabled(value, 'end_month')) {
                        scope.end_time_month = value;
                        scope.end_time = scope.end_time_year + scope.end_time_month;
                        scope.temp.end_time = scope.end_time.replace('年', '.').replace('月', '');
                    } else {
                        scope.time_list = 'end_month';
                    }
                }

                // 判断当前列表项是否选中
                scope.isSelected = function(item, type) {
                    if (type === 'start_year') {
                        return item === scope.start_time_year ? true : false;
                    };
                    if (type === 'start_month') {
                        return item === scope.start_time_month ? true : false;
                    };
                    if (type === 'end_year') {
                        return item === scope.end_time_year ? true : false;
                    };
                    if (type === 'end_month') {
                        return item === scope.end_time_month ? true : false;
                    };
                }

                // 判断当前列表项是否可选
                scope.isDisabled = function(item, type) {
                    if (type === 'start_year') {
                        if (scope.end_time != undefined){
                            if(scope.end_time_year != '至今') {
                                var item_year = parseInt(item.split('年')[0]),
                                    curr_end_year = parseInt(scope.end_time_year.split('年')[0]);
                                return item_year > curr_end_year ? true : false;
                            } else {
                                return false;
                            }
                        } else {
                            return false;
                        }
                    };
                    if (type === 'start_month') {
                        if (scope.end_time != undefined) {
                            if(scope.end_time != '至今') {
                                if (scope.end_time.split('年')[1].length != 0){
                                    var curr_end_year = parseInt(scope.end_time_year.split('年')[0]),
                                        curr_start_year = parseInt(scope.start_time_year.split('年')[0]);
                                    if (curr_end_year === curr_start_year) {
                                        var item_month = parseInt(item.split('月')[0]),
                                            curr_end_month = parseInt(scope.end_time_month.split('月')[0]);
                                        return item_month > curr_end_month ? true : false;
                                    } else {
                                        return false;
                                    }
                                } else {
                                    return false;
                                }
                            } else {
                                return false;
                            }
                        } else {
                            return false;
                        }
                    };
                    if (type === 'end_year') {
                        if (scope.start_time != undefined){
                            var item_year = parseInt(item.split('年')[0]),
                                curr_start_year = parseInt(scope.start_time_year.split('年')[0]);
                            return item_year < curr_start_year ? true : false;
                        } else {
                            return false;
                        }
                    };
                    if (type === 'end_month') {
                        if (scope.start_time != undefined) {
                            if (scope.start_time.split('年')[1].length != 0){
                                var curr_end_year = parseInt(scope.end_time_year.split('年')[0]),
                                    curr_start_year = parseInt(scope.start_time_year.split('年')[0]);
                                if (curr_end_year === curr_start_year) {
                                    var item_month = parseInt(item.split('月')[0]),
                                        curr_start_month = parseInt(scope.start_time_month.split('月')[0]);
                                    return item_month < curr_start_month ? true : false;
                                } else {
                                    return false;
                                }
                            } else {
                                return false;
                            }
                        } else {
                            return false;
                        }
                    };
                    return false;
                }
            },
            scope: {
                // 包含开始时间和结束时间的temp对象
                temp: '=',
                belong: '='
            }
        }
    });

    app.directive('baseInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/edit_base_info.html'),
            controller: 'editBaseInfo',
            link: function(scope, elem, attrs) {},
            scope: {
                resume: '=resume'
                /*,
                city_list: '=city_list',
                showCityList: '=showCityList'*/
            }

        }
    });

    app.directive('workInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/edit_work_info.html'),
            controller: 'additionController',
            link: function(scope, elem, attrs) {
            },
            scope: {
                experience: '=',
                belong: '='
            }
        }
    });

    app.directive('eduInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/edit_edu_info.html'),
            controller: 'additionController',
            link: function(scope, elem, attrs) {
            },
            scope: {
                experience: '=',
                belong: '='
            }
        }
    });

    app.directive('projectInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/edit_project_info.html'),
            controller: 'additionController',
            link: function(scope, elem, attrs, ctrl) {

            },
            scope: {
                experience: '=',
                action: '&',
                belong: '='
            }
        }
    });

    app.directive('skillInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/edit_skill_info.html'),
            controller: 'additionController',
            link: function(scope, elem, attrs) {
            },
            scope: {
                experience: '=',
                action: '&',
                belong: '='
            }
        }
    });

    app.directive('jobWish', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/edit_job_wish.html'),
            controller: 'candidateStatus',
            link: function(scope, elem, attrs) {
            },
            scope: {

            }
        }
    });

    app.directive('latestTime', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/edit_latest_time.html'),
            controller: 'candidateStatus',
            link: function(scope, elem, attrs) {
            },
            scope: {

            }
        }
    });

    app.directive('taskInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/task_info.html'),
            controller: 'taskInfo',
            link: function(scope, elem, attrs) {
            },
            scope: {
                resume: '=resume'
            }
        }
    });

    app.filter('endTime', function(){
        return function( i ){
            return i === '2100.01' ? '至今' : i;
        };
    });

    app.filter( 'category' , function(){
        return function( arr ){
            if( !arr || !arr.length ) return '';
            var newArr = [];
            for( var i = 0 , l = arr.length ; i < l ; i++ ){
                newArr.push( arr[ i ] );
            };
            return newArr.join(',');
        };
    });

})(angular);

$(function(){
    // input占位符兼容ie9
    if (!('placeholder' in document.createElement('input'))) {
        $('input[placeholder]').each(function() {

            var $input = $(this);
            var $label = $('<label>');
            $label.html($input.attr('placeholder'));
            $label.css({
                'font-size': '14px',
                'position': 'absolute',
                'left': '15px',
                'top': '13px',
                'color': '#999',
                'cursor': 'text',
                'width': '100%',
                'text-align': 'left'
            });

            $input.on('keydown paste', function() {
                setTimeout(function() {
                    $label[ $input.val() ? 'hide' : 'show' ]();
                }, 0);
            }).parent().append(
                $label.on('click', function() {
                    $input.focus();
                })
            );
        });
    }

});
