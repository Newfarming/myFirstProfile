(function() {
    var app = angular.module('job_detail', ['app.config', 'ui.router', 'app.django', 'app.utils' , 'app.filter' ]);
    var $injector = angular.injector(['app.django', 'app.utils']);
    var tmpl = $injector.get('tmpl');
    var api = $injector.get('api');
    var id_url = $injector.get('id_url');

    app.controller(
        'jobDetailCtrl',
        [ '$scope' , '$http' , function( $scope , $http ){

            $scope.showDetail = false;
            $scope.nonzero = false;

            $scope.getParam = function(){
                var $dom = angular.element('#JS_praise_btn'),
                    count = parseInt( $dom.attr( 'data-count' ) ),
                    company_id = $dom.attr( 'data-company_id' ),
                    favour = $dom.attr( 'data-favour' );

                $scope.count = count;
                $scope.company_id = company_id;
                $scope.favour = favour && favour.toLowerCase() != 'false';
            };
            
            $scope.getParam();

            $scope.toggleDetail = function(){
                $scope.showDetail = !$scope.showDetail;
            };

            $scope.praiseCompany = function( e ){

                if( $scope.lockPraise ) return;
                $scope.lockPraise = true;

                var favour = $scope.favour,
                    id = $scope.company_id,
                    url = id_url(api.job.job_favour_company, id);

                $http.get( url ).success( function( data ){
                    if( data && data.status == 'ok' ){
                        if( data.data.action == 'favour' ){
                            $scope.favour = true;
                            $scope.count++;
                            angular.element('#JS_praised').addClass('active');
                        }else{
                            $scope.favour = false;
                            $scope.count--;
                            angular.element('#JS_praised').removeClass('active');
                        };
                    }
                    $scope.lockPraise = false;
                }).error(function(){
                    $scope.lockPraise = false;
                });
            };

        }]
    )

})();
