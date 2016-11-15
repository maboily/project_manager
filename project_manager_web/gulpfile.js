'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var livereload = require('gulp-livereload');
var babel = require('gulp-babel');
var sourcemaps = require('gulp-sourcemaps');
var gutil = require('gulp-util');
var source = require('vinyl-source-stream');
var browserify = require('browserify');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var combiner = require('stream-combiner2');
var babelify = require('babelify');

gulp.task('sass', function () {
    return gulp.src('./sass/app.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./static/'))
        .pipe(livereload());
});

gulp.task('sass:watch', function () {
    watch('./sass/**/*.scss', function () {
        gulp.start('sass');
    });
});

gulp.task('js', function () {
    var b = browserify({
        entries: './js/app.js',
        debug: true
    });

    var combined = combiner(
        b.transform(babelify, {presets: ['es2015']}),
        b.bundle(),
        source('app.js'),
        buffer(),
        sourcemaps.init({loadMaps: true}),
        uglify(),
        sourcemaps.write('.'),
        gulp.dest('./static/')
    );

    combined.on('error', gutil.log);

    return combined;
});

gulp.task('js:watch', function () {
    watch('./js/**/*.js', function () {
        gulp.start('js');
    });
});

gulp.task('livereload', function () {
    livereload.listen({start: true});

    // SASS & JS
    gulp.start('sass:watch')
    gulp.start('js:watch');

    // Templates
    watch('../templates/**/*.html', function () {
        livereload.changed('/');
    });

    // Polymer
    watch('./static/polymer/**/*.html', function () {
        livereload.changed('/static/polymer/');
    });
});