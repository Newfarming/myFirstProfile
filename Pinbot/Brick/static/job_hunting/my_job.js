(function() {
    var app = angular.module('my_job', ['app.config', 'ui.router', 'app.django', 'app.utils' , 'app.filter' ]);
    var $injector = angular.injector(['app.django', 'app.utils']);
    var tmpl = $injector.get('tmpl');
    var api = $injector.get('api');
    var id_url = $injector.get('id_url');
    var tpls = {
        my_job_send_list: 'send_list',
        my_job_favorite_list: 'favorite_list',
        my_job_card_list: 'card_list'
    };

    app.config([
        '$stateProvider',
        '$urlRouterProvider',
        function( $stateProvider , $urlRouterProvider ){

            $urlRouterProvider.otherwise('/favorite/');

            $stateProvider.state(
                'send',
                {
                    url: '/send/',
                    templateUrl: tmpl('job_hunting/send_list.html'),
                    controller: 'sendList'
                }
            );

            $stateProvider.state(
                'favorite',
                {
                    url: '/favorite/',
                    templateUrl: tmpl('job_hunting/favorite_list.html'),
                    controller: 'favoriteList'
                }
            );

            $stateProvider.state(
                'card_job_list',
                {
                    url: '/card_job_list/',
                    templateUrl: tmpl('job_hunting/card_list.html'),
                    controller: 'cardList'
                }
            );

        }
    ]);

    app.controller(
        'jobController',
        [ '$scope' , '$http' , '$rootScope' , '$compile' , 'id_url' , '$filter' , function( $scope , $http , $rootScope , $compile , id_url , $filter ){

            $rootScope.page = $rootScope.page || 1;

            $scope.cookieStatus = function( type ){

                var types = {
                    send: '确认投递吗？',
                    favorite: '确定收藏后，可以去我的职位里查看哦！',
                    dislike: '不喜欢该职位？聘宝将根据你的反馈推荐更匹配的职位哦！'
                };

                if( type && !$.cookie( type ) ){
                    $.cookie( type , "true" , {expires: 30, path: '/', domain: document.domain});
                    if( type != 'favorite' ){
                        if( !window.confirm( types[ type ] ) ) return false;
                    }else{
                        alert( types[ type ] );
                    };
                };
                return true;
            };

            $scope.lock = function(){
                window.lockSubmit = true;
            };

            $scope.unlock = function(){
                window.lockSubmit = false;
            };

            $scope.loadMorePage = function(){

                if( $rootScope.loading ) return false;
                if( $rootScope.page >= $rootScope.pages ) return false;

                $rootScope.loading = true;

                //隐藏更多按钮
                $rootScope.hasMore = false;

                $rootScope.page++;

                /* 通过 directive 创建一个空的模板,等ajax请求完成，刷新模板 */
                var moreItem = $compile('<load-more page="page"></load-more>')($scope);
                angular.element('[ui-view]').append( moreItem );

            };

            $scope.toDetail = function( id ){
                location.href = id_url(api.job.job_detail, id);
            };

            $scope.toCardDetail = function( id ){
                location.href = id_url(api.job.job_card_detail, id);
            };

            $scope.createChat = function( id , e ){
                location.href = id_url(api.chat.start_job_chat, id);
                e.stopPropagation();
            };

            $scope.createCardChat = function( id , e ){
                location.href = id_url(api.chat.start_card_job_chat, id);
                e.stopPropagation();
            };

            $scope.delete = function( id , e ){

                e.stopPropagation();

                if( window.lockSubmit ) return false;
                $scope.lock();

                var api_url = id_url( api.job.my_job_delete, id );
                $http.get(
                    api_url
                ).success(function( data ){
                    if( data.status == 'ok' ){
                        angular.element('.job_panel[data-id="' + id + '"]').remove();
                    };
                    $scope.unlock();
                }).error(function(){
                    $scope.unlock();
                });

            };

            $scope.cardDelete = function( id , e ){

                e.stopPropagation();

                if( window.lockSubmit ) return false;
                $scope.lock();

                var api_url = id_url( api.job.my_job_card_delete, id );
                $http.get(
                    api_url
                ).success(function( data ){
                    if( data.status == 'ok' ){
                        angular.element('.job_panel[data-id="' + id + '"]').remove();
                    };
                    $scope.unlock();
                }).error(function(){
                    $scope.unlock();
                });

            };

            $scope.dislike = function( id , item , e ){

                e.stopPropagation();

                if( window.lockSubmit ) return false;
                $scope.lock();

                if( !$scope.cookieStatus( 'dislike' ) ){
                    $scope.unlock();
                    return false;
                };

                var api_url = id_url( api.job.my_job_dislike, id );

                $http.get(
                    api_url
                ).success(function( data ){
                    if( data.status == 'ok' ){
                        item.action = 'dislike';
                        item.statusText = '取消收藏';
                    };
                    $scope.unlock();
                }).error(function(){
                    $scope.unlock();
                });
            };

            $scope.favorite = function( id , item , e ){

                e.stopPropagation();

                if( window.lockSubmit ) return false;
                $scope.lock();

                if( !$scope.cookieStatus( 'favorite' ) ){
                    $scope.unlock();
                    return false;
                };

                var api_url = id_url( api.job.my_job_favorite, id );
                $http.get(
                    api_url
                ).success(function( data ){
                    if( data.status == 'ok' ){
                        item.action = 'favorite';
                        item.statusText = '';
                    };
                    $scope.unlock();
                }).error(function(){
                    $scope.unlock();
                });
            };

            $scope.send = function( id , item , e ){

                e.stopPropagation();

                if( window.lockSubmit ) return false;
                $scope.lock();

                e.stopPropagation();

                if( !$scope.cookieStatus( 'send' ) ){
                    $scope.unlock();
                    return false;
                };

                var api_url = id_url( api.job.send, id );
                $http.get(
                    api_url
                ).success(function( data ){
                    if( data.status == 'ok' ){
                        item.action = '';
                        item.statusText = '已投递';
                    }else{
                        var oper = data.operation;
                        if( oper == 'send' && data.redirect_url ){
                            alert('第一次投递，请完善简历！');
                            location.href = data.redirect_url;
                        };
                    };
                    $scope.unlock();
                }).error(function(){
                    $scope.unlock();
                });

            };

            $scope.accept = function( id , item , e ){

                e.stopPropagation();

                if( window.lockSubmit ) return false;
                $scope.lock();

                var api_url = id_url( api.job.my_job_card_accept, id );
                $http.get(
                    api_url
                ).success(function( data ){
                    if( data.status == 'ok' ){
                        item.status = 'accept';
                    };
                    $scope.unlock();
                }).error(function(){
                    $scope.unlock();
                });

            };

            $scope.reject = function( id , item , e ){

                e.stopPropagation();

                if( window.lockSubmit ) return false;
                $scope.lock();

                var api_url = id_url( api.job.my_job_card_reject, id );
                $http.get(
                    api_url
                ).success(function( data ){
                    if( data.status == 'ok' ){
                        item.status = 'reject';
                    };
                    $scope.unlock();
                }).error(function(){
                    $scope.unlock();
                });

            };

        }]
    );

    app.directive( 'loadMore', function(){
        return {
            restrict: 'E',
            templateUrl: tmpl('job_hunting/' + tpls[ window.activePage ] + '.html'),
            controller: 'loadMoreController',
            scope: true
        };
    });

    app.controller(
        'loadMoreController',
        [ '$scope' , '$http' , '$state' , '$rootScope' , function( $scope , $http , $state , $rootScope ){
            $http.get(
                api.job[ $rootScope.activePage ],
                {
                    params: {
                        page: $scope.page
                    }
                }
            ).success( function( data ){
                $scope.data = data;
                $rootScope.pages = data.pages;
                $rootScope.loading = false;

                //判断更多按钮显示
                $rootScope.hasMore = data.current < data.pages ? true : false;

            }).error(function(){
                $rootScope.loading = false;
            });
        }]
    );

    app.controller(
        'sendList',
        ['$scope', '$http' , '$rootScope' , function( $scope, $http , $rootScope ) {
            $rootScope.hasMore = false;
            $rootScope.activePage = window.activePage = 'my_job_send_list';
            $scope.page = $rootScope.page = 1;
            $http.get(api.job.my_job_send_list).success(function(data) {
                if( data.data && data.data.length ){
                    $scope.data = data;
                    $scope.pages = $rootScope.pages = data.pages;
                    $rootScope.hasMore = data.current < data.pages ? true : false;
                    $rootScope.noRecord = false;
                }else{
                    $rootScope.noRecord = true;
                };
            });

        }]
    );

    app.controller(
        'favoriteList',
        ['$scope', '$http' , '$rootScope' , function( $scope, $http , $rootScope ) {
            $rootScope.hasMore = false;
            $rootScope.activePage = window.activePage = 'my_job_favorite_list';
            $scope.page = $rootScope.page = 1;
            $http.get(api.job.my_job_favorite_list).success(function(data) {
                if( data.data && data.data.length ){
                    $scope.data = data;
                    $scope.pages = $rootScope.pages = data.pages;
                    $rootScope.hasMore = data.current < data.pages ? true : false;
                    $rootScope.noRecord = false;
                }else{
                    $rootScope.noRecord = true;
                };
            });

        }]
    );

    app.controller(
        'cardList',
        ['$scope', '$http' , '$rootScope' , function( $scope, $http , $rootScope ) {
            $rootScope.hasMore = false;
            $rootScope.activePage = window.activePage = 'my_job_card_list';
            $scope.page = $rootScope.page = 1;
            $http.get(api.job.my_job_card_list).success(function(data) {
                if( data.data && data.data.length ){
                    $scope.data = data;
                    $scope.pages = $rootScope.pages = data.pages;
                    $rootScope.hasMore = data.current < data.pages ? true : false;
                    $rootScope.noRecord = false;
                }else{
                    $rootScope.noRecord = true;
                };
            });

        }]
    );

})();
