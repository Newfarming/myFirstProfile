(function() {
    angular.module('validation.rule', ['validation'])
        .config([
            '$validationProvider',
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
                    array = function(value) {
                        return value === 0 ? false : true;
                    },
                    numReg = /^[0-9]*[1-9][0-9]*$/,
                    phoneReg = /(^(?:\+86)?(\d{3})\d{8}$)|(^0\d{2,3}\d{7,8}$)/,
                    qqFun = function(val) {
                        if (val) {
                            return numReg.test(val);
                        };
                        return true;
                    };

                var expression = {
                    required: reqFun,
                    name: reqFun,
                    gender: reqFun,
                    email: /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/,
                    number: numReg,
                    phone: phoneReg,
                    degree: reqFun,
                    company_name: reqFun,
                    position_title: reqFun,
                    job_desc: reqFun,
                    start_time: reqFun,
                    end_time: reqFun,
                    school: reqFun,
                    major: reqFun,
                    project_name: reqFun,
                    title: reqFun,
                    jobDesc: reqFun,
                    job_wish: reqFun,
                    last_contact: reqFun,
                    array: array,
                    qq: qqFun
                };

                var defaultMsg = {
                    required: {
                        error: '此项为必填项！'
                        //success: 'It\'s Required'
                    },
                    name: {
                        error: '姓名不能为空！'
                    },
                    gender: {
                        error: '请选择性别！'
                    },
                    email: {
                        error: '邮件格式不正确！'
                    },
                    number: {
                        error: '请输入正整数！'
                    },
                    salary: {
                        error: '薪资格式不正确！'
                    },
                    phone: {
                        error: '手机格式不正确！'
                    },
                    degree: {
                        error: '请选择最高学历！',
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
                        error: '请选择开始时间！'
                    },
                    end_time: {
                        error: '请选择结束时间！'
                    },
                    school: {
                        error: '学校名称不能为空！'
                    },
                    major: {
                        error: '专业名称不能为空！'
                    },
                    project_name: {
                        error: '项目名称不能为空！'
                    },
                    title: {
                        error: '此项为必填项！'
                    },
                    jobDesc: {
                        error: '此项为必填项！'
                    },
                    job_wish: {
                        error: '请选择求职意愿！'
                    },
                    last_contact: {
                        error: '请选择最近联系候选人时间！'
                    },
                    array: {
                        error: '请填写该经历！'
                    },
                    qq: {
                        error: 'qq格式不正确！'
                    }
                };

                $validationProvider.setExpression(expression).setDefaultMsg(defaultMsg);

            }
        ]);

}).call(this);
