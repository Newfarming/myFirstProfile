(function() {
    var app = angular.module('account', ['app.config']);

    app.controller(
        'checkUserIn',
        ['$scope', '$http', function($scope, $http) {

            $scope.user = {};
            $scope.submit = function() {
                $http.post('/account/check_user_in/', {
                    'username': $scope.user.username,
                    'password': $scope.user.password,
                    'csrfmiddlewaretoken': $scope.csrf_token
                }).success(function(data) {
                    alert(data.msg);
                });
            };
    }]);
})();
