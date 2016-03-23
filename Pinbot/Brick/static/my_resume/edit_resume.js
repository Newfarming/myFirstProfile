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
    var app = angular.module('app.edit_resume', ['app.config', 'ui.router', 'app.django', 'app.utils']);

    var $django = angular.injector(['app.django']);
    var tmpl = $django.get('tmpl');
    var api = $django.get('api');
    var static_url = $django.get('static_url');

    app.config([
        '$stateProvider', '$urlRouterProvider',
        function($stateProvider, $urlRouterProvider) {
            $urlRouterProvider.otherwise('/show_tag/');
            $stateProvider.state(
                'showTag',
                {
                    url: '/show_tag/',
                    templateUrl: tmpl('my_resume/show_tag.html'),
                    controller: 'showTag'
                }
            );
            $stateProvider.state(
                'edit_gender',
                {
                    url: '/edit_gender/',
                    templateUrl: tmpl('my_resume/select_gender.html'),
                    controller: 'editGender'
                }
            );
            $stateProvider.state(
                'edit_city',
                {
                    url: '/edit_city/',
                    templateUrl: tmpl('my_resume/select_city.html'),
                    controller: 'editCity'
                }
            );
            $stateProvider.state(
                'edit_position_category',
                {
                    url: '/edit_position_category/',
                    templateUrl: tmpl('my_resume/select_position_category.html'),
                    controller: "editPositionCategory"
                }
            );
            $stateProvider.state(
                'edit_category_tag',
                {
                    url: '/edit_category_tag/:category',
                    templateUrl: tmpl('my_resume/select_category_tag.html'),
                    controller: "editCategoryTag"
                }
            );
            $stateProvider.state(
                'edit_work_years',
                {
                    url: '/edit_work_years/',
                    templateUrl: tmpl('my_resume/select_workyears.html'),
                    controller: "editWorkyears"
                }
            );
            $stateProvider.state(
                'edit_degree',
                {
                    url: '/edit_degree/',
                    templateUrl: tmpl('my_resume/select_degree.html'),
                    controller: "editDegree"
                }
            );
            $stateProvider.state(
                'edit_field',
                {
                    url: '/edit_field/',
                    templateUrl: tmpl('my_resume/select_field.html'),
                    controller: "editField"
                }
            );
            $stateProvider.state(
                'edit_salary',
                {
                    url: '/edit_salary/',
                    templateUrl: tmpl('my_resume/select_salary.html'),
                    controller: "editSalary"
                }
            );
        }
    ]);

    app.controller(
        'showTag',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.static_url = static_url;
            $scope.go_job_rec = function() {
                window.location.href = '/job/#/recommend_job_list/'
            }
            $scope.check_first_li = function(index) {
                if(index % 5 == 0){
                    return true;
                }
                return false;
            }
            $scope.check_second_li = function(index) {
                if(index % 2 == 0){
                    return true;
                }
                return false;
            }
            $scope.check_third_li = function(index) {
                if(index % 3 == 0){
                    return true;
                }
                return false;
            }
            $scope.toggle_input_div = function(e) {
                var $a = $(e.target);
                    $tag_input_div = $('.tag_input_div'),
                    display = $tag_input_div.css('display');
                if(display != 'none') {
                    $a.removeClass('minus');
                    $tag_input_div.css('display', 'none');
                    $('div.tag_input_div ul').css('display', 'none');
                    $('div.tag_input_div input').val('');
                } else {
                    $a.addClass('minus');
                    $tag_input_div.css('display', 'table');
                    $http.get('/my_resume/add_resume_tag/').success(function(data) {
                       $scope.allTags = data.data;
                    });
                    $('html, body').animate({scrollTop: $(document).height()}, 500);
                }
            }
            $scope.dropDown = function(event) {
                $('.addTag').unbind('click').attr('isUse', 'unuse');
                $scope.workTags = []
                var e = event,
                    $input = $(e.target),
                    value = $input.val();
                for (var i = $scope.allTags.length - 1; i >= 0; i--) {
                    var index = $scope.allTags[i].name.toLowerCase().indexOf(value.toLowerCase());
                    if(index != -1){
                        $scope.workTags.push($scope.allTags[i]);
                    }
                };
                if(value != '') {
                    $('div.tag_input_div ul').css('display', 'block');
                    if($scope.workTags.length != 0) {
                        $('.show_tag_form div.tag_input_div ul li.none_info').css('display', 'none');
                    } else {
                        $('.show_tag_form div.tag_input_div ul li.none_info').css('display', 'block');
                    }
                }
                else {
                    $('div.tag_input_div ul').css('display', 'none');
                }
                $('html, body').animate({scrollTop: $('.tag_input_div input').offset().top}, 500);
            }
            $scope.setValue = function(event) {
                var e = event,
                    $a = $(e.target),
                    value = $a.html(),
                    tag_id = $a.attr('id');
                $scope.tagName = value;
                $('div.tag_input_div ul').css('display', 'none');
                $('.addTag').attr('isUse', 'use').one('click', function(){
                    $('.addTag').attr('isUse', 'unuse');
                    $http.post(
                        '/my_resume/add_resume_tag/',
                        $.param({tag_id: tag_id})
                    ).success(function(data) {
                        $scope.data.selected.category_tag = data.data;
                        $('.addTag').attr('isUse', 'use');
                    });
                });
            }
            $scope.isUnuse = function() {
                var $a = $('.addTag'),
                    $input = $('.tag_input_div input');
                if($a.attr('isuse') != 'unuse' || $input.val() == '') return false;
                return true;
            }
            $scope.delete_tag = function(id, index) {
                $scope.data.selected.category_tag.remove(index);
            	var api_url = api.resume.delete_resume_tag + id;
	            $http.get(api_url).success(function(data) {
                    console.log(data.status);
	            });
            }
            $scope.show_delete_btn = function(id, type) {
            	var $item = $('#' + id);
            	var color = $item.css('color');
            	if(color == "rgb(255, 255, 255)"){
            		$item.css('background', '#fff').css('color', '#0091fa').find('img').show();
            	} else {
            		$item.css('background', '#0091fa').css('color', '#fff').find('img').hide();
            	}
            }
            $http.get(api.resume.edit_resume_tag).success(function(data) {
                $scope.data = data.data;
                if( $scope.data.selected.city.length > 1 ){
                    $scope.data.selected.city = '意向城市';
                }else{
                    for (var i = $scope.data.selected.city.length - 1; i >= 0; i--) {
                        $scope.data.selected.city = $scope.data.selected.city[i];
                    };
                }
                $scope.data.selected.salary_lowest = $scope.data.selected.salary_lowest/1000 + 'K';
            });
        }]
    );

    app.controller(
        'editGender',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.gender = '';
            $scope.static_url = static_url;
            $scope.setGender = function(gender) {
                $scope.gender = gender;
                $('a').removeClass('checked');
                $('#' + $scope.gender).addClass('checked');
                $('.opt_part').css('display', 'block');
            };

            $scope.confirm = function() {
                $http.post(
                    api.resume.select_gender,
                    $.param({gender: $scope.gender})
                ).success(function(data) {
                    $state.go('showTag');
                });
            };

            $http.get(api.resume.select_gender).success(function(data) {
                $scope.gender = data.data.gender;
                if($scope.gender != ''){
                    $('#' + $scope.gender).addClass('checked');
                }
                $('p').html('<a class="back"><img src="' + static_url + 'my_resume/img/arrow_1_32x46.fw.png"/></a>请修改你的性别');
                $('.back').click(function(){
                    $state.go('showTag');
                });
            });
        }]
    );

    app.controller(
        'editCity',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.select_city = [];
            $scope.static_url = static_url;

            $scope.back = function() {
                $state.go('showTag');
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
                    $opt_part = $('.opt_part');
                    $opt_part.css('display', 'block');
                    if( $opt_part.find('a').css('font-size') == '18px' && $('.city_form ul li').css('margin-bottom') != '20px' && $('.city_form ul ul').css('padding-bottom') != '20px'){
                        $opt_part.find('a').css('padding', '15px 0');
                    }
                    $('html, body').animate({scrollTop: $(document).height()}, 500);
                } else{
                    $('.opt_part').css('display', 'none');
                }
            };

            $scope.confirm = function() {
                $http.post(
                    api.resume.select_city,
                    $.param({city: $scope.select_city})
                ).success(function(data) {
                    $state.go('showTag')
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
                $('p').html('<a class="back"><img src="' + static_url + 'my_resume/img/arrow_1_32x46.fw.png"/></a>请修改求职意向地');
                $('.back').click(function(){
                    $state.go('showTag');
                });
            });
        }]
    );
    app.controller(
        'editPositionCategory',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.category = '';
            $scope.static_url = static_url;

            $scope.check_selected = function(id) {
                if(id == $scope.category) return true;
                return false;
            }

            $scope.back = function() {
                $state.go('show_tag');
            }

            $scope.setPosition = function(category) {
                $state.go('edit_category_tag', {category: category});
            };

            $http.get(api.resume.select_position_category).success(function(data) {
                $scope.data = data.data;
                $scope.category = data.data.category;
                $('p').html('<a class="back"><img src="' + static_url + 'my_resume/img/arrow_1_32x46.fw.png"/></a>请修改职位');
                $('.back').click(function(){
                    $state.go('showTag');
                });
            });
        }]
    );
    app.controller(
        'editCategoryTag',
        ['$scope', '$http', '$state', '$stateParams', function($scope, $http, $state, $stateParams) {
            $scope.tag = [];
            $scope.static_url = static_url;

            $scope.back = function() {
                $state.go('edit_position_category');
            }

            $scope.previous = function(tag) {
                var level = tag.level;
                if (level == 1) {
                    $state.go('edit_position_category');
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
                    var previous_level = $scope.data.previous_tag.level;
                    if(tag_index >= 0) {
                        $scope.tag.remove(tag_index);
                        $('.' + tag.id).removeClass('checked');
                        if($('a.checked').length == 0){
                            $scope.tag.remove($scope.data.previous_tag.id);
                        }
                    }
                    else {
                        $scope.tag.push(tag.id);
                        $('.' + tag.id).addClass('checked');
                        $('.' + tag.id).find('img').addClass('checked');
                        if($('.checked').length != 0 && previous_tag_index < 0 && previous_level != 1){
                            $scope.tag.push($scope.data.previous_tag.id);
                        }
                    }
                    if ($('a.checked').length != 0) {
                        $opt_part = $('.opt_part');
                        $opt_part.css('display', 'block');
                        if( $opt_part.find('a').css('font-size') == '18px' && $('.city_form ul li').css('margin-bottom') != '20px' && $('.city_form ul ul').css('padding-bottom') != '20px'){
                            $opt_part.find('a').css('padding', '15px 0');
                        }
                        $('html, body').animate({scrollTop: $(document).height()}, 500);
                    } else{
                        $('.opt_part').css('display', 'none');
                    }
                }

            };

            $scope.confirm = function() {
                $scope.category = $scope.root_id;
                $http.post(
                    api.resume.edit_category_tag,
                    $.param({'tag': $scope.tag, 'category': $scope.category})
                ).success(function(data) {
                    $state.go('showTag');
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
                        return true;
                    }
                }
                return false;
            }
            var api_url = api.resume.edit_category_tag + '?category=' + $stateParams.category;
            $http.get(api_url).success(function(data) {
                $scope.data = data.data;
                //将选过的节点放入$scope.tag中
                for (var i = $scope.data.resume_tag.length - 1; i >= 0; i--) {
                    $scope.tag.push($scope.data.resume_tag[i].position_tag__id);
                };
                //保存一级菜单节点id
                $scope.root_id = $scope.data.previous_tag.id;
               $('p')[0].childNodes[1].data = '请修改职位标签';
            });
        }]
    );
    app.controller(
        'editWorkyears',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.work_years = '';
            $scope.static_url = static_url;

            $scope.back = function() {
                $state.go('showTag');
            }

            $scope.setWorkyears = function(work_years) {
                $scope.work_years = work_years;
                $('a').removeClass('checked');
                $('#' + $scope.work_years).addClass('checked');
                $('.opt_part').css('display', 'block');
                $('html, body').animate({scrollTop: $(document).height()}, 500);
            };

            $scope.confirm = function(){
                $http.post(
                    api.resume.select_workyears,
                    $.param({work_years: $scope.work_years})
                ).success(function(data) {
                    $state.go('showTag');
                });
            }
            $scope.check_selected = function(index){
                if(index == $scope.work_years) return true;
                return false;
            }
            $http.get(api.resume.select_workyears).success(function(data) {
                $scope.work_years = data.data.work_years;
                $('p').html('<a class="back"><img src="' + static_url + 'my_resume/img/arrow_1_32x46.fw.png"/></a>请修改工作年限');
                $('.back').click(function(){
                    $state.go('showTag');
                });
            });
        }]
    )

    app.controller(
        'editDegree',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.degree = '';
            $scope.static_url = static_url;
            $scope.back = function() {
                $state.go('showTag');
            }
            $scope.setDegree = function(degree) {
                $scope.degree = degree;
                $('a').removeClass('checked');
                $('#' + $scope.degree).addClass('checked');
                if($('.checked').length != 0){
                    $('.opt_part').css('display', 'block');
                }
                $('html, body').animate({scrollTop: $(document).height()}, 500);
            };

            $scope.confirm = function(){
                $http.post(
                    api.resume.select_degree,
                    $.param({degree: $scope.degree})
                ).success(function(data) {
                    $state.go('showTag');
                });
            }

            $scope.check_degree = function(degree){
                for (var i = degree.length - 1; i >= 0; i--) {
                    if($scope.data.degree == degree[i]) return true;
                };
                return false;
            }

            $http.get(api.resume.select_degree).success(function(data) {
                $scope.data = data.data;
                $('p').html('<a class="back"><img src="' + static_url + 'my_resume/img/arrow_1_32x46.fw.png"/></a>请修改你的学历');
                $('.back').click(function(){
                    $state.go('showTag');
                });
            });
        }]
    );

    app.controller(
        'editField',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.select_field = [];
            $scope.static_url = static_url;
            $scope.back = function() {
                $state.go('showTag');
            }
            $scope.checkField = function(field) {
                var field_index = $scope.select_field.indexOf(field);
                if(field_index >= 0) {
                    $scope.select_field.remove(field_index);
                    $('.' + field).removeClass('checked');
                }
                else {
                    $scope.select_field.push(field);
                    $('.' + field).addClass('checked');
                }
                if ($scope.select_field.length != 0) {
                    $opt_part = $('.opt_part');
                    $opt_part.css('display', 'block');
                    if( $opt_part.find('a').css('font-size') == '18px' && $('.city_form ul li').css('margin-bottom') != '20px' && $('.city_form ul ul').css('padding-bottom') != '20px'){
                        $opt_part.find('a').css('padding', '15px 0');
                    }
                    // $('html, body').animate({scrollTop: $(document).height()}, 500);
                } else{
                    $('.opt_part').css('display', 'none');
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
            $scope.isShow = function() {
                return false;
            }

            $scope.confirm = function(){
                field_id_list = $scope.select_field;
                $http.post(
                    api.resume.select_prefer_field,
                    $.param({'field_id_list': field_id_list})
                ).success(function(data) {
                    $state.go('showTag')
                });
            }
            $scope.hideGetRec = function() {
                return true;
            }
            $http.get(api.resume.select_prefer_field).success(function(data) {
                $scope.data = data.data;
                for(var i = 0;i < $scope.data.prefer_fields.length; i++){
                    $scope.select_field.push($scope.data.prefer_fields[i].category__id);
                }
                $('p').html('<a class="back"><img src="' + static_url + 'my_resume/img/arrow_1_32x46.fw.png"/></a>请修改偏好领域');
                $('.back').click(function(){
                    $state.go('showTag');
                });
            });
        }]
    );

    app.controller(
        'editSalary',
        ['$scope', '$http', '$state', function($scope, $http, $state) {
            $scope.salary = '';
            $scope.static_url = static_url;
            $scope.back = function() {
                $state.go('showTag');
            }

            $scope.confirm = function(){
                if($('.error').css('display') == 'none'){
                    $http.post(
                        api.resume.select_salary_lowest,
                        $.param({salary_lowest: $scope.salary + '000'})
                    ).success(function(data) {
                        if(data && data.status == 'ok'){
                            $state.go('showTag');
                        } else {
                            alert(data.msg);
                        }

                    }).error(function(){
                        console.log('请求失败')
                    });
                }
            }

            $scope.confrimShow = function(salary) {
                if($('.error').css('display') != 'none')
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
            $scope.hideInfo = function(e) {
                var target = e.target;
                $(target).parent().css('border', '1px solid #d7d7d7');
            }
            $scope.addColor = function(e){
                var target = e.target;
                $(target).css('border-right', 0).parent().css('border', '1px solid #0091fa');
            }
            $scope.none = function() {
                return true;
            }
            $scope.focusInput = function(event) {
                $(event.target).find('input').focus();
            }
            $http.get(api.resume.select_salary_lowest).success(function(data) {
                $scope.data = data.data;
                var salary = $scope.data.salary_lowest;
                $scope.salary = salary/1000;
                $scope.salary = $scope.salary == 0 ?  '' : $scope.salary;
                if($scope.data.salary_lowest != 0) {
                    $('.info span').html($scope.salary * 1000);
                    $('.info').css('display', 'block');
                }
            });
        }]
    );

})();
