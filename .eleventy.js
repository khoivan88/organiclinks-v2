const yaml = require("js-yaml");

module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy('./src/admin');
  eleventyConfig.addDataExtension("yaml", contents => yaml.safeLoad(contents));
  return {
    dir: {
      input: 'src',
      // includes: '../_includes',
      // output: '_output',
    },
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
  };
};
