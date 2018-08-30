import pytest

from bankparser.constants import KEY_ACCOUNT, KEY_AMOUNT

from bankparser.readers.parse_rabo import RaboParser, parse_date


@pytest.fixture
def rabo_parser():
    dct = {}
    p = RaboParser(dct, None)
    return p


line_1 = '"NL77RABO015456615","EUR","RABU","000000000000003622","2017-07-03","2017-07-03","-13,98","+1567,38","","Kvat 4960 NEN","","","","ba","","","","","","Beta10:16 pasnr. 0"," ","","","","",""'
line_2 = '"NL77RABO015456615","EUR","RABU","000000000000003626","2017-07-03","2017-07-05","-32,50","+937,54","NL67RABO010396","City camp","","","RABONL2U","ei","","M06","1751","NL30ZZ091740000","","20101 jul 201ul 2017, 5"," ","","","","",""'

#todo: test labelling

def test_find_cols(rabo_parser):
    date, desc, account, other, amount = rabo_parser.find_cols(line_1)
    assert date == "2017-07-03"
    assert desc == "Kvat 4960 NEN"
    assert account == "NL77RABO015456615"
    assert other == ""
    assert amount == "-13,98"


def test_parse_date():
    date = "2017-12-31"
    year, month, day = parse_date(date)
    assert year == "2017"
    assert month == "12"
    assert day == "31"


def test_parse_amount(rabo_parser):
    val = rabo_parser.parse_amount("123")
    assert val == 123

    val = rabo_parser.parse_amount("-123")
    assert val == -123

    val = rabo_parser.parse_amount("123,4")
    assert val == 123.4

    val = rabo_parser.parse_amount("-1.234,44")
    assert val == -1234.44


def test_parse(rabo_parser):
    rabo_parser.parse(line_1)
    assert isinstance(rabo_parser.parsed["2017"], dict)
    transactions = rabo_parser.parsed["2017"]["07"]["03"]
    assert transactions[0][KEY_ACCOUNT] == "NL77RABO015456615"
    assert transactions[0][KEY_AMOUNT] == -13.98

    rabo_parser.parse(line_1)
    assert len(transactions) == 1

    rabo_parser.parse(line_2)
    assert len(transactions) == 2
