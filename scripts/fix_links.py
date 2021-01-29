import csv
import logging
from pathlib import Path, PurePath
from typing import Dict

from rich.console import Console
from rich.logging import RichHandler


console = Console()


# Set logger using Rich: https://rich.readthedocs.io/en/latest/logging.html
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")

ORGANICLINKS_URL = 'https://www.organicdivision.org/organicsyntheticfaculty/'
CSV_COLUMNS = ['primary_investigator', 'school',
               'state', 'city', 'institute_carnegie_classification',
               'website', 'research_interest', 'postdoc_wanted', 'source'
               ]
ORGANICLINKS_CSV_FILENAME = 'data/organiclinks_website_extraction.csv'
LINK_CHECK_FILENAME = 'data/link_check_report.csv'

TARGET_CSV = 'data/organiclinks_db.csv'
TARGET_CSV_MODIFIED = 'data/organiclinks_db.csv'
REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}


def fix_links():
    checked_url_directory = load_checked_url_directory()
    # console.log(checked_url_directory)

    changed_links = []
    with open(Path(TARGET_CSV_MODIFIED).resolve(), 'r') as f_in:
        dict_reader = csv.DictReader(f_in)
        fieldnames = dict_reader.fieldnames
        data = list(dict_reader)

    # console.log(f'{data=}')

    with open(Path(TARGET_CSV_MODIFIED).resolve(), 'w') as f_out:
        dict_writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        dict_writer.writeheader()
        for row in data:
            url_in_report = checked_url_directory.get(row['website'])
            # console.log(f'{url_in_report=}')
            if url_in_report and url_in_report['status_code'].startswith('30'):
                new_url = url_in_report['redirected_url']
                changed_links.append((row['website'], new_url))
                row['website'] = new_url

            dict_writer.writerow(row)

    # Report to console
    console.log(f'Number of links changes: {len(changed_links)}')
    console.log('Details:')
    for old_link, new_link in changed_links:
        console.log(f'\t{old_link} --> {new_link}')


def load_checked_url_directory() -> Dict:
    """ Load dict for directory file to rename files """
    files = [LINK_CHECK_FILENAME]
    links_directory = {}
    for file in files:
        with open(Path(file).resolve(), 'r') as f:
            dict_reader = csv.DictReader(f)
            [url, *fields] = dict_reader.fieldnames
            links_directory.update({
                row[url]: {field: row[field] for field in ['status_code', 'redirected_url']}
                for row in dict_reader
            })
    return links_directory


if __name__ == "__main__":
    fix_links()
