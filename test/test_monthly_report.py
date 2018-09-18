import cmath

from bankparser.constants import KEY_LABELS, KEY_ACCOUNTS
from bankparser.reports.monthly_report import (
    get_month_data,
    interpret_transactions,
    print_monthly,
    KEY_PLUS,
    KEY_MINUS,
    KEY_TOTAL,
    print_labels,
    print_key_value,
    print_line,
    print_months,
    print_hor_line,
    get_year,
    KEY_GRAND_TOTAL,
    make_unique)


def test_interpret_transactions(parsed_account_data):
    val = interpret_transactions(parsed_account_data)
    assert "2018" in val
    year = val["2018"][KEY_ACCOUNTS]

    assert "NL49INGB0004568299" in year
    assert "NL49INGB0004568333" in year

    _account = year["NL49INGB0004568299"]
    _plus = _account[KEY_PLUS]
    assert _plus["04"] == 57.9
    _minus = _account[KEY_MINUS]
    assert _minus["04"] == -97.17
    _total = _account[KEY_TOTAL]
    assert cmath.isclose(_total["04"], -39.27, abs_tol=0.0001)

    _charity = _account["charity"]
    assert _charity["04"] == -97.17

    _account = year["NL49INGB0004568333"]
    _minus = _account[KEY_MINUS]
    assert _minus["06"] == -88.52


def test_print_monthly(parsed_account_data):
    monthly_data = interpret_transactions(parsed_account_data)
    print_monthly(monthly_data, "2018")


def test_get_month_data():
    dct = {}
    val = get_month_data(dct, "plus")
    keys = [key for key in val]
    assert keys[0] == "01"
    assert "01" in val
    assert len(val) == 13
    assert "00" not in val
    assert "12" in val
    assert "plus" in dct
    assert val["01"] == 0


def test_print_labels(parsed_account_data):
    monthly_data = interpret_transactions(parsed_account_data)
    out = []
    labels = parsed_account_data[KEY_LABELS]
    data = monthly_data["2018"][KEY_ACCOUNTS]["NL49INGB0004568299"]
    print_labels(labels, data, out)

    # The amount of labels added is 2, but one extra header "LABELS" is added
    # to the list too.
    assert len(out) == 3



def test_get_year():
    account_data = {}
    get_year(account_data, "2018")
    assert "2018" in account_data
    assert KEY_GRAND_TOTAL in account_data["2018"]


def test_print_key_value():
    container = []
    print_key_value("value", 1, container)
    assert len(container) == 1


def test_print_line():
    container = []
    data = {"a": 1, "b": 2}
    print_line("value", data, container)
    assert len(container) == 1


def test_print_months():
    container = []
    print_months(container)
    assert len(container) == 1


def test_print_hor_line():
    container = []
    print_hor_line(container)
    assert len(container) == 1
