module.exports = function (eleventyConfig) {

  eleventyConfig.addFilter("dateFilter", function (value) {
    return new Date(value);
  });

  eleventyConfig.addFilter("expirationFilter", function (value) {
    let expirationDate = new Date(value);
    return Date.now() > expirationDate;
  });

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
