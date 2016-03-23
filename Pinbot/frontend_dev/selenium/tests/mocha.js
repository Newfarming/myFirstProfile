//mocha -t 5000 sms.js
var assert = require('assert'),
    test = require('selenium-webdriver/testing'),
    webdriver = require('selenium-webdriver');

test.describe('短信模块测试', function() {
  test.it('should work', function() {
    var driver = new webdriver.Builder()
    //.withCapabilities(webdriver.Capabilities.safari())
    .withCapabilities(webdriver.Capabilities.chrome())
    //.withCapabilities(webdriver.Capabilities.firefox())
    .build();
    var homeUrl = 'http://192.168.199.223:8000/';

    driver.manage().timeouts().implicitlyWait(30000);
    driver.manage().timeouts().pageLoadTimeout(30000);
    driver.get(homeUrl);

    var testUser = '46916597@qq.com';
    var testMobile = '18228392117';
    var testPasswd = 'q1w2e3r4';

    var loginPage = function() {
        var d = webdriver.promise.defer();
        driver.findElement(webdriver.By.css('a.signin')).click(function() {
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
        driver.manage().timeouts().implicitlyWait(30000);
        driver.manage().timeouts().pageLoadTimeout(30000);
        driver.findElement(webdriver.By.name('password')).sendKeys(testPasswd);
        driver.findElement(webdriver.By.name('username')).sendKeys(testMobile);
        driver.findElement(webdriver.By.css('button.login-btn')).then(function(element) {
            d.fulfill(element);
            element.click();
            element.sendKeys(webdriver.Key.RETURN);
            var target = driver.findElement(webdriver.By.css('a.main-user-control-icon'));
            target.getAttribute('class').then(function(value) {
              assert.equal(value, 'main-user-control-icon ');
            });
        });
        //d.fulfill();
        return d.promise;
    };

    loginPage();
    loginAction();

    /*var searchBox = driver.findElement(webdriver.By.name('q'));
    searchBox.sendKeys('webdriver');
    searchBox.getAttribute('value').then(function(value) {
      assert.equal(value, 'webdriver');
    });*/

    driver.quit();
  });
});

