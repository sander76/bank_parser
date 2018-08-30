import cmath

from bankparser.reports.monthly_report import (
    get_month_data,
    interpret_transactions,
    print_monthly,
    KEY_PLUS,
    KEY_MINUS,
    KEY_TOTAL,
)


def test_interpret_transactions(parsed_account_data):
    val = interpret_transactions(parsed_account_data)
    assert "2018" in val
    year = val["2018"]
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


# def test_extract_accounts(parsed_account_data):
#     accounts = extract_accounts(parsed_account_data)
#     assert 'NL49INGB0004568299' in accounts
#     assert "2018" in accounts['NL49INGB0004568299'].years
#     pass
#
#
# def test_output(parsed_account_data):
#     # accounts = extract_accounts(parsed_account_data)
#     go(parsed_account_data)


def test_get_month_data():
    dct = {}
    val = get_month_data(dct, "plus")
    keys = [key for key in val]
    assert keys[0] == "01"
    assert "01" in val
    assert len(val) == 12
    assert "00" not in val
    assert "12" in val
    assert "plus" in dct
    assert val["01"] == 0
