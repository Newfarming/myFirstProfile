(function(){
    var app = angular.module( 'settingApp' , [ 'app.config' ] );

    app.controller(
        'settingCtrl',
        [
            '$scope',
            '$http',
            function( $scope , $http ){

                //初始化数据
                $scope.datas = angular.fromJson( angular.element( document.getElementsByTagName( 'form' )[0] ).attr('data-datas') );
                $scope.allAreaChecked = $scope.datas.setting.job_domain.length ? false : true;

                //判断是否选中, true:选中 | false：未选中
                $scope.isActive = function( id , list ){

                    for( var i = 0 , l = list.length ; i < l ; i++ ){
                        var v = list[ i ];
                        if( v.id == id ) {
                            return true;
                        };
                    };

                    return false;
                };

                //切换选中
                $scope.toggleActive = function( item , list ){

                    if( $scope.isActive( item.id , list ) ){

                        //已经选中，取消选中
                        for( var i = 0 , l = list.length ; i < l ; i++ ){
                            var v = list[ i ];
                            if( v.id == item.id ) {
                                list.splice( i , 1 );
                                break;
                            };
                        };

                    }else{

                        //未选中，则选中
                        list.push( angular.copy( item ) );

                    };

                };

                //添加关键词
                $scope.addTile = function( item , list ){
                    list.push( angular.copy( item ) );
                };

                //移除关键词
                $scope.removeTitle = function( item , list ){

                    for( var i = 0 , l = list.length ; i < l ; i++ ){
                        var v = list[ i ];
                        if( v == item ) {
                            list.splice( i , 1 );
                            break;
                        };
                    };

                };

                //是否已经选择了关键词
                $scope.isActiveTitle = function(  item , list ){

                    for( var i = 0 , l = list.length ; i < l ; i++ ){
                        var v = list[ i ];
                        if( v == item ) {
                            return true;
                        };
                    };

                    return false;

                };

                //输入关键词按下回车
                $scope.setKeywords = function(){
                    if( !$scope.keywordText ) return false;
                    $scope.addTile( $scope.keywordText , $scope.datas.setting.title );
                    $scope.keywordText = '';
                };

                //监控关键词变化
                $scope.watchKeyword =function( $e ){
                    if( $scope.canSave( $e ) ){
                        $scope.setKeywords();
                    };
                };

                //判断是否按下空格、分号
                $scope.canSave = function( $e ){
                    var code = $e.keyCode;
                    if( code == 188 ){
                        $scope.keywordText = $scope.keywordText.substring( 0 , $scope.keywordText.length - 1 );
                        return true;
                    };
                    return false;
                };

                //设置领域不限
                $scope.resetJobDomain = function( $event ){
                    $scope.datas.setting.job_domain = [];
                };

                //保存数据
                $scope.save = function(){
                    $http.post(
                        '.' ,
                        JSON.stringify( $scope.datas.setting )
                    ).success(function( res ){
                        if( res && res.status == 'ok' && res.redirect_url ){
                            location.href = res.redirect_url;
                        };
                    });
                };

            }
        ]
    );

    app.directive('ngEnter', function() {
        return function(scope, element, attrs) {
            element.bind("keydown keypress", function(event) {
                if(event.which === 13) {
                    scope.$apply(function(){
                        scope.$eval(attrs.ngEnter);
                    });

                    event.preventDefault();
                };
            });
        };
    });

})();