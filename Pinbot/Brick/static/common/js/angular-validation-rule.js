(function() {
    angular.module('validation.rule', ['validation'])
        .config(['$validationProvider',
            function($validationProvider) {

                var reqFun = function(value) {
                        return !!value;
                    },
                    month = function( val ){
                        if( !val ) return false;
                        if( typeof val == 'object' ){
                            return true;
                        }else{
                            var reg = /^\d{4}-\d{1,2}$/;
                            return reg.test( val );
                        };
                    },
                    numReg = /^\d+$/;

                var expression = {
                    required: reqFun,
                    name: reqFun,
                    url: /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/,
                    email: /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/,
                    number: numReg,
                    phone: numReg,
                    username: reqFun,
                    password: reqFun,
                    old_password: reqFun,
                    newpassword: reqFun,
                    confirm_password: reqFun,
                    company_name: reqFun,
                    position_title: reqFun,
                    job_desc: reqFun,
                    start_time: month,
                    end_time: month,
                    school: reqFun,
                    project_name: reqFun,
                    title: reqFun,
                    jobDesc: reqFun
                };

                var defaultMsg = {
                    required: {
                        error: '这是必填项！'
                        //success: 'It\'s Required'
                    },
                    name: {
                        error: '姓名不能为空！'
                    },
                    url: {
                        error: 'url格式不正确！'
                    },
                    email: {
                        error: '邮件格式不正确！'
                    },
                    number: {
                        error: '格式应该为数字！'
                    },
                    phone: {
                        error: '手机格式不正确！'
                    },
                    username: {
                        error: '请输入关联账号！'
                    },
                    password: {
                        error: '请输入密码！'
                    },
                    old_password: {
                        error: '请输入当前密码！'
                    },
                    newpassword: {
                        error: '请输入新密码！'
                    },
                    confirm_password: {
                        error: '请确认新密码！'
                    },
                    company_name: {
                        error: '请输入公司名称！'
                    },
                    position_title: {
                        error: '请输入职位名称！'
                    },
                    job_desc: {
                        error: '请输入工作描述！'
                    },
                    start_time: {
                        error: '开始日期格式不对！'
                    },
                    end_time: {
                        error: '结束日期格式不对！'
                    },
                    school: {
                        error: '学校名称不能为空！'
                    },
                    project_name: {
                        error: '项目名称不能为空！'
                    },
                    title: {
                        error: '此项为必填项！'
                    },
                    jobDesc: {
                        error: '此项为必填项！'
                    }
                };

                $validationProvider.setExpression(expression).setDefaultMsg(defaultMsg);

            }
        ]);

}).call(this);
