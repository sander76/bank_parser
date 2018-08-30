import json
import logging
from csv import DictReader

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


def get_daily_transations(bank_data):
    for year, months in bank_data.items():
        for month, days in months.items():
            for day, transactions in days.items():
                yield year, month, day, transactions


def load_json(fname) -> dict:
    """Load a json file"""
    with open(fname) as f:
        _js = json.load(f)

    return _js

def load_csv_to_dict(fname) ->list:
    """Load a csv file into a dict."""
    with open(fname) as fl:
        dct = DictReader(fl)
        return list(dct)


def unique_accounts(bank_data: dict,output_file):
    """Extract unique accounts out of all parsed accounts.
    Convenience method for labelling accounts later."""
    all_transactions = []

    def is_in_all_transactions(transaction):
        for _trans in all_transactions:
            if _trans[KEY_OTHER] == transaction[KEY_OTHER]:
                return True
        return False

    for year, month, day, transactions in get_daily_transations(bank_data):
        for transaction in transactions:
            if not is_in_all_transactions(transaction):
                all_transactions.append(transaction)

    out = []
    for _trans in all_transactions:
        out.append((_trans[KEY_OTHER], _trans[KEY_DESC]))

    with open(output_file,'w') as fl:
        json.dump(out,fl)


def get_transactions(dct):
    for year, months in dct.items():
        for month, days in months.items():
            for day, transactions in days.items():
                for transaction in transactions:
                    yield year, month, day, transaction