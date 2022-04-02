/**
 *  Welcome to your gulpfile!
 *  The gulp tasks are splitted in several files in the gulp directory
 *  because putting all here was really too long
 */

'use strict';

var gulp = require('gulp');
var fse = require('fs-extra');
var nodemon = require('gulp-nodemon');
/**
 *  This will load all js or coffee files in the gulp directory
 *  in order to load all gulp tasks
 */
fse.walkSync('./gulp').filter(function (file)
    {
        return (/\.(js|coffee)$/i).test(file);
    }
).map(function (file)
    {
        require('./' + file);
    }
);


/*wrench.readdirSyncRecursive('./gulp').filter(function(file) {
 return (/\.(js|coffee)$/i).test(file);
 }).map(function(file) {
 require('./gulp/' + file);
 });*/

/**
 *  Default task clean temporaries directories and launch the
 *  main optimization build task
 */
gulp.task('server', ['build'], function () {
    nodemon({
        script: './server.js',
        watch: false
    })
})

gulp.task('default', ['clean'], function ()
{
    gulp.start('build');
});
