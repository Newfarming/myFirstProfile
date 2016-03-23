// Karma configuration
// Generated on Fri Jul 31 2015 16:57:02 GMT+0800 (CST)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: './',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
        /*'dist/angular.js',
        //'./dist/angular.min.js.map',
        'dist/angular-ui-router.js',
        'dist/angular-mocks.js',*/

        '../public/beta/scripts/lib.js',
        '../public/alpha/scripts/jquery.cookie.js',
        '../public/alpha/scripts/jquery.form.js',
        '../public/alpha/scripts/jquery.validate.js',
        '../public/alpha/scripts/common.js',
        '../public/users/scripts/form.js',
        'js/pb.js',
        //'js/**/*.js',

        'tests/**/*.js'
    ],


    // list of files to exclude
    exclude: [
        './*.js',
        './**/*min.js',
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher 'Chrome' 'Safari'
    browsers: ['Safari'],

    plugins: [
            'karma-safari-launcher',
            'karma-jasmine'
        ],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false
  })
}
