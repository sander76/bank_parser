import logging

from bankparser.helpers import get_day, make_mutation
from bankparser.readers.parser import Parser

LOGGER = logging.getLogger(__name__)

RABO_COL_ACCOUNT = 0
RABO_COL_AMOUNT = 6
RABO_COL_DESC = 19
RABO_COL_DATE = 4
RABO_COL_OTHER = 8
RABO_COL_NAME = 9
RABO_DELIMITER = '","'


def parse_date(date) -> (str, str, str):
    """Chop a ing date string to year, month, day
    """
    year = date[0:4]
    month = date[5:7]
    day = date[8:]
    return year, month, day


class RaboParser(Parser):
    @staticmethod
    def parse_amount(amount: str):
        """Comma character is used as decimal separator."""

        val = []
        for _char in amount:
            if _char == ".":
                pass
            elif _char == ",":
                val.append(".")
            else:
                val.append(_char)
        val = "".join(val)
        val = float(val)

        return val

    def find_cols(self, line):
        cols = line.split(RABO_DELIMITER)

        return (
            cols[RABO_COL_DATE],
            cols[RABO_COL_DESC],
            cols[RABO_COL_ACCOUNT][1:],
            cols[RABO_COL_OTHER],
            cols[RABO_COL_NAME],
            cols[RABO_COL_AMOUNT],
        )

    def parse(self, line: str):
        """Parse incoming line from ING format"""

        LOGGER.debug("Parsing line: %s", line)

        date, desc, account, other,name, amount = self.find_cols(line)

        amount = self.parse_amount(amount)

        new_mutation = make_mutation(account, amount, other,name, desc)

        mutations = get_day(self.parsed, *parse_date(date))

        # self.label_mutation(new_mutation, self.labels)

        if new_mutation not in mutations:
            LOGGER.debug("Adding mutation: %s", new_mutation)
            mutations.append(new_mutation)
        else:
            LOGGER.info("Skipping mutation: %s", new_mutation)
