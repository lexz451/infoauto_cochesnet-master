'use strict';

var path = require('path');
var gulp = require('gulp');
var conf = require('./conf');

var browserSync = require('browser-sync');
var browserSyncSpa = require('browser-sync-spa');

var util = require('util');

var proxyMiddleware = require('http-proxy-middleware');

function browserSyncInit(baseDir, browser, targetBackend) {
    browser = browser === undefined ? 'default' : browser;

    var routes = null;
    if (baseDir === conf.paths.src || (util.isArray(baseDir) && baseDir.indexOf(conf.paths.src) !== -1)) {
        routes = {
            '/bower_components': 'bower_components'
        };
    }

    var server = {
        baseDir: baseDir,
        routes: routes
    };

    /*
     * You can add a proxy to your backend by uncommenting the line below.
     * You just have to configure a context which will we redirected and the target url.
     * Example: $http.get('/users') requests will be automatically proxified.
     *
     * For more details and option, https://github.com/chimurai/http-proxy-middleware/blob/v0.9.0/README.md
     */

    server.middleware = proxyMiddleware('/api/**/*.json', {
        target: 'http://localhost:3000',
        // target: 'http://192.168.2.15:3000',
        secure: false,
        pathRewrite: {
            '^/api': '/'
        },
        changeOrigin: true
    });

    // var target=targetBackend || 'https://sail.artificialintelligencelead.com';
    // var target= "https://sail.artificialintelligencelead.com";
    var target = "http://infoauto-backend:8000";
    server.middleware = proxyMiddleware(['/api/**', '!**/*.json'], {
        target: target,
        secure: false,
        changeOrigin: false
    });

    browserSync.instance = browserSync.init({
        startPath: '/',
        server: server,
        browser: browser
    });
}

browserSync.use(browserSyncSpa({
    selector: '[ng-app]'// Only needed for angular apps
}));

gulp.task('serve', ['watch'], function () {
    browserSyncInit([path.join(conf.paths.tmp, '/serve'), conf.paths.src]);
});
gulp.task('serve:docker', ['watch'], function () {
    //browserSyncInit([path.join(conf.paths.tmp, '/serve'), conf.paths.src], null, 'https://sail.artificialintelligencelead.com');
    browserSyncInit([path.join(conf.paths.tmp, '/serve'), conf.paths.src], null, 'http://localhost:8000');
});

gulp.task('serve:dist', ['build'], function () {
    browserSyncInit(conf.paths.dist);
});

gulp.task('serve:e2e', ['inject'], function () {
    browserSyncInit([conf.paths.tmp + '/serve', conf.paths.src], []);
});

gulp.task('serve:e2e-dist', ['build'], function () {
    browserSyncInit(conf.paths.dist, []);
});
