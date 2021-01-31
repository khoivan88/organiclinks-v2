module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy('./src/admin');
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
