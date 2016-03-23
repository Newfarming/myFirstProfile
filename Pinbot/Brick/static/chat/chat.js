(function() {
    var app = angular.module('app.chat', [ 'app.config' , 'ui.router' , 'app.django' , 'app.utils' , 'app.filter' ]);
    var $inject = angular.injector(['app.django', 'app.utils']);
    var tmpl = $inject.get('tmpl');
    var api = $inject.get('api');
    var id_url = $inject.get('id_url');

    app.config(
        [
            '$stateProvider',
            '$urlRouterProvider',
            function( $stateProvider , $urlRouterProvider ){

                $urlRouterProvider.otherwise('/history_chat/');

                $stateProvider.state(
                    'chat_book',
                    {
                        url: '/chat_book/',
                        templateUrl: tmpl('chat/chat.html'),
                        controller: 'chatList',
                        onExit: function(){
                            angular.element(window).unbind('scroll');
                        },
                        data: {
                            pageActive: 'book_list'
                        }
                    }
                );

                $stateProvider.state(
                    'history_chat',
                    {
                        url: '/history_chat/',
                        templateUrl: tmpl('chat/history_chat.html'),
                        controller: 'chatList',
                        onExit: function(){
                            angular.element(window).unbind('scroll');
                        },
                        data: {
                            pageActive: 'history_list'
                        }
                    }
                );

            }
        ]
    );

    app.controller(
        'chatList',
        [ '$scope' , '$http' , '$state' , '$rootScope' , '$compile' , '$filter' , function( $scope , $http , $state , $rootScope , $compile , $filter ){

            $rootScope.pageActive = window.pageActive = $state.current.data.pageActive;
            $scope.page = $scope.pages = 1;
            $rootScope.loading = false;

            $http.get(
                api.chat[ $state.current.data.pageActive ],
                {
                    params: {
                        page: $scope.page
                    }
                }
            ).success( function( data ){
                if( data.data && data.data.length ){
                    $scope.data = data;
                    $scope.userid = data.user_id;
                    $scope.pages = data.pages;
                    $rootScope.noRecord = false;
                }else{
                    $rootScope.noRecord = true;
                };
            }).error(function(){
                $rootScope.noRecord = true;
            });

            $scope.toDetail = function( id ){
                location.href = '/chat/chat_detail/' + id + '/';
            };

            $scope.loadMoreFun = function(){
                if( $( document ).height() - $( window ).height() - $( document ).scrollTop() > 100 ) return false;
                if( $rootScope.loading ) return false;
                if( $scope.page >= $scope.pages ) return false;
                $rootScope.loading = true;
                $scope.page++;

                /* 通过 directive 创建一个空的模板,等ajax请求完成，刷新模板 */
                var moreItem = $compile('<load-more' + ( window.pageActive == 'history_list' ? '-history' : '' ) + ' page="' + $scope.page + '" ></load-more>')($scope);
                angular.element('[ui-view]').append( moreItem );
            };

            angular.element( window ).on( 'scroll' , $scope.loadMoreFun );

        }]
    );

    app.directive( 'loadMore', function( $templateCache ){
        var tplName = window.pageActive == 'history_list' ? 'history_chat' : 'chat';
        return {
            restrict: 'E',
            templateUrl: tmpl('chat/' + tplName + '.html'),
            controller: 'loadMoreChat',
            scope: true
        };
    });

    app.directive( 'loadMoreHistory', function( $templateCache ){
        var tplName = window.pageActive == 'history_list' ? 'history_chat' : 'chat';
        return {
            restrict: 'E',
            templateUrl: tmpl('chat/' + tplName + '.html'),
            controller: 'loadMoreChat',
            scope: true
        };
    });

    app.controller(
        'loadMoreChat',
        [ '$scope' , '$http' , '$state' , '$rootScope' , '$filter' , function( $scope , $http , $state , $rootScope , $filter ){
            $http.get(
                api.chat[ $state.current.data.pageActive ],
                {
                    params: {
                        page: $scope.page
                    }
                }
            ).success( function( data ){
                $scope.data = data;
                $rootScope.loading = false;
            }).error(function(){
                $rootScope.loading = false;
            });
        }]
    );

})();
