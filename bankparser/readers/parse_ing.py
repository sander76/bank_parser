import logging

from bankparser.helpers import get_day, make_mutation
from bankparser.readers.parser import Parser

LOGGER = logging.getLogger(__name__)

ING_COL_ACCOUNT = 2
ING_COL_SIGN = 5
ING_COL_AMOUNT = 6
ING_COL_DESC = 8
ING_COL_DATE = 0
ING_COL_OTHER = 3
ING_COL_NAME = 1

ING_DELIMITER = '","'
ING_SIGN_MINUS = "af"
ING_SIGN_ADDED = "bij"


def parse_date(date) -> (str, str, str):
    """Chop a ing date string to year, month, day
    """
    year = date[0:4]
    month = date[4:6]
    day = date[6:]
    return year, month, day


class IngParser(Parser):

    @staticmethod
    def parse_amount(amount: str, sign):
        """Comma character is used as decimal separator."""

        sign = sign.lower()

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

        if sign == ING_SIGN_MINUS:
            val = -val
        elif sign == ING_SIGN_ADDED:
            pass
        else:
            raise Exception("incorrect minus sign")
        return val

    def find_cols(self, line):
        cols = line.split(ING_DELIMITER)

        return (
            cols[ING_COL_DATE][1:],
            cols[ING_COL_DESC],
            cols[ING_COL_ACCOUNT],
            cols[ING_COL_OTHER],
            cols[ING_COL_NAME],
            cols[ING_COL_AMOUNT],
            cols[ING_COL_SIGN],
        )

    def parse(self, line: str):
        """Parse incoming line from ING format"""

        LOGGER.debug("Parsing line: %s", line)

        date, desc, account, other, name, amount, sign = self.find_cols(line)

        amount = self.parse_amount(amount, sign)

        new_mutation = make_mutation(account, amount, other, name, desc)

        mutations = get_day(self.parsed, *parse_date(date))

        # self.label_mutation(new_mutation, self.labels)

        if new_mutation not in mutations:

            LOGGER.debug("Adding mutation: %s", new_mutation)
            mutations.append(new_mutation)

        else:
            LOGGER.info("Skipping mutation: %s", new_mutation)
