'use strict';

var cookieLib = {
    eggCookieName: 'isShowEggNew',
    countDayByDayTime: function(offsetNum) {
        var getDateObj = function(t) {
            var dt;
            if (t != undefined) {
                if (typeof t == 'string' || typeof t == 'number') {
                    dt = new Date(t);
                } else {
                    dt = new Date();
                }
            } else {
                dt = new Date();
            }
            return {
                y: dt.getFullYear(),
                m: dt.getMonth() + 1,
                d: dt.getDate(),
                h: 0,//dt.getHours(),
                i: 0,//dt.getMinutes(),
                s: 0,//dt.getSeconds()
            };
        };
        var monthStartObj = getDateObj();
        var monthEnd = new Date(monthStartObj.y, monthStartObj.m - 1, monthStartObj.d + offsetNum, monthStartObj.h, monthStartObj.i, monthStartObj.s);
        return monthEnd.getFullYear() + '-' + (monthEnd.getMonth() + 1) + '-' + monthEnd.getDate() + 'T00:00:00';
    },
    countDayByDayTimeSeconds: function(offsetNum) {
        var getDateObj = function(t) {
            var dt;
            if (t != undefined) {
                if (typeof t == 'string' || typeof t == 'number') {
                    dt = new Date(t);
                } else {
                    dt = new Date();
                }
            } else {
                dt = new Date();
            }
            return {
                y: dt.getFullYear(),
                m: dt.getMonth() + 1,
                d: dt.getDate(),
                h: dt.getHours(),
                i: dt.getMinutes(),
                s: dt.getSeconds()
            };
        };
        var formatNum = function(n){
            if(parseInt(n) <= 9){
                return '0'+n;
            }else{
                return n;
            }
        };
        var monthStartObj = getDateObj();
        var monthEnd = new Date(monthStartObj.y, monthStartObj.m - 1, monthStartObj.d, monthStartObj.h, monthStartObj.i, monthStartObj.s + offsetNum);
        return monthEnd.getFullYear() + '-' + (monthEnd.getMonth() + 1) + '-' + monthEnd.getDate() + ' '+formatNum(monthEnd.getHours())+':'+formatNum(monthEnd.getMinutes())+':'+formatNum(monthEnd.getSeconds())+'';
    },
    getTimeStamp: function(t){
        var dt = new Date();
        if (typeof t == 'string' || typeof t == 'number') {
            dt = new Date(t);
        }
        return Math.round(dt/1000);
    },
    getTimeStampM: function(t){
        var dt = new Date();
        if (typeof t == 'string') {
            if(t.match(/^([0-9]{4})\-([0-9]{1,2})\-([0-9]{1,2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})$/i)){
                dt = new Date(RegExp.$1,parseInt(RegExp.$2)-1,RegExp.$3,RegExp.$4,RegExp.$5,RegExp.$6);
            }else{
                dt = new Date(t);
            }
            console.log('getTimeStampM',dt,t);
        }else if(typeof t == 'number'){
            dt = new Date(t);
        }
        return dt.getTime();
    },
    setCookieToday: function(key, value) {
       var ckTime = 86400000;
       //var tomorrow = this.countDayByDayTime(1);
       var tomorrow = this.countDayByDayTimeSeconds(60);
       var expires = new Date();
       var deadline = this.getTimeStampM(tomorrow);
       expires.setTime(deadline);
       console.log('setTime',expires);

       /*var expires2 = new Date();
       expires2.setTime(expires2.getTime());
       console.log('expires2',expires2.toUTCString());*/


       document.cookie = key + '=' + value + ';expires=' + expires.toUTCString()+';path=/;';
    },
    setCookie: function(key, value, day) {
       var ckTime = (day != undefined && typeof day == 'number')? parseInt(day)*86400000:86400000;
       var expires = new Date();
       expires.setTime(expires.getTime() + ckTime);
       document.cookie = key + '=' + value + ';expires=' + expires.toUTCString()+';path=/;';
    },
    delCookie: function(key) {
       var expires = new Date();
       expires.setTime(expires.getTime() - 86400);
       document.cookie = key + '=;expires=' + expires.toUTCString()+';path=/;';
    },
    getCookie: function(key) {
       var keyValue = document.cookie.match('(^|;) ?' + key + '=([^; ]*)(;|$)');
       return keyValue ? keyValue[2] : null;
    }
};

describe("controller test",function(){

    var ua = navigator.userAgent;

    //isValidEmail(email)
    it("isValidEmail test",function(){
        //mockScope.incrementMe();
        expect(isValidEmail('test@pb.com')).toEqual(true);
        expect(isValidEmail('test-@pb.com')).toEqual(false);
        expect(isValidEmail('test,@pb.com')).toEqual(false);
    });

    //PB.request request: function(method, url, format, cbOk, cbErr, postData, postFormat)
    /*it("PB.request test",function(){
        //mockScope.incrementMe();
        //
    });*/

    it("safari cookie test",function(){
        if(ua.match(/safari/i)){
            cookieLib.setCookieToday('test','1');
            expect(cookieLib.getCookie('test')).toEqual('1');
        }
    });

    it("chrome cookie test",function(){
        if(ua.match(/chrome/i)){
            cookieLib.setCookieToday('test','1');
            expect(cookieLib.getCookie('test')).toEqual('1');
        }
    });

    //2015-12-28T16:00:00.000
    it("cookie date string test",function(){
        if(ua.match(/safari/i)){
            expect(new Date('2015-12-28 16:00:00')).not.toEqual(new Date(2015,11,29,0,0,0));
            //Thu, 01 Jan 1970 00:00:00 GMT
            expect(new Date('Tue, 29 Dec 2015 00:00:00 GMT+0800')).toEqual(new Date(2015,11,29,0,0,0));
        }else{
            expect(new Date('2015-12-28 16:00:00')).toEqual(new Date(2015,11,29,0,0,0));
        }
        expect(new Date('2015-12-28T16:00:00')).toEqual(new Date(2015,11,29,0,0,0));
        expect(new Date('2015-12-28T16:00:00Z')).toEqual(new Date(2015,11,29,0,0,0));
    });
});


