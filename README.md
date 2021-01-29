# organiclinks-v2

This is a new workflow for [OrganicLinks page](https://www.organicdivision.org/organicsyntheticfaculty/).

It does several of these things:

- Automatic checking of broken links and redirected links. The result of this check is save in the [link-check-report file](data/link_check_report.csv) (to be implemented)
- If there is any redirected link, the 11ty build process will automatically build a new html page for [OrganicLinks page](https://www.organicdivision.org/organicsyntheticfaculty/). The resulted HTML page is at [`_site/organicsyntheticfaculty.html`](_site/organicsyntheticfaculty.html)
- Any changes to the [OrganicLinks database](data/organiclinks_db.csv) will also trigger a new 11ty build.
