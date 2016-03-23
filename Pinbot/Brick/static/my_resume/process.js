//扩展数组对象，添加方法，根据索引删除元素
Array.prototype.remove=function(dx)
{
    if(isNaN(dx)||dx>this.length){return false;}
    for(var i=0,n=0;i<this.length;i++)
    {
        if(this[i]!=this[dx])
        {
            this[n++]=this[i]
        }
    }
    this.length-=1
};
(function() {
    var app = angular.module('app.process', ['app.config', 'ui.router', 'app.django', 'app.utils']);

    var $django = angular.injector(['app.django']);
    var tmpl = $django.get('tmpl');
    var api = $django.get('api');
    var static_url = $django.get('static_url');

    app.config([
        '$stateProvider', '$urlRouterProvider',
        function($stateProvider, $urlRouterProvider) {
            $urlRouterProvider.otherwise('/select_gender/');
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
            $stateProvider.state(
                'select_field',
                {
                    url: '/select_field/',
                    templateUrl: tmpl('my_resume/select_field.html'),
                    controller: "selectField"
                }
            );
            $stateProvider.state(
                'select_salary',
                {
                    url: '/select_salary/',
                    templateUrl: tmpl('my_resume/select_salary.html'),
                    controller: "selectSalary"
                }
            );
        }
    ]);

    app.controller(
        'selectGender',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.gender = '';
            $scope.static_url = static_url;
            $scope.setGender = function(gender) {
                $scope.gender = gender;
                $('a').removeClass('checked');
                $('#' + $scope.gender).addClass('checked');
                $http.post(
                    api.resume.select_gender,
                    $.param({gender: $scope.gender})
                ).success(function(data) {
                    $state.go('select_city');
                }).error(function() {
                    console.log('请求失败');
                });
            };

            $http.get(api.resume.select_gender).success(function(data) {
                $scope.gender = data.data.gender;
                if($scope.gender != ''){
                    $('#' + $scope.gender).addClass('checked');
                }
                changeSelectedState($state);
            }).error(function() {
                console.log('请求失败');
            });
        }]
    );

    app.controller(
        'selectCity',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.select_city = [];
            $scope.static_url = static_url;

            $scope.back = function() {
                $state.go('select_gender');
            }
            $scope.isShow = function(length) {
                if (length != 0) {return true};
                return false;
            }
            $scope.checkCity = function(city) {
                var city_index = $scope.select_city.indexOf(city);
                if(city_index >= 0) {
                    $scope.select_city.remove(city_index);
                    $('.' + city).removeClass('checked');
                }
                else {
                    $scope.select_city.push(city);
                    $('.' + city).addClass('checked');
                }
                if ($scope.select_city.length != 0) {
                    $('.city_form_next_btn').css('display', 'block');
                    $('.city_form_next_btn img').removeClass('hide').addClass('show');
                    $('html, body').animate({scrollTop: $(document).height()}, 500);
                } else{
                    $('.city_form_next_btn').css('display', 'none');
                    $('.city_form_next_btn img').removeClass('show').addClass('hide');
                }
            };

            $scope.next = function() {
                $http.post(
                    api.resume.select_city,
                    $.param({city: $scope.select_city})
                ).success(function(data) {
                    $state.go('select_position_category')
                }).error(function() {
                    console.log('请求失败');
                });
            };
            $scope.checked_area = function(city){
                for(var i = 0;i < $scope.data.expectation_area.length; i++){
                    if($scope.data.expectation_area[i].city__id == city.id){
                        return true;
                    }
                }
                return false;
            }
            $scope.check_first = function(index){
                if(index % 3 == 0){
                    return true;
                }
                return false;
            }
            $scope.check_second = function(index){
                if(index % 2 != 0){
                    return true;
                }
                return false;
            }
            $http.get(api.resume.select_city).success(function(data) {
                $scope.data = data.data;
                for(var i = 0;i < $scope.data.expectation_area.length; i++){
                    $scope.select_city.push($scope.data.expectation_area[i].city__id);
                }
                changeSelectedState($state);
            }).error(function() {
                console.log('请求失败');
            });
        }]
    )

    app.controller(
        'selectPositionCategory',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.category = '';
            $scope.static_url = static_url;

            $scope.back = function() {
                $state.go('select_city');
            }

            $scope.check_selected = function(id){
                if(id == $scope.category) return true;
                return false;
            }

            $scope.setPosition = function(category) {
                $scope.category = category;
                $http.post(
                    api.resume.select_position_category,
                    $.param({'category': $scope.category})
                ).success(function(data) {
                    $state.go('select_category_tag');
                }).error(function() {
                    console.log('请求失败');
                });
            };

            $http.get(api.resume.select_position_category).success(function(data) {
                $scope.data = data.data;
                $scope.category = data.data.category;
                changeSelectedState($state);
            }).error(function() {
                console.log('请求失败');
            });
        }]
    );

    app.controller(
        'selectCategoryTag',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.tag = [];
            $scope.static_url = static_url;

            $scope.back = function() {
                $state.go('select_position_category');
            }

            $scope.previous = function(tag) {
                var level = tag.level;
                if (level == 1) {
                    $http.post(
                        api.resume.select_category_tag,
                        $.param({'tag': $scope.tag})
                    ).success(function(data) {
                        $state.go('select_position_category');
                    }).error(function() {
                        console.log('请求失败');
                    });
                } else {
                    var checked_length = $('.checked').length;
                    if(checked_length != 0){
                        var tag_index = $scope.tag.indexOf($scope.data.previous_tag.id);
                        if(tag_index < 0) {
                            $scope.tag.push($scope.data.previous_tag.id);
                        }
                    } else {
                        var tag_index = $scope.tag.indexOf($scope.data.previous_tag.id);
                        if (tag_index > 0) {
                            $scope.tag.remove(tag_index);
                        };
                    }
                    $scope.data.previous_tag.id = $scope.data.save_id;
                    $scope.data.previous_tag.name = $scope.data.save_name;
                    $scope.data.previous_tag.level = 1;
                    $scope.data.category_tag = $scope.data.save_tag;
                }
            };

            $scope.checkTag = function(tag) {
                var hasChild = tag.child ? tag.child.length : false;
                if(hasChild) {
                    //有子节点
                    $scope.data.save_id = $scope.data.previous_tag.id;
                    $scope.data.save_name = $scope.data.previous_tag.name;
                    $scope.data.save_tag = $scope.data.category_tag;
                    $scope.data.previous_tag.id = tag.id;
                    $scope.data.previous_tag.level = 2;
                    $scope.data.previous_tag.name = tag.name;
                    $scope.data.category_tag = tag.child;
                } else {
                    //无子节点
                    var tag_index = $scope.tag.indexOf(tag.id);
                    var previous_tag_index = $scope.tag.indexOf($scope.data.previous_tag.id);
                    if(tag_index >= 0) {
                        $scope.tag.remove(tag_index);
                        $('.' + tag.id).removeClass('checked');
                        if($('.checked').length == 0){
                            $scope.tag.remove($scope.data.previous_tag.id);
                        }
                    }
                    else {
                        $scope.tag.push(tag.id);
                        $('.' + tag.id).addClass('checked');
                        $('.' + tag.id).find('img').addClass('checked');
                        if($('.checked').length == 0 && previous_tag_index < 0){
                            $scope.tag.push($scope.data.previous_tag.id);
                        }
                    }
                    if ($scope.tag.length != 0) {
                        $('.city_form_next_btn').css('display', 'block');
                        $('.city_form_next_btn img').removeClass('hide').addClass('show');
                        $('html, body').animate({scrollTop: $(document).height()}, 500);
                    } else{
                        $('.city_form_next_btn').css('display', 'none');
                        $('.city_form_next_btn img').removeClass('show').addClass('hide');
                    }
                }

            };

            $scope.next = function() {
                $http.post(
                    api.resume.select_category_tag,
                    $.param({'tag': $scope.tag})
                ).success(function(data) {
                    $state.go('select_work_years');
                }).error(function() {
                    console.log('请求失败');
                });
            };
            $scope.check_first = function(index){
                if(index % 3 == 0){
                    return true;
                }
                return false;
            }
            $scope.check_second = function(index){
                if(index % 2 != 0){
                    return true;
                }
                return false;
            }
            $scope.check_selected = function(id){
                for (i in $scope.tag){
                    if (id == $scope.tag[i]) {
                        $('.city_form_next_btn').css('display', 'block');
                        $('.city_form_next_btn img').removeClass('hide').addClass('show');
                        return true;
                    }
                }
                return false;
            }
            $http.get(api.resume.select_category_tag).success(function(data) {
                $scope.data = data.data;
                //将选过的节点放入$scope.tag中
                for (var i = $scope.data.resume_tag.length - 1; i >= 0; i--) {
                    $scope.tag.push($scope.data.resume_tag[i].position_tag__id);
                };
            }).error(function() {
                console.log('请求失败');
            });
        }]
    );

    app.controller(
        'selectWorkyears',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.work_years = '';
            $scope.static_url = static_url;

            $scope.back = function() {
                $state.go('select_position_category');
            }

            $scope.setWorkyears = function(work_years) {
                $scope.work_years = work_years;
                $('a').removeClass('checked');
                $('#' + $scope.work_years).addClass('checked');
                $http.post(
                    api.resume.select_workyears,
                    $.param({work_years: $scope.work_years})
                ).success(function(data) {
                    $state.go('select_degree');
                }).error(function() {
                    console.log('请求失败');
                });
            };

            $http.get(api.resume.select_workyears).success(function(data) {
                $scope.work_years = data.data.work_years;
                if($scope.work_years != ''){
                    $('#' + $scope.work_years).addClass('checked');
                }
                changeSelectedState($state);
            }).error(function() {
                console.log('请求失败');
            });
        }]
    );

    app.controller(
        'selectDegree',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.degree = '';
            $scope.static_url = static_url;
            $scope.back = function() {
                $state.go('select_work_years');
            }
            $scope.setDegree = function(degree) {
                $scope.degree = degree;
                $('a').removeClass('checked');
                $('#' + $scope.degree).addClass('checked');
                $http.post(
                    api.resume.select_degree,
                    $.param({degree: $scope.degree})
                ).success(function(data) {
                    $state.go('select_salary');
                }).error(function() {
                    console.log('请求失败');
                });
            };

            $scope.check_degree = function(degree) {
                for (var i = degree.length - 1; i >= 0; i--) {
                    if($scope.data.degree == degree[i]) return true;
                };
                return false;
            }

            $http.get(api.resume.select_degree).success(function(data) {
                $scope.data = data.data;
                changeSelectedState($state);
            }).error(function() {
                console.log('请求失败');
            });
        }]
    );
    app.controller(
        'selectSalary',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.static_url = static_url;
            $scope.back = function() {
                $state.go('select_degree');
            }

            $scope.next = function() {
                if($('.error').css('display') == 'none'){
                    $http.post(
                        api.resume.select_salary_lowest,
                        $.param({salary_lowest: $scope.salary + '000'})
                    ).success(function(data) {
                        if(data && data.status == 'ok'){
                            $state.go('select_field');
                        } else {
                            alert(data.msg);
                        }
                    }).error(function(){
                        console.log('请求失败')
                    });
                }
            };

            $scope.hideInfo = function(e) {
                var target = e.target;
                $(target).parent().css('border', '1px solid #d7d7d7');
            }

            $scope.isShow = function() {
                if($scope.salary == '0' || $scope.salary == '' || $scope.salary == '00')
                    return false;
                return true;
            }

            $scope.showInfo = function(event) {
                //把非数字的都替换掉
                $scope.salary  = event.target.value.replace(/[^\d]/g,"");
                if($scope.salary != 0 && $scope.salary != '') {
                    $('.error').css('display', 'none');
                    $('.info span').html($scope.salary * 1000);
                    $('.info').css('display', 'block');
                } else if ($scope.salary == 0 || $scope.salary == 00) {
                    $('.info').css('display', 'none');
                    $('.error').css('display', 'block');
                }
                else {
                    $('.info').css('display', 'none');
                }
            }

            $scope.focusInput = function(event) {
                var $input = $(event.target).find('input'),
                    value = $input.val();
                $input.val('');
                $input.focus();
                $input.val(value);
                $input.focus();
            }

            $http.get(api.resume.select_salary_lowest).success(function(data) {
                $scope.data = data.data;
                var salary = $scope.data.salary_lowest;
                $scope.salary = salary/1000;
                $scope.salary = $scope.salary == 0 ?  '' : $scope.salary;
                changeSelectedState($state);
                if($scope.data.salary_lowest != 0) {
                    $('.info span').html($scope.salary * 1000);
                    $('.info').css('display', 'block');
                }
            });
            $scope.addColor = function(e){
                var target = e.target;
                $(target).css('border-right', 0).parent().css('border', '1px solid #0091fa');
            }
        }]
    );
    app.controller(
        'selectField',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.select_field = [];
            $scope.static_url = static_url;
            $scope.back = function() {
                $state.go('select_salary');
            }
            $scope.checkField = function(city) {
                var city_index = $scope.select_field.indexOf(city);
                if(city_index >= 0) {
                    $scope.select_field.remove(city_index);
                    $('.' + city).removeClass('checked');
                }
                else {
                    $scope.select_field.push(city);
                    $('.' + city).addClass('checked');
                }
                if ($scope.select_field.length != 0) {
                    $('.city_form_next_btn').css('display', 'block');
                    $('.city_form_next_btn img').removeClass('hide').addClass('show');
                    // $('html, body').animate({scrollTop: $(document).height()}, 500);
                } else{
                    $('.city_form_next_btn').css('display', 'none');
                    $('.city_form_next_btn img').removeClass('show').addClass('hide');
                }
            };
            $scope.isShow = function() {
                return true;
            }
            $scope.isDisabled = function() {
                if($scope.select_field != '') return false;
                return true;
            }
            $scope.next = function() {
                field_id_list = $scope.select_field;
                if(field_id_list != '') {
                    $http.post(
                        api.resume.select_prefer_field,
                        $.param({'field_id_list': field_id_list})
                    ).success(function(data) {
                        if(data && data.status == 'ok'){
                            window.location.href = '/job/#/recommend_job_list/';
                        } else {
                            console.log(data.msg);
                        }
                    }).error(function() {
                        console.log('请求失败');
                    });
                }
            };
            $scope.checked_field = function(field){
                for(var i = 0;i < $scope.data.prefer_fields.length; i++){
                    if($scope.data.prefer_fields[i].category__id == field.id){
                        return true;
                    }
                }
                return false;
            }
            $http.get(api.resume.select_prefer_field).success(function(data) {
                $scope.data = data.data;
                if($scope.data.prefer_fields.length == 0){
                    for(var i = 0;i < $scope.data.all_fields.length; i++){
                        $scope.data.prefer_fields.push({'category__id': $scope.data.all_fields[i].id});
                    }
                }
                for(var i = 0;i < $scope.data.prefer_fields.length; i++){
                    $scope.select_field.push($scope.data.prefer_fields[i].category__id);
                }
                changeSelectedState($state);
            }).error(function() {
                console.log('请求失败');
            });
        }]
    );

    //定义每种状态蓝色进度条长度
    var line_length = {
        'select_gender': '0',
        'select_city': '18%',
        'select_position_category': '36%',
        'select_work_years': '49.5%',
        'select_degree': '66%',
        'select_salary': '82.5%',
        'select_field': '99%'
    };
    //定义每个状态名称
    var state_name = ['select_gender', 'select_city', 'select_position_category', 'select_work_years', 'select_degree', 'select_salary', 'select_field'];
    function changeSelectedState(state){
        var current_name = state.current.name;
        current_index = state_name.indexOf(current_name);
        for (var i = current_index; i >= 0; i--) {
            $('.'+state_name[i]).parent().addClass("has_show");
        };
        for (var i = state_name.length - 1; i >= current_index; i--) {
             $('.'+state_name[i]).parent().removeClass("has_show");
        };
        $('.step_line_blue').css('width', line_length[current_name]);
        $('ul.step_dot_ul li').each(function(){
            $(this).removeClass('selected');
        });
        $('.'+current_name).parent().addClass('selected');
    }
})();
