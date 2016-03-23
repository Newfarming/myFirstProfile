(function() {
    var app = angular.module('app.resume', ['app.config', 'ui.router', 'app.django', 'app.utils' , 'validation', 'validation.rule' ]);

    var $django = angular.injector(['app.django']);
    var tmpl = $django.get('tmpl');
    var api = $django.get('api');
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

    Date.prototype.pattern=function(fmt) {
        var o = {
            "M+" : this.getMonth()+1, //月份
            "d+" : this.getDate(), //日
            "h+" : this.getHours()%12 == 0 ? 12 : this.getHours()%12, //小时
            "H+" : this.getHours(), //小时
            "m+" : this.getMinutes(), //分
            "s+" : this.getSeconds(), //秒
            "q+" : Math.floor((this.getMonth()+3)/3), //季度
            "S" : this.getMilliseconds() //毫秒
            };
            var week = {
            "0" : "/u65e5",
            "1" : "/u4e00",
            "2" : "/u4e8c",
            "3" : "/u4e09",
            "4" : "/u56db",
            "5" : "/u4e94",
            "6" : "/u516d"
        };
        if(/(y+)/.test(fmt)){
            fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
        }
        if(/(E+)/.test(fmt)){
            fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "/u661f/u671f" : "/u5468") : "")+week[this.getDay()+""]);
        }
        for(var k in o){
            if(new RegExp("("+ k +")").test(fmt)){
                fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
            }
        }
        return fmt;
    };

    app.config([
        '$stateProvider', '$urlRouterProvider',
        function($stateProvider, $urlRouterProvider) {
            $stateProvider.state(
                'select_gender',
                {
                    url: '/select_gender/',
                    templateUrl: tmpl('my_resume/select_gender.html'),
                    controller: 'selectGender'
                }
            );
            $stateProvider.state(
                'select_city',
                {
                    url: '/select_city/',
                    templateUrl: tmpl('my_resume/select_city.html'),
                    controller: 'selectCity'
                }
            );
            $stateProvider.state(
                'select_position_category',
                {
                    url: '/select_position_category/',
                    templateUrl: tmpl('my_resume/select_position_category.html'),
                    controller: "selectPositionCategory"
                }
            );
            $stateProvider.state(
                'select_category_tag',
                {
                    url: '/select_category_tag/',
                    templateUrl: tmpl('my_resume/select_category_tag.html'),
                    controller: "selectCategoryTag"
                }
            );
            $stateProvider.state(
                'select_work_years',
                {
                    url: '/select_work_years/',
                    templateUrl: tmpl('my_resume/select_workyears.html'),
                    controller: "selectWorkyears"
                }
            );
            $stateProvider.state(
                'select_degree',
                {
                    url: '/select_degree/',
                    templateUrl: tmpl('my_resume/select_degree.html'),
                    controller: "selectDegree"
                }
            );
        }
    ]);

    app.controller(
        'selectGender',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.gender = '';
            $scope.setGender = function(gender) {
                $scope.gender = gender;
            };

            $scope.next = function() {
                $http.post(
                    api.resume.select_gender,
                    $.param({gender: $scope.gender})
                ).success(function(data) {
                    alert(data.msg);
                    $state.go('select_city');
                });
            };

            $http.get(api.resume.select_gender).success(function(data) {
                $scope.gender = data.data.gender;
            });
        }]
    );

    app.controller(
        'selectCity',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.select_city = [];

            $scope.previous = function() {
            }

            $scope.checkCity = function(city) {
                var city_index = $scope.select_city.indexOf(city);
                if(city_index >= 0) {
                    $scope.select_city.pop(city_index);
                }
                else {
                    $scope.select_city.push(city);
                }
            };

            $scope.next = function() {
                $http.post(
                    api.resume.select_city,
                    $.param({city: $scope.select_city})
                ).success(function(data) {
                    alert(data.msg);
                    $state.go('select_position_category')
                });
            };

            $http.get(api.resume.select_city).success(function(data) {
                $scope.data = data.data;
            });
        }]
    )

    app.controller(
        'selectPositionCategory',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.category = '';
            $scope.previous = function() {
                $state.go('select_city');
            };

            $scope.setPosition = function(category) {
                $scope.category = category;
            };

            $scope.next = function() {
                $http.post(
                    api.resume.select_position_category,
                    $.param({'category': $scope.category})
                ).success(function(data) {
                    alert(data.msg);
                    $state.go('select_category_tag');
                });
            };

            $http.get(api.resume.select_position_category).success(function(data) {
                $scope.data = data.data;
            });
        }]
    );

    app.controller(
        'selectCategoryTag',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.tag = [];
            $scope.previous = function() {
                $state.go('select_position_category');
            };

            $scope.checkTag = function(tag) {
                var tag_index = $scope.tag.indexOf(tag);
                if(tag_index >= 0) {
                    $scope.tag.pop(tag_index);
                }
                else {
                    $scope.tag.push(tag);
                }
            };

            $scope.next = function() {
                $http.post(
                    api.resume.select_category_tag,
                    $.param({'tag': $scope.tag})
                ).success(function(data) {
                    alert(data.msg);
                    $state.go('select_work_years');
                });
            };

            $http.get(api.resume.select_category_tag).success(function(data) {
                $scope.data = data.data;
            });
        }]
    );

    app.controller(
        'selectWorkyears',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.work_years = '';

            $scope.previous = function() {
                $state.go('select_category_tag');
            };

            $scope.setWorkyears = function(work_years) {
                $scope.work_years = work_years;
            };

            $scope.next = function() {
                $http.post(
                    api.resume.select_workyears,
                    $.param({work_years: $scope.work_years})
                ).success(function(data) {
                    alert(data.msg);
                    $state.go('select_degree');
                });
            };

            $http.get(api.resume.select_workyears).success(function(data) {
                $scope.work_years = data.data.work_years;
            });
        }]
    );

    app.controller(
        'selectDegree',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.degree = '';

            $scope.previous = function() {
                $state.go('select_work_years');
            };

            $scope.setDegree = function(degree) {
                $scope.degree = degree;
            };

            $scope.next = function() {
                $http.post(
                    api.resume.select_degree,
                    $.param({degree: $scope.degree})
                ).success(function(data) {
                    alert(data.msg);
                });
            };

            $http.get(api.resume.select_degree).success(function(data) {
                $scope.data = data.data;
            });
        }]
    );

    app.controller(
        'editProfile',
        [ '$scope' , '$http' , '$element' , 'id_url' , function( $scope , $http , $element , id_url ){

            $scope.saved = angular.copy( $scope.resume );

            $scope.update = function() {
                $scope.saved = angular.copy($scope.resume);
            };

            $scope.reset = function() {
                $scope.resume = angular.copy($scope.saved);
            };

            $scope.isShowEditProfile = $scope.isShowCancelBtn = !$scope.resume.name && !$scope.resume.age ? true : false;

            $scope.toggleEditProfile = function( bool ){
                if( !bool ){
                    $scope.reset();
                };
                $scope.isShowEditProfile = bool;
            };

            $scope.savePersonInfo = function() {
                $http.post(
                    api.resume.save_person_info,
                    $.param({
                        name: $scope.resume.name,
                        age: $scope.resume.age,
                        self_evaluation: $scope.resume.self_evaluation
                    })
                ).success(function(data) {
                    if( data && data.status == 'ok' ){
                        $scope.update();
                        $scope.isShowEditProfile = false;
                        $scope.isShowCancelBtn = false;
                    }else{
                        if( data.data && data.data.errors ){
                            var form = $element.find('form')[0];
                            errorFunction( data.data.errors , form );
                        };
                    };
                });
            };

        }]
    );

    app.controller(
        'editSns',
        [ '$scope' , '$http' , '$element', 'id_url' , function( $scope , $http , $element , id_url ){

            var defaultUrl = {
                linkedin: 'https://www.linkedin.com/',
                weibo: 'http://weibo.com/',
                github: 'https://github.com/',
                zhihu: 'http://www.zhihu.com/',
                dribbble: 'https://dribbble.com/'
            };
            $scope.isShowEditSns = true;
            $scope.isSetSns = false;
            for( var i in $scope.sns ){
                if( $scope.sns[ i ] ){
                    $scope.isShowEditSns = false;
                    $scope.isSetSns = true;
                };
            };
            $scope.page_type = 'linkedin';
            $scope.current_url = $scope.sns[ $scope.page_type ] || defaultUrl[ $scope.page_type ];

            $scope.saved = angular.copy( $scope.sns );

            $scope.update = function() {
                $scope.saved = angular.copy($scope.sns);
            };

            $scope.reset = function() {
                $scope.sns = angular.copy($scope.saved);
            };

            $scope.setPageType = function(page_type) {
                $scope.page_type = page_type;
                $scope.current_url = $scope.sns[ page_type ] || defaultUrl[ page_type ];
                $scope.isShowEditSns = true;
            };

            $scope.toggleEditSns = function( bool ){
                if( !$scope.isSetSns ) return false;
                if( !bool ){
                    $scope.reset();
                    $scope.current_url = $scope.sns[ $scope.page_type ];
                }else{
                    $scope.current_url = $scope.sns[ $scope.page_type ] || defaultUrl[ $scope.page_type ];
                };
                $scope.isShowEditSns = bool;
            }

            $scope.hasSocial = function( i ){
                return i ? 'active' : '';
            };

            $scope.getUrl = function(){
                return $scope.sns[ $scope.page_type ] ? $scope.sns[ $scope.page_type ] : '';
            };

            $scope.saveSocialPage = function() {
                
                if( defaultUrl[ $scope.page_type ] == $scope.current_url ){
                    $element.find('[name="url"]').focus();
                    return false;
                };
                var api_url = id_url(api.resume.save_social_page, $scope.page_type);
                $http.post(
                    api_url,
                    $.param({
                        url: $scope.current_url
                    })
                ).success(function(data) {
                    if( data && data.status == 'ok' ){
                        $scope.sns[ $scope.page_type ] = $scope.current_url;
                        $scope.update();
                        $scope.isShowEditSns = false;
                        $scope.isSetSns = true;
                    }else{
                        if( data.data && data.data.errors ){
                            var form = $element.find('form')[0];
                            errorFunction( data.data.errors , form );
                        };
                    };
                });
            };

        }]
    );

    app.controller(
        'editContact' ,
        [ '$scope' , '$http' , '$element' , 'id_url' , function( $scope , $http, $element , id_url ){

            $scope.isShowEditContact = $scope.isHideCancelBtn = !$scope.contact.email && !$scope.contact.phone ? true : false;

            $scope.saved = angular.copy( $scope.contact );

            $scope.update = function() {
                $scope.saved = angular.copy($scope.contact);
            };

            $scope.reset = function() {
                $scope.contact = angular.copy($scope.saved);
            };

            $scope.toggleEditContact = function( bool ){
                if( !bool ){
                    $scope.reset();
                };
                $scope.isShowEditContact = bool;
            };

            $scope.saveContactInfo = function() {
                if( window.lockContactSubmit ) return false;
                window.lockContactSubmit = true;

                $http.post(
                    api.resume.save_contact_info,
                    $.param({
                        phone: $scope.contact.phone,
                        email: $scope.contact.email
                    })
                ).success(function(data) {
                    if( data && data.status == 'ok' ){
                        $scope.update();
                        $scope.isShowEditContact = false;
                        $scope.isHideCancelBtn = false;
                    }else{
                        if( data.data && data.data.errors ){
                            var form = $element.find('form')[0];
                            errorFunction( data.data.errors , form );
                        };
                    };
                    window.lockContactSubmit = false;
                }).error( function(){
                    window.lockContactSubmit = false;
                });
            };

        }]
    );

    app.controller(
        'editRelation',
        [ '$scope' , '$http' ,'$element' , 'id_url' , function( $scope , $http , $element , id_url ){

            $scope.isShowEditRelation = false;

            $scope.saved = angular.copy( $scope.relation );

            $scope.update = function() {
                $scope.saved = angular.copy($scope.relation);
            };

            $scope.reset = function() {
                $scope.relation = angular.copy($scope.saved);
            };

            $scope.showRelation = function( site ){
                $scope.isShowEditRelation = true;
                $scope.relationSite = site;
            };

            $scope.isActive = function( i ){
                return i ? 'active' : '';
            }

            $scope.toggleEditRelation = function( bool ){
                if( !bool ){
                    $scope.reset();
                };
                $scope.isShowEditRelation = bool;
            };

            $scope.saveRelationInfo = function(){
                var api_url = id_url( api.resume.save_relation_site , $scope.relationSite );
                $http.post(
                    api_url,
                    $.param({
                        username: $scope.relation.username,
                        password: $scope.relation.password
                    })
                ).success( function( data ){
                    if( data && data.status == 'ok' ){
                        $scope.update();
                        $scope.isShowEditRelation = false;
                    }else{
                        if( data.data && data.data.errors ){
                            var form = $element.find('form')[0];
                            errorFunction( data.data.errors , form );
                        };
                    };
                });
            };

        }]
    )

    app.controller(
        'editResume',
        ['$scope', '$http', 'id_url', function($scope, $http, id_url) {

            $scope.openProjects = $scope.openSkills = false;

            $scope.initResume = function() {
                $scope.resume = window.jsonResume;
                if( !$scope.resume.age ){
                    $scope.resume.age = '';
                };
            };

            $scope.isOpenProjects = function( bool ){
                $scope.openProjects = bool;
            };

            $scope.isOpenSkills = function( bool ){
                $scope.openSkills = bool;
            };

            $scope.saveSelfEvaInfo = function() {
                $http.post(
                    api.resume.save_self_eva_info,
                    $.param({
                        self_evaluation: $scope.resume.self_evaluation,
                    })
                ).success(function(data) {
                    alert(data.msg);
                });
            };
        }]
    );

    app.directive('profileInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('my_resume/profile.html'),
            controller: 'editProfile',
            link: function(scope, elem, attrs) {},
            scope: {
                resume: "=resume"
            }
        }
    });

    app.directive( 'snsInfo' , function(){
        return {
            restrict: 'E',
            templateUrl: tmpl( 'my_resume/sns_info.html' ),
            controller: 'editSns',
            scope: {
                sns: '=sns'
            }
        }
    });

    app.directive( 'contactInfo' , function(){
        return {
            restrict: 'E',
            templateUrl: tmpl( 'my_resume/contact_info.html' ),
            controller: 'editContact',
            scope: {
                contact: '=contact'
            }
        }
    });

    app.directive( 'relationResume' , function(){
        return {
            restrict: 'E',
            templateUrl: tmpl( 'my_resume/relation_resume.html' ),
            controller: 'editRelation',
            scope: {
                relation: '=relation'
            }
        }
    });

    app.directive('projectInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('my_resume/project.html'),
            controller: 'additionController',
            link: function(scope, elem, attrs) {
                scope.api_url = api.resume.save_project;
                scope.directive_tag = '<project-info project="{}" projects="list"></project-info>';
                scope.delete_url = api.resume.delete_project;
                scope.isShowEditItem = scope.project && !$.isEmptyObject( scope.project ) ? false : true;
                scope.listType = 'project';
                angular.forEach( scope.list , function( project , index , arr ){
                    project.start_time = project.start_time ? new Date( project.start_time ) : '';
                    project.end_time = project.end_time ? new Date( project.end_time ) : '';
                });
                scope.saved = angular.copy( scope.list );
            },
            scope: {
                list: '=projects',
                project: "=project"
            }
        }
    });

    app.directive('educationInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('my_resume/education.html'),
            controller: 'additionController',
            link: function(scope, elem, attrs) {
                scope.api_url = api.resume.save_education;
                scope.directive_tag = '<education-info edu="{}" edus="list"></education-info>';
                scope.delete_url = api.resume.delete_education;
                scope.isShowEditItem = scope.edu && !$.isEmptyObject( scope.edu ) ? false : true;
                scope.listType = 'edu';
                angular.forEach( scope.list , function( education , index , arr ){
                    education.start_time = education.start_time ? new Date( education.start_time ) : '';
                    education.end_time = education.end_time ? new Date( education.end_time ) : '';
                });
                scope.saved = angular.copy( scope.list );
            },
            scope: {
                list: '=edus',
                edu: "=edu"
            }
        }
    });

    app.directive('workInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('my_resume/work.html'),
            controller: 'additionController',
            link: function(scope, elem, attrs) {
                scope.api_url = api.resume.save_work_expreimence;
                scope.directive_tag = '<work-info work="{}" works="list"></work-info>';
                scope.delete_url = api.resume.delete_work_experience;
                scope.isShowEditItem = scope.work && !$.isEmptyObject( scope.work ) ? false : true;
                scope.listType = 'work';
                angular.forEach( scope.list , function( work , index , arr ){
                    work.start_time = work.start_time ? new Date( work.start_time ) : '';
                    work.end_time = work.end_time ? new Date( work.end_time ) : '';
                });
                scope.saved = angular.copy( scope.list );
            },
            scope: {
                list: '=works',
                work: '=work'
            }
        }
    });

    app.directive('skillInfo', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('my_resume/professional_skill.html'),
            link: function(scope, elem, attrs) {
                scope.api_url = api.resume.save_professional_skill;
                scope.directive_tag = '<skill-info skill="{}" skills="list"></skill-info>';
                scope.delete_url = api.resume.delete_professional_skill;
                scope.isShowEditItem = scope.skill && !$.isEmptyObject( scope.skill ) ? false : true;
                scope.listType = 'skill';
                scope.saved = angular.copy( scope.list );
            },
            controller: 'additionController',
            scope: {
                list: '=skills',
                skill: "=skill"
            }
        }
    });

    app.controller(
        'additionController',
        ['$scope', '$http', '$element', '$compile', 'id_url', function($scope, $http, $element, $compile, id_url) {

            $scope.save_work_experience_url = api.resume.save_work_experience;
            $scope.save_education_url = api.resume.save_education;
            $scope.save_project_url = api.resume.save_project;
            $scope.save_professional_skill_url = api.resume.save_professional_skill;

            $scope.update = function() {
                $scope.saved = angular.copy( $scope.list );
            };

            $scope.reset = function() {
                $scope.list = angular.copy($scope.saved);
            };

            $scope.save = function(api_url, param) {
                var isAdd = $scope[$scope.listType].id ? false : true;
                $http.post(
                    api_url,
                    $.param(param)
                ).success(function(data) {
                    if( data && data.status == 'ok' ){
                        $scope.update();
                        $scope.update_id = data.data.update_id;
                        $scope.isShowEditItem = false;
                        if( isAdd ){
                            $scope[$scope.listType].id = data.data.update_id;
                            var a = $.extend( $scope[$scope.listType] , {});
                            $element.remove();
                            $scope.list.push( a );
                        };
                        // console.log( $scope )
                    }else{
                        if( data.data && data.data.errors ){
                            var form = $element.find('form')[0];
                            errorFunction( data.data.errors , form );
                        };
                    };
                });
            };

            $scope.toggleEditItem = function( bool , isDelete ){
                var type = $scope.listType;
                // console.log( $scope )
                if( $scope.list && $scope.list.length ){
                    $scope.isShowEditItem = bool;
                };
                if( $scope[type].id && !bool ){
                    $scope.reset();
                };
                if( !$scope[type].id && isDelete && $scope.list && $scope.list.length ){
                    $element.remove();
                };
            };

            $scope.isShowDelete = function(){
                return $scope.list && $scope.list.length > 1 ? true : false;
            };

            $scope.delete = function(obj_id) {
                var delFun = function(){
                    $element.remove();
                };
                if( $scope.list.length <= 1 || $.isEmptyObject( $scope.list ) ) return;
                if( !obj_id ){
                    delFun();
                    return;
                };
                if( window.confirm('确认删除本条记录吗？') ){
                    var api_url = id_url($scope.delete_url, obj_id);
                    $http.get( api_url ).success(function(data) {
                        if( data && data.status == 'ok' ){
                            delFun();
                            for( var i = 0 , l = $scope.list.length ; i < l ; i++ ){
                                if( $scope.list[i].id == obj_id ){
                                    $scope.list.splice( i , 1 );
                                };
                            };
                        };
                    });
                };
            };

            $scope.add = function() {
                var new_item = $compile($scope.directive_tag)($scope);
                $element.parent().append(new_item);
            };

            $scope.getDate = function( date , style ){
                if(  date && typeof date == 'object' ){
                    date = date.pattern( style );
                };
                return date;
            };

        }]
    );

    app.filter( 'formartDate' , function(){
        return function( date ){
            if( date && typeof date == 'object' ){
                return date.pattern('yyyy-MM');
            }else{
                return date;
            };
        };
    });

})();
