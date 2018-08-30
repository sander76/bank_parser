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

from bankparser.constants import KEY_AMOUNT, KEY_ACCOUNT, KEY_LABEL, months, \
    KEY_LABELS
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
    try:
        _year = result[year]
    except KeyError:
        _year = {}
        result[year] = _year
    return _year


def get_account(year_data: dict, account_key: str) -> dict:
    try:
        _account = year_data[account_key]
    except KeyError:
        _account = {}
        year_data[account_key] = _account
    return _account


def get_month_data(account_data: dict, data_name) -> dict:
    try:
        _month_data = account_data[data_name]
    except KeyError:
        _month_data = OrderedDict(
            (("{:02d}".format(month_nr), 0) for month_nr in range(1, 13))
        )
        account_data[data_name] = _month_data
    return _month_data


KEY_PLUS = "plus"
KEY_MINUS = "minus"
KEY_TOTAL = "total"


def interpret_transactions(bank_data) -> dict:
    """Interpret all bank transactions. Group them by year and account
    Amounts are added on monthly basis.

    a = {
    "labels": [
        {"label": "charity", "account": "NL49INGB0345299"},
        {"label": "charity", "account": "NL49INGB0004568299"},
        {"label": "taxes", "account": "NL49INGB0004568299"},
    ],
    "2018": {
        "NL49INGB0004568299": {  # account
            "total": OrderedDict( # The totals row.
                [
                    ("01", 0), # month 01, total = 0
                    ("02", 0),
                    ("03", 0),
                    ("04", -39.27000000000001),
                    ("05", 0),
                    ("06", -2078.81),
                    ("07", 0),
                    ("08", 0),
                    ("09", 0),
                    ("10", 0),
                    ("11", 0),
                    ("12", 0),
                ]
            ),
            "plus": OrderedDict(
                [
                    ("01", 0),
                    ("02", 0),
                    ("03", 0),
                    ("04", 57.9),
                    ("05", 0),
                    ("06", 0),
                    ("07", 0),
                    ("08", 0),
                    ("09", 0),
                    ("10", 0),
                    ("11", 0),
                    ("12", 0),
                ]
            ),
            "minus": OrderedDict(
                [
                    ("01", 0),
                    ("02", 0),
                    ("03", 0),
                    ("04", -97.17),
                    ("05", 0),
                    ("06", -2078.81),
                    ("07", 0),
                    ("08", 0),
                    ("09", 0),
                    ("10", 0),
                    ("11", 0),
                    ("12", 0),
                ]
            ),
            "charity": OrderedDict(
                [
                    ("01", 0),
                    ("02", 0),
                    ("03", 0),
                    ("04", -97.17),
                    ("05", 0),
                    ("06", -20.09),
                    ("07", 0),
                    ("08", 0),
                    ("09", 0),
                    ("10", 0),
                    ("11", 0),
                    ("12", 0),
                ]
            ),
            "taxes": OrderedDict(
                [
                    ("01", 0),
                    ("02", 0),
                    ("03", 0),
                    ("04", 0),
                    ("05", 0),
                    ("06", -0.47),
                    ("07", 0),
                    ("08", 0),
                    ("09", 0),
                    ("10", 0),
                    ("11", 0),
                    ("12", 0),
                ]
            ),
        },
        "NL49INGB0004568333": {  # New account
            "total": OrderedDict(
                [
                    ("01", 0),
                    ("02", 0),
                    ("03", 0),
                    ("04", 6556.3099999999995),
                    ("05", 0),
                    ("06", -88.52),
                    ("07", 0),
                    ("08", 0),
                    ("09", 0),
                    ("10", 0),
                    ("11", 0),
                    ("12", 0),
                ]
            ),

    """
    result = {}
    labels = bank_data.get(KEY_LABELS)
    if labels:
        result[KEY_LABELS] = labels
    # todo: sum transactions for a year.
    for year, month, day, transaction in get_transactions(bank_data):
        _year = get_year(result, year)
        _account = get_account(_year, transaction[KEY_ACCOUNT])

        total = get_month_data(_account, KEY_TOTAL)
        if transaction[KEY_AMOUNT] > 0:
            amount = get_month_data(_account, KEY_PLUS)
        else:
            amount = get_month_data(_account, KEY_MINUS)
        amount[month] += transaction[KEY_AMOUNT]
        total[month] += transaction[KEY_AMOUNT]

        label = transaction.get(KEY_LABEL)
        if label:
            label_data = get_month_data(_account, label)
            label_data[month] += transaction[KEY_AMOUNT]
    return result


def print_monthly(monthly_data: dict, year: str):
    print_output = ["{}:{}".format("year".ljust(FIRST_COL_WIDTH), year), ""]
    _year = monthly_data[year]
    for _account, data in _year.items():
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

        # print_output.append("labels:")

        labels = monthly_data.get(KEY_LABELS)
        if labels:
            print_labels(labels, data, print_output)

        print_output.append("")

    print("")
    for ln in print_output:
        print(ln)

    return print_output


FIRST_COL_WIDTH = 30
VALUES_COL_WIDTH = 10


def print_labels(labels, data, container: list):
    _labels = []
    labels = set([val[KEY_LABEL] for val in labels])
    for label in labels:
        if label in data:
            print_line(label, data[label], _labels)
    if _labels:
        container.append("LABELS")
        container.extend(_labels)


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
    month_names = "{}{}".format(
        FIRST_COL_WIDTH * " ",
        "".join(
            [
                "{}".format(month.rjust(VALUES_COL_WIDTH))
                for month in months.values()
            ]
        ),
    )
    container.append(month_names)


def print_hor_line(container: list):
    """Print horizontal divider."""
    line = FIRST_COL_WIDTH * "-" + 12 * VALUES_COL_WIDTH * "-"
    container.append(line)
