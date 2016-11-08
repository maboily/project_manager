'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var watch = require('gulp-watch');

gulp.task('sass', function () {
    return gulp.src('./sass/app.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./static/'));
});

gulp.task('sass:watch', function() {
    watch('./sass/**/*.scss', function () {
        gulp.start('sass');
    });
})