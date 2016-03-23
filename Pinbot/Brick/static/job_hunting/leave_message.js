(function() {
    var app = angular.module('job', ['app.config', 'ui.router', 'app.django', 'app.utils' , 'validation', 'validation.rule' ]);
    var $injector = angular.injector(['app.django', 'app.utils']);
    var tmpl = $injector.get('tmpl');
    var api = $injector.get('api');
    var id_url = $injector.get('id_url');
    var errorFunction = function( errors , formName ){
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

    app.controller(
        'message',
        ['$scope', '$http', '$element' , function( $scope, $http , $element ) {
            $scope.sendSuccess = false;
            $scope.change = function(){
                $scope.sendSuccess = false;
            };
            $scope.sendMsg = function(){
                $http.post(
                    api.job.job_leave_message,
                    {
                        message: $scope.message
                    }
                ).success(function( data ){
                    if( data.status == 'ok' ){
                        $scope.sendSuccess = true;
                        $scope.message = '';
                    }else{
                        if( data.errors ){
                            var form = $element.find('form')[0];
                            errorFunction( data.errors , form );
                        };
                    };
                });
            };
        }]
    );

})();
