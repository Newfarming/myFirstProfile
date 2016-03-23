var app = angular.module('app.questionnaire', ['app.config', 'ui.router', 'app.django', 'app.utils', 'app.filter']),
    $django = angular.injector(['app.django']),
    $funcs = angular.injector(['app.utils']),
    tmpl = $django.get('tmpl'),
    static_url = $django.get('static_url');

app.config([
    '$interpolateProvider',
    function($interpolateProvider) {
        $interpolateProvider.startSymbol('{-');
        $interpolateProvider.endSymbol('-}');
    }
]);

app.factory('$', [
    '$window',
    function($window) {
        return $window.jQuery.noConflict();
    }
]);

var pbLib = $funcs.get('pbLib');
var confirmBox = $funcs.get('confirmBox');
var confirmBoxRed = $funcs.get('confirmBoxRed');
var alertBox = $funcs.get('alertBox');
var getModeData = $funcs.get('getModeData');
var postModeData = $funcs.get('postModeData');
var inArray = $funcs.get('inArray');
var pbFunc = $funcs.get('pbFunc');

app.config([
    '$stateProvider', '$urlRouterProvider',
    function($stateProvider, $urlRouterProvider) {
        var otherwiseUrl = '/';
        $urlRouterProvider.otherwise(otherwiseUrl);
        $stateProvider.state(
            'default', {
                url: '/',
                template: '',
                controller: 'questionnaire'
            }
        );
    }
]);
app.controller(
    'questionnaire', [
        '$rootScope', '$scope', '$http', '$state',
        function($rootScope, $scope, $http, $state) {

        }
    ]
);
app.directive('questionlistDirective', function() {
    return {

        scope: {
            qrUrl: '='
        },
        controller: function($rootScope, $scope, $element, $attrs, $transclude, $http, $state) {
            var question_types_count;
            var postArr = [];
            $scope.posted = false;
            //二维码显示中间变量
            $scope.QRshow = false;
            var isValidSubmit = true;
            $scope.localData = {
                questions: {},
                questionTypes: []
            };
            /*ajax获取后端数据*/
            var req = getModeData($http, '/activity/questions/', '', function(data) {
                $scope.products = data;
                pushQuestion('products', 'localData');
            }, undefined, function() {
                req.abort();
                alert("an unexpected error ocurred!");
            }, undefined);

            var judgeQuestionType = function(getObjName, localObjName) {
                var num = $scope[getObjName].question_types_count;
                var questionstypes = $scope[getObjName].question_types;
                for (i = 0; i < num; i++) {
                    localObjName.questions[questionstypes[i]] = [];
                }
            }


            /*

             对获取对数据进行分类并填充
             参数
             getObjName ：用get方法获取到的json数据
            localObjName ： 需要填充的本地数据
            */

            var pushQuestion = function(getObjName, localObjName) {
                question_types_count = $scope[getObjName].question_types_count;
                //get方法得到的问题类型
                var questionstypes = $scope[getObjName].question_types;
                $scope[localObjName].questionTypes = questionstypes;
                $scope[localObjName].question_types_zh_CN = $scope[getObjName].question_types_zh_CN;
                $scope[localObjName].questionNumber = $scope[getObjName].questions.length;
                for (i = 0; i < question_types_count; i++) {

                    $scope[localObjName].questions[questionstypes[i]] = [];
                    for (var j = 0, imax = $scope[getObjName].questions.length; j < imax; j++) {
                        var temp = {};
                        if ($scope[getObjName].questions[j].question_type == questionstypes[i]) {
                            temp = {};
                            temp.question_id = $scope[getObjName].questions[j].question_id;
                            temp.answer_type = $scope[getObjName].questions[j].anwser_type;
                            temp.answers_count = $scope[getObjName].questions[j].anwsers_count;
                            temp.answer_options = [];
                            temp.order = $scope[getObjName].questions[j].order;
                            temp.is_other_option = $scope[getObjName].questions[j].is_other_option;
                            temp.answer_word = "";
                            temp.wrong_show = true;
                            temp.question = $scope[getObjName].questions[j].question;
                            temp.other_opinion_selected = false;
                            if (temp.answer_type == 'single_choies' || temp.answer_type == 'single_choies_or_text' || temp.answer_type == 'multi_choies' || temp.answer_type == 'multi_choies_or_text') {
                                var tempObj = {}
                                for (answer in $scope[getObjName].questions[j].anwser_options) {
                                    if ($scope[getObjName].questions[j].anwser_options.hasOwnProperty(answer)) {
                                        tempObj = {};
                                        tempObj.name = $scope[getObjName].questions[j].anwser_options[answer];
                                        tempObj.selected = false;
                                        temp.answer_options.push(tempObj);
                                    }
                                }
                                delete tempObj;
                            }

                            if (temp.answer_type == 'address') {
                                temp.answer_word = ['', '', ''];
                            }
                            $scope[localObjName].questions[questionstypes[i]].push(temp);
                            delete temp;
                        }
                    }
                }
            };
            //提交表单时的表单验证
            var formValidate = function(postar) {
                    for (var i = 0, imax = postar.length; i < imax; i++) {
                        if (postar[i].answer == '') {
                            isValidSubmit = false;
                            break;
                        }
                    }
                    $scope.posted = true;
                }
                //双向绑定实时进行表单验证
            var actualTime = function(answer_obj) {
                answer_obj.wrong_show = true;
                var judge = true;
                if (answer_obj.answer_type == 'address') {
                    for (var j = 0, jmax = answer_obj.answer_word.length; j < jmax; j++) {
                        if (answer_obj.answer_word[j] == '') {

                            judge = false;
                            break;
                        }
                    }
                    if (judge == true) {
                        answer_obj.wrong_show = false;
                    }

                } else if (answer_obj.answer_type == 'single_choies' || answer_obj.answer_type == 'single_choies_or_text' || answer_obj.answer_type == 'multi_choies' || answer_obj.answer_type == 'multi_choies_or_text') {
                    for (var j = 0, jmax = answer_obj.answer_options.length; j < jmax; j++) {
                        if (answer_obj.answer_options[j].selected == true) {
                            answer_obj.wrong_show = false;
                            break;
                        }
                    }
                    if (answer_obj.is_other_option == true) {
                        if (answer_obj.answer_word !== '') {
                            answer_obj.wrong_show = false;
                        }
                    }
                } else if (answer_obj.answer_type == 'long_text' || answer_obj.answer_type == 'short_text') {
                    if (answer_obj.answer_word !== '') {
                        answer_obj.wrong_show = false;

                    }
                }
            }
            $scope.actualtime = function(answer_obj) {
                actualTime(answer_obj);
            }
            $scope.showjudge = function(answer_obj, posted) {
                return answer_obj
            }
            //单选
            $scope.singleSelect = function(answer_obj, index) {
                if (index == 'other') {
                    for (var i = answer_obj.answers_count - 1; i >= 0; i--) {
                        answer_obj.answer_options[i].selected = false;

                    }
                    answer_obj.other_opinion_selected = true;
                } else {
                    for (var j = answer_obj.answers_count - 1; j >= 0; j--) {
                        if (index == j) {
                            for (var i = answer_obj.answers_count - 1; i >= 0; i--) {
                                answer_obj.answer_options[i].selected = false;

                            }
                            answer_obj.other_opinion_selected = false;
                            answer_obj.answer_options[j].selected = true;

                            break;
                        }
                    }
                }
                actualTime(answer_obj);
            }



            //复选
            $scope.multiSelect = function(answer_obj, index) {
                if (index == 'other') {
                    answer_obj.other_opinion_selected = !answer_obj.other_opinion_selected;
                } else {
                    for (var j = answer_obj.answers_count - 1; j >= 0; j--) {
                        if (index == j) {
                            answer_obj.answer_options[j].selected = !answer_obj.answer_options[j].selected;
                        }
                    }
                }
                actualTime(answer_obj);
            }
            //对本地数据进行序列化
            //参数
            //localObjName ： 需要被序列化的本地数据
            //postObj ：序列化后需要提交的数据
            //
            var changeQuestion = function(localObjName, posArr) {
                    var pushArr = [];
                    for (obj in $scope[localObjName].questions) {
                        if ($scope[localObjName].questions.hasOwnProperty(obj)) {

                            for (var i = 0, imax = $scope[localObjName].questions[obj].length; i < imax; i++) {
                                pushArr.push($scope[localObjName].questions[obj][i]);
                            }
                        }
                    }
                    for (var i = 0, imax = pushArr.length; i < imax; i++) {
                        if (pushArr[i].answer_type == 'address') {
                            var addressJudge = true;
                            for (var j = 0, jmax = pushArr[i].answer_word.length; j < jmax; j++) {
                                if (pushArr[i].answer_word[j] == '') {
                                    addressJudge = false;
                                }
                            }
                            if (addressJudge) {
                                pushArr[i].postAnswer = pushArr[i].answer_word.join(',');
                            } else {
                                pushArr[i].postAnswer = '';
                            }

                        } else if (pushArr[i].answer_type == 'single_choies' || pushArr[i].answer_type == 'single_choies_or_text' || pushArr[i].answer_type == 'multi_choies' || pushArr[i].answer_type == 'multi_choies_or_text') {
                            pushArr[i].postAnswer = [];
                            for (var j = 0, jmax = pushArr[i].answer_options.length; j < jmax; j++) {
                                if (pushArr[i].answer_options[j].selected == true) {
                                    pushArr[i].postAnswer.push(pushArr[i].answer_options[j].name);
                                }

                            }
                            if (pushArr[i].other_opinion_selected == true) {
                                pushArr[i].postAnswer.push(pushArr[i].answer_word);
                            }

                            pushArr[i].postAnswer = pushArr[i].postAnswer.join(',');
                        } else {
                            pushArr[i].postAnswer = pushArr[i].answer_word;
                        }

                    }
                    for (var i = 0, imax = $scope[localObjName].questionNumber - 1; i <= imax; i++) {
                        var temp = {};
                        temp.question_id = pushArr[i].question_id;
                        temp.answer = pushArr[i].postAnswer;
                        posArr.push(temp);
                    }

                    posArr = posArr.join(',');
                    posArr = JSON.stringify(posArr);
                }
                //提交表单
            $scope.saveFolder = function() {
                postArr = []
                changeQuestion("localData", postArr);
                formValidate(postArr);
                var html = '<div style="margin: 0 auto;width: 400px;">' +
                    '<div class="f16 text-center"><i class="i-l-notice"></i>表单内容提交后不可修改</div>'
                '</div>';
                $.alert(
                    html,
                    '',
                    '', {
                        handlers: [{
                            title: '返回修改',
                            eventType: 'click',
                            className: 'button button-normal w158 f16',
                            event: function() {
                                $._LayerOut.close();
                            }
                        }, {
                            title: '确定',
                            eventType: 'click',
                            className: 'button button-primary w158 f16',
                            event: function() {
                                if (!isValidSubmit) {
                                    $.alert(
                                        '<p style="text-align:center;font-size:25px;color:#77c7ef;">请将调查问卷填写完整后保存</p>'
                                    );
                                    isValidSubmit = true;
                                    return false;
                                }
                                if (postArr.length > 0) {

                                    var save_folder = postModeData($http, {
                                            'anwsers': postArr
                                        },
                                        '/activity/questionnaire_feedback/',
                                        "",
                                        function(data) {
                                            if (data.status == 'ok') {
                                                document.location.href = "/";
                                            }
                                        }, undefined, function(err) {
                                            save_folder.abort();
                                        }, 'json');
                                }
                                $._LayerOut.close();
                            }
                        }]
                    }
                );

            };
            $scope.changeQR = function() {
                if ($scope.QRshow == false) {
                    $scope.QRshow = true;
                } else {
                    $scope.QRshow = false;
                }
            };
        },
        restrict: 'E',
        templateUrl: tmpl('activity/questionnaire/quesList.html'),
        replace: true,
        link: function($scope, iElm, iAttrs, controller) {

        }
    };
});
/**/
/**/