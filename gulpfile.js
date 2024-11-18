const path = require("path");
const { src, watch, dest, parallel } = require("gulp");
const sass = require("gulp-sass")(require("sass"));
const if_ = require("gulp-if");
const sourcemaps = require("gulp-sourcemaps");
const rename = require("gulp-rename");

const with_sourcemaps = () => !!process.env.DEBUG || !!process.argv[4];

const renamer = (path) => {
  const variant = process.argv[3];
  if (variant) {
    // convert main/main-rtl into green/green-rtl
    path.basename = path.basename.replace("main", variant.slice(2));
  }
  return path;
};


const build = () =>
  src([
    __dirname + "/ckanext/odn/public/scss/main.scss",
    __dirname + "/ckanext/odn/public/scss/main-rtl.scss",
  ])
    .pipe(if_(with_sourcemaps(), sourcemaps.init()))
    .pipe(sass({ outputStyle: 'expanded' }).on('error', sass.logError))
    .pipe(if_(with_sourcemaps(), sourcemaps.write()))
    .pipe(rename(renamer))
    .pipe(dest(__dirname + "/ckanext/odn/assets/css/"));


const watchSource = () =>
  watch(
    __dirname + "/ckanext/odn/public/scss/**/*.scss",
    { ignoreInitial: false },
    build
  );


const bootstrapScss = () =>
  src([__dirname + "/node_modules/bootstrap/scss/**/*",]).pipe(
    dest(__dirname + "/ckanext/odn/public/vendor/bootstrap/scss")
  );


exports.build = build;
exports.watch = watchSource;

exports.updateVendorLibs = parallel(
  bootstrapScss,
);
