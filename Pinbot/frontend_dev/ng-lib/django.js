(function() {
    var sp = '/static/';
    var service = angular.module('app.django', []);
    // angular tmpl method
    service.factory('tmpl', function() {
        return function(template_path) {
            var static_path = sp;
            return static_path + template_path;
        }
    });
    // angular tmp static url
    service.factory('static_url', function() {
        var static_path = sp;
        return static_path;
    });
})();