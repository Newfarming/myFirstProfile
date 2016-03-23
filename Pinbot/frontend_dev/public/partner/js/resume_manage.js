// 跨浏览器取消冒泡
function cancelBubble(e){
    if (!e)
        var e = window.event;
        e.cancelBubble = true;
    if (e.stopPropagation)
        e.stopPropagation();
}
(function(angular,undefined){

    var app = angular.module( 'manageApp' , [ 'app.config' , 'ui.router' , 'app.utils' , 'app.filter' , 'app.django' , 'validation', 'validation.rule' ] ),
        $django = angular.injector(['app.django']),
        $service = angular.injector( [ 'app.django' , 'app.utils' ] ),
        tmpl = $service.get('tmpl'),
        static_url = $django.get('static_url');
        clean = $service.get('clean'),

    app.config([
        '$stateProvider', '$urlRouterProvider',
        function($stateProvider, $urlRouterProvider) {
            $urlRouterProvider.otherwise('/manage_detail/');
            $stateProvider.state(
                'manage_detail',
                {
                    url: '/manage_detail/',
                    templateUrl: tmpl('partner/manage_detail.html'),
                    controller: 'manageResume'
                }
            );
            $stateProvider.state(
                'manage_preview',
                {
                    url: '/manage_preview/:task_id/',
                    templateUrl: tmpl('partner/manage_preview.html'),
                    controller: 'manageResume'
                }
            );
            $stateProvider.state(
                'manage_blank',
                {
                    url: '/manage_blank/:page_type/',
                    templateUrl: tmpl('partner/manage_blank.html'),
                    controller: 'manageResume'
                }
            );
            $stateProvider.state(
                'preview_blank',
                {
                    url: '/preview_blank/:task_id/',
                    templateUrl: tmpl('partner/preview_blank.html'),
                    controller: 'previewBlank'
                }
            );
        }
    ]);

    app.controller(
        'manageResume',
        [
            '$scope',
            '$http',
            '$state',
            '$stateParams',
            '$timeout',
            function( $scope , $http , $state , $stateParams, $timeout){
                $scope.list_data = null;
                $scope.is_paginated = false;
                $scope.hasMore = false;
                $scope.currentPage = -1;
                $scope.pages = 0;
                $scope.isSubmiting = false;
                $scope.isLoading = true;
                $scope.task_id = $stateParams.task_id;

                // 搜索关键字
                $scope.query = '';
                if(window.location.hash.indexOf('query') != -1){
                    $scope.query = window.location.hash.split('=')[1];
                }

                // 定制预览
                $scope.feedData = null;
                $scope.viewFeed = false;
                $scope.showViewDesc = true;

                // 搜索关键字
                $scope.search_key = '';

                if(window.location.hash.indexOf('manage_blank') === -1){
                    // 获取数据(空白页不执行)
                    $http.get(
                        '/partner/upload_resume_list/?query=' + $scope.query + '&task_id=' + $scope.task_id
                    ).success(
                        function(data){
                            if(data.data.length > 0){
                                $scope.list_data = data.data;
                                $scope.currentPage = data.current;
                                $scope.pages = data.pages;
                                $scope.is_paginated = $scope.currentPage === $scope.pages ? false : true;
                                $scope.hasMore = $scope.currentPage === $scope.pages ? false : true;
                                $scope.isLoading = false;
                            } else {
                                // 区分detail和preview
                                var page_type = window.location.hash.split('/')[1] + '/',
                                    task_id = window.location.hash.split('/')[2];
                                if(page_type != 'manage_detail/'){
                                    page_type = page_type + '?' + task_id;
                                }
                                // 无数据，跳转至空白页
                                if(page_type != 'manage_blank/' && page_type.indexOf('manage_preview') === -1){
                                    window.location.hash = '#/manage_blank/' + page_type;
                                } else if (page_type.indexOf('manage_preview') != -1) {
                                    $state.go(
                                        'preview_blank',
                                        {
                                            task_id: task_id
                                        }
                                    );
                                }
                            }
                        }
                    );
                }

                var url = '';

                $scope.link2edit_resume = function(resume_id, e) {
                    url = '/partner/edit_resume/' + resume_id + '/';
                    window.location.href = url;
                    cancelBubble(e);
                }

                $scope.link2resume_detail = function(resume_id) {
                    url = '/resumes/display/' + resume_id + '/';
                    window.open(url);
                }

                $scope.show_feed = function(feed) {
                    $scope.feedData = feed;
                    $scope.viewFeed = true;
                    $scope.refresh();
                }

                // 任务接受成功弹窗
                var html =  '<div class="mission-success">' +
                                '<h3 class="text-center"><i class="i-ms"></i>恭喜！任务接受成功！</h3>' +
                                '<p class="mt20 text-center">' +
                                    '<a class="btn red-btn" href="/partner/reco_task/#/list">继续认领任务</a>' +
                                    '<a class="btn blue-btn" href="/partner/task_manage/">查看我的任务</a>' +
                                '</p>' +
                            '</div>';

                // 接受任务
                $scope.accept_mission = function(task_id, resume_id, e, task) {

                    var task_id = clean(task_id.toString(),'[^0-9]');
                    var resume_id = clean(resume_id.toString(),'[^0-9]');
                    
                    // 接受任务时，增加弹窗确认 bg Adam 2015-08-04 18:48
                    var confirmOkFunc=function(){
                        
                        url = '/partner/accept_resume_task/' + task_id + '/' + resume_id + '/';
                        if(!$scope.isSubmiting) {
                            $scope.isSubmiting = true;
                            $http.get(url)
                            .success(function(data){
                                if(data.status == 'ok'){
                                    $.LayerOut({html: html});
                                    $('#myModal').unbind('click');
                                    $scope.refreshTaskData(resume_id, task_id);
                                } else {
                                    $.alert(data.msg);
                                }
                                $scope.isSubmiting = false;
                            })
                            .error(function(data){
                                $.alert('请求失败，请重新请求！');
                                $scope.isSubmiting = false;
                            });
                        }
                        cancelBubble(e);

                    };

                    var resumeName=$('.resume-content-'+resume_id+' .info .work span:first-child').text()
                                    +'-'+$('.resume-content-'+resume_id+' .info .name').text();//
                    $.confirm( '<p class="c607d8b f14 fcenter">你选择将简历：[<span class="c44b5e8">'+resumeName+'</span>]推荐给任务：[<span class="c44b5e8">'+task.feed.title+'</span>]？</p>', confirmOkFunc, function(){}, '<p><i class="i-ask"></i> <span>需要您的确认</span></p>', 
                        {
                            handlers: [
                                {
                                    title: '重新选择',
                                    eventType: 'click',
                                    className: 'button button-primary main-color-btn w158 f16',
                                    event: function(){
                                        $._LayerOut.close();
                                    }
                                },
                                {
                                    title: '确认',
                                    eventType: 'click',
                                    className: 'button button-primary red-btn w158 f16',
                                    event: function(){
                                        confirmOkFunc();
                                        $._LayerOut.close();
                                    }
                                }
                            ]
                        }
                    );

                    cancelBubble(e);

                }

                // 选我
                $scope.pick_resume = function(resume_id, e) {
                    var resume_id = clean(resume_id.toString(),'[^0-9]');
                    var task_id = clean($scope.task_id,'[^0-9]');

                    //显示是否匹配信息
                    var htmlForMatch = function(reason_name,task_id){
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
                                /*'<p class="caaa f14 text-center">(PS. 您录入的简历已保存至<a href="/partner/resume_manage/#/manage_detail/"><span class="c44b5e8">我的简历</span></a>中，系统将为您的简历匹配合适的任务)</p>' +*/
                                '<p class="mt20 text-center">' +
                                    '<a class="btn red-btn JS_close_layerout" href="javascript:void(0);">我知道了</a>' +
                                    /*'<a class="btn red-btn" href="/partner/edit_resume/?task_id='+task_id+'">重新录入简历</a>' +*/
                                '</p>' +
                            '</div>';
                        };

                    // 选择已有简历匹配任务时，增加弹窗确认 bg Adam 2015-08-04 15:11
                    var confirmOkFunc=function(){

                        //var task_id = clean(window.location.hash.split('/')[2],'[^0-9]');
                        url = '/partner/accept_task/' + task_id + '/' + resume_id + '/';

                        if(task_id.match(/^[0-9a-z]+$/i) && !$scope.isSubmiting) {
                            $scope.isSubmiting = true;
                            $http.get(url)
                                .success(function(data){
                                    if(data.status == 'ok'){
                                        $.LayerOut({html: html});
                                        $('#myModal').unbind('click');
                                        $scope.refreshListData(resume_id, task_id);
                                    } else {
                                        $.alert(data.msg);
                                    }
                                    $scope.isSubmiting = false;
                                })
                                .error(function(data){
                                    $.alert('请求失败，请重新请求！');
                                    $scope.isSubmiting = false;
                                });
                        }
                        cancelBubble(e);

                    };

                    var resumeName=$('.resume-content-'+resume_id+' .info .work span:first-child').text()
                                    +'-'+$('.resume-content-'+resume_id+' .info .name').text();//
                    var taskTitle=$('.task-title a').text();//task-title

                    //检查简历是否匹配要求
                    $http.get('/partner/check_accept_task/'+task_id+'/' + resume_id + '/')
                        .success(function(data){
                            if(data.hasOwnProperty('status')){
                                if (data.status === 'city_unfit') {
                                    //city_unfit 简历期望工作地和任务的工作地不匹配
                                    $.LayerOut({html: htmlForMatch('location',task_id)});
                                } else if (data.status === 'salary_unfit') {
                                    //salary_unfit 简历的期望薪资和任务的薪资不匹配
                                    $.LayerOut({html: htmlForMatch('salary',task_id)});
                                } else {
                                    $.confirm( '<p class="c607d8b f14 fcenter">你选择将简历：[<span class="c44b5e8">'+resumeName+'</span>]推荐给任务：[<span class="c44b5e8">'+taskTitle+'</span>]？</p>', confirmOkFunc, function(){}, '<p><i class="i-ask"></i> <span>需要您的确认</span></p>', 
                                        {
                                            handlers: [
                                                {
                                                    title: '重新选择',
                                                    eventType: 'click',
                                                    className: 'button button-primary main-color-btn w158 f16',
                                                    event: function(){
                                                        $._LayerOut.close();
                                                    }
                                                },
                                                {
                                                    title: '确认',
                                                    eventType: 'click',
                                                    className: 'button button-primary red-btn w158 f16',
                                                    event: function(){
                                                        confirmOkFunc();
                                                        $._LayerOut.close();
                                                    }
                                                }
                                            ]
                                        }
                                    );
                                }
                            } else {
                                $.alert(data.msg);
                            }
                            $scope.isSubmiting = false;
                        })
                        .error(function(data){
                            $.alert('请求失败，请重新请求！');
                            $scope.isSubmiting = false;
                        });

                    cancelBubble(e);

                    
                }

                // 点击接受任务后刷新任务列表
                $scope.refreshTaskData = function(resume_id, task_id) {
                    var temp_task_list = [];
                    for(var key in $scope.list_data){
                        if ($scope.list_data[key].id === resume_id) {
                            for(var key_2 in $scope.list_data[key].reco_resume_tasks) {
                                if($scope.list_data[key].reco_resume_tasks[key_2].id != task_id)
                                    temp_task_list.push($scope.list_data[key].reco_resume_tasks[key_2]);
                            }
                            $scope.list_data[key].reco_resume_tasks = temp_task_list;
                        };
                    }
                }

                // 点击选我后刷新list_data
                $scope.refreshListData = function(resume_id, task_id) {
                    var temp_list_data = [];
                    for(var key in $scope.list_data){
                        if($scope.list_data[key].id != resume_id){
                            temp_list_data.push($scope.list_data[key])
                        }
                    }
                    $scope.list_data = temp_list_data;
                    if($scope.list_data.length === 0){
                        window.location.hash = '#/manage_blank/manage_preview/?' + task_id;
                    }
                }

                $scope.fetchMore = function() {
                    $scope.hasMore = false;
                    if($scope.is_paginated) {
                        var nextPage = $scope.currentPage + 1;
                        $http.get(
                            '/partner/upload_resume_list/?page=' + nextPage
                        ).success(
                            function(data){
                                $scope.list_data = $scope.list_data.concat(data.data);
                                $scope.currentPage = data.current;
                                $scope.pages = data.pages;
                                $scope.is_paginated = $scope.currentPage === $scope.pages ? false : true;
                                $scope.hasMore = $scope.currentPage === $scope.pages ? false : true;
                            }
                        );
                    } else {
                        $scope.is_paginated = false;
                    }
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

                // 搜索简历
                $scope.searchResume = function(e) {
                    // 获取key值
                    var query_key = $scope.search_key,
                        task_id = '';
                    // 空白页上的操作
                    if(window.location.hash.indexOf('manage_blank') != -1){
                        var page_type = window.location.hash.split('/')[2];
                        if(page_type === 'manage_detail') {
                            window.location.hash = '#/manage_detail/?query=' + query_key;
                        } else if (page_type === 'manage_preview'){
                            task_id = window.location.hash.split('?')[1];
                            window.location.hash = '#/manage_preview/'+ task_id +'/?query=' + query_key;
                        }
                    } else {
                        $scope.isLoading = true;
                        $scope.hasMore = false;
                        $scope.is_paginated = false;
                        $http.get(
                            '/partner/upload_resume_list/?query=' + query_key + '&task_id=' + task_id
                        ).success(
                            function(data){
                                if(data.data.length > 0){
                                    $scope.list_data = data.data;
                                    $scope.currentPage = data.current;
                                    $scope.pages = data.pages;
                                    $scope.is_paginated = $scope.currentPage === $scope.pages ? false : true;
                                    $scope.hasMore = $scope.currentPage === $scope.pages ? false : true;
                                    $scope.isLoading = false;
                                } else {
                                    // 区分detail和preview
                                    var page_type = window.location.hash.split('/')[1] + '/',
                                        task_id = window.location.hash.split('/')[2];
                                    page_type = (task_id === '' ? page_type : page_type + '?' + task_id);
                                    // 无数据，跳转至空白页
                                    if(page_type != 'manage_blank'){
                                        window.location.hash = '#/manage_blank/' + page_type;
                                    }
                                }
                            }
                        );
                    }
                }
            }
        ]
    );

    app.controller(
        'previewBlank',
        [
            '$scope',
            '$state',
            '$stateParams',
            function( $scope , $state , $stateParams ){
                var task_id = $stateParams.task_id;
                    url = "/partner/edit_resume/?task_id=" + task_id;
                $scope.link2edit_resume = function() {
                    window.location.href = url;
                }
            }
        ]
    );

    app.controller(
        'taskInfo',
        [
            '$scope',
            '$http',
            function($scope, $http){
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
        ]
    );

    app.directive('taskInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/task_info.html'),
            controller: 'taskInfo',
            link: function(scope, elem, attrs) {
            },
            scope: true
        }
    });

    app.filter('salary', function(){
        return function( i ){
            return i / 1000;
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

    app.filter( 'limitword' , function(){
        return function( val ){
            if( val.length > 7 ){
                val = val.substring(0, 7) + '...';
            }
            return val;
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
                'font-size': '15px',
                'position': 'absolute',
                'left': '11px',
                'top': '42px',
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

    // 加载更多
    $(window).on('scroll', function(){
        var $doc = $(document),
            $fetchMore = $('#JS_fetch_more');
        if (!$fetchMore.length) return !1;
        if (!$fetchMore.is(":hidden")) {
            var n = $doc.height() - $doc.scrollTop() - $(window).height();
            100 > n && $fetchMore.get(0).click();
        }
    });

    $(document).on('keyup', function(event){
        if(event.keyCode ==13){
            $('#JS_search').trigger("click");
        }
    });
});
