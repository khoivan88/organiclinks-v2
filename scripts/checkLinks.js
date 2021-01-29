const hyperlink = require('hyperlink')
const storeData = require('./fileOps').storeData;
const rootUrl = 'https://www.organicdivision.org';
const canonicalRoot = rootUrl;
const inputUrl = 'https://www.organicdivision.org/organicsyntheticfaculty/'

(async () => {
  try {
    await hyperlink(
      {
        root: rootUrl,
        canonicalRoot: canonicalRoot,
        inputUrls: inputUrls,
        // followSourceMaps: followSourceMaps,
        // recursive: commandLineOptions.recursive,
        // internalOnly: commandLineOptions.internal,
        // pretty: commandLineOptions.pretty,
        // skipFilter,
        // todoFilter,
        // verbose: commandLineOptions.verbose,
        // concurrency: commandLineOptions.concurrency,
        // memdebug: commandLineOptions.debug,
      },
      t
    );
  } catch (err) {
    console.log(err.stack);
    process.exit(1);
  }
  const results = t.close();

  process.exit(results.fail ? 1 : 0);
})();
