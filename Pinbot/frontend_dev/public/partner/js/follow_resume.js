(function(angular,undefined){

    var app = angular.module( 'followResume' , [ 'app.config' , 'ui.router' , 'app.utils' , 'app.filter' , 'app.django' , 'validation', 'validation.rule' ] ),
        $service = angular.injector( [ 'app.django' , 'app.utils' ] ),
        id_url = $service.get('id_url'),
        tmpl = $service.get('tmpl');

    app.controller(
        'followResumeController',
        [
            '$scope',
            '$validation',
            '$http',
            '$injector',
            function( $scope , $validation , $http , $injector ){

                // 获取数据
                $scope.data = JSON.parse($('#JS_get_data').attr('data'));

                // init msgType
                $scope.msgType = 1;

                $scope.isSending = false;
                $scope.isGetting = false;

                // init name & phone
                $scope.send_info = {
                    name: '',
                    phone: ''
                }

                // init has_hr_info
                $scope.has_hr_info = $scope.data.hr_contact_info.has_hr_info;

                // init hr 联系信息
                $scope.hr_info = {
                    company_name: '',
                    phone: '',
                    name: '',
                    email: '',
                    qq: ''
                }

                // 发送状态
                $scope.sendStatus = false;

                // 是否可发送消息
                if($scope.data.has_send_notify){
                    $scope.sendBtn = '明天再来吧';
                    $scope.isSending = true;
                } else {
                    $scope.sendBtn = '发送给对方';
                }

                // 是否已输入name&phone
                if($scope.data.user_info.name != undefined) {
                    $scope.send_info.name = $scope.data.user_info.name;
                    $scope.send_info.phone = $scope.data.user_info.phone;
                }

                // 是否已有hr联系信息
                if($scope.has_hr_info) {
                    $scope.hr_info.company_name = $scope.data.hr_contact_info.company_name;
                    $scope.hr_info.phone = $scope.data.hr_contact_info.phone;
                    $scope.hr_info.name = $scope.data.hr_contact_info.name;
                    $scope.hr_info.email = $scope.data.hr_contact_info.email;
                    $scope.hr_info.qq = $scope.data.hr_contact_info.qq;
                }

                $scope.selectMsg = function(msgType) {
                    $scope.msgType = msgType;
                }

                // 给需求方HR发站内信
                $scope.sendMsg = function() {
                    if ($scope.isSending === false) {
                        $scope.isSending = true;
                        $http.post(
                            '.',
                            $.param({msg_type: $scope.msgType})
                        )
                        .success(function(data){
                            if(data.status === 'ok') {
                                // 发送成功，按钮改变文案
                                $scope.sendBtn = '明天再来吧';
                                $scope.sendStatus = true;
                            } else {
                                $.alert(data.msg);
                                $scope.isSending = false;
                                $scope.sendBtn = '发送给对方';
                            }
                        })
                        .error(function(){
                            // 发送失败，恢复按钮
                            $scope.isSending = false;
                            $scope.sendBtn = '发送给对方';
                        });
                    };
                }

                // 展示推荐话术弹窗
                $scope.showTalk = function() {
                    var html =  '<div class="rec-talk text-center">' +
                                    '<h3>互助伙伴推荐话术</h3>' +
                                    '<p class="sub-title">试试这些官方话术，让你更好地促进任务进展哦~</p>' +
                                    '<p class="talk-content">“Hi~XX你好，我是聘宝互助伙伴XXX，我看到你在聘宝上提交的定制XX职位。<br>我向你推荐了一名非常符合JD需求的候选人，欢迎在专属定制推荐列表中查看……”</p>' +
                                    '<p class="handle JS_close_layerout"><a href="javascript:void(0)" class="btn">关闭</a></p>' +
                                '</div>';
                    $.LayerOut({
                        html: html
                    })
                }

                // 获取联系方式表单验证
                $scope.contact_form = {
                    submit: function (form) {
                        $validation.validate(form)
                            .success($scope.success)
                            .error($scope.error);
                    }
                };

                // 验证成功，发送获取联系方式请求
                $scope.success = function (message) {
                    if ($scope.isGetting === false) {
                        $scope.isGetting = true;
                        var task_id = $scope.data.task_id,
                            resume_id = $scope.data.resume_id;
                        $http.post(
                            '/partner/get_hr_contact/' + task_id + '/' + resume_id + '/',
                            $.param({name: $scope.send_info.name, phone: $scope.send_info.phone})
                        ).success(function(data){
                            console.log(data);
                            $scope.isGetting = false;
                            if(data.status === 'ok') {
                                $scope.has_hr_info = true;
                                $scope.hr_info.company_name = data.contact_info.company_name;
                                $scope.hr_info.phone = data.contact_info.phone;
                                $scope.hr_info.name = data.contact_info.name;
                                $scope.hr_info.email = data.contact_info.email;
                                $scope.hr_info.qq = data.contact_info.qq;
                            } else {
                                $.alert('表单错误，请重新填写！');
                            }
                        }).error(function(data){
                            $.alert('请求失败，请重新请求...');
                            $scope.isGetting = false;
                        });
                    };
                };

                // 验证失败
                $scope.error = function (message) {
                    return;
                };
            }
        ]
    );

    app.directive('sendMsg', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/follow_resume_send_msg.html'),
            controller: 'followResumeController',
            link: function(scope, elem, attrs) {},
            scope: true
        }
    });

    app.directive('getContact', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/follow_resume_contact.html'),
            controller: 'followResumeController',
            link: function(scope, elem, attrs) {},
            scope: true
        }
    });

    app.directive('contactCandidate', function() {
        return {
            restrict: 'E',
            templateUrl: tmpl('partner/follow_resume_contact_candidate.html'),
            controller: 'followResumeController',
            link: function(scope, elem, attrs) {},
            scope: true
        }
    });

})(angular);

$(function(){
    // input占位符兼容ie9
    if (!('placeholder' in document.createElement('input'))) {
        $('input[placeholder]').each(function() {

            var $input = $(this);
            var $label = $('<label>');
            $label.html($input.attr('placeholder'));
            $label.css({
                'font-size': '14px',
                'position': 'absolute',
                'left': '15px',
                'top': '13px',
                'color': '#999',
                'cursor': 'text',
                'width': '100%',
                'text-align': 'left'
            });

            $input.on('keydown paste', function() {
                setTimeout(function() {
                    $label[ $input.val() ? 'hide' : 'show' ]();
                }, 0);
            }).parent().append(
                $label.on('click', function() {
                    $input.focus();
                })
            );
        });
    }

});
