(function(){
    var account = angular.module( 'app.account' ,[ 'app.config' , 'validation' , 'validation.rule' ]),
        errorFunction = function( errors , formName ){
            for( var i in errors ){
                var input = $(formName).find('[name="' + i + '"]'),
                    span = input.next(),
                    tagName = span[0] && span[0].tagName ? span[0].tagName.toLowerCase() : '',
                    p = span.find('p');
                if( tagName == 'span' && p.length ){
                    p.html( errors[i] );
                }else{
                    input.after('<span><p class="validation-invalid">' + errors[i] + '</p></span>');
                };
                span.show();
            };
        };
    account.controller(
        'editAccount',
        [ '$scope' , '$element', '$http' , function( $scope , $element , $http ){

            $scope.isChangePassword  = $scope.isOpenContact = $scope.isOpenRecommend = false;

            $scope.csrfmiddlewaretoken = angular.element('[name="csrfmiddlewaretoken"]').val();

            $scope.toggleChangePassword = function( bool ){
                $scope.isChangePassword = bool;
            };

            $scope.toggleOpenContact = function( bool ){
                $scope.isOpenContact = bool;
            };

            $scope.toggleOpenRecommend = function( bool ){
                $scope.isOpenRecommend = bool;
            };

            $scope.togglePasswordType = function( $event ){
                var ele = angular.element( $event.target ),
                    input = ele.next(),
                    type = input.attr('type');
                type = type == 'text' ? 'password' : 'text';
                ele.toggleClass( 'active' );
                input.attr( 'type' , type );
            };

            $scope.changePassword = function(){
                var form = $element.find('form')[0];
                if( $scope.password != $scope.confirm_password ){
                    errorFunction( { 'confirm_password' : '确认密码与新密码不一致！' } , form );
                    return false;
                };
                $http.post(
                    '.',
                    $.param({
                        old_password: $scope.old_password,
                        password: $scope.password,
                        confirm_password: $scope.confirm_password,
                        csrfmiddlewaretoken: $scope.csrfmiddlewaretoken
                    })
                ).success( function( data ){
                    if( data.status == 'ok' ){
                        $scope.isChangePassword = false;
                        $scope.old_password = $scope.password = $scope.confirm_password = '';
                    }else{
                        if( data.data && data.data.errors ){
                            errorFunction( data.data.errors , form );
                        };
                    };
                }).error( function(){
                    console.log( '请求失败了.' )
                });
            };

        }]
    );
})();
