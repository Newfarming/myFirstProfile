var gulp = require('gulp');
var browserSync = require('browser-sync').create();
var reload = browserSync.reload;

var less = require('gulp-less');
var path = require('path');
var clean = require('gulp-clean');
var nano = require('gulp-cssnano');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var watch = require('gulp-watch');
var exec = require('child_process').exec;
var ngmin = require('gulp-ngmin');
var minifyCss = require('gulp-minify-css');
var gulpif = require('gulp-if');
var argv = require('yargs').argv;

//压缩css插件
var LessPluginCleanCSS = require('less-plugin-clean-css'),
    cleancss = new LessPluginCleanCSS({
        advanced: true
    });

var merge = require('merge-stream');
var fs = require('fs');
var gulpif = require('gulp-if');

//http://www.ituring.com.cn/article/54547
var Q = require('q');
var karmaServer = require('karma').Server;

gulp.task('default', function() {

});

//deploy前请gulp karma进行测试
gulp.task('karma', function(done) {
    new karmaServer({
        configFile: __dirname + '/karma.test.conf.js',
        singleRun: true
    }, done).start();
});

//js生成压缩版js
gulp.task('jsmin', function() {
    var miniPublic = gulp.src('../public/alpha/scripts/common.js')
        .pipe(watch('../public/alpha/scripts/common.js'))
        .pipe(uglify({
            /*output: {
                beautify: true
            },*/
            /*compress: {
                sequences: true,
                booleans: true,
                conditionals: true,
                hoist_funs: false,
                hoist_vars: false,
                warnings: false,
            },*/
            /*mangle: false,
            outSourceMap: false,
            basePath: '../www',
            sourceRoot: '/'*/
        }))
        .pipe(rename({
            suffix: '.min'
        }))
        .pipe(gulp.dest('../public/alpha/scripts/'));

    return merge(
        miniPublic
    );
});

//css生成压缩版css
gulp.task('cssmin', function() {
    var miniPublic = gulp.src('../public/alpha/styles/common.css')
        .pipe(nano())
        .pipe(rename({
            suffix: '.min'
        }));

    var miniBrick = gulp.src('../Brick/static/common/css/qz_common.css')
        .pipe(nano())
        .pipe(rename({
            suffix: '.min'
        }));

    return merge(
        miniPublic, miniBrick
    );
});

//less生成压缩版css
gulp.task('lessmin', function() {
    return gulp.src('./css/*.less')
        .pipe(less({
            paths: [path.join(__dirname, 'css')],
            plugins: [cleancss]
        }))
        .pipe(gulp.dest('css'))
        .pipe(browserSync.stream({
            match: "**/*.css"
        }));
});

//生成css
gulp.task('less', function() {
    return gulp.src('./css/**/*.less')
        .pipe(less({
            paths: [path.join(__dirname, 'css')]
        }))
        .pipe(gulp.dest('css'))
        .pipe(browserSync.stream({
            match: "**/*.css"
        }));
});

gulp.task('cleanCssFiles', function() {
    // Specify the directories to clean.
    return gulp.src(['./css/**/*.css'], {
            read: false
        })
        // Clean them.
        .pipe(clean());
});

//不明白不要使用
/*
这个任务的目的是收集整个网站的所有静态文件，方便gulp打包处理css／js／images文件
注意：如果static_root目录存在，网站将会读取该目录的静态文件。
 */
gulp.task('run:collectstatic', function() {
    var collectstatic = function() {
        var deferred = Q.defer();
        var cmd = '. ../pin_venv/bin/activate';
        exec(cmd + ' && python ../manage.py collectstatic --noinput', function(error, stdout, stderr) {
            console.log('collectstatic=', stdout.toString());
            //0 static files copied to '/Users/admin/Pinbot/static_root', 1976 unmodified.
            if (error === null) {
                var num = 0;
                if (stdout.toString().match(/([0-9]+) static files/i)) {
                    num = parseInt(RegExp.$1);
                    if (num == 0) {
                        if (stdout.toString().match(/([0-9]+) unmodified/i)) {
                            num = parseInt(RegExp.$1);
                        }
                    }
                }
                deferred.resolve({
                    num: num
                });
            }
        });
        return deferred.promise;
    };
    var allPromise = Q.all([
        collectstatic()
    ]);
    allPromise.then(function(data) {
        console.log('finished', data);
        return deferred.promise;
    }, function(data) {
        console.log('error', data);
        return deferred.promise;
    });
    //return proc;
});
//start django server
gulp.task('runserver:python', function() {
    var cmd = '. ../pin_venv/bin/activate';
    var proc = exec(cmd + ' && python ../manage.py migrate && python ../manage.py runserver');
    return proc;
});
//watch django server
gulp.task('django', ['runserver:python'], function() {
    var bs = browserSync({
        notify: false,
        proxy: "0.0.0.0:8000"
    });
});

