//mocha -t 5000 exp_user_test.js

//体验型用户测试
var assert = require('assert'),
    test = require('selenium-webdriver/testing'),
    webdriver = require('selenium-webdriver');

/*var driver = new webdriver.Builder()
    //ie test: use Remote WebDriver: https://code.google.com/p/selenium/wiki/RemoteWebDriver
    //Allows tests to be run with browsers not available on the current OS
    //.withCapabilities(webdriver.Capabilities.ie())
    //.withCapabilities(webdriver.Capabilities.safari())
    .withCapabilities(webdriver.Capabilities.chrome())
    //.withCapabilities(webdriver.Capabilities.firefox())
    .build();*/
var driver;

//主页测试
/*test.describe('主页测试', function() {
    test.it('should work', function() {
        driver = new webdriver.Builder().withCapabilities(webdriver.Capabilities.chrome()).build();
        driver.get('http://b.pinbot.me/');
        var header = driver.findElement(webdriver.By.className("signup"));
        header.getAttribute('innerHTML').then(function(value) {
            assert.equal(value, '注册');
            driver.quit();
        }, function(err) {
            console.error("An error was thrown! " + err);
        });

    });
});*/

/*driver.wait(function() {
 return driver.getTitle().then(function(title) {
   return title === 'webdriver - Google Search';
 });
}, 1000);*/

//driver.quit();

//注册
/*test.describe('注册', function() {
    test.it('should work', function() {
        driver = new webdriver.Builder().withCapabilities(webdriver.Capabilities.chrome()).build();
        driver.get('http://b.pinbot.me/signup/');
        driver.findElement(webdriver.By.className("register-confirm")).click();

        driver.quit();
    });
});*/

var funcs= require('./funcs');
var config = require('./config');
if(funcs.fileExists('./_config.js')){
    config = require('./_config');
}
var testAccount=config.account;
var testAccountPasswd=config.password;

//登录
test.describe('登录', function() {
    test.it('should work', function() {
        driver = new webdriver.Builder().withCapabilities(webdriver.Capabilities.chrome()).build();
        driver.get('http://b.pinbot.me/signin/');
        driver.findElement(webdriver.By.name('password')).sendKeys(testAccountPasswd);
        driver.findElement(webdriver.By.name('email')).sendKeys(testAccount, webdriver.Key.RETURN);
        driver.quit();
    });
});



//提示条

//简历下载

//用户模式

//交易记录

//我的套餐

//我的钱包