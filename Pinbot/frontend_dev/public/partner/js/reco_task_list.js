(function(){

    var app = angular.module( 'taskListApp' , [ 'ui.router' , 'app.config' , 'app.filter' ] ),
        $injector = angular.injector( [ 'app.utils' , 'app.django' ] ),
        id_url = $injector.get('id_url'),
        tmpl = $injector.get('tmpl'),
        static_url = $injector.get('static_url');

    app.config([
        '$stateProvider',
        '$urlRouterProvider',
        function( $stateProvider , $urlRouterProvider ){

            $urlRouterProvider.otherwise('/list');

            $stateProvider
                .state( 'list' ,{
                    url: '/list?query&page',
                    controller: 'listCtrl',
                    templateUrl: tmpl( 'partner/task_list.html' )
                });

        }
    ]);

    app.controller( 'taskListCtrl' , [
        '$scope',
        '$http',
        '$state',
        '$location',
        '$rootScope',
        '$compile',
        function( $scope , $http , $state , $location , $rootScope , $compile ){

            $scope.page = $location.$$search.page || 1;
            $scope.query = $location.$$search.query || '';

            //搜索关键词
            $scope.search = function(){
                angular.element('[ui-view]').html('');
                $scope.page = 1;
                $state.go( 'list' , {
                    query: $scope.query,
                    page: $scope.page
                });
            };

            //定制预览
            $scope.showViewDesc = true;
            $scope.viewFeed = false;

            //定制显示开关
            $scope.toggleView = function( bool ){
                $scope.viewFeed = bool;
            };

            //预览定制
            $scope.showFeed = function( task , $e ){
                if( angular.element( $e.target).hasClass('JS_view_desc') ) return false;
                $scope.toggleView( true );
                $scope.feedData = {
                    task: task,
                    feed: task.feed,
                    company: task.feed.company
                };
                $scope.refresh();
            };

            //接受任务弹窗开关
            $scope.toogleBackdrop = function( bool ){
                $scope.showBackdrop = bool;
            };

            //接受任务事件
            $scope.isShowLayer = function( $e , id ){
                $scope.viewFeed = false;
                $scope.toogleBackdrop( true );
                $scope.upload_url =  '/partner/edit_resume/?task_id=' + id;
                $scope.select_url =  '/partner/resume_manage/#/manage_preview/' + id + '/';
                $e.stopPropagation();
            };

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

            //跳转简历详情页面
            $scope.toViewResume = function( resume ){

                var url = '/resumes/display/' + resume.resume_id + '/?feed_id=' + resume.feed_id,
                    new_tab = window.open();

                new_tab.opener = null;
                new_tab.open( '' , '_self' , '' );
                new_tab.location = url;

            };

            $scope.loadMoreFun = function(){
                if( $( document ).height() - $( window ).height() - $( document ).scrollTop() > 100 ) return false;
                if( $rootScope.loading ) return false;
                if( $scope.page >= $rootScope.pages ) return false;
                $rootScope.loading = true;
                $scope.page++;

                /* 通过 directive 创建一个空的模板,等ajax请求完成，刷新模板 */
                var moreItem = $compile('<load-more page="' + $scope.page + '"></load-more>')($scope);
                angular.element('[ui-view]').append( moreItem );
            };

            angular.element( window ).on( 'scroll' , $scope.loadMoreFun );

        }
    ])

    app.controller( 'listCtrl' , [
        '$scope',
        '$http',
        '$stateParams',
        '$rootScope',
        function( $scope , $http , $stateParams , $rootScope ){

            //获取关键词
            $scope.query = $stateParams.query;
            $scope.page = $scope.page || 1;

            $rootScope.loading = true;

            //显示弹窗
            $scope.showBackdrop = false;

            //跟进简历
            $scope.followResume = function( $e ){
                $e.stopPropagation();
            };

            //阻止冒泡
            $scope.stopPropagation = function( $e ){
                $e.stopPropagation();
            };

            $http.get(
                '/partner/accept_task_list/',
                {
                    params: {
                        query: $scope.query,
                        page: $scope.page,
                        ___: new Date().getTime()
                    }
                }
            ).success(function( res ){
                if( res && res.data && res.data.length ){
                    $rootScope.pages = res.pages;
                    $scope.data = res.data;
                    $rootScope.noAnyData = false;
                }else if( $scope.page == 1 ){
                    $rootScope.noAnyData = true;
                }else{
                    $rootScope.noAnyData = false;
                };
                $rootScope.loading = false;

            }).error(function(){
                $rootScope.loading = false;
                if( $scope.page == 1 ){
                    $rootScope.noAnyData = true;
                };
            });

        }
    ])

    app.directive( 'ngEnter' , function(){
        return function( scope , element , attrs ){
            element.bind( 'keydown keypress' , function( event ){
                if( event.keyCode === 13 ){
                    scope.$apply(function(){
                        scope.$eval( attrs.ngEnter );
                    });

                    event.preventDefault();
                };
            });
        };
    });

    app.directive( 'loadMore' , function(){
        return {
            restrict: 'E',
            controller: 'listCtrl',
            scope: true,
            templateUrl: tmpl( 'partner/task_list.html' )
        };
    });

})();

$(function(){

    $.Tip({
        selector: '.JS_view_desc',
        cssText: 'width:400px;',
        success: function( datas ){
            var that = this,
                $model = $('#JS_tip_model'),
                html = '',
                data = datas.data;

            if( !$model.length ) return false;

            if( data.length ){
                html += '<table cellpadding="0" cellspacing="0" class="ajax-tip-list" width="100%">';
                for( var i = 0 , l = data.length ; i < l ; i++ ){
                    var item = data[ i ];
                    html += '<tr>' +
                                '<td>' + item[ 'record_time' ] + '</td><td>' + item[ 'resume_name' ] + '</td><td>' + item[ 'desc' ] + '</td>' +
                                '<td><span style="color:#' + ( item['coin'] >= 0 ? '45b5e9' : 'f46c62' ) + ';font-family:arial;">' + item['coin'] + '</span>金币</td>' +
                            '</tr>';
                };
                html += '</table>';
            }else{
                html += '<p class="text-center">暂无数据！</p>';
            };

            html += '<p class="tip-pages clearfix">';
            if( datas.current > 1 ){
                html += '<a class="JS_tip_page" href="javascript:;" data-url="' + this.setting.url + '" data-page="' + ( datas.current - 1 )  + '">上一页</a>';
            };
            if( datas.current < datas.pages ){
                html += '<a class="JS_tip_page" href="javascript:;" data-url="' + this.setting.url + '" data-page="' + ( datas.current + 1 )  + '">下一页</a>';
            }
            html += '</p>';

            $model.html( html );
            this.setPosition( that.setting.eventTarget );

            $('.JS_tip_page').on( 'click' , function(){
                that.loadData( this );
            });
        }
    });

});