//check python compress
gulp.task('checkCompress:python', function() {
    var cmd = '. ../pin_venv/bin/activate';
    var proc = exec(cmd + ' && python ../manage.py compress --false');
    return proc;
});

var chgdFiles = {};
var chgdCss = {};
var chgdLess = {};

//watch:Django时是否压缩css/js
var isCompress = true;

//Django文件监控(压缩)
//gulp watch:Django --src=yes/no
gulp.task('watch:Django', function() {

    if (typeof argv.src == 'string' && argv.src.match(/^(yes|no)$/i)) isCompress = (RegExp.$1.match(/^yes$/i)) ? false : true;
    if(isCompress){
        console.log('［压缩模式］');
    }else{
        console.log('［非压缩模式］');
    }
    console.log('请注意：push／pull代码时请暂停watch:Django文件监控［Ctrl + c］');
    browserSync.init({
        server: {
            baseDir: "../",
            directory: true
        },
        //不弹窗
        open: false,
        //notify: false
        //startPath: "/index.html"
        //scrollProportionally: false // Sync viewports to TOP position
        //scrollThrottle: 100 // only send scroll events every 100 milliseconds
        //https://www.browsersync.io/docs/options/
        port: 3031
    });
    //Default: ['add', 'change', 'unlink']
    gulp.watch("../**/*.html").on("change", function(chg) {
        console.log('watch', chg);
        gulp.start('dev', function(done) {
            browserSync.reload();
        });
    });
    //如果文件有修改，编译less到目录
    gulp.watch("./css/**/*.less").on("change", function(chg) {
        console.log('watch', chg);
        gulp.start('dev', function(done) {
            browserSync.reload();
        });
    });
    //如果文件有修改，编译less到public目录(同一个目录less=>css)
    gulp.watch("./public/**/*.less").on("change", function(chg) {
        console.log('watch', chg);
        if (chg.type == 'changed') {
            //有文件被修改
            chgdLess = chg;
            gulp.start('deploy_local_less', function(done) {
                browserSync.reload();
            });
        }
    });
    //如果文件有修改，发布页面css代码
    gulp.watch("./public/**/*.css").on("change", function(chg) {
        console.log('watch', chg);
        if (chg.type == 'changed') {
            //有文件被修改
            chgdCss = chg;
            gulp.start('deploy_local_css', function(done) {
                browserSync.reload();
            });
        }
    });
    //如果文件有修改，发布angularjs公用库代码
    gulp.watch("./ng-lib/**/*.js").on("change", function(chg) {
        gulp.start('deploy_local_ng_lib', function(done) {
            browserSync.reload();
        });
    });
    //如果文件有修改，发布页面js代码
    gulp.watch("./public/**/*.js").on("change", function(chg) {
        //{ type: 'changed', path: '' }
        console.log('watch', chg);
        if (chg.type == 'changed') {
            //有文件被修改
            chgdFiles = chg;
            gulp.start('deploy_local_ng_js', function(done) {
                browserSync.reload();
            });
        }

    });
});
//如果文件有修改，同步最新less到目录 ./public/ to ./public/
gulp.task('deploy_local_less', ['dev'], function() {
    console.log('deploy_local_less');
    var all;
    var chgdFiles = chgdLess;
    if (chgdFiles.path != undefined && chgdFiles.path != null && chgdFiles.path.match(/\.(less)$/i)) {
        if (chgdFiles.path.match(/^(.*)\/([^\/]+)$/i)) {
            var basePath = RegExp.$2;
            var destDir = RegExp.$1 + '/';
            if (chgdFiles.path.match(/^(.+)\/frontend_dev\/public\/(.+)\/([^\/]+)$/i)) {

                //console.log('destDir', basePath, destDir);
                var go = function() {
                    var deferred = Q.defer();
                    gulp.src(chgdFiles.path)
                        .pipe(less({
                            paths: [destDir]
                        }))
                        .pipe(gulp.dest(destDir))
                        .pipe(browserSync.stream({
                            match: "**/*.css"
                        }));

                    return deferred.promise;
                };
                var allPromise = Q.all([
                    go()
                ]);
                allPromise.then(function(data) {
                    console.log('finished', data, '../public/' + data[0].destDir + data[0].basePath);

                    return deferred2.promise;
                }, function(data) {
                    console.log('error', data);
                    return deferred.promise;
                });

            }
        }
    }
});
//如果文件有修改，同步最新css到目录 ./public/ to ../public/
gulp.task('deploy_local_css', function() {
    var all;
    var chgdFiles = chgdCss;
    if (chgdFiles.path != undefined && chgdFiles.path != null && chgdFiles.path.match(/\.(css)$/i) && !chgdFiles.path.match(/\.min\.(css)$/i)) {
        if (chgdFiles.path.match(/^(.*)\/([^\/]+)$/i)) {
            var basePath = RegExp.$2;
            var destDir = '';
            if (chgdFiles.path.match(/^(.+)\/frontend_dev\/public\/(.+)\/([^\/]+)$/i)) {
                destDir = RegExp.$2 + '/';
                console.log('destDir', basePath, '../public/' + destDir);


                var go = function() {
                    var deferred = Q.defer();
                    gulp.src(chgdFiles.path)
                        .pipe(gulpif(isCompress, minifyCss({
                            compatibility: 'ie9'
                        })))
                        .pipe(gulp.dest('../public/' + destDir))
                        .on('end', function() {
                            //console.log('end ');
                            deferred.resolve({
                                destDir: destDir,
                                basePath: basePath
                            });
                        });
                    return deferred.promise;
                };
                var allPromise = Q.all([
                    go()
                ]);
                allPromise.then(function(data) {
                    console.log('finished', data, '../public/' + data[0].destDir + data[0].basePath);
                    //貌似无效，生成min.css也有点多余
                    /*var deferred2 = Q.defer();
                    gulp.src('../public/' + data[0].destDir + data[0].basePath)
                        .pipe(nano())
                        .pipe(rename({
                            suffix: '.min'
                        }))
                        .on('end', function() {
                            console.log('end deferred2');
                            deferred2.resolve(true);
                        });*/
                    return deferred2.promise;
                }, function(data) {
                    console.log('error', data);
                    return deferred.promise;
                });


            }
        }
    }
});
//发布页面js代码 ./public/ to ../public/
gulp.task('deploy_local_ng_js', function() {
    var all;
    if (chgdFiles.path != undefined && chgdFiles.path != null && chgdFiles.path.match(/\.(js)$/i) && !chgdFiles.path.match(/\.min\.(js)$/i)) {
        if (chgdFiles.path.match(/^(.*)\/([^\/]+)$/i)) {
            var basePath = RegExp.$2;
            var destDir = '';
            if (chgdFiles.path.match(/^(.+)\/frontend_dev\/public\/(.+)\/([^\/]+)$/i)) {
                destDir = RegExp.$2 + '/';
                console.log('destDir', '../public/' + destDir + basePath);
                all = gulp.src([
                    chgdFiles.path
                ])
                    .pipe(gulpif(isCompress, ngmin({
                        dynamic: false
                    })))
                    .pipe(gulpif(isCompress, uglify({
                        output: {
                            beautify: false
                        },
                        mangle: true,
                        outSourceMap: false,
                        basePath: basePath,
                        sourceRoot: '/'
                    })))
                    .pipe(gulp.dest('../public/' + destDir));
            }
        }
    }
    return merge(
        all
    );
});
//发布angularjs公用库代码 ./ng-lib/ to ../Brick/static/brick/utils/
gulp.task('deploy_local_ng_lib', function() {
    var all = gulp.src([
            './ng-lib/django.js',
            './ng-lib/filter.js',
            './ng-lib/service.js',
            './ng-lib/ng_config.js'
        ])
        .pipe(gulpif(isCompress, ngmin({
            dynamic: false
        })))
        .pipe(gulpif(isCompress, uglify({
            output: {
                beautify: false
            },
            /*compress: {
                sequences: true,
                booleans: true,
                conditionals: true,
                hoist_funs: false,
                hoist_vars: false,
                warnings: false,
            },*/
            mangle: true,
            outSourceMap: false,
            basePath: '../Brick/static/brick/utils/',
            sourceRoot: '/'
        })))
        .pipe(gulp.dest('../Brick/static/brick/utils/'))
    return merge(
        all
    );
});

