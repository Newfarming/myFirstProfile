/**
 * 前端自动化测试 selenium
 */
/*
WebElement element1 = webdriver.findElement(By.id("header"));
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

var funcs= require('./funcs');
var config = require('./config');
if(funcs.fileExists('./_config.js')){
    config = require('./_config');
}
var testAccount=config.account;
var testAccountPasswd=config.password;

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

weixinUrl='http://192.168.199.114:8000/signin/';
//driver.get(weixinUrl);
//console.log(webdriver);
var app={
    pressEnterToSend:function (title) {
        var deferred = webdriver.promise.defer(function() {
            throw Error('no header!');
        });
        //console.log(deferred);
        //driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(30);
        driver.manage().timeouts().pageLoadTimeout(30);
        //driver.switchTo().window(title);

        driver.findElement(By.id('mainMenu')).then(function (element) {
            deferred.fulfill(element);
            console.log('mainMenu',element);
            //element.click();
            //element.sendKeys(webdriver.Key.RETURN);
        });
        //console.log(deferred.promise);

        return deferred.promise;
    }
};

var ptSNOpenUrl = function (weixinUrl,cb,args) {
    var deferred = webdriver.promise.defer();
    //console.log(deferred.promise);
    driver.manage().timeouts().implicitlyWait(30);
    driver.get(weixinUrl);
    driver.getTitle().then(function(title) {
        //Calling fulfill() will set the promise value and invoke the callback chain
        deferred.fulfill(title);
        // call reject() to set an error and trigger any error-handlers
        //console.log('title',title);
        //console.log(deferred.promise);
        //if(typeof deferred=='object') deferred.resolve();
        if(app[cb] instanceof Function){
            app[cb](title);
        }
    });

    return deferred.promise;
};

var loginPage = function(isGood){
    var d = webdriver.promise.defer();
    driver.findElement(By.css('img.pt-logo-w')).click(function() {
        d.fulfill();
    });
    return d.promise;
};



//driver.findElement(By.name('userId')).sendKeys('weibo@pinbot.me');
//driver.findElement(By.name('passwd')).sendKeys('');
//driver.findElement(By.xpath('//*[@id="userId"]')).sendKeys('weibo@pinbot.me');
//driver.findElement(By.className('pt-btn-success2')).click();
//console.log(webdriver.Key);
//var ok=pressEnterToSend();
//driver.findElement(By.className('pt-btn-success2')).sendKeys(webdriver.Key.RETURN);
//console.log(ok);

//ptSNOpenUrl(weixinUrl,'pressEnterToSend',null);

driver.get(weixinUrl);
/*driver.wait(function() {
    return driver.isElementPresent(By.id('mainMenu'));
    //driver.wait(function() {webdriver.promise.delayed(250).then(function(){return true})}, 100);
    driver.findElement(By.id('mainMenu')).then(function (element) {

        console.log('mainMenu',element);
        //element.click();
        //element.sendKeys(webdriver.Key.RETURN);
    });
}, 10000);*/

// driver.wait(function () {
//     return driver.isElementPresent(By.className('pt-btn-success2'));
// }, 3000);

driver.findElement(By.name('email')).then(function(element) {
    //console.log(element);
    //element.click();

    driver.findElement(By.name('password')).sendKeys(testAccount);
    driver.findElement(By.name('email')).sendKeys(testAccountPasswd, webdriver.Key.RETURN);

    //element.sendKeys(webdriver.Key.RETURN);

});
//driver.quit();


/*test.describe('PB Weixin', function() {
  test.it('should work', function() {
    driver.get(weixinUrl);
    var searchBox = driver.findElement(By.name('q'));
    searchBox.sendKeys('webdriver');
    searchBox.getAttribute('value').then(function(value) {
      assert.equal(value, 'webdriver');
    });

    driver.quit();
  });
});*/
