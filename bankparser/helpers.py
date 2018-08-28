import json
import logging
import os

from bankparser.constants import KEY_ACCOUNT, KEY_AMOUNT, KEY_OTHER, KEY_DESC

LOGGER = logging.getLogger(__name__)


def get_day(data: dict, year: str, month: str, day: str) -> list:
    """Get the list of transactions for a specific year, month and day."""
    _year = data.get(year)
    if _year is not None:
        _month = data[year].get(month)

        if _month is not None:
            _day = data[year][month].get(day)

            if _day is not None:
                return _day
            else:
                data[year][month][day] = []
        else:
            data[year][month] = {}
    else:
        data[year] = {}
    return get_day(data, year, month, day)


def make_mutation(account, amount, other, desc):
    """create a dict containing one mutation."""
    # todo: validate incoming parameters

    return {
        KEY_ACCOUNT: account,
        KEY_AMOUNT: amount,
        KEY_OTHER: other,
        KEY_DESC: desc,
    }




def load_labels(fname) -> dict:
    """Load a json file"""
    with open(fname) as f:
        _js = json.load(f)

    return _js
