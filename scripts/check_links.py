import csv
import logging
import requests
from multiprocessing import Pool
from datetime import datetime

from pathlib import Path, PurePath
from typing import Dict

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress

console = Console()


# Set logger using Rich: https://rich.readthedocs.io/en/latest/logging.html
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")

CSV_COLUMNS = ['url', 'status_code', 'reason', 'redirected_url', 'date_checked']
CSV_FILENAME = 'data/organiclinks_db'
TARGET_CSV = f'{CSV_FILENAME}.csv'
REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}

DATETIME_FORMAT = '%Y-%m-%dT%X'


def check_links():
    # Get all of the links in databases
    links = get_organiclinks_links()
    # console.log(f'Links in OrganicLinks: {links}')

    pool_size = 25
    # Ref: https://github.com/willmcgugan/rich/issues/121
    with Progress() as progress:
        task_id = progress.add_task("[cyan]Completed...", total=len(links))

        try:
            with Pool(processes=pool_size) as p:
                results = p.imap(check_link,
                                 links,
                                 chunksize=8)
                with open(Path('data/link_check_report.csv').resolve(), 'w') as f_out:
                    dict_writer = csv.DictWriter(f_out, fieldnames=CSV_COLUMNS)
                    dict_writer.writeheader()
                    for result in results:
                        progress.advance(task_id)
                        if result:
                            dict_writer.writerow(result)

        except Exception as error:
            log.exception(error)


def get_organiclinks_links():
    links = set()
    with open(Path(TARGET_CSV).resolve(), 'r') as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            links.add(row['website'])
    return links


def check_link(link: str):
    result = {'url': link,
              'status_code': '',
              'reason': '',
              'date_checked': datetime.now().strftime(DATETIME_FORMAT)
              }
    try:
        # console.log(f'{link=}')
        r = requests.get(link,
                         stream=True,    # to get only the response header, otherwise the whole page will be downloaded
                         timeout=3, headers=REQUEST_HEADERS,
                        #  verify=False
                         )
        if r.status_code in [400, 404, 403, 408, 409, 501, 502, 503]:
            result.update({'status_code': r.status_code,
                           'reason': r.reason,
                           })
        elif r.history:
            redirected_url = r.url
            # console.log(f'{r.status_code}-{r.reason}: {link} --> {redirected_url}')
            result.update({'status_code': r.history[0].status_code,
                           'reason': r.history[0].reason,
                           'redirected_url': redirected_url
                           })

    except Exception as error:
        error_message = str(error)
        result.update({'reason': error_message})

    finally:
        if (result['reason']
            or (result['status_code'] and result['status_code'] != 200)):
            return result


if __name__ == "__main__":
    check_links()
