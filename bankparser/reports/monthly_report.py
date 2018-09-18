"""
Year 2018
Month             1       2        3

account 3789215
plus          100.1   100.1
minus        1243.0    34.3
---------------------------------------------------------
total        - 99.9

savings account
plus        11123.2
minus        -333.5
---------------------------------------------------------
total       50000.0

account2
plus
minus
---------------------------------------------------------

savings account
plus
minus


total

gemeente
goede doelen


"""
from collections import OrderedDict
from typing import List

from bankparser.constants import (
    KEY_AMOUNT,
    KEY_ACCOUNT,
    KEY_LABEL,
    months,
    KEY_LABELS,
    KEY_ACCOUNTS,
)
from bankparser.helpers import get_transactions


def make_report(bank_data: dict, year: str, report_file=None):
    result = interpret_transactions(bank_data)
    output = print_monthly(result, year)
    if report_file:
        save_report(output, report_file)
    return output


def save_report(output, report_file):
    with open(report_file, "w") as fl:
        fl.write("\n".join(output))


def get_year(result: dict, year: str) -> dict:
    """Get monthly data from a specific year.

    If not present create it."""
    try:
        _year = result[year]
    except KeyError:
        _year = {KEY_ACCOUNTS: {}}
        get_month_data(_year, KEY_GRAND_TOTAL)
        result[year] = _year
    return _year


def get_account(year_data: dict, account_key: str) -> dict:
    try:
        _account = year_data[KEY_ACCOUNTS][account_key]
    except KeyError:
        _account = {}
        year_data[KEY_ACCOUNTS][account_key] = _account
    return _account


def get_month_data(account_data: dict, data_name) -> dict:
    """Get monthtly data based on a specifc data_name or subject.

    If not present create it."""
    try:
        _month_data = account_data[data_name]
    except KeyError:
        _month_data = OrderedDict(
            (("{:02d}".format(month_nr), 0) for month_nr in range(1, 13))
        )
        _month_data[KEY_TOTAL] = 0
        account_data[data_name] = _month_data

    return _month_data


KEY_PLUS = "plus"
KEY_MINUS = "minus"
KEY_TOTAL = "total"
KEY_GRAND_TOTAL = "GRAND_TOTAL"


class Months:
    def __init__(self, title):
        self.title = title
        self.amounts = 12 * [0]

    @property
    def total(self):
        """Return the total"""
        return sum(self.amounts)


class AccountData:
    def __init__(self, account):
        self.account = account
        self.plus = Months("plus")
        self.minus = Months("minus")
        self.total = Months("total")


class MonthlyData:
    """Yearly data summed per month."""

    def __init__(self):
        self.accounts: List[AccountData] = []
        self.labels: List[Months]


def interpret_transactions(bank_data) -> dict:
    """Interpret all bank transactions. Group them by year and account
    Amounts are added on monthly basis.
    """
    result = {}
    labels = bank_data.get(KEY_LABELS)
    if labels:
        result[KEY_LABELS] = labels

    for year, month, day, transaction in get_transactions(bank_data):
        _year = get_year(result, year)
        _account = get_account(_year, transaction[KEY_ACCOUNT])

        total = get_month_data(_account, KEY_TOTAL)
        if transaction[KEY_AMOUNT] > 0:
            amount = get_month_data(_account, KEY_PLUS)
        else:
            amount = get_month_data(_account, KEY_MINUS)
        amount[month] += transaction[KEY_AMOUNT]
        amount[KEY_TOTAL] += transaction[KEY_AMOUNT]

        total[month] += transaction[KEY_AMOUNT]
        total[KEY_TOTAL] += transaction[KEY_AMOUNT]

        _year[KEY_GRAND_TOTAL][month] += transaction[KEY_AMOUNT]
        _year[KEY_GRAND_TOTAL][KEY_TOTAL] += transaction[KEY_AMOUNT]

        label = transaction.get(KEY_LABEL)
        if label:
            label_data = get_month_data(_account, label)
            label_data[month] += transaction[KEY_AMOUNT]
            label_data[KEY_TOTAL] += transaction[KEY_AMOUNT]
    return result


def print_monthly(monthly_data: dict, year: str):
    print_output = ["{}:{}".format("year".ljust(FIRST_COL_WIDTH), year), ""]
    _year = monthly_data[year]
    labels = monthly_data.get(KEY_LABELS)
    for _account, data in _year[KEY_ACCOUNTS].items():
        print_key_value("ACCOUNT", _account, print_output)

        print_output.append("")

        print_months(print_output)

        if KEY_PLUS in data:
            print_line(KEY_PLUS, data[KEY_PLUS], print_output)
        if KEY_MINUS in data:
            print_line(KEY_MINUS, data[KEY_MINUS], print_output)
        print_hor_line(print_output)
        print_line(KEY_TOTAL, data[KEY_TOTAL], print_output)

        print_output.append("")

        print_output.append("")
    print_line(KEY_GRAND_TOTAL, _year[KEY_GRAND_TOTAL], print_output)

    print_output.append("")
    print_output.append("")
    print_output.append("")
    # Print labels merged for all accounts.
    print_labels(labels, merge_labels(monthly_data, year), print_output)

    for ln in print_output:
        print(ln)

    return print_output


FIRST_COL_WIDTH = 30
VALUES_COL_WIDTH = 10


def merge_labels(monthly_data, year):
    """merge labels from different accounts."""
    _year = monthly_data[year]
    merged = {}
    for _account, data in _year[KEY_ACCOUNTS].items():

        for key, value in data.items():
            val = get_month_data(merged, key)

            for month, amount in value.items():
                val[month] += amount

    return merged


def print_labels(labels, data, container: list):
    _labels = []
    labels = make_unique(labels)
    for group in labels:
        found_label = False
        for label in group:
            if label in data:
                found_label = True
                print_line(label, data[label], _labels)
        if found_label:
            _labels.append("")

    if _labels:
        container.append("LABELS")
        container.append("")
        container.extend(_labels)


def make_unique(labels):
    """Get a list of unique labels."""
    _labels = []
    for group in labels:
        _labels.append(set([val[1] for val in group]))
    return _labels


def print_key_value(key: str, value, container: list):
    """Print out a key value pair"""
    val = "{}:{}".format(key.ljust(FIRST_COL_WIDTH), value)
    container.append(val)


def print_line(key, data: dict, container: list):
    line = "{}{}".format(
        key.ljust(FIRST_COL_WIDTH),
        "".join(
            [
                "{:.2f}".format(val).rjust(VALUES_COL_WIDTH)
                for val in data.values()
            ]
        ),
    )
    container.append(line)


def print_months(container: list):
    """Print months."""
    month_names = "{}{}{}".format(
        FIRST_COL_WIDTH * " ",
        "".join(
            [
                "{}".format(month.rjust(VALUES_COL_WIDTH))
                for month in months.values()
            ]
        ),
        "Total".rjust(VALUES_COL_WIDTH),
    )
    container.append(month_names)


def print_hor_line(container: list):
    """Print horizontal divider."""
    line = FIRST_COL_WIDTH * "-" + 12 * VALUES_COL_WIDTH * "-"
    container.append(line)
