(function() {
    var app = angular.module('job', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter' ]);
    var $injector = angular.injector(['app.django', 'app.utils']);
    var tmpl = $injector.get('tmpl');
    var api = $injector.get('api');
    var id_url = $injector.get('id_url');

    app.config([
        '$stateProvider', '$urlRouterProvider',
        function($stateProvider, $urlRouterProvider) {
            $urlRouterProvider.otherwise('/recommend_job_list/');
            $stateProvider.state(
                'recommend',
                {
                    url: '/recommend_job_list/',
                    templateUrl: tmpl('job_hunting/job_list.html'),
                    controller: 'recommendJobList'
                }
            );
            $stateProvider.state(
                'end_recommend',
                {
                    url: '/end_recommend/',
                    templateUrl: tmpl('job_hunting/end_recommend.html')
                }
            );
        }
    ]);

    app.controller(
        'recommendJobList',
        ['$scope', '$http' , '$state' , '$stateParams' , '$filter' , function( $scope, $http , $state , $stateParams , $filter ) {

            $scope.showSendbtn = $scope.isShowMark = true;
            $scope.page = $stateParams.page;
            $scope.pages = 0;
            $scope.build_url = id_url;

            $scope.favorite_url = api.job.favorite;
            $scope.dislike_url = api.job.dislike;
            $scope.send_url = api.job.send;

            $scope.showJobGuess = false;    //显示机器猜测职位

            $scope.showDetail = false;
            $scope.toggleDetail = function(){
                $scope.showDetail = !$scope.showDetail;
            };

            $scope.operation = function(url_prefix, job_id , type ) {
                if( window.lockSubmit ) return false;
                window.lockSubmit = true;
                var types = {
                    send: '确认投递吗？',
                    favorite: '确定收藏后，可以去我的职位里查看哦！',
                    dislike: '不喜欢该职位？聘宝将根据你的反馈推荐更匹配的职位哦！'
                };

                if( type && !$.cookie( type ) ){
                    $.cookie( type , "true" , {expires: 30, path: '/', domain: document.domain});
                    if( type != 'favorite' ){
                        if( !window.confirm( types[ type ] ) ){
                            window.lockSubmit = false;
                            return false;
                        };
                    }else{
                        alert( types[ type ] );
                    };
                };

                var url = id_url(url_prefix, job_id);
                $http.get(url).success(function(data) {
                    if( data.status == 'ok' ){
                        var oper = data.operation;
                        if( oper == 'send' ){
                            $scope.showSendbtn = false;
                        }else if( oper == 'favorite' ){
                            $scope.isShowMark = false;
                        };
                        setTimeout( function(){
                            $scope.next();
                            window.lockSubmit = false;
                        } , 1000 );
                    }else{
                        var oper = data.operation;
                        if( oper == 'send' && data.redirect_url ){
                            alert('第一次投递，请完善简历！');
                            location.href = data.redirect_url;
                        };
                        window.lockSubmit = false;
                    };

                }).error(function(){
                    window.lockSubmit = false;
                });
            };

            $scope.next = function( type ){
                if( type && !$.cookie( type ) ){
                    $.cookie( type , "true" , {expires: 30, path: '/', domain: document.domain});
                   alert( '刷新后，该职位将不再推荐给你，聘宝建议好的职位优先收藏！');
                };
                if( $scope.page >= $scope.pages ){
                    $state.go('end_recommend');
                    return false;
                };
                $scope.page++;
                $http.post(
                    api.job.mark_job_read,
                    $.param({'job_id_list': $scope.job_id_list})
                ).success(function(data) {
                    $state.reload( 'recommend' );
                });
            };

            $scope.praiseCompany = function(){
                if( $scope.lockPraise ) return;
                $scope.lockPraise = true;
                var favour = $scope.data.data[0].has_favour,
                    id = $scope.data.data[0].job__company__id,
                    url = id_url(api.job.job_favour_company, id);
                $http.get( url ).success( function( data ){
                    if( data && data.status == 'ok' ){
                        if( data.data.action == 'favour' ){
                            $scope.data.data[0].has_favour = true;
                            $scope.data.data[0].job__company__favour_count++;
                            angular.element('#JS_praised').addClass('active');
                        }else{
                            $scope.data.data[0].has_favour = false;
                            $scope.data.data[0].job__company__favour_count--;
                            angular.element('#JS_praised').removeClass('active');
                        };
                    }
                    $scope.lockPraise = false;
                }).error(function(){
                    $scope.lockPraise = false;
                });
            };

            var url = api.job.recommend_job_list;
            $http.get( url ).success(function(data) {
                if( data.data && data.data.length ){
                    $scope.data = data;
                    $scope.hasRecord = true;
                    $scope.pages = data.pages;
                    $scope.resume_tag = data.resume_tag;
                    // $scope.process = data.data[0].succ_rate > 60 ? 'green': data.data[0].succ_rate > 20 ? 'orange' : 'red'; //投递成功率 
                    $scope.job_id_list = [];
                    angular.forEach($scope.data.data, function(value, key) {
                        this.push(value.id);
                    }, $scope.job_id_list);
                }else{
                    $state.go('end_recommend');
                };

            });
        }]
    );

})();