//文件监控
gulp.task('serve', function() {
    browserSync.init({
        server: {
            baseDir: "./",
            directory: true
        }
    });
    gulp.watch("*.html").on("change", function() {
        gulp.start('dev', function(done) {
            browserSync.reload();
        });
    });
    gulp.watch("./css/**/*.less").on("change", function() {
        gulp.start('dev', function(done) {
            browserSync.reload();
        });
    });
    gulp.watch("./js/new/**/*.js").on("change", function() {
        gulp.start('dev', function(done) {
            browserSync.reload();
        });
    });
});

gulp.task('reload', function() {
    browserSync.init({
        server: {
            baseDir: "./",
            directory: true
        }
    });
    browserSync.reload
});

gulp.task('gallery', function() {
    browserSync.init({
        server: {
            baseDir: "./temp/",
            directory: true
        }
    });
    //browserSync.reload
});

gulp.task('framework', function() {
    browserSync.init({
        server: {
            baseDir: "./demo/",
            directory: false
        }
    });
    //browserSync.reload
    gulp.watch("./demo/**/*.html").on("change", function() {
        browserSync.reload();
    });
    gulp.watch("./demo/**/*.css").on("change", function() {
        browserSync.reload();
    });
    gulp.watch("./demo/**/*.js").on("change", function() {
        browserSync.reload();
    });

});

