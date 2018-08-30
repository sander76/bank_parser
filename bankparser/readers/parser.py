import json
import logging
import os

from bankparser.constants import KEY_ACCOUNT, KEY_OTHER, KEY_LABEL, KEY_DESC
from bankparser.helpers import get_daily_transations, make_mutation

LOGGER = logging.getLogger(__name__)


def read_csv(csv_file):
    """Load a csv file and read the contents line by line"""
    LOGGER.debug("Opening file: %s", csv_file)
    with open(csv_file) as f:
        for line in f:
            yield line


def scan_folder(folder):
    """Scan a folder for csv files"""
    LOGGER.debug("Scanning folder: %s", folder)
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            yield os.path.join(folder, file)


def save_file(fname, data: dict):
    LOGGER.info("Save data to: %s", fname)
    with open(fname, "w") as f:
        json.dump(data, f)





class Parser:
    def __init__(self, parsed, csv_folder, skip_lines=0):
        self.parsed = parsed
        self.csv_folder = csv_folder
        self.skip_lines = skip_lines

    @staticmethod
    def parse_amount(amount: str, *args):
        pass


    def parse(self, line):
        pass

    def find_cols(self, line):
        pass

    def process_folder(self):
        for _file in scan_folder(self.csv_folder):
            reader = read_csv(_file)

            # The first line(s) of the CSV file might be a row with titles.
            # Skipping those.
            for i in range(self.skip_lines):
                next(reader)

            for line in reader:
                self.parse(line)
