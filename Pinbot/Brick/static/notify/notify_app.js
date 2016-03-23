(function() {
    var app = angular.module('app.notify', ['app.config', 'app.django', 'ui.router', 'app.utils']);

    var $inject = angular.injector(['app.django', 'app.utils']);
    var tmpl = $inject.get('tmpl');
    var api = $inject.get('api');
    var id_url = $inject.get('id_url');

    var autoMarkRead = function(data, $http) {
        var mark_id = [];
        angular.forEach(data, function(value, key) {
            if(value.unread) {
                mark_id.push(value.id);
            }
        });

        if(mark_id != []) {
            $http.get(
                api.notify.mark_all_read,
                {
                    params: {
                        'bat_id': mark_id
                    }
                }
            ).success(function(data) {
            });
        }
    };

    app.config([
        '$stateProvider', '$urlRouterProvider',
        function($stateProvider, $urlRouterProvider) {
            $urlRouterProvider.otherwise('/all/');

            $stateProvider.state(
                'unread',
                {
                    url: '/unread/',
                    templateUrl: tmpl('notify/notify_list.html'),
                    controller: 'notifyList',
                    onExit: function(){
                        angular.element(window).unbind('scroll');
                    }
                }
            );
            $stateProvider.state(
                'all',
                {
                    url: '/all/',
                    templateUrl: tmpl('notify/notify_list.html'),
                    onExit: function(){
                        angular.element(window).unbind('scroll');
                    },
                    controller: 'notifyList'
                }
            );
            $stateProvider.state(
                'read',
                {
                    url: '/read/',
                    templateUrl: tmpl('notify/notify_list.html'),
                    controller: 'notifyList'
                }
            );
            $stateProvider.state(
                'upload_resume',
                {
                    url: '/upload_resume/',
                    templateUrl: tmpl('notify/notify_list.html'),
                    controller: 'notifyList'
                }
            );
            $stateProvider.state(
                'follow_resume',
                {
                    url: '/follow_resume/',
                    templateUrl: tmpl('notify/notify_list.html'),
                    controller: 'notifyList'
                }
            );
            $stateProvider.state(
                'reco_resume_task',
                {
                    url: '/reco_resume_task/',
                    templateUrl: tmpl('notify/notify_list.html'),
                    controller: 'notifyList'
                }
            );

         }
    ]);

    app.controller(
        'notify',
        ['$scope', '$http', function($scope, $http) {

            $scope.markAllRead = function() {
                $http.get(api.notify.mark_all_read).success(function(data) {
                    location.reload();
                });
            };
        }]
    );

    app.controller(
        'notifyList',
        ['$scope', '$http', '$state' , '$compile', '$rootScope' , function( $scope, $http, $state , $compile , $rootScope ) {

            $scope.notify_type = $state.current.name;
            $rootScope.activePage = $state.current.name;
            $scope.page = $scope.page || 1;
            $rootScope.loading = false;

            $http.get(
                api.notify.notify_list,
                {
                    params: {
                        page: $scope.page,
                        notify_type: $scope.notify_type,
                    }
                }
            ).success(function(data) {
                if( data.data && data.data.length ){
                    $scope.data = data;
                    $scope.pages = data.pages;
                    autoMarkRead(data.data, $http);
                    $rootScope.noRecord = false;
                }else{
                    $rootScope.noRecord = true;
                };
            });

            $scope.markNotifyRead = function(notify_id) {
                var url = id_url(api.notify.mark_notify_read, notify_id);
                $http.get(url).success(function(data) {
                    alert(data.msg);
                });
            };

            $scope.view = function( e ){
                target = e.target;
                if( target.tagName.toLowerCase() == 'a' ) return true;
                var url = angular.element( target ).parent().find('a').attr('href');
                location.href = url;
            };

            $scope.loadMoreFun = function(){
                if( $( document ).height() - $( window ).height() - $( document ).scrollTop() > 100 ) return false;
                if( $rootScope.loading ) return false;
                if( $scope.page >= $scope.pages ) return false;
                $rootScope.loading = true;
                $scope.page++;

                /* 通过 directive 创建一个空的模板,等ajax请求完成，刷新模板 */
                var moreItem = $compile('<load-more page="page" notifytype="notify_type"></load-more>')($scope);
                angular.element('[ui-view]').append( moreItem );
            };

            angular.element( window ).on( 'scroll' , $scope.loadMoreFun );

        }]
    );

    app.controller(
        'loadNotify',
        [ '$scope' , '$element' , '$http' , '$compile' , '$rootScope' , function( $scope , $element , $http , $compile , $rootScope ){

            $http.get(
                api.notify.notify_list,
                {
                    params: {
                        page: $scope.page,
                        notify_type: $scope.notify_type,
                    }
                }
            ).success(function(data) {
                $scope.data = data;
                $rootScope.loading = false;
                autoMarkRead(data.data, $http);
            }).error( function(){
                $rootScope.loading = false;
            });

        }]
    );

    app.directive( 'loadMore' , function(){
        return {
            restrict: 'E',
            templateUrl: tmpl('notify/notify_list.html'),
            controller: 'loadNotify',
            scope: {
                notify_type: '=notifytype',
                page: '=page'
            }
        }
    });

    app.filter('to_trusted', ['$sce', function($sce){
        return function(text) {
            return $sce.trustAsHtml(text);
        };
    }]);

    app.filter( 'farmatDate' , function(){
        return function( time ){
            var index = time.indexOf('+');
            return time.substring(0,index);
        };
    });

})();
