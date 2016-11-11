'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var livereload = require('gulp-livereload');

gulp.task('sass', function () {
    return gulp.src('./sass/app.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./static/'))
        .pipe(livereload());
});

gulp.task('sass:watch', function() {
    watch('./sass/**/*.scss', function () {
        gulp.start('sass');
    });
})

gulp.task('livereload', function() {
    livereload.listen({ start: true});

    // SASS
    watch('./sass/**/*.scss', function () {
        gulp.start('sass');
    });

    // Templates
    watch('../templates/**/*.html', function () {
        livereload.changed('../templates/');
    });
});