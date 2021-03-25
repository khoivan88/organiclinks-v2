const externalLinks = require('eleventy-plugin-external-links') // https://github.com/vimtor/eleventy-plugin-external-links

module.exports = function (eleventyConfig) {
  eleventyConfig.addPlugin(externalLinks, {
    // Plugin defaults:
    name: 'external-links',         // Plugin name
    regex: /^(([a-z]+:)|(\/\/))/i,  // Regex that test if href is external
    target: "_blank",               // 'target' attribute for external links
    rel: "noopener",                // 'rel' attribute for external links
    extensions: [".html"],          // Extensions to apply transform to
  })

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
