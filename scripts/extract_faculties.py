import csv
import logging
import re
from pathlib import Path, PurePath
from typing import Dict
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.logging import RichHandler

console = Console()


# Set logger using Rich: https://rich.readthedocs.io/en/latest/logging.html
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")

CSV_COLUMNS = [
    'primary_investigator', 'school', 'institute_carnegie_classification',
    'website', 'research_interest', 'postdoc_wanted', 'postdoc_ads_link', 'source']
ORGANICLINKS_URL = 'https://www.organicdivision.org/organicsyntheticfaculty/'
ORGANICLINKS_PUI_URL = 'https://organiclinkspui.net/'


CURRENT_PATH = Path(__file__).resolve().parent
DATA_FOLDER = CURRENT_PATH.parent / 'data'


def extract_faculties_from_organiclinks(filename: str):
    """ Prepare the csv file of problem sets and info from 'https://www.organicdivision.org/organicsyntheticfaculty/'

    It does:
    1. Go to the VOT problem set website
    2. Extract each internal link and its info
    3. Create csv file with the info above
    4. Copy the original files into the staging dir for convertion to files used by 11ty
    """

    try:
        r = requests.get(ORGANICLINKS_URL)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(r.text)

        data = []

        faculties = soup.select('ul.faclist li')
        # print(f'{faculties=}')
        for li in faculties:
            faculty_name, _, school = li.text.replace('  ', ' ').partition(',')
            faculty_name = faculty_name.strip()

            # Extract postdoc_wanted and postdoc_ads_link if exists
            re_postdoc = re.compile(r'\s*postdoc wanted', re.IGNORECASE)
            postdoc_wanted = bool(re_postdoc.search(school)) or None
            postdoc_ads_link = li.find('a', string=re_postdoc)['href'] if postdoc_wanted else None

            school = re_postdoc.sub('', school).strip()
            # print(faculty_name, end='')
            website = li.a["href"]
            # print(f', website: {website}')

            line = {key: '' for key in CSV_COLUMNS}
            line.update({
                'primary_investigator': faculty_name,
                'school': school,
                'website': website,
                'research_interest': 'synthetic organic',
                'postdoc_wanted': postdoc_wanted,
                'postdoc_ads_link': postdoc_ads_link,
                'source': ORGANICLINKS_URL,
            })
            data.append(line)

        write_csv(filename, data)

    except Exception as error:
        log.exception(error)


def extract_faculties_from_organiclinkspui(filename: str):
    """ Prepare the csv file of problem sets and info from 'https://www.organicdivision.org/organicsyntheticfaculty/'

    It does:
    1. Go to the VOT problem set website
    2. Extract each internal link and its info
    3. Create csv file with the info above
    4. Copy the original files into the staging dir for convertion to files used by 11ty
    """

    try:
        r = requests.get(ORGANICLINKS_PUI_URL)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(r.text)

        data = []

        faculties = soup.find_all(li_no_attributes_and_containing_anchor)
        # print(f'{faculties=}')
        for li in faculties:
            faculty_name, _, school = li.text.replace('  ', ' ').partition(',')
            faculty_name = faculty_name.strip()
            school = school.strip()
            # print(faculty_name, end='')
            website = li.a["href"]
            # print(f', website: {website}')

            line = {key: '' for key in CSV_COLUMNS}
            line.update({
                'primary_investigator': faculty_name,
                'school': school,
                'website': website,
                'source': ORGANICLINKS_PUI_URL,
                'institute_carnegie_classification': 'PUI',
            })
            data.append(line)

        write_csv(filename, data)

    except Exception as error:
        log.exception(error)


def li_no_attributes_and_containing_anchor(tag):
    return (tag.name == 'li'
            and not tag.attrs
            and tag.a)


def write_csv(filename, data: Dict) -> None:
    try:
        with open(filename, 'w', newline='\n', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
    except IOError:
        print("I/O error")


if __name__ == "__main__":
    now = datetime.now()

    # organiclinks_csv_filename = f'organiclinks_website_extraction-{now.strftime("%Y-%m-%d")}.csv'
    organiclinks_csv_filename = DATA_FOLDER / 'organiclinks_website_extraction.csv'
    extract_faculties_from_organiclinks(organiclinks_csv_filename)

    # organiclinks_csv_filename = f'organiclinks_pui_website_extraction-{now.strftime("%Y-%m-%d")}.csv'
    # organiclinks_csv_filename = f'organiclinks_pui_website_extraction.csv'
    # extract_faculties_from_organiclinkspui(organiclinks_csv_filename)