//////////////////// js相关
//输出 angular.js
gulp.task('angular', function() {
    var angular = gulp.src('./node_modules/angular/angular.js')
        .pipe(gulp.dest('./vendor/'));

    /*var angularmap = gulp.src('./node_modules/angular/angular.min.js.map')
        .pipe(gulp.dest('./vendor/'));*/

    var angular_ui_router = gulp.src('./node_modules/angular-ui-router/release/angular-ui-router.js')
        .pipe(gulp.dest('./vendor/'));

    var angular_mocks = gulp.src('./node_modules/angular-mocks/angular-mocks.js')
        .pipe(gulp.dest('./vendor/'));

    return merge(
        angular
        //, angularmap
        , angular_ui_router, angular_mocks
    );
});

//注意原始js文件只复制一次，以免覆盖修改后的的文件
gulp.task('signup', function() {
    var notCZ = function(dir, fn) {
        var deferred = Q.defer();
        fs.stat('./js/' + dir + '/' + fn, function(err, stat) {
            if (err == null) {
                console.log('Exists');
                //deferred.reject('Exists');
            } else {
                console.log('not Exists');
                //console.log(err.code);
                deferred.resolve({
                    dir: dir,
                    fn: fn
                });
            }
        });
        return deferred.promise;
    };

    /*notCZ('beta/scripts', 'lib.js').then(function(data){
        return gulp.src('../public/' + data.dir + '/' + data.fn)
                .pipe(gulp.dest('./js/' + data.dir + '/'));
    }).then(function(data){
        console.log('data',data);
    });*/

    var allPromise = Q.all([
        notCZ('beta/scripts', 'lib.js'),
        notCZ('alpha/scripts', 'jquery.form.js'),
        notCZ('alpha/scripts', 'jquery.validate.js'),
        notCZ('alpha/scripts', 'common.js'),
        notCZ('users/scripts', 'form.js')
    ]);
    allPromise.then(function(data) {
        for (var f in data) {
            gulp.src('../public/' + data[f].dir + '/' + data[f].fn)
                .pipe(gulp.dest('./js/' + data[f].dir + '/'));
        }
        console.log('updated');
        return deferred.promise;
    }, function(data) {
        console.log('error', data);
        return deferred.promise;
    });

    /*var lib = getStream('beta/scripts', 'lib.js');
    var jquery_form = getStream('alpha/scripts', 'jquery.form.js');
    var jquery_validate = getStream('alpha/scripts', 'jquery.validate.js');*/

    /*var jquery_form = gulp.src('../public/alpha/scripts/jquery.form.js')
        .pipe(gulp.dest('./js/alpha/scripts/'));

    var jquery_validate = gulp.src('../public/alpha/scripts/jquery.validate.js')
        .pipe(gulp.dest('./js/alpha/scripts/'));

    var common = gulp.src('../public/alpha/scripts/common.js')
        .pipe(gulp.dest('./js/alpha/scripts/'));

    var form = gulp.src('../public/users/scripts/form.js')
        .pipe(gulp.dest('./js/users/scripts/')); */

    /*return merge(
        lib
        //, jquery_form, jquery_validate
        , common
        , form
    );*/

});

////////////////////////////

//同步最新sprite图片到正式目录
gulp.task('updateSprite', function() {
    //http://192.168.199.114:8000/static/b_index/img/logo_162x48.png
    var sprite = gulp.src('./img/sprite.png')
        .pipe(gulp.dest('../public/b_index/img/'));
    return merge(
        sprite

    );
});

//正式发布
gulp.task('deploy', [
    'cleanCssFiles'
    //, 'less'
    , 'lessmin'
]);
//引入相关第三方文件（方便测试）、旧的文件
gulp.task('import', [
    'angular' //ng相关、mock脚本
    , 'signup' //注册所需的旧文件
]);
//重新发布测试环境
gulp.task('dev', [
    'cleanCssFiles', 'less'
]);
//启动默认开发环境： gulp
gulp.task('default', [
    'dev', 'serve' //启动本地测试服务器
]);