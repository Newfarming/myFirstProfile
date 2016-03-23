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
var webdriver = require('selenium-webdriver'),
    By = require('selenium-webdriver').By,
    until = require('selenium-webdriver').until;
/*var assert = require('assert');
var test = require('selenium-webdriver/testing');*/
//console.log('test',test);

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

homeUrl = 'http://192.168.199.223:8000/';
//driver.get(weixinUrl);
//console.log(webdriver);
var app = {
    pressEnterToSend: function(title) {
        var deferred = webdriver.promise.defer(function() {
            throw Error('no header!');
        });
        //console.log(deferred);
        //driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(30);
        driver.manage().timeouts().pageLoadTimeout(30);
        //driver.switchTo().window(title);

        driver.findElement(By.id('mainMenu')).then(function(element) {
            deferred.fulfill(element);
            console.log('mainMenu', element);
            //element.click();
            //element.sendKeys(webdriver.Key.RETURN);
        });
        //console.log(deferred.promise);

        return deferred.promise;
    }
};

var ptSNOpenUrl = function(weixinUrl, cb, args) {
    var deferred = webdriver.promise.defer();
    //console.log(deferred.promise);
    driver.manage().timeouts().implicitlyWait(30);
    driver.get(homeUrl);
    driver.getTitle().then(function(title) {
        //Calling fulfill() will set the promise value and invoke the callback chain
        deferred.fulfill(title);
        // call reject() to set an error and trigger any error-handlers
        //console.log('title',title);
        //console.log(deferred.promise);
        //if(typeof deferred=='object') deferred.resolve();
        if (app[cb] instanceof Function) {
            app[cb](title);
        }
    });

    return deferred.promise;
};

var loginPage = function() {
    var d = webdriver.promise.defer();
    driver.findElement(By.css('a.signin')).click(function() {
        d.fulfill();
    });
    /*driver.findElement(By.css('a.signin')).then(function(element) {
        d.fulfill(element);
        element.click();
        element.sendKeys(webdriver.Key.RETURN);
    });*/
    return d.promise;
};
var loginAction = function() {
    var d = webdriver.promise.defer();
    driver.findElement(By.name('password')).sendKeys(testPasswd);
    driver.findElement(By.name('username')).sendKeys(testMobile);
    driver.findElement(By.css('button.login-btn')).then(function(element) {
        d.fulfill(element);
        element.click();
        element.sendKeys(webdriver.Key.RETURN);
    });
    //d.fulfill();
    return d.promise;
};

var profilePage = function() {
    driver.get('http://192.168.199.223:8000/users/profile/');
    var d = webdriver.promise.defer();
    driver.isElementPresent(By.css('a.main-user-control-icon'));
    driver.findElement(By.css('a.main-user-control-icon')).then(function(element) {
        console.log('mainMenu', element);
        d.fulfill(element);
        element.click();
        element.sendKeys(webdriver.Key.RETURN);
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
driver.manage().timeouts().implicitlyWait(30000);
driver.manage().timeouts().pageLoadTimeout(30000);
driver.get(homeUrl);
/*driver.wait(function() {
    return driver.isElementPresent(By.id('mainMenu'));
    //driver.wait(function() {webdriver.promise.delayed(250).then(function(){return true})}, 100);
    driver.findElement(By.id('mainMenu')).then(function (element) {

        console.log('mainMenu',element);
        //element.click();
        //element.sendKeys(webdriver.Key.RETURN);
    });
}, 10000);*/

var testUser = '46916597@qq.com';
var testMobile = '18228392117';
var testPasswd = 'q1w2e3r4';

/*loginPage().
then(loginAction).
then(null, function(err) {
  console.error("An error was thrown! " + err);
});*/

loginPage();
loginAction();
//profilePage();

/*driver.wait(function () {
     return driver.quit();
}, 1000);*/
driver.quit();


//mocha -t 5000 sms.js
/*test.describe('', function() {
  test.it('should work', function() {
    driver.get(homeUrl);
    var searchBox = driver.findElement(By.name('q'));
    searchBox.sendKeys('webdriver');
    searchBox.getAttribute('value').then(function(value) {
      assert.equal(value, 'webdriver');
    });

    driver.quit();
  });
});*/


