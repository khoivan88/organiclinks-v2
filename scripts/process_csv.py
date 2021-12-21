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
               'website', 'research_interest',
               'postdoc_wanted', 'postdoc_ads_link', 'source'
               ]

CURRENT_PATH = Path(__file__).resolve().parent
DATA_FOLDER = CURRENT_PATH.parent / 'data'

PI_DETAILS_FILENAME = DATA_FOLDER / 'pi_details.csv'
# ORGANICLINKS_PUI_CSV_FILENAME = 'organiclinks_pui_website_extraction.csv'

ORGANICLINKS_CSV_FILENAME = DATA_FOLDER / 'organiclinks_website_extraction.csv'
# ORGANICLINKS_CSV_FILENAME = f'{ORGANICLINKS_CSV_FILENAME}.csv'
TARGET_CSV_MODIFIED = ORGANICLINKS_CSV_FILENAME.with_stem(f'{ORGANICLINKS_CSV_FILENAME.stem}_modified')
# TARGET_CSV_MODIFIED = f'{ORGANICLINKS_CSV_FILENAME}_modified.csv'
REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}


def process_csv():
    location_directory = load_location_directory()
    log.debug('Get info about Daniel Romo: ')
    log.debug(location_directory.get('Daniel Romo'.lower()))
    # log.debug('Get info about Brian Myers: ')
    # log.debug(location_directory.get('Brian Myers'.lower()))
    # log.debug(f'Info lookup directory size: {len(location_directory)}')
    # # console.log(location_directory)

    with open(Path(ORGANICLINKS_CSV_FILENAME).resolve(), 'r', newline='\r\n') as f_in, open(Path(TARGET_CSV_MODIFIED).resolve(), 'w', newline='\n') as f_out:
        dict_reader = csv.DictReader(f_in)
        fieldnames = CSV_COLUMNS
        dict_writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        dict_writer.writeheader()
        # count = 0
        for row in dict_reader:
            faculty = location_directory.get(row['primary_investigator'].lower())
            if faculty:
                # count += 1
                to_be_updated = ['school', 'state', 'city']
                for item in to_be_updated:
                    row[item] = faculty[item]

            dict_writer.writerow(row)
        # console.log(f'Number of faculties found in OrganicLinks: {count}')


def load_location_directory() -> Dict:
    """ Load dict for directory file to rename files """
    files = [PI_DETAILS_FILENAME]
    names_directory = {}
    for file in files:
        with open(Path(file).resolve(), 'r') as f:
            dict_reader = csv.DictReader(f)
            fields = dict_reader.fieldnames
            names_directory.update({
                row['primary_investigator'].lower(): {field: row[field] for field in fields}
                for row in dict_reader
            })
    return names_directory


if __name__ == "__main__":
    process_csv()
