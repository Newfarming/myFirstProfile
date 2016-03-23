(function() {
    var app = angular.module('app.chat', [ 'app.config' , 'ui.router' , 'app.django' , 'app.utils' ]);
    var $inject = angular.injector(['app.django', 'app.utils']);
    var tmpl = $inject.get('tmpl');
    var api = $inject.get('api');
    var id_url = $inject.get('id_url');

    app.controller(
        'chatDetail',
        [ '$scope' , '$http' , '$compile' , '$rootScope' , function( $scope , $http , $compile , $rootScope ){

            $scope.page = $scope.page || 1;
            $rootScope.nextPage = true;

            $scope.back = function(){
                history.back(1);
            };

            $scope.loadMore = function(){

                if( $scope.page >= $scope.pages ) return false;
                $rootScope.loading = true;
                $rootScope.nextPage = false;
                $scope.page++;

                var moreItem = $compile( '<msg-info page="page"></msg-info>' )( $scope );
                angular.element('.p50').prepend( moreItem );
            };

            $scope.sendMsg = function( id ){
                var url = id_url( api.chat.send_msg , id ),
                    msg = $scope.msg;
                $http.post(
                    url,
                    $.param({
                        msg: msg
                    })
                ).success(function( data ){
                    $scope.msg = '';
                    var html = '<aside class="clearfix ng-scope self">' +
                                    '<div class="avatar ng-binding">我</div>' +
                                    '<div class="chat-info">' +
                                        '<p class="ng-binding">' + msg + '</p>' +
                                    '</div>' +
                                    '<div class="text-center time ng-binding">' +
                                        data.data.send_time +
                                    '</div>' +
                                '</aside>';
                    angular.element('.p50').append( html );
                    $(document).scrollTop($(document).height() - $(window).height());
                });
            };

        }]
    );

    app.controller(
        'msgController',
        [ '$scope' , '$http' , '$rootScope' , function( $scope , $http , $rootScope ){

            $http.get(
                id_url( api.chat.msg_list , chat_id ),
                {
                    params: {
                        page: $scope.page
                    }
                }
            ).success(function( data ){
                $scope.data = data;
                $scope.data.data.reverse();
                $scope.pages = data.pages;
                $scope.userid = data.user_id;
                $rootScope.nextPage = data.current < data.pages ? true : false;
                $rootScope.loading = false;
            }).error(function(){
                $rootScope.loading = false;
            });

            $scope.sender = function( uid , rid ){
                if( !window.C_chatDetail ){
                    return uid == rid ? '我' : '求职者';
                }else{
                    return uid == rid ? '我' : '企业';
                };
            };

        }]
    );

    app.directive( 'msgInfo' , function(){
        return {
            restrict: 'E',
            templateUrl: tmpl( 'chat/chat_detail.html' ),
            controller: 'msgController',
            scope:{
                page: '=page'
            }
        };
    });

    app.filter( 'farmatDate' , function(){
        return function( time ){
            var index = time.indexOf('+');
            return time.substring(0,index);
        };
    });

})();
