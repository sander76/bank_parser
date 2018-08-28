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

from bankparser.constants import KEY_AMOUNT, KEY_ACCOUNT, KEY_LABEL, months

# class MonthlyTransactions:
#     def __init__(self):
#         self.plus = 0
#         self.minus = 0
#         self.total = 0
#         self.transactions = []
#
#         self.labels = {}
#
#     def add_transaction(self, mutation: dict):
#         self.transactions.append(mutation)
#         if mutation[KEY_AMOUNT] < 0:
#             self.minus += mutation[KEY_AMOUNT]
#         else:
#             self.plus += mutation[KEY_AMOUNT]
#
#         label = mutation.get(KEY_LABEL)
#         if label:
#             if label not in self.labels:
#                 self.labels[label] = 0
#             self.labels[label] += mutation[KEY_AMOUNT]
#
#
# class Year:
#     def __init__(self, year, output):
#         self.year = year
#         self.output = output
#         self.months = []
#         for i in range(12):
#             self.months.append(MonthlyTransactions())
#
#     def add_transaction(self, transaction, month):
#         self.months[month].add_transaction(transaction)
#
#     def print_label(self):
#         labels = []
#         for month in self.months:
#             for label in month.labels:
#                 labels.append(label)
#         labels = set(labels)
#
#         output = []
#         # todo: left here.
#         for label in labels:
#             output.append(label)
#             for month in self.months:
#                 val = month.labels.get(label)
#                 output.append(val)
#
#
# class Account:
#     def __init__(self, account, output):
#         self.years = {}
#         self.output = output
#         self.name = account
#
#     def _get_month(self, month: str):
#         _month = int(month)
#         return _month
#
#     def add_transaction(self, transaction, month: str, year: str):
#         if year not in self.years:
#             self.years[year] = Year(year, self.output)
#         _month = self._get_month(month)
#         self.years[year].add_transaction(transaction, _month)
#         # _month = self._get_month(month)
#         # self.years[year].months[_month].add_transaction(transaction)
#
#     def print_output(self, year):
#         vals = []
#         year = self.years[year]
#         vals.append(self.name)
#         vals.append(
#             "{:<10}{}".format(
#                 "",
#                 "".join(["{:>10}".format(month) for month in months.values()]),
#             )
#         )
#         vals.append(
#             "{:<10}{}".format(
#                 "plus",
#                 "".join(
#                     ["{:10.2f}".format(month.plus) for month in year.months]
#                 ),
#             )
#         )
#         vals.append(
#             "{:<10}{}".format(
#                 "minus",
#                 "".join(
#                     ["{:10.2f}".format(month.minus) for month in year.months]
#                 ),
#             )
#         )
#         vals.append(
#             "{:<10}{}".format(
#                 "total",
#                 "".join(
#                     [
#                         "{:10.2f}".format(month.plus + month.minus)
#                         for month in year.months
#                     ]
#                 ),
#             )
#         )
#         return vals
#
#
# data = []
#
#
# def extract_accounts(dct):
#     accounts = {}
#     for year, months in dct.items():
#         for month, days in months.items():
#             for day, transactions in days.items():
#                 for transaction in transactions:
#                     _account = transaction[KEY_ACCOUNT]
#                     if _account not in accounts:
#                         accounts[_account] = Account(_account, data)
#                     accounts[_account].add_transaction(
#                         transaction, month, year
#                     )
#     return accounts
#
#
# def go(dct):
#     monthly_account_data = extract_accounts(dct)
#
#     for account in monthly_account_data.values():
#
#         vals = account.print_output("2018")
#
#         for val in vals:
#             print(val)


"""Compose dict :

{"1017":
    {
        "ING1778211":{"plus":{"01":2344,"02":223})
                    {"minus":{"01":2344,"02":223})

}

"""


def run_transactions(dct):
    for year, months in dct.items():
        for month, days in months.items():
            for day, transactions in days.items():
                for transaction in transactions:
                    yield year, month, day, transaction


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
        # _month_data = {
        #     "{:02d}".format(month_nr): 0 for month_nr in range(1, 13)
        # }
        _month_data = OrderedDict(
            (("{:02d}".format(month_nr), 0) for month_nr in range(1, 13))
        )
        account_data[data_name] = _month_data
    return _month_data


KEY_PLUS = "plus"
KEY_MINUS = "minus"
KEY_TOTAL = "total"


def interpret_transactions(dct) -> dict:
    result = {}
    for year, month, day, transaction in run_transactions(dct):
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


def print_monthly(monthly_data: dict, year: str, labels: dict = None):
    print_output = ["{}:{}".format("year".ljust(FIRST_COL_WIDTH), year),""]
    _year = monthly_data[year]
    for _account, data in _year.items():
        print_key_value("ACCOUNT", _account, print_output)

        print_output.append("")

        print_months(print_output)


        if KEY_PLUS in data:
            print_line(KEY_PLUS, data[KEY_PLUS],print_output)
        if KEY_MINUS in data:
            print_line(KEY_MINUS, data[KEY_MINUS],print_output)
        print_hor_line(print_output)
        print_line(KEY_TOTAL, data[KEY_TOTAL],print_output)

        print_output.append("")

        #print_output.append("labels:")

        if labels:
            print_labels(labels,data,print_output)

        print_output.append("")

    print("")
    for ln in print_output:
        print(ln)


FIRST_COL_WIDTH = 10
VALUES_COL_WIDTH = 10

def print_labels(labels,data,container:list):
    _labels=[]
    for label in labels:
        if label in data:
            print_line(label,data[label],_labels)
    if _labels:
        container.append("LABELS")
        container.extend(_labels)



def print_key_value(key: str, value, container: list):
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


def print_hor_line(container:list):
    line = FIRST_COL_WIDTH * "-" + 12 * VALUES_COL_WIDTH * "-"
    container.append(line)
