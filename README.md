![11ty-build](https://github.com/khoivan88/organiclinks-v2/workflows/11ty-build/badge.svg)
![CI Check links and Build](https://github.com/khoivan88/organiclinks-v2/workflows/CI%20Check%20links%20and%20Build/badge.svg)


# organiclinks-v2

This is a new workflow for [OrganicLinks page](https://www.organicdivision.org/organicsyntheticfaculty/).

It does several of these things:

- Use Google Sheet as the Content Management System (CMS). The info can be edited directly on the google sheet and "published" to generate the new HTML content. The Google Sheet is [here](https://docs.google.com/spreadsheets/d/1_9Y1I1gU1isijy3ljXOKA8C2NM5mbM5tqDEwI6tuWC8/edit#gid=0). The instructrion on how to use the Google Sheet can be found on the [2nd sheet](https://docs.google.com/spreadsheets/d/1_9Y1I1gU1isijy3ljXOKA8C2NM5mbM5tqDEwI6tuWC8/edit#gid=374082547)
  - Specifically, the use of Google Sheet allows for multiple collaborators to be able to edit the info inside the google sheet. The google app script is used to accomplish many tasks:
    1. Update the google sheet with the latest info from the CSV file inside the GitHub repo;
    2. Create a custom button so that a collaborate can "Publish" their changes after changing the content of the google sheet (under the hood, the google app script commit any of the changes into the GitHub repo);
    3. Notify collaborators (users of google sheet) when the commit is done as well as when the sheet content is updated.
    4. Automatically add current date for `postdoc_ads_added_date` if `postdoc_wanted` is `true`
    5. Automatically add expiration date (default to 60 days in the future from the `postdoc_ads_added_date`) if `postdoc_wanted` is `true`
- 11ty build has the following features:
  - Sort the faculty list by alphabetical states then alphabetical school names. TODO: sort faculty's names alphabetically using 11ty build regardless of the order in the csv database
  - Automatically add 'Postdoc Wanted' and link to ads if `postdoc_wanted` is `true`
  - Automatically remove 'Postdoc Wanted' link after the expiration date
- Automatic checking of broken links and redirected links (by Github Action running specifc python scripts). The result of this check is save in the [link-check-report file](data/link_check_report.csv)
- If there is any redirected link, the 11ty build process will automatically build a new html page for [OrganicLinks page](https://www.organicdivision.org/organicsyntheticfaculty/). The resulted HTML page is at [`_site/organicsyntheticfaculty.html`](_site/organicsyntheticfaculty.html)
- Any changes to the [OrganicLinks database](data/organiclinks_db.csv) will also trigger a new 11ty build.
