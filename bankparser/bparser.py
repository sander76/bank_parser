"""Main entry point."""
import logging

from bankparser.helpers import load_json
from bankparser.readers.parse_ing import IngParser
from bankparser.readers.parser import save_file

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    dct = {}

    folder = "../test/csv/ing"
    label_location = "../test/csv/labels.json"
    labels = load_json(label_location)

    ing_parser = IngParser(dct, labels, folder, skip_lines=1)

    ing_parser.process_folder()

    save_file("c:\\temp\\out.json", dct)
