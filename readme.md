

[![travis](https://travis-ci.org/sander76/bank_parser.svg?branch=master)](https://travis-ci.org/sander76/bank_parser.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/sander76/bank_parser/badge.svg?branch=master)](https://coveralls.io/github/sander76/bank_parser?branch=master)

# BankParser

Tool to load bank data and convert it to a monthly overview.


Work in progress.
Currently a startup file will look like this:

By default the tool wil look for a base folder along the following structure:

```python

import logging
from pathlib import Path

from bankparser.helpers import get_bank_data
from bankparser.post_processors.extract import Extract
from bankparser.post_processors.label import Label
from bankparser.readers.parse_ing import IngParser
from bankparser.readers.parse_rabo import RaboParser
from bankparser.readers.parser import save_file
from bankparser.reports.monthly_report import make_report

LOGGER = logging.getLogger(__name__)


def make_report_location(base_banking_folder: Path, year: str):
    return base_banking_folder.joinpath(
        "output/report_{}.txt".format(year)
    )


if __name__ == "__main__":
    bank_data = get_bank_data()

    base_banking_folder = Path(
        "~/base_bank_data_folder"
    )

    # CSV data containing ING bank csv data.
    csv_ing_folder = base_banking_folder.joinpath("csv\\ing")
    LOGGER.info("ING_FOLDER: %s", csv_ing_folder)

    ing_parser = IngParser(bank_data, csv_ing_folder, skip_lines=1)
    ing_parser.process_folder()

    # CSV data containing Rabo bank transaction data.
    csv_rabo_folder = base_banking_folder.joinpath("csv\\rabo")
    LOGGER.info("RABO Folder: %s", csv_rabo_folder)
    
    rabo_parser = RaboParser(bank_data, csv_rabo_folder, skip_lines=1)
    rabo_parser.process_folder()

    # The location to store one big dict containing all above banking data.
    out_location = base_banking_folder.joinpath("output/out.json")
    LOGGER.info("OUTPUT_FILE: %s", out_location)

    save_file(out_location, bank_data)

    # A post processor modifying the data dict.
    labeller = Label(bank_data, base_banking_folder)
    labeller.setup()
    labeller.process()

    extractor = Extract(bank_data,base_banking_folder)
    extractor.setup()
    extractor.process()

    # Output file contain the year.
    make_report(bank_data, "2018",
                make_report_location(base_banking_folder, "2018"))



```