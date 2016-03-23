//mocha -t 5000 resume_shield.js
/*WebElement element1 = webdriver.findElement(By.id("header"));
 WebElement element2 = webdriver.findElement(By.name("name"));
 WebElement element3 = webdriver.findElement(By.tagName("a"));
 WebElement element4 = webdriver.findElement(By.xpath("//a[@title='logo']"));
 WebElement element5 = webdriver.findElement(By.cssSelector(".feautures"));
 WebElement element6 = webdriver.findElement(By.linkText("Blog"));
 WebElement element7 = webdriver.findElement(By.partialLinkText("Ruby"));
 WebElement element8 = webdriver.findElement(By.className("login"));

 android: [Function],
 chrome: [Function],
 firefox: [Function],
 ie: [Function],
 ipad: [Function],
 iphone: [Function],
 opera: [Function],
 phantomjs: [Function],
 safari: [Function],
 htmlunit: [Function],
 htmlunitwithjs: [Function] },
*/
'use strict';

var funcs = require('./funcs');
var config = require('./config');
if (funcs.fileExists('./_config.js')) {
    config = require('./_config');
}

var testAccount = config.account;
var testAccountPasswd = config.password;

var webdriver = require('selenium-webdriver'),
    By = require('selenium-webdriver').By,
    until = require('selenium-webdriver').until;
/*var assert = require('assert'),
test = require('selenium-webdriver/testing');*/

//var driver = new FirefoxDriver(new FirefoxBinary(new File("D:\\Program Files\\Mozilla Firefox\\firefox.exe")), profile);
//capabilities.setCapability(InternetExplorerDriver.INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS, true);

var driver = new webdriver.Builder()
    //ie test: use Remote WebDriver: https://code.google.com/p/selenium/wiki/RemoteWebDriver
    //Allows tests to be run with browsers not available on the current OS
    //.withCapabilities(webdriver.Capabilities.ie())

//.withCapabilities(webdriver.Capabilities.safari())
.withCapabilities(webdriver.Capabilities.chrome())
//.withCapabilities(webdriver.Capabilities.firefox())
.build();

var trgUrl = 'http://192.168.199.223:8000/statis/feed_result/group/5466fb20b1c3373c92e98935?username=likaiguo.happy@163.com#/group/55f4d9c5152ab502f486f6e9?0896db6a';


var app = {
    login: function(args) {
        var deferred = webdriver.promise.defer();
        //console.log(deferred);
        //driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(300);
        //driver.manage().timeouts().pageLoadTimeout(30);
        //driver.switchTo().window(title);

        driver.findElement(By.name('username')).then(function(element) {

            driver.findElement(By.name('username')).sendKeys(testAccount);
            driver.findElement(By.name('password')).sendKeys(testAccountPasswd, webdriver.Key.RETURN);

            webdriver.promise.delayed(500).then(function() {
                deferred.fulfill(element);
            });
        });
        //console.log(deferred.promise);

        return deferred.promise;
    },
    //后台简历屏蔽
    banResume: function(trgUrl, className) {
        //http://192.168.199.223:8000/statis/feed_result/group/5553087ab1c3371f7b8dc149?username=likaiguo.happy@163.com#/group/55f4d9c5152ab502f486f6e9
        var d = webdriver.promise.defer();
        driver.manage().timeouts().implicitlyWait(30);
        driver.get(trgUrl);
        if (driver.isElementPresent(By.className(className))) {
            console.log(className, 'ok');
            //
            driver.findElement(By.linkText("当前")).click();
            /*driver.findElement(By.name('username')).sendKeys(testAccount);
            driver.findElement(By.name('password')).sendKeys(testAccountPasswd, webdriver.Key.RETURN);*/
            d.fulfill(className);
        } else {
            d.rejected(new Error(className));
        }
        return d.promise;
    }
};

var pbOpenUrlCb = function(trgUrl, elementIdName, cb, args) {
    var deferred = webdriver.promise.defer();
    driver.manage().timeouts().implicitlyWait(600);
    driver.get(trgUrl);
    if (driver.isElementPresent(By.id(elementIdName))) {
        if (app[cb] instanceof Function) {
            app[cb](args).then(function() {
                deferred.fulfill(elementIdName);
            }, function(err) {
                deferred.rejected(new Error(elementIdName));
            });
        } else {
            deferred.rejected(new Error(elementIdName));
        }
    } else {
        deferred.rejected(new Error(elementIdName));
    }
    return deferred.promise;
};

/*
var loginPage = function(trgUrl) {
    var d = webdriver.promise.defer();
    driver.manage().timeouts().implicitlyWait(60);
    driver.get(trgUrl);
    if(driver.isElementPresent(By.name('username'))){
        driver.findElement(By.name('username')).sendKeys(testAccount);
        driver.findElement(By.name('password')).sendKeys(testAccountPasswd, webdriver.Key.RETURN);
        d.fulfill('username');
    }else{
        d.rejected(new Error('username'));
    }
    return d.promise;
};
var p = loginPage('http://192.168.199.223:8000/signin/');
p.then(function(){
    console.log('login OK');
    //driver.quit();
},function(err){
    console.log('login error'+err.toString());
    driver.quit();
}).then(null, function(e) {
    console.error('There was an error: ' + e);
    driver.quit();
});*/

var p = pbOpenUrlCb('http://192.168.199.223:8000/signin/', 'username', 'login', null);
p.then(function() {
    console.log('登录成功');
    //driver.quit();
}, function(err) {
    console.log('登录错误' + err.toString());
    driver.quit();
}).then(function() {
    console.log('进入简历屏蔽页面');
    //driver.get(trgUrl);
    var p2 = app.banResume('http://192.168.199.223:8000/statis/feed_result/group/5466fb20b1c3373c92e98935?username=likaiguo.happy@163.com#/group/55f4d9c5152ab502f486f6e9?0896db6a', 'admin-custom-control-block');
}).then(null, function(e) {
    console.error('Error: ' + e);
    driver.quit();
});


//driver.get(trgUrl);
/*driver.wait(function() {
    return driver.isElementPresent(By.id('mainMenu'));
    //driver.wait(function() {webdriver.promise.delayed(250).then(function(){return true})}, 100);
    driver.findElement(By.id('mainMenu')).then(function (element) {

        console.log('mainMenu',element);
        //element.click();
        //element.sendKeys(webdriver.Key.RETURN);
    });
}, 10000);*/


/*test.describe('PB Weixin', function() {
  test.it('should work', function() {
    driver.get(trgUrl);
    var searchBox = driver.findElement(By.name('q'));
    searchBox.sendKeys('webdriver');
    searchBox.getAttribute('value').then(function(value) {
      assert.equal(value, 'webdriver');
    });

    driver.quit();
  });
});
*/