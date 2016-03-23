    $("#url").on('blur', function() {
        var myurl = $("#url").prop('value');
        if (myurl != '' && !myurl.match(/^https?:\/\/(.*)$/i)) {
            $("#url").prop('value', 'http://' + myurl);
        }
    });

    var postData = {
        change_company_data: {
            company_name: '',
            url: ''
        },
        change_contact_data: {
            name: '',
            qq: ''
        },
        change_passwd_data: {
            old_password: '',
            new_password1: '',
            new_password2: ''
        },
        recv_data: {
            province: '',
            city: '',
            area: '',
            street: '',
            recv_phone: '',
            recv_name: ''
        }
    };

    var handleError = function(trg, data) {
        if (data.status == 'ok') {
            document.location.reload();
        } else {
            if (data.msg) {
                $(trg).parent().find('.pb-error-info').text(data.msg);
            } else {
                $(trg).parent().find('.pb-error-info').text('提交失败！');
            }
        }
    };

    //$(function() {

    //check input
    var isChgPasswd = false;
    //company_name
    var chkInput = function(id, postDataTrg, isSubInput, mustChk) {
        var myid = (id != undefined && typeof id == 'string') ? '#' + id : '';
        var mustChk = (mustChk != undefined) ? false : true;
        //是否是短的input 比如：省市区的input
        var isSubInput = (isSubInput != undefined) ? true : false;
        var errInfo = $(myid).attr('placeholder');
        if (mustChk && $.trim($(myid).val()) == "") {
            $(myid).addClass('pb-input-error');
            if (isSubInput) {
                $(myid).parent().parent().parent().find('.pb-error-info').text(errInfo);
            } else {
                $(myid).parent().parent().find('.pb-error-info').text(errInfo);
            }
            $(myid).focus();
            return false;
        } else {
            $(myid).removeClass('pb-input-error');
            if (isSubInput) {
                $(myid).parent().parent().parent().find('.pb-error-info').text('');
            } else {
                $(myid).parent().parent().find('.pb-error-info').text('');
            }
            postData[postDataTrg][id] = $.trim($(myid).val());
            return true;
        }
    };

    //blur event
    $('.pb-line>div>span>input').on('blur', function(e) {
        var id = $(this).attr('id');
        var postDataTrg = (id.match(/password/i)) ? 'change_passwd_data' : 'recv_data';
        if (id.match(/^(name|qq)$/i)) postDataTrg = 'change_contact_data';
        if (id.match(/^(company_name|url)$/i)) postDataTrg = 'change_company_data';

        if ($.trim($(this).val()) != "") {
            $(this).removeClass('pb-input-error');
            $(this).parent().parent().find('.pb-error-info').text('');
            postData[postDataTrg][id] = $.trim($(this).val());
        } else {
            var errInfo = $(this).attr('placeholder');
            $(this).addClass('pb-input-error');
            $(this).parent().parent().find('.pb-error-info').text(errInfo);
            //$(this).focus();
        }
    });
    //保存企业基本信息
    $('#btn-save-company').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        //console.log('#btn-save-company', 1);

        var company_name_ok = chkInput('company_name', 'change_company_data');
        if (!company_name_ok) return false;

        var url_ok = chkInput('url', 'change_company_data');
        if (!url_ok) return false;

        var newPostData = {};
        if (postData['change_company_data'].company_name) newPostData['company_name'] = postData['change_company_data'].company_name;
        if (postData['change_company_data'].url) newPostData['company_url'] = postData['change_company_data'].url;

        PB.request('post', '/users/change_company_info/', 'json', function(data) {
            //console.log('change_company', data);
            document.location.reload();
        }, function(data, status) {
            return false;
        }, newPostData, 'json');
    });

    //保存密码
    $('#btn-save-passwd').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var _this = this;
        //console.log('#btn-save-passwd', 1);

        var old_password_ok = chkInput('old_password', 'change_passwd_data');
        if (!old_password_ok) return false;

        var new_password1_ok = chkInput('new_password1', 'change_passwd_data');
        if (!new_password1_ok) return false;

        var new_password2_ok = chkInput('new_password2', 'change_passwd_data');
        if (!new_password2_ok) return false;

        var newPostData = {};
        if (postData['change_passwd_data'].old_password) newPostData['old_password'] = postData['change_passwd_data'].old_password;
        if (postData['change_passwd_data'].new_password1) newPostData['new_password'] = postData['change_passwd_data'].new_password1;
        if (postData['change_passwd_data'].new_password2) newPostData['confirm_password'] = postData['change_passwd_data'].new_password2;

        PB.request('post', '/users/change_my_pwd/', 'json', function(data) {
            //console.log('change_passwd', data);
            handleError(_this, data);
        }, function(data, status) {
            return false;
        }, newPostData, 'json');
    });

    //保存个人信息
    $('#btn-save-contact').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        ////console.log('#btn-save-contact', 1);

        var name_ok = chkInput('name', 'change_contact_data');
        if (!name_ok) return false;

        var qq_ok = chkInput('qq', 'change_contact_data');
        if (!qq_ok) return false;

        var newPostData = {};
        if (postData['change_contact_data'].name) newPostData['realname'] = postData['change_contact_data'].name;
        if (postData['change_contact_data'].qq) newPostData['qq'] = postData['change_contact_data'].qq;

        PB.request('post', '/users/change_my_info/', 'json', function(data) {
            //console.log('change_contact', data);
            document.location.reload();
        }, function(data, status) {
            return false;
        }, newPostData, 'json');
    });

    var $navs = $('.tab-nav a');
    var $tabs = $('.tab-content .tab');
    var timer;
    $navs.each(function(idx) {
        var $nav = $(this);
        $nav.on('click', function(e) {
            e.preventDefault();
            window.location.hash = $nav.attr('href')
            $('.tab-content .on').removeClass('on');
            $('.tab-nav .on').removeClass('on');
            $navs.eq(idx).addClass('on');
            $tabs.eq(idx).addClass('on');
        });
    });

    $('.profile-rss').find('li>a').on('click', function() {
        clearTimeout(timer);
        var $a = $(this);
        if ($a.hasClass('selected')) return false;
        $a.parents('ul').find('.selected').removeClass('selected');
        $a.addClass('selected');
        var selected = $a.data('selected');
        $('.selected-tip').remove();
        timer = setTimeout(function() {
            $.post('/feed/modify_frequency', {
                frequency: selected
            }, function(ret) {
                if (ret.status == 'success') {
                    var tip = $('<p class="selected-tip">设置成功！</p>').appendTo($a.parent());
                    tip.fadeOut(2000, function() {
                        tip.remove();
                    });
                }
            });
        }, 1000);
        return false;
    });
    /*var hash = window.location.hash;
    if (!hash) return false;
    if (/^(#pwd|#rss)$/.test(hash)) {
        $('a[href="' + hash + '"]').click();
    }*/
    //});


    //收货地址 icon-pen
    var pbCurrentSelectClass = '';
    var goodsReceiptModal = function() {
        var provinceList = [];
        /*var provinceList = [{
            "f_id": "3763",
            "f_name": "\u5317\u4eac"
        }, {
            "f_id": "3764",
            "f_name": "\u4e0a\u6d77"
        }, {
            "f_id": "3765",
            "f_name": "\u5929\u6d25"
        }, {
            "f_id": "3766",
            "f_name": "\u91cd\u5e86"
        }, {
            "f_id": "4",
            "f_name": "\u6cb3\u5317\u7701"
        }, {
            "f_id": "5",
            "f_name": "\u5c71\u897f\u7701"
        }, {
            "f_id": "16",
            "f_name": "\u6cb3\u5357\u7701"
        }, {
            "f_id": "7",
            "f_name": "\u8fbd\u5b81\u7701"
        }, {
            "f_id": "8",
            "f_name": "\u5409\u6797\u7701"
        }, {
            "f_id": "9",
            "f_name": "\u9ed1\u9f99\u6c5f\u7701"
        }, {
            "f_id": "6",
            "f_name": "\u5185\u8499\u53e4"
        }, {
            "f_id": "10",
            "f_name": "\u6c5f\u82cf\u7701"
        }, {
            "f_id": "15",
            "f_name": "\u5c71\u4e1c\u7701"
        }, {
            "f_id": "12",
            "f_name": "\u5b89\u5fbd\u7701"
        }, {
            "f_id": "11",
            "f_name": "\u6d59\u6c5f\u7701"
        }, {
            "f_id": "13",
            "f_name": "\u798f\u5efa\u7701"
        }, {
            "f_id": "17",
            "f_name": "\u6e56\u5317\u7701"
        }, {
            "f_id": "18",
            "f_name": "\u6e56\u5357\u7701"
        }, {
            "f_id": "19",
            "f_name": "\u5e7f\u4e1c\u7701"
        }, {
            "f_id": "20",
            "f_name": "\u5e7f\u897f\u7701"
        }, {
            "f_id": "14",
            "f_name": "\u6c5f\u897f\u7701"
        }, {
            "f_id": "21",
            "f_name": "\u6d77\u5357\u7701"
        }, {
            "f_id": "23",
            "f_name": "\u56db\u5ddd\u7701"
        }, {
            "f_id": "24",
            "f_name": "\u8d35\u5dde\u7701"
        }, {
            "f_id": "25",
            "f_name": "\u4e91\u5357\u7701"
        }, {
            "f_id": "26",
            "f_name": "\u897f\u85cf"
        }, {
            "f_id": "27",
            "f_name": "\u9655\u897f\u7701"
        }, {
            "f_id": "28",
            "f_name": "\u7518\u8083\u7701"
        }, {
            "f_id": "29",
            "f_name": "\u9752\u6d77\u7701"
        }, {
            "f_id": "30",
            "f_name": "\u5b81\u590f"
        }, {
            "f_id": "31",
            "f_name": "\u65b0\u7586"
        }];*/
        var getCities = function() {
            return {};
            /*return {
                "3763": [{
                    "f_id": "1",
                    "f_name": "\u5317\u4eac\u5e02"
                }],
                "3764": [{
                    "f_id": "2",
                    "f_name": "\u4e0a\u6d77\u5e02"
                }],
                "3765": [{
                    "f_id": "3",
                    "f_name": "\u5929\u6d25\u5e02"
                }],
                "3766": [{
                    "f_id": "22",
                    "f_name": "\u91cd\u5e86\u5e02"
                }],
                "4": [{
                    "f_id": "90",
                    "f_name": "\u77f3\u5bb6\u5e84\u5e02"
                }, {
                    "f_id": "93",
                    "f_name": "\u90af\u90f8\u5e02"
                }, {
                    "f_id": "94",
                    "f_name": "\u90a2\u53f0\u5e02"
                }, {
                    "f_id": "95",
                    "f_name": "\u4fdd\u5b9a\u5e02"
                }, {
                    "f_id": "96",
                    "f_name": "\u5f20\u5bb6\u53e3\u5e02"
                }, {
                    "f_id": "97",
                    "f_name": "\u627f\u5fb7\u5e02"
                }, {
                    "f_id": "92",
                    "f_name": "\u79e6\u7687\u5c9b\u5e02"
                }, {
                    "f_id": "91",
                    "f_name": "\u5510\u5c71\u5e02"
                }, {
                    "f_id": "686",
                    "f_name": "\u6ca7\u5dde\u5e02"
                }, {
                    "f_id": "98",
                    "f_name": "\u5eca\u574a\u5e02"
                }, {
                    "f_id": "99",
                    "f_name": "\u8861\u6c34\u5e02"
                }],
                "5": [{
                    "f_id": "100",
                    "f_name": "\u592a\u539f\u5e02"
                }, {
                    "f_id": "101",
                    "f_name": "\u5927\u540c\u5e02"
                }, {
                    "f_id": "102",
                    "f_name": "\u9633\u6cc9\u5e02"
                }, {
                    "f_id": "104",
                    "f_name": "\u664b\u57ce\u5e02"
                }, {
                    "f_id": "105",
                    "f_name": "\u6714\u5dde\u5e02"
                }, {
                    "f_id": "106",
                    "f_name": "\u664b\u4e2d\u5e02"
                }, {
                    "f_id": "108",
                    "f_name": "\u5ffb\u5dde\u5e02"
                }, {
                    "f_id": "110",
                    "f_name": "\u5415\u6881\u5e02"
                }, {
                    "f_id": "109",
                    "f_name": "\u4e34\u6c7e\u5e02"
                }, {
                    "f_id": "107",
                    "f_name": "\u8fd0\u57ce\u5e02"
                }, {
                    "f_id": "103",
                    "f_name": "\u957f\u6cbb\u5e02"
                }],
                "16": [{
                    "f_id": "237",
                    "f_name": "\u90d1\u5dde\u5e02"
                }, {
                    "f_id": "238",
                    "f_name": "\u5f00\u5c01\u5e02"
                }, {
                    "f_id": "239",
                    "f_name": "\u6d1b\u9633\u5e02"
                }, {
                    "f_id": "240",
                    "f_name": "\u5e73\u9876\u5c71\u5e02"
                }, {
                    "f_id": "244",
                    "f_name": "\u7126\u4f5c\u5e02"
                }, {
                    "f_id": "242",
                    "f_name": "\u9e64\u58c1\u5e02"
                }, {
                    "f_id": "243",
                    "f_name": "\u65b0\u4e61\u5e02"
                }, {
                    "f_id": "241",
                    "f_name": "\u5b89\u9633\u5e02"
                }, {
                    "f_id": "245",
                    "f_name": "\u6fee\u9633\u5e02"
                }, {
                    "f_id": "246",
                    "f_name": "\u8bb8\u660c\u5e02"
                }, {
                    "f_id": "247",
                    "f_name": "\u6f2f\u6cb3\u5e02"
                }, {
                    "f_id": "248",
                    "f_name": "\u4e09\u95e8\u5ce1\u5e02"
                }, {
                    "f_id": "249",
                    "f_name": "\u5357\u9633\u5e02"
                }, {
                    "f_id": "250",
                    "f_name": "\u5546\u4e18\u5e02"
                }, {
                    "f_id": "252",
                    "f_name": "\u5468\u53e3\u5e02"
                }, {
                    "f_id": "253",
                    "f_name": "\u9a7b\u9a6c\u5e97\u5e02"
                }, {
                    "f_id": "251",
                    "f_name": "\u4fe1\u9633\u5e02"
                }],
                "7": [{
                    "f_id": "123",
                    "f_name": "\u6c88\u9633\u5e02"
                }, {
                    "f_id": "124",
                    "f_name": "\u5927\u8fde\u5e02"
                }, {
                    "f_id": "125",
                    "f_name": "\u978d\u5c71\u5e02"
                }, {
                    "f_id": "126",
                    "f_name": "\u629a\u987a\u5e02"
                }, {
                    "f_id": "127",
                    "f_name": "\u672c\u6eaa\u5e02"
                }, {
                    "f_id": "128",
                    "f_name": "\u4e39\u4e1c\u5e02"
                }, {
                    "f_id": "129",
                    "f_name": "\u9526\u5dde\u5e02"
                }, {
                    "f_id": "136",
                    "f_name": "\u846b\u82a6\u5c9b\u5e02"
                }, {
                    "f_id": "130",
                    "f_name": "\u8425\u53e3\u5e02"
                }, {
                    "f_id": "133",
                    "f_name": "\u76d8\u9526\u5e02"
                }, {
                    "f_id": "131",
                    "f_name": "\u961c\u65b0\u5e02"
                }, {
                    "f_id": "132",
                    "f_name": "\u8fbd\u9633\u5e02"
                }, {
                    "f_id": "135",
                    "f_name": "\u671d\u9633\u5e02"
                }, {
                    "f_id": "134",
                    "f_name": "\u94c1\u5cad\u5e02"
                }],
                "8": [{
                    "f_id": "137",
                    "f_name": "\u957f\u6625\u5e02"
                }, {
                    "f_id": "138",
                    "f_name": "\u5409\u6797\u5e02"
                }, {
                    "f_id": "139",
                    "f_name": "\u56db\u5e73\u5e02"
                }, {
                    "f_id": "141",
                    "f_name": "\u901a\u5316\u5e02"
                }, {
                    "f_id": "142",
                    "f_name": "\u767d\u5c71\u5e02"
                }, {
                    "f_id": "143",
                    "f_name": "\u677e\u539f\u5e02"
                }, {
                    "f_id": "144",
                    "f_name": "\u767d\u57ce\u5e02"
                }, {
                    "f_id": "145",
                    "f_name": "\u5ef6\u8fb9\u671d\u9c9c\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "140",
                    "f_name": "\u8fbd\u6e90\u5e02"
                }],
                "9": [{
                    "f_id": "146",
                    "f_name": "\u54c8\u5c14\u6ee8\u5e02"
                }, {
                    "f_id": "147",
                    "f_name": "\u9f50\u9f50\u54c8\u5c14\u5e02"
                }, {
                    "f_id": "149",
                    "f_name": "\u9e64\u5c97\u5e02"
                }, {
                    "f_id": "150",
                    "f_name": "\u53cc\u9e2d\u5c71\u5e02"
                }, {
                    "f_id": "148",
                    "f_name": "\u9e21\u897f\u5e02"
                }, {
                    "f_id": "151",
                    "f_name": "\u5927\u5e86\u5e02"
                }, {
                    "f_id": "152",
                    "f_name": "\u4f0a\u6625\u5e02"
                }, {
                    "f_id": "155",
                    "f_name": "\u7261\u4e39\u6c5f\u5e02"
                }, {
                    "f_id": "153",
                    "f_name": "\u4f73\u6728\u65af\u5e02"
                }, {
                    "f_id": "154",
                    "f_name": "\u4e03\u53f0\u6cb3\u5e02"
                }, {
                    "f_id": "156",
                    "f_name": "\u9ed1\u6cb3\u5e02"
                }, {
                    "f_id": "157",
                    "f_name": "\u7ee5\u5316\u5e02"
                }, {
                    "f_id": "158",
                    "f_name": "\u5927\u5174\u5b89\u5cad\u5e02"
                }],
                "6": [{
                    "f_id": "111",
                    "f_name": "\u547c\u548c\u6d69\u7279\u5e02"
                }, {
                    "f_id": "112",
                    "f_name": "\u5305\u5934\u5e02"
                }, {
                    "f_id": "113",
                    "f_name": "\u4e4c\u6d77\u5e02"
                }, {
                    "f_id": "114",
                    "f_name": "\u8d64\u5cf0\u5e02"
                }, {
                    "f_id": "119",
                    "f_name": "\u4e4c\u5170\u5bdf\u5e03\u5e02"
                }, {
                    "f_id": "121",
                    "f_name": "\u9521\u6797\u90ed\u52d2\u76df"
                }, {
                    "f_id": "117",
                    "f_name": "\u547c\u4f26\u8d1d\u5c14\u5e02"
                }, {
                    "f_id": "116",
                    "f_name": "\u9102\u5c14\u591a\u65af\u5e02"
                }, {
                    "f_id": "118",
                    "f_name": "\u5df4\u5f66\u6dd6\u5c14\u5e02"
                }, {
                    "f_id": "122",
                    "f_name": "\u963f\u62c9\u5584\u76df"
                }, {
                    "f_id": "120",
                    "f_name": "\u5174\u5b89\u76df"
                }, {
                    "f_id": "115",
                    "f_name": "\u901a\u8fbd\u5e02"
                }],
                "10": [{
                    "f_id": "159",
                    "f_name": "\u5357\u4eac\u5e02"
                }, {
                    "f_id": "161",
                    "f_name": "\u5f90\u5dde\u5e02"
                }, {
                    "f_id": "165",
                    "f_name": "\u8fde\u4e91\u6e2f\u5e02"
                }, {
                    "f_id": "166",
                    "f_name": "\u6dee\u5b89\u5e02"
                }, {
                    "f_id": "171",
                    "f_name": "\u5bbf\u8fc1\u5e02"
                }, {
                    "f_id": "167",
                    "f_name": "\u76d0\u57ce\u5e02"
                }, {
                    "f_id": "168",
                    "f_name": "\u626c\u5dde\u5e02"
                }, {
                    "f_id": "170",
                    "f_name": "\u6cf0\u5dde\u5e02"
                }, {
                    "f_id": "164",
                    "f_name": "\u5357\u901a\u5e02"
                }, {
                    "f_id": "169",
                    "f_name": "\u9547\u6c5f\u5e02"
                }, {
                    "f_id": "162",
                    "f_name": "\u5e38\u5dde\u5e02"
                }, {
                    "f_id": "160",
                    "f_name": "\u65e0\u9521\u5e02"
                }, {
                    "f_id": "163",
                    "f_name": "\u82cf\u5dde\u5e02"
                }],
                "15": [{
                    "f_id": "220",
                    "f_name": "\u6d4e\u5357\u5e02"
                }, {
                    "f_id": "221",
                    "f_name": "\u9752\u5c9b\u5e02"
                }, {
                    "f_id": "222",
                    "f_name": "\u6dc4\u535a\u5e02"
                }, {
                    "f_id": "223",
                    "f_name": "\u67a3\u5e84\u5e02"
                }, {
                    "f_id": "224",
                    "f_name": "\u4e1c\u8425\u5e02"
                }, {
                    "f_id": "226",
                    "f_name": "\u6f4d\u574a\u5e02"
                }, {
                    "f_id": "225",
                    "f_name": "\u70df\u53f0\u5e02"
                }, {
                    "f_id": "229",
                    "f_name": "\u5a01\u6d77\u5e02"
                }, {
                    "f_id": "231",
                    "f_name": "\u83b1\u829c\u5e02"
                }, {
                    "f_id": "233",
                    "f_name": "\u5fb7\u5dde\u5e02"
                }, {
                    "f_id": "232",
                    "f_name": "\u4e34\u6c82\u5e02"
                }, {
                    "f_id": "234",
                    "f_name": "\u804a\u57ce\u5e02"
                }, {
                    "f_id": "235",
                    "f_name": "\u6ee8\u5dde\u5e02"
                }, {
                    "f_id": "236",
                    "f_name": "\u83cf\u6cfd\u5e02"
                }, {
                    "f_id": "230",
                    "f_name": "\u65e5\u7167\u5e02"
                }, {
                    "f_id": "228",
                    "f_name": "\u6cf0\u5b89\u5e02"
                }, {
                    "f_id": "227",
                    "f_name": "\u6d4e\u5b81\u5e02"
                }],
                "12": [{
                    "f_id": "189",
                    "f_name": "\u94dc\u9675\u5e02"
                }, {
                    "f_id": "183",
                    "f_name": "\u5408\u80a5\u5e02"
                }, {
                    "f_id": "186",
                    "f_name": "\u6dee\u5357\u5e02"
                }, {
                    "f_id": "188",
                    "f_name": "\u6dee\u5317\u5e02"
                }, {
                    "f_id": "184",
                    "f_name": "\u829c\u6e56\u5e02"
                }, {
                    "f_id": "185",
                    "f_name": "\u868c\u57e0\u5e02"
                }, {
                    "f_id": "187",
                    "f_name": "\u9a6c\u978d\u5c71\u5e02"
                }, {
                    "f_id": "190",
                    "f_name": "\u5b89\u5e86\u5e02"
                }, {
                    "f_id": "191",
                    "f_name": "\u9ec4\u5c71\u5e02"
                }, {
                    "f_id": "192",
                    "f_name": "\u6ec1\u5dde\u5e02"
                }, {
                    "f_id": "193",
                    "f_name": "\u961c\u9633\u5e02"
                }, {
                    "f_id": "197",
                    "f_name": "\u4eb3\u5dde\u5e02"
                }, {
                    "f_id": "194",
                    "f_name": "\u5bbf\u5dde\u5e02"
                }, {
                    "f_id": "198",
                    "f_name": "\u6c60\u5dde\u5e02"
                }, {
                    "f_id": "196",
                    "f_name": "\u516d\u5b89\u5e02"
                }, {
                    "f_id": "199",
                    "f_name": "\u5ba3\u57ce\u5e02"
                }, {
                    "f_id": "195",
                    "f_name": "\u5de2\u6e56\u5e02"
                }],
                "11": [{
                    "f_id": "173",
                    "f_name": "\u5b81\u6ce2\u5e02"
                }, {
                    "f_id": "172",
                    "f_name": "\u676d\u5dde\u5e02"
                }, {
                    "f_id": "174",
                    "f_name": "\u6e29\u5dde\u5e02"
                }, {
                    "f_id": "175",
                    "f_name": "\u5609\u5174\u5e02"
                }, {
                    "f_id": "176",
                    "f_name": "\u6e56\u5dde\u5e02"
                }, {
                    "f_id": "177",
                    "f_name": "\u7ecd\u5174\u5e02"
                }, {
                    "f_id": "178",
                    "f_name": "\u91d1\u534e\u5e02"
                }, {
                    "f_id": "179",
                    "f_name": "\u8862\u5dde\u5e02"
                }, {
                    "f_id": "182",
                    "f_name": "\u4e3d\u6c34\u5e02"
                }, {
                    "f_id": "181",
                    "f_name": "\u53f0\u5dde\u5e02"
                }, {
                    "f_id": "180",
                    "f_name": "\u821f\u5c71\u5e02"
                }],
                "13": [{
                    "f_id": "200",
                    "f_name": "\u798f\u5dde\u5e02"
                }, {
                    "f_id": "201",
                    "f_name": "\u53a6\u95e8\u5e02"
                }, {
                    "f_id": "203",
                    "f_name": "\u4e09\u660e\u5e02"
                }, {
                    "f_id": "202",
                    "f_name": "\u8386\u7530\u5e02"
                }, {
                    "f_id": "204",
                    "f_name": "\u6cc9\u5dde\u5e02"
                }, {
                    "f_id": "205",
                    "f_name": "\u6f33\u5dde\u5e02"
                }, {
                    "f_id": "206",
                    "f_name": "\u5357\u5e73\u5e02"
                }, {
                    "f_id": "207",
                    "f_name": "\u9f99\u5ca9\u5e02"
                }, {
                    "f_id": "208",
                    "f_name": "\u5b81\u5fb7\u5e02"
                }],
                "17": [{
                    "f_id": "254",
                    "f_name": "\u6b66\u6c49\u5e02"
                }, {
                    "f_id": "255",
                    "f_name": "\u9ec4\u77f3\u5e02"
                }, {
                    "f_id": "2058",
                    "f_name": "\u8944\u9633\u5e02"
                }, {
                    "f_id": "256",
                    "f_name": "\u5341\u5830\u5e02"
                }, {
                    "f_id": "261",
                    "f_name": "\u8346\u5dde\u5e02"
                }, {
                    "f_id": "257",
                    "f_name": "\u5b9c\u660c\u5e02"
                }, {
                    "f_id": "260",
                    "f_name": "\u5b5d\u611f\u5e02"
                }, {
                    "f_id": "262",
                    "f_name": "\u9ec4\u5188\u5e02"
                }, {
                    "f_id": "263",
                    "f_name": "\u54b8\u5b81\u5e02"
                }, {
                    "f_id": "265",
                    "f_name": "\u6069\u65bd\u571f\u5bb6\u65cf\u82d7\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "258",
                    "f_name": "\u9102\u5dde\u5e02"
                }, {
                    "f_id": "259",
                    "f_name": "\u8346\u95e8\u5e02"
                }, {
                    "f_id": "264",
                    "f_name": "\u968f\u5dde\u5e02"
                }, {
                    "f_id": "267",
                    "f_name": "\u6f5c\u6c5f\u5e02"
                }, {
                    "f_id": "268",
                    "f_name": "\u5929\u95e8\u5e02"
                }, {
                    "f_id": "266",
                    "f_name": "\u4ed9\u6843\u5e02"
                }, {
                    "f_id": "269",
                    "f_name": "\u795e\u519c\u67b6"
                }],
                "18": [{
                    "f_id": "270",
                    "f_name": "\u957f\u6c99\u5e02"
                }, {
                    "f_id": "271",
                    "f_name": "\u682a\u6d32\u5e02"
                }, {
                    "f_id": "272",
                    "f_name": "\u6e58\u6f6d\u5e02"
                }, {
                    "f_id": "273",
                    "f_name": "\u8861\u9633\u5e02"
                }, {
                    "f_id": "274",
                    "f_name": "\u90b5\u9633\u5e02"
                }, {
                    "f_id": "275",
                    "f_name": "\u5cb3\u9633\u5e02"
                }, {
                    "f_id": "276",
                    "f_name": "\u5e38\u5fb7\u5e02"
                }, {
                    "f_id": "277",
                    "f_name": "\u5f20\u5bb6\u754c\u5e02"
                }, {
                    "f_id": "279",
                    "f_name": "\u90f4\u5dde\u5e02"
                }, {
                    "f_id": "278",
                    "f_name": "\u76ca\u9633\u5e02"
                }, {
                    "f_id": "280",
                    "f_name": "\u6c38\u5dde\u5e02"
                }, {
                    "f_id": "281",
                    "f_name": "\u6000\u5316\u5e02"
                }, {
                    "f_id": "282",
                    "f_name": "\u5a04\u5e95\u5e02"
                }, {
                    "f_id": "283",
                    "f_name": "\u6e58\u897f\u571f\u5bb6\u65cf\u82d7\u65cf\u81ea\u6cbb\u5dde"
                }],
                "19": [{
                    "f_id": "284",
                    "f_name": "\u5e7f\u5dde\u5e02"
                }, {
                    "f_id": "286",
                    "f_name": "\u6df1\u5733\u5e02"
                }, {
                    "f_id": "287",
                    "f_name": "\u73e0\u6d77\u5e02"
                }, {
                    "f_id": "288",
                    "f_name": "\u6c55\u5934\u5e02"
                }, {
                    "f_id": "285",
                    "f_name": "\u97f6\u5173\u5e02"
                }, {
                    "f_id": "297",
                    "f_name": "\u6cb3\u6e90\u5e02"
                }, {
                    "f_id": "295",
                    "f_name": "\u6885\u5dde\u5e02"
                }, {
                    "f_id": "294",
                    "f_name": "\u60e0\u5dde\u5e02"
                }, {
                    "f_id": "296",
                    "f_name": "\u6c55\u5c3e\u5e02"
                }, {
                    "f_id": "300",
                    "f_name": "\u4e1c\u839e\u5e02"
                }, {
                    "f_id": "301",
                    "f_name": "\u4e2d\u5c71\u5e02"
                }, {
                    "f_id": "290",
                    "f_name": "\u6c5f\u95e8\u5e02"
                }, {
                    "f_id": "289",
                    "f_name": "\u4f5b\u5c71\u5e02"
                }, {
                    "f_id": "298",
                    "f_name": "\u9633\u6c5f\u5e02"
                }, {
                    "f_id": "291",
                    "f_name": "\u6e5b\u6c5f\u5e02"
                }, {
                    "f_id": "292",
                    "f_name": "\u8302\u540d\u5e02"
                }, {
                    "f_id": "293",
                    "f_name": "\u8087\u5e86\u5e02"
                }, {
                    "f_id": "304",
                    "f_name": "\u4e91\u6d6e\u5e02"
                }, {
                    "f_id": "299",
                    "f_name": "\u6e05\u8fdc\u5e02"
                }, {
                    "f_id": "302",
                    "f_name": "\u6f6e\u5dde\u5e02"
                }, {
                    "f_id": "303",
                    "f_name": "\u63ed\u9633\u5e02"
                }],
                "20": [{
                    "f_id": "305",
                    "f_name": "\u5357\u5b81\u5e02"
                }, {
                    "f_id": "306",
                    "f_name": "\u67f3\u5dde\u5e02"
                }, {
                    "f_id": "307",
                    "f_name": "\u6842\u6797\u5e02"
                }, {
                    "f_id": "308",
                    "f_name": "\u68a7\u5dde\u5e02"
                }, {
                    "f_id": "309",
                    "f_name": "\u5317\u6d77\u5e02"
                }, {
                    "f_id": "310",
                    "f_name": "\u9632\u57ce\u6e2f\u5e02"
                }, {
                    "f_id": "311",
                    "f_name": "\u94a6\u5dde\u5e02"
                }, {
                    "f_id": "312",
                    "f_name": "\u8d35\u6e2f\u5e02"
                }, {
                    "f_id": "313",
                    "f_name": "\u7389\u6797\u5e02"
                }, {
                    "f_id": "315",
                    "f_name": "\u8d3a\u5dde\u5e02"
                }, {
                    "f_id": "314",
                    "f_name": "\u767e\u8272\u5e02"
                }, {
                    "f_id": "316",
                    "f_name": "\u6cb3\u6c60\u5e02"
                }, {
                    "f_id": "317",
                    "f_name": "\u6765\u5bbe\u5e02"
                }, {
                    "f_id": "318",
                    "f_name": "\u5d07\u5de6\u5e02"
                }],
                "14": [{
                    "f_id": "209",
                    "f_name": "\u5357\u660c\u5e02"
                }, {
                    "f_id": "210",
                    "f_name": "\u666f\u5fb7\u9547\u5e02"
                }, {
                    "f_id": "211",
                    "f_name": "\u840d\u4e61\u5e02"
                }, {
                    "f_id": "213",
                    "f_name": "\u65b0\u4f59\u5e02"
                }, {
                    "f_id": "212",
                    "f_name": "\u4e5d\u6c5f\u5e02"
                }, {
                    "f_id": "214",
                    "f_name": "\u9e70\u6f6d\u5e02"
                }, {
                    "f_id": "219",
                    "f_name": "\u4e0a\u9976\u5e02"
                }, {
                    "f_id": "217",
                    "f_name": "\u5b9c\u6625\u5e02"
                }, {
                    "f_id": "218",
                    "f_name": "\u629a\u5dde\u5e02"
                }, {
                    "f_id": "216",
                    "f_name": "\u5409\u5b89\u5e02"
                }, {
                    "f_id": "215",
                    "f_name": "\u8d63\u5dde\u5e02"
                }],
                "23": [{
                    "f_id": "380",
                    "f_name": "\u6210\u90fd\u5e02"
                }, {
                    "f_id": "381",
                    "f_name": "\u81ea\u8d21\u5e02"
                }, {
                    "f_id": "382",
                    "f_name": "\u6500\u679d\u82b1\u5e02"
                }, {
                    "f_id": "383",
                    "f_name": "\u6cf8\u5dde\u5e02"
                }, {
                    "f_id": "385",
                    "f_name": "\u7ef5\u9633\u5e02"
                }, {
                    "f_id": "384",
                    "f_name": "\u5fb7\u9633\u5e02"
                }, {
                    "f_id": "386",
                    "f_name": "\u5e7f\u5143\u5e02"
                }, {
                    "f_id": "387",
                    "f_name": "\u9042\u5b81\u5e02"
                }, {
                    "f_id": "388",
                    "f_name": "\u5185\u6c5f\u5e02"
                }, {
                    "f_id": "389",
                    "f_name": "\u4e50\u5c71\u5e02"
                }, {
                    "f_id": "392",
                    "f_name": "\u5b9c\u5bbe\u5e02"
                }, {
                    "f_id": "393",
                    "f_name": "\u5e7f\u5b89\u5e02"
                }, {
                    "f_id": "390",
                    "f_name": "\u5357\u5145\u5e02"
                }, {
                    "f_id": "394",
                    "f_name": "\u8fbe\u5dde\u5e02"
                }, {
                    "f_id": "396",
                    "f_name": "\u5df4\u4e2d\u5e02"
                }, {
                    "f_id": "395",
                    "f_name": "\u96c5\u5b89\u5e02"
                }, {
                    "f_id": "391",
                    "f_name": "\u7709\u5c71\u5e02"
                }, {
                    "f_id": "397",
                    "f_name": "\u8d44\u9633\u5e02"
                }, {
                    "f_id": "398",
                    "f_name": "\u963f\u575d\u5dde"
                }, {
                    "f_id": "399",
                    "f_name": "\u7518\u5b5c\u5dde"
                }, {
                    "f_id": "400",
                    "f_name": "\u51c9\u5c71\u5dde"
                }],
                "21": [{
                    "f_id": "319",
                    "f_name": "\u6d77\u53e3\u5e02"
                }, {
                    "f_id": "323",
                    "f_name": "\u510b\u5dde\u5e02"
                }, {
                    "f_id": "322",
                    "f_name": "\u743c\u6d77\u5e02"
                }, {
                    "f_id": "325",
                    "f_name": "\u4e07\u5b81\u5e02"
                }, {
                    "f_id": "326",
                    "f_name": "\u4e1c\u65b9\u5e02"
                }, {
                    "f_id": "320",
                    "f_name": "\u4e09\u4e9a\u5e02"
                }, {
                    "f_id": "324",
                    "f_name": "\u6587\u660c\u5e02"
                }, {
                    "f_id": "321",
                    "f_name": "\u4e94\u6307\u5c71\u5e02"
                }, {
                    "f_id": "330",
                    "f_name": "\u4e34\u9ad8\u53bf"
                }, {
                    "f_id": "329",
                    "f_name": "\u6f84\u8fc8\u53bf"
                }, {
                    "f_id": "327",
                    "f_name": "\u5b9a\u5b89\u53bf"
                }, {
                    "f_id": "328",
                    "f_name": "\u5c6f\u660c\u53bf"
                }, {
                    "f_id": "332",
                    "f_name": "\u660c\u6c5f\u53bf"
                }, {
                    "f_id": "331",
                    "f_name": "\u767d\u6c99\u53bf"
                }, {
                    "f_id": "336",
                    "f_name": "\u743c\u4e2d\u53bf"
                }, {
                    "f_id": "334",
                    "f_name": "\u9675\u6c34\u53bf"
                }, {
                    "f_id": "335",
                    "f_name": "\u4fdd\u4ead\u53bf"
                }, {
                    "f_id": "333",
                    "f_name": "\u4e50\u4e1c\u53bf"
                }, {
                    "f_id": "3783",
                    "f_name": "\u4e09\u6c99\u5e02"
                }, {
                    "f_id": "337",
                    "f_name": "\u897f\u6c99\u7fa4\u5c9b"
                }, {
                    "f_id": "338",
                    "f_name": "\u5357\u6c99\u7fa4\u5c9b"
                }, {
                    "f_id": "339",
                    "f_name": "\u4e2d\u6c99\u7fa4\u5c9b"
                }],
                "24": [{
                    "f_id": "401",
                    "f_name": "\u8d35\u9633\u5e02"
                }, {
                    "f_id": "402",
                    "f_name": "\u516d\u76d8\u6c34\u5e02"
                }, {
                    "f_id": "403",
                    "f_name": "\u9075\u4e49\u5e02"
                }, {
                    "f_id": "405",
                    "f_name": "\u94dc\u4ec1\u5e02"
                }, {
                    "f_id": "407",
                    "f_name": "\u6bd5\u8282\u5e02"
                }, {
                    "f_id": "404",
                    "f_name": "\u5b89\u987a\u5e02"
                }, {
                    "f_id": "406",
                    "f_name": "\u9ed4\u897f\u5357\u5dde"
                }, {
                    "f_id": "408",
                    "f_name": "\u9ed4\u4e1c\u5357\u5dde"
                }, {
                    "f_id": "409",
                    "f_name": "\u9ed4\u5357\u5dde"
                }],
                "25": [{
                    "f_id": "410",
                    "f_name": "\u6606\u660e\u5e02"
                }, {
                    "f_id": "411",
                    "f_name": "\u66f2\u9756\u5e02"
                }, {
                    "f_id": "412",
                    "f_name": "\u7389\u6eaa\u5e02"
                }, {
                    "f_id": "414",
                    "f_name": "\u662d\u901a\u5e02"
                }, {
                    "f_id": "416",
                    "f_name": "\u666e\u6d31\u5e02"
                }, {
                    "f_id": "417",
                    "f_name": "\u4e34\u6ca7\u5e02"
                }, {
                    "f_id": "413",
                    "f_name": "\u4fdd\u5c71\u5e02"
                }, {
                    "f_id": "415",
                    "f_name": "\u4e3d\u6c5f\u5e02"
                }, {
                    "f_id": "420",
                    "f_name": "\u6587\u5c71\u5dde"
                }, {
                    "f_id": "419",
                    "f_name": "\u7ea2\u6cb3\u5dde"
                }, {
                    "f_id": "421",
                    "f_name": "\u897f\u53cc\u7248\u7eb3\u5dde"
                }, {
                    "f_id": "418",
                    "f_name": "\u695a\u96c4\u5e02"
                }, {
                    "f_id": "422",
                    "f_name": "\u5927\u7406\u767d\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "2896",
                    "f_name": "\u5fb7\u5b8f\u5dde"
                }, {
                    "f_id": "423",
                    "f_name": "\u6012\u6c5f\u5088\u50f3\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "424",
                    "f_name": "\u8fea\u5e86\u85cf\u65cf\u81ea\u6cbb\u5dde"
                }],
                "26": [{
                    "f_id": "425",
                    "f_name": "\u62c9\u8428\u5e02"
                }, {
                    "f_id": "429",
                    "f_name": "\u90a3\u66f2\u5e02"
                }, {
                    "f_id": "427",
                    "f_name": "\u5c71\u5357\u5e02"
                }, {
                    "f_id": "426",
                    "f_name": "\u660c\u90fd\u5e02"
                }, {
                    "f_id": "428",
                    "f_name": "\u65e5\u5580\u5219\u5e02"
                }, {
                    "f_id": "430",
                    "f_name": "\u963f\u91cc\u5e02"
                }, {
                    "f_id": "431",
                    "f_name": "\u6797\u829d\u5e02"
                }],
                "27": [{
                    "f_id": "432",
                    "f_name": "\u897f\u5b89\u5e02"
                }, {
                    "f_id": "433",
                    "f_name": "\u94dc\u5ddd\u5e02"
                }, {
                    "f_id": "434",
                    "f_name": "\u5b9d\u9e21\u5e02"
                }, {
                    "f_id": "435",
                    "f_name": "\u54b8\u9633\u5e02"
                }, {
                    "f_id": "436",
                    "f_name": "\u6e2d\u5357\u5e02"
                }, {
                    "f_id": "437",
                    "f_name": "\u5ef6\u5b89\u5e02"
                }, {
                    "f_id": "438",
                    "f_name": "\u6c49\u4e2d\u5e02"
                }, {
                    "f_id": "439",
                    "f_name": "\u6986\u6797\u5e02"
                }, {
                    "f_id": "441",
                    "f_name": "\u5546\u6d1b\u5e02"
                }, {
                    "f_id": "440",
                    "f_name": "\u5b89\u5eb7\u5e02"
                }],
                "28": [{
                    "f_id": "442",
                    "f_name": "\u5170\u5dde\u5e02"
                }, {
                    "f_id": "444",
                    "f_name": "\u91d1\u660c\u5e02"
                }, {
                    "f_id": "445",
                    "f_name": "\u767d\u94f6\u5e02"
                }, {
                    "f_id": "446",
                    "f_name": "\u5929\u6c34\u5e02"
                }, {
                    "f_id": "443",
                    "f_name": "\u5609\u5cea\u5173\u5e02"
                }, {
                    "f_id": "449",
                    "f_name": "\u5e73\u51c9\u5e02"
                }, {
                    "f_id": "451",
                    "f_name": "\u5e86\u9633\u5e02"
                }, {
                    "f_id": "453",
                    "f_name": "\u9647\u5357\u5e02"
                }, {
                    "f_id": "447",
                    "f_name": "\u6b66\u5a01\u5e02"
                }, {
                    "f_id": "448",
                    "f_name": "\u5f20\u6396\u5e02"
                }, {
                    "f_id": "450",
                    "f_name": "\u9152\u6cc9\u5e02"
                }, {
                    "f_id": "455",
                    "f_name": "\u7518\u5357\u85cf\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "454",
                    "f_name": "\u4e34\u590f\u56de\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "452",
                    "f_name": "\u5b9a\u897f\u5e02"
                }],
                "29": [{
                    "f_id": "456",
                    "f_name": "\u897f\u5b81\u5e02"
                }, {
                    "f_id": "457",
                    "f_name": "\u6d77\u4e1c\u5e02"
                }, {
                    "f_id": "458",
                    "f_name": "\u6d77\u5317\u85cf\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "459",
                    "f_name": "\u9ec4\u5357\u85cf\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "460",
                    "f_name": "\u6d77\u5357\u85cf\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "461",
                    "f_name": "\u679c\u6d1b\u85cf\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "462",
                    "f_name": "\u7389\u6811\u85cf\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "463",
                    "f_name": "\u6d77\u897f\u8499\u53e4\u65cf\u85cf\u65cf\u81ea\u6cbb\u5dde"
                }],
                "30": [{
                    "f_id": "464",
                    "f_name": "\u94f6\u5ddd\u5e02"
                }, {
                    "f_id": "465",
                    "f_name": "\u77f3\u5634\u5c71\u5e02"
                }, {
                    "f_id": "466",
                    "f_name": "\u5434\u5fe0\u5e02"
                }, {
                    "f_id": "467",
                    "f_name": "\u56fa\u539f\u5e02"
                }, {
                    "f_id": "468",
                    "f_name": "\u4e2d\u536b\u5e02"
                }],
                "31": [{
                    "f_id": "469",
                    "f_name": "\u4e4c\u9c81\u6728\u9f50\u5e02"
                }, {
                    "f_id": "470",
                    "f_name": "\u514b\u62c9\u739b\u4f9d\u5e02"
                }, {
                    "f_id": "483",
                    "f_name": "\u77f3\u6cb3\u5b50\u5e02"
                }, {
                    "f_id": "471",
                    "f_name": "\u5410\u9c81\u756a\u5e02"
                }, {
                    "f_id": "472",
                    "f_name": "\u54c8\u5bc6\u5e02"
                }, {
                    "f_id": "479",
                    "f_name": "\u548c\u7530\u5e02"
                }, {
                    "f_id": "476",
                    "f_name": "\u963f\u514b\u82cf\u5e02"
                }, {
                    "f_id": "478",
                    "f_name": "\u5580\u4ec0\u5e02"
                }, {
                    "f_id": "477",
                    "f_name": "\u514b\u5b5c\u52d2\u82cf\u67ef\u5c14\u514b\u5b5c\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "475",
                    "f_name": "\u5df4\u97f3\u90ed\u695e\u8499\u53e4\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "473",
                    "f_name": "\u660c\u5409\u56de\u65cf\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "474",
                    "f_name": "\u535a\u5c14\u5854\u62c9\u8499\u53e4\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "480",
                    "f_name": "\u4f0a\u7281\u54c8\u8428\u514b\u81ea\u6cbb\u5dde"
                }, {
                    "f_id": "481",
                    "f_name": "\u5854\u57ce\u5e02"
                }, {
                    "f_id": "482",
                    "f_name": "\u963f\u52d2\u6cf0\u5e02"
                }, {
                    "f_id": "486",
                    "f_name": "\u4e94\u5bb6\u6e20\u5e02"
                }, {
                    "f_id": "484",
                    "f_name": "\u963f\u62c9\u5c14\u5e02"
                }, {
                    "f_id": "485",
                    "f_name": "\u56fe\u6728\u8212\u514b\u5e02"
                }],
                "32": [{
                    "f_id": "487",
                    "f_name": "\u53f0\u5317\u5e02"
                }, {
                    "f_id": "509",
                    "f_name": "\u5357\u6295\u5e02"
                }, {
                    "f_id": "511",
                    "f_name": "\u592a\u4fdd\u5e02"
                }, {
                    "f_id": "512",
                    "f_name": "\u4e91\u6797\u53bf"
                }, {
                    "f_id": "513",
                    "f_name": "\u6597\u516d\u5e02"
                }, {
                    "f_id": "515",
                    "f_name": "\u65b0\u8425\u5e02"
                }, {
                    "f_id": "517",
                    "f_name": "\u51e4\u5c71\u5e02"
                }, {
                    "f_id": "519",
                    "f_name": "\u5c4f\u4e1c\u5e02"
                }, {
                    "f_id": "521",
                    "f_name": "\u53f0\u4e1c\u5e02"
                }, {
                    "f_id": "523",
                    "f_name": "\u82b1\u83b2\u5e02"
                }, {
                    "f_id": "524",
                    "f_name": "\u6f8e\u6e56\u53bf"
                }, {
                    "f_id": "525",
                    "f_name": "\u9a6c\u516c\u5e02"
                }, {
                    "f_id": "507",
                    "f_name": "\u5f70\u5316\u5e02"
                }, {
                    "f_id": "505",
                    "f_name": "\u4e30\u539f\u5e02"
                }, {
                    "f_id": "503",
                    "f_name": "\u82d7\u6817\u5e02"
                }, {
                    "f_id": "488",
                    "f_name": "\u9ad8\u96c4\u5e02"
                }, {
                    "f_id": "489",
                    "f_name": "\u57fa\u9686\u5e02"
                }, {
                    "f_id": "490",
                    "f_name": "\u53f0\u4e2d\u5e02"
                }, {
                    "f_id": "491",
                    "f_name": "\u53f0\u5357\u5e02"
                }, {
                    "f_id": "492",
                    "f_name": "\u65b0\u7af9\u5e02"
                }, {
                    "f_id": "493",
                    "f_name": "\u5609\u4e49\u5e02"
                }, {
                    "f_id": "494",
                    "f_name": "\u65b0\u5317\u5e02"
                }, {
                    "f_id": "495",
                    "f_name": "\u677f\u6865\u5e02"
                }, {
                    "f_id": "497",
                    "f_name": "\u5b9c\u5170\u5e02"
                }, {
                    "f_id": "499",
                    "f_name": "\u7af9\u5317\u5e02"
                }, {
                    "f_id": "501",
                    "f_name": "\u6843\u56ed\u5e02"
                }, {
                    "f_id": "3777",
                    "f_name": "\u91d1\u95e8\u53bf"
                }],
                "3774": [{
                    "f_id": "33",
                    "f_name": "\u9999\u6e2f"
                }],
                "3775": [{
                    "f_id": "34",
                    "f_name": "\u6fb3\u95e8"
                }],
                "3778": [{
                    "f_id": "3782",
                    "f_name": "\u9493\u9c7c\u5c9b"
                }]
            };*/
        };

        var htmlProvince = '';
        for (var p in provinceList) {
            htmlProvince += '<li class="noselect"><a href="javascript:void(0);" fid="' + provinceList[p].f_id + '" title="' + provinceList[p].f_name + '"><span>' + provinceList[p].f_name + '</span></a></li>';
        }

        var recv_name = ($('.form_recv_name').length) ? $('.form_recv_name').text() : '';
        var province = ($('.form_province').length) ? $('.form_province').text() : '';
        var city = ($('.form_city').length) ? $('.form_city').text() : '';
        var area = ($('.form_area').length) ? $('.form_area').text() : '';
        var street = ($('.form_street').length) ? $('.form_street').text() : '';
        var recv_phone = ($('.form_recv_phone').length) ? $('.form_recv_phone').text() : '';

        var html = '<h2 class="text-center"><i class="pb-icon pb-icon-cargo pb-icon-fix"></i> 请填写您的收货地址</h2><div class="bangding clearFix pt20">';
        html += '<div class="pb-line pb-line-50">';
        html += '         <div class="pb-line-left">';
        html += '           <span class="c607d8b">所在地区：</span>';
        html += '         </div>';
        html += '         <div class="pb-line-right">';
        html += '           <div class="pb-line-33"><span ><input type="text" name="province" id="province" value="' + province + '" placeholder="请输入省份"></span><span class="pbs-error-info"></span></div>';
        html += '           <div class="pb-line-33"><span ><input type="text" name="city" id="city" value="' + city + '" placeholder="请输入城市"></span><span class="pbs-error-info"></span></div>';
        html += '           <div class="pb-line-33"><span ><input type="text" name="area" id="area" value="' + area + '" placeholder="请输入区域"></span><span class="pbs-error-info"></span></div>';

        /*html += '           <div class="pb-line-33"><div class="pb-select noselect pb-select-province"><span>请选择</span> <i class="pb-icon pb-icon-arrow-down pb-icon-fix"></i></div>';
        html += '           <div class="pb-select-options pb-hide pb-select-options-province" ><ul>' + htmlProvince + '</ul></div></div>';
        html += '           <div class="pb-line-33"><div class="pb-select noselect pb-select-city"><span>请选择</span> <i class="pb-icon pb-icon-arrow-down pb-icon-fix"></i></div>';
        html += '           <div class="pb-select-options pb-hide pb-select-options-city" ><ul></ul></div></div>';

        html += '           <div class="pb-line-33"><div class="pb-select noselect pb-select-area"><span>请选择</span> <i class="pb-icon pb-icon-arrow-down pb-icon-fix"></i></div>';
        html += '           <div class="pb-select-options pb-hide pb-select-options-area" ><ul></ul></div></div>';*/

        html += '         </div>';
        html += '       </div>';

        html += '<div class="pb-line pb-line-50">';
        html += '         <div class="pb-line-left">';
        html += '           <span class="c607d8b">详细地址：</span>';
        html += '         </div>';
        html += '         <div class="pb-line-right">';

        html += '<span ><input type="text" name="street" id="street" value="' + street + '" placeholder="请输入详细地址"></span><span class="pbs-error-info"></span>';

        html += '         </div>';
        html += '       </div>';

        html += '<div class="pb-line pb-line-50">';
        html += '         <div class="pb-line-left">';
        html += '           <span class="c607d8b">收货人姓名：</span>';
        html += '         </div>';
        html += '         <div class="pb-line-right">';

        html += '<span ><input type="text" name="recv_name" id="recv_name" value="' + recv_name + '" placeholder="请输入收货人姓名"></span><span class="pbs-error-info"></span>';

        html += '         </div>';
        html += '       </div>';

        html += '<div class="pb-line pb-line-50">';
        html += '         <div class="pb-line-left">';
        html += '           <span class="c607d8b">手机号码：</span>';
        html += '         </div>';
        html += '         <div class="pb-line-right">';

        html += '<span ><input type="text" name="recv_phone" id="recv_phone" value="' + recv_phone + '" placeholder="请输入手机号码"></span><span class="pbs-error-info"></span>';

        html += '         </div>';
        html += '       </div>';

        html += '</div><div class=""><a href="javascript:void(0);" class=" bangding-confirm recv-btn-save">保存</a><span class="pb-error-info text-center pb-error-info-fix"></span></div>';
        $.LayerOut({
            html: html
        });
        $('.bangding-confirm').on('click', function() {
            //$('.modal-backdrop,.modal').remove();
            //delete $._LayerOut;
        });
        //
        $('.pb-line').undelegate("input").delegate("input", "blur", function(e) {
            var id = $(this).attr('id');
            var postDataTrg = (id.match(/password/i)) ? 'change_passwd_data' : 'recv_data';
            if (id.match(/^(name|qq)$/i)) postDataTrg = 'change_contact_data';
            if (id.match(/^(company_name|url)$/i)) postDataTrg = 'change_company_data';
            if (id.match(/^(area)$/i) || $.trim($(this).val()) != "") {
                $(this).removeClass('pb-input-error');
                if (id.match(/^(province|city|area)$/i)) {
                    $(this).parent().parent().parent().find('.pb-error-info').text('');
                } else {
                    $(this).parent().parent().find('.pb-error-info').text('');
                }
                postData[postDataTrg][id] = $.trim($(this).val());
            } else {
                var errInfo = $(this).attr('placeholder');
                $(this).addClass('pb-input-error');
                if (id.match(/^(province|city|area)$/i)) {
                    $(this).parent().parent().parent().find('.pb-error-info').text(errInfo);
                } else {
                    $(this).parent().parent().find('.pb-error-info').text(errInfo);
                }
                //$(this).focus();
            }
        });
        //save
        $('.modal').undelegate(".recv-btn-save").delegate(".recv-btn-save", "click", function(e) {
            //console.log('recv-btn-save');
            var _this = this;

            var province_ok = chkInput('province', 'recv_data', true);
            if (!province_ok) return false;

            var city_ok = chkInput('city', 'recv_data', true);
            if (!city_ok) return false;

            var area_ok = chkInput('area', 'recv_data', true, false);
            //if (!area_ok) return false;

            var street_ok = chkInput('street', 'recv_data');
            if (!street_ok) return false;

            var recv_name_ok = chkInput('recv_name', 'recv_data');
            if (!recv_name_ok) return false;

            var recv_phone_ok = chkInput('recv_phone', 'recv_data');
            if (!recv_phone_ok) return false;

            var newPostData = {};
            if (postData['recv_data'].province) newPostData['province'] = postData['recv_data'].province;
            if (postData['recv_data'].city) newPostData['city'] = postData['recv_data'].city;
            if (postData['recv_data'].area) newPostData['area'] = postData['recv_data'].area;
            if (postData['recv_data'].street) newPostData['street'] = postData['recv_data'].street;
            if (postData['recv_data'].recv_name) newPostData['recv_name'] = postData['recv_data'].recv_name;
            if (postData['recv_data'].recv_phone) newPostData['recv_phone'] = postData['recv_data'].recv_phone;

            PB.request('post', '/users/change_my_recv_info/', 'json', function(data) {
                //console.log('change_recv', data);
                handleError(_this, data);
            }, function(data, status) {
                if(document.location.href.toString().match(/#person\-info/i)){
                    $('.modal-backdrop,.modal').remove();
                    delete $._LayerOut;
                    setTimeout(function(){
                        //document.location.href = document.location.href.toString().replace('#person-info','');
                    },500);
                }
                return false;
            }, newPostData, 'json');
        });
        //展开下拉列表
        $('.pb-line').undelegate(".pb-select").delegate(".pb-select", "click", function(e) {
            var thisClass = $(this).attr('class');
            if (thisClass.match(/pb\-select\-([0-9a-z_\-]+)/i)) {
                var trg = RegExp.$1;
                if ($('.pb-select-options-' + trg).length) {
                    var status = $('.pb-select-options-' + trg).css('display');
                    if (status == 'none') {
                        $(this).find('i.pb-icon').addClass('pb-icon-arrow-up');
                        $('.pb-select-options-' + trg).removeClass('pb-hide');
                        pbCurrentSelectClass = trg;
                    } else {
                        $(this).find('i.pb-icon').removeClass('pb-icon-arrow-up');
                        $('.pb-select-options-' + trg).addClass('pb-hide');
                        pbCurrentSelectClass = '';
                    }
                }
            }
        });
        //选中关闭下拉列表
        $('.pb-select-options').undelegate("li").delegate("li", "click", function(e) {
            var selectEle = $(this).parent().parent();
            var thisClass = selectEle.attr('class');
            if (thisClass.match(/pb\-select\-options\-([0-9a-z_\-]+)/i)) {
                var trg = RegExp.$1;
                if ($('.pb-select-options-' + trg).length) {
                    var value = $(this).find('a > span').text();
                    postData['change_profile_data'][trg] = value;
                    $('.pb-select-' + trg + ' > span:first-child').text(value);
                    $('.pb-select-' + trg + ' > span:first-child').addClass('selected');
                    $('.pb-select-' + trg).find('i.pb-icon').removeClass('pb-icon-arrow-up');
                    $('.pb-select-options-' + trg).addClass('pb-hide');
                    pbCurrentSelectClass = '';
                    if (trg == 'province') {
                        //load cities
                        var cities = getCities();
                        var fid = $(this).find('a').attr('fid');
                        //console.log('cities', trg, cities, fid, cities[fid]);
                        var htmlData = '';
                        for (var p in cities[fid]) {
                            htmlData += '<li class="noselect"><a href="javascript:void(0);" fid="' + cities[fid][p].f_id + '" title="' + cities[fid][p].f_name + '"><span>' + cities[fid][p].f_name + '</span></a></li>';
                        }
                        $('.pb-select-options-city').find('ul').html(htmlData);
                        $('.pb-select-city > span:first-child').text('请选择');
                        $('.pb-select-city > span:first-child').removeClass('selected');
                        postData['change_profile_data']['city'] = '';
                    } else if (trg == 'city') {

                    }
                    //console.log('postData', postData);
                }
            }
        });
        //点击其他区域自动关闭下拉列表
        $('body').on('click', '*', function(event) {
            event.stopPropagation();
            if (pbCurrentSelectClass != '') {
                if (($(this).parent() && $(this).parent().attr('class') && $(this).parent().attr('class').match(/pb\-select/i))) {
                    //|| $(this).find('.pb-select').length > 0
                } else {
                    $('.pb-select').find('i.pb-icon').removeClass('pb-icon-arrow-up');
                    $('.pb-select-options').addClass('pb-hide');
                }
            }
        });
    }
    $('.form-panel .open-recv-modal').on('click', function() {
        goodsReceiptModal();
    });
    //是否自动弹出收货地址弹窗
    $(document).ready(function(){
        if(document.location.href.toString().match(/#person\-info/i) && PB.getCookie('auto_modal')==null){
            PB.setCookie('auto_modal',1, 60000);
            PB.jumpTo('#user-info');
            goodsReceiptModal();
        }
    });

    //同步微信绑定状态
    var isScanWx = false;
    var tickTime = 0;
    var chkWeixinBinding = function() {
        if (!isWxBinding && isScanWx) {
            var wxBindingInterval = setInterval(function() {
                tickTime++;
                if (tickTime > 300) {
                    clearInterval(wxBindingInterval);
                }
                //console.log('check wxBindingInterval');
                $.ajax({
                    type: 'get',
                    url: '/users/weixin_isbind/',
                    format: 'json',
                    success: function(data) {
                        if (data.status == "ok" && data.is_bind == true) {
                            $('.modal-backdrop,.modal').remove();
                            delete $._LayerOut;
                            clearInterval(wxBindingInterval);
                            isWxBinding = true;
                            //document.location.reload();
                            $('.pb-add-wx-binding').addClass('pb-hide');
                            $('.pb-cancel-wx-binding').removeClass('pb-hide');
                            $('.weixin_nickname').text(data.nickname);
                            isScanWx = false;
                        }
                    },
                    error: function() {

                    }
                });
            }, 1000);
        }
    };

    //添加绑定的提示
    $('#js-bangding').on('click', function() {
        alertBangdingTip();
    })

    var alertBangdingTip = function() {
        isScanWx = true;
        chkWeixinBinding();
        var barcodeImg = '/hr/qrcode_bind/?t=' + Math.random();
        var html = '<h2 class="text-center"><i class="pb-icon pb-icon-weixin pb-icon-fix"></i> 扫一扫绑定微信号</h2><div class="bangding clearFix pt20 weixin-barcode text-center"><img src="/static/partner/images/loading.gif" width="30" border="0"></div><div class=""><a href="javascript:void(0);" class="bangding-confirm">确定</a></div>';
        $.LayerOut({
            html: html,
            afterClose: function() {
                isScanWx = false;
            }
        });
        var loadImage = function(url) {
            var loadImage = function(deferred) {
                var image = new Image();
                image.onload = loaded;
                image.onerror = errored;
                image.onabort = errored;
                image.src = url;

                function loaded() {
                    unbindEvents();
                    deferred.resolve(image);
                }

                function errored() {
                    unbindEvents();
                    deferred.reject(image);
                }

                function unbindEvents() {
                    image.onload = null;
                    image.onerror = null;
                    image.onabort = null;
                }
            };
            return $.Deferred(loadImage).promise();
        };
        var p1 = loadImage(barcodeImg);
        p1.then(function(image) {
            $('.weixin-barcode img').attr('src', barcodeImg);
            $('.weixin-barcode img').attr('width', '160');
        })
        $('.bangding-confirm').on('click', function() {
            $('.modal-backdrop,.modal').remove();
            delete $._LayerOut;
        });
        ///hr/qrcode_bind/
    }
    var windowUrl = window.location.href;
    if (windowUrl.match(/users\/profile\/#bangding/g)) {
        alertBangdingTip();
        $('#js-bangding').addClass('cf46c62');
    }
    $(".pb-line").undelegate(".unbindWeixin").delegate(".unbindWeixin", "click", function(e) {
        //console.log('unbindWeixin', 1);
        var html = '<div class="no-feed-alert">' +
            '<h2><i class="i-warning"></i>解除微信绑定</h2>' +
            '<p class="tip"><br>您确认解除与“<span class="cf46c62">聘宝招聘版</span>”的微信绑定吗？解绑后将不再收到新的简历推荐提醒！</p>' +
            '<p>' +

            '<a class="btn confirm unbindNow" href="javascript:void(0);">确认解除</a>' +
            '<a class="btn cancel closeLayer" href="javascript:void(0);">取消</a>' +
            '</p>' +
            '</div>';
        $.LayerOut({
            html: html
        });
        $('.closeLayer').on('click', function() {
            $('.modal-backdrop,.modal').remove();
            delete $._LayerOut;
        });
        $('.unbindNow').on('click', function() {

            var aj = $.ajax({
                url: '/hr/unbind_weixin/',
                type: 'get',
                cache: false,
                dataType: 'json',
                success: function(data) {
                    if (data != undefined && data.status == 'ok') {
                        document.location.reload();
                    } else {
                        alert('解绑失败！' + data.msg);
                    }
                },
                error: function() {
                    $('.modal-backdrop,.modal').remove();
                    delete $._LayerOut;
                    alert('解绑失败！');
                }
            });
        });
    });


    var isReSend = false;
    var timeInterval;

    //修改手机绑定
    $(".pb-line").undelegate(".chg-phone").delegate(".chg-phone", "click", function(e) {
        var html = '<div class="no-feed-alert">' +
            '<h2><i class="i-warning"></i>绑定手机号码</h2><br><br>' +
            PB.modalLine3Col('请输入登录密码', 'login-passwd', 'password') +
            PB.modalLine3Col('请输入新的手机号码', 'new-phone') +
            PB.modalLine3Col('请输入短信验证码', 'code', 'text', 'use-sms-code') +
            '<br>' +

            '<p>' +
            '<a class="btn confirm chg-phone-now" href="javascript:void(0);">确认绑定</a>' +
            //'<a class="btn cancel closeLayer" href="javascript:void(0);">取消</a>' +
            '</p>' +
            '</div>';
        PB.box(html, '.chg-phone-now', function(trg, box) {
            var verifyCode = trg.parent().parent().find('.code').prop('value');
            var phoneNumber = trg.parent().parent().find('.new-phone').prop('value');
            var loginPasswd = trg.parent().parent().find('.login-passwd').prop('value');

            if ($.trim(loginPasswd) == "") {
                //PB.btnAlert('.chg-phone-now', '请输入登录密码！');
                PB.labelErr('login-passwd', '请输入登录密码！');
                trg.parent().parent().find('.login-passwd').focus();
                return false;
            }

            if (!phoneNumber.match(/^1[0-9]{10}$/i)) {
                //PB.btnAlert('.chg-phone-now', '请输入新的手机号码！');
                PB.labelErr('new-phone', '请输入新的手机号码！');
                trg.parent().parent().find('.new-phone').focus();
                return false;
            }

            if (!verifyCode.match(/^[0-9]{6}$/i)) {
                //PB.btnAlert('.chg-phone-now', '请输入六位短信验证码！');
                PB.labelErr('code', '请输入六位短信验证码！');
                trg.parent().parent().find('.code').focus();
                return false;
            }
            var smsBtnTitle = $('.sms-code').html();
            $('.chg-phone-now').attr('disabled', 'true');

            //PB.getSmsCode(phoneNumber, '.chg-phone-now',smsBtnTitle,'ChangeMobile');

            PB.request('post', '/users/change_mobile/', 'json', function(data) {

                $('.chg-phone-now').removeAttr('disabled');

                PB.formErrHandler(data, function(data) {
                    box.close();
                    document.location.href = '/users/profile/';
                }, null, '.chg-phone-now', '确认修改');

            }, function(data, status) {
                PB.btnAlert('.chg-phone-now', '修改绑定手机失败！请重新获取');
                return false;
            }, {
                password: loginPasswd,
                mobile: phoneNumber,
                code: verifyCode
            }, 'json');
        }, null, 'new-phone', isReSend, timeInterval, 'ChangeMobile');
    });

    //修改接收邮箱
    $(".pb-line").undelegate(".chg-email").delegate(".chg-email", "click", function(e) {
        PB.chgNotifyEmail(isReSend, timeInterval);
    });

    //验证接收邮箱
    $(".pb-line").undelegate(".verify-email").delegate(".verify-email", "click", function(e) {
        var currentEmail = $('.receive_email').text();
        if (!PB.isValidEmail(currentEmail)) {
            currentEmail = '';
        }

        var html = '<div class="no-feed-alert">' +
            '<h2><i class="i-warning"></i>立即验证邮箱</h2>' +
            PB.modalLine3Col('请输入登录密码', 'login-passwd', 'password', null, 'mg-top-30') +
            PB.modalLine3Col('请输入要验证的邮箱', 'to-chg-email', 'text', null, 'mg-bottom-30', currentEmail) +

            '<p class="tip line mg-bottom-30"><span class=" line-width-100">该邮箱仅用于您接收聘宝简历推荐的邮箱，不用于登录，您可至“<a class="c42b4e6" href="/users/profile/">个人设置</a>”中修改</span></p>' +
            '<p>' +
            '<a class="btn confirm verify-email-now" href="javascript:void(0);">发送邮箱验证码</a>' +
            //'<a class="btn cancel closeLayer" href="javascript:void(0);">取消</a>' +
            '</p>' +
            '</div>';
        PB.box(html, '.verify-email-now', function(trg, box) {
            var toChgEmail = trg.parent().parent().find('.to-chg-email').prop('value');
            var loginPasswd = trg.parent().parent().find('.login-passwd').prop('value');

            if ($.trim(loginPasswd) == "") {
                //PB.btnAlert('.verify-email-now', '请输入登录密码！');
                PB.labelErr('login-passwd', '请输入登录密码！');
                trg.parent().parent().find('.login-passwd').focus();
                return false;
            }

            if (!PB.isValidEmail(toChgEmail)) {
                //PB.btnAlert('.verify-email-now', '请输入要修改的邮箱！');
                PB.labelErr('to-chg-email', '请输入要修改的邮箱！');
                trg.parent().parent().find('.to-chg-email').focus();
                return false;
            }

            $('.verify-email-now').attr('disabled', 'true');

            PB.request('post', '/users/send_email_code/', 'json', function(data) {
                //box.close()
                //发送成功

                $('.verify-email-now').removeAttr('disabled');

                PB.formErrHandler(data, function(data) {
                    box.close();
                    //document.location.href = '/users/profile/';
                }, null, '.verify-email-now', '发送邮箱验证码');

            }, function(data, status) {
                PB.btnAlert('.verify-email-now', '发送邮箱验证码失败！请重新获取');
                return false;
            }, {
                password: loginPasswd,
                email: toChgEmail
            }, 'json');
        });
    });