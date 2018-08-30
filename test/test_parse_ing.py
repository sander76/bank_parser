import pytest

from bankparser.constants import KEY_ACCOUNT, KEY_AMOUNT
from bankparser.helpers import get_bank_data
from bankparser.readers.parse_ing import IngParser, parse_date


@pytest.fixture
def ing_parser():
    dct = get_bank_data()
    p = IngParser(dct, None)
    return p


ing_1 = '"20180817","BAXTEY AT ","NL44INGB0004532215","","BA","Af","1,70","Betaalautomaat","Pasvolgnr:906 16-08-2018 12:22 Transactie:N7EG48 Term:50873369"'
ing_2 = '"20180817","BAXTEY AT ","NL44INGB0004532333","","BA","bij","100","Betaalautomaat","Pasvolgnr:906 16-08-2018 12:22 Transactie:N7EG48 Term:50873369"'


def test_find_cols(ing_parser):
    date, desc, account, other, amount, sign = ing_parser.find_cols(ing_1)
    assert date == "20180817"
    assert desc == "BAXTEY AT "
    assert account == "NL44INGB0004532215"
    assert other == ""
    assert amount == "1,70"
    assert sign == "Af"


def test_parse_date():
    date = "20180817"
    year, month, day = parse_date(date)
    assert year == "2018"
    assert month == "08"
    assert day == "17"


def test_parse_amount(ing_parser):
    val = ing_parser.parse_amount("123", "bij")
    assert val == 123

    val = ing_parser.parse_amount("123", "af")
    assert val == -123

    val = ing_parser.parse_amount("123,4", "bij")
    assert val == 123.4

    val = ing_parser.parse_amount("1.234,44", "af")
    assert val == -1234.44


def test_parse(ing_parser):
    ing_parser.parse(ing_1)
    assert isinstance(ing_parser.parsed["2018"], dict)
    transactions = ing_parser.parsed["2018"]["08"]["17"]
    assert transactions[0][KEY_ACCOUNT] == "NL44INGB0004532215"
    assert transactions[0][KEY_AMOUNT] == -1.7

    ing_parser.parse(ing_1)
    assert len(transactions) == 1

    ing_parser.parse(ing_2)
    assert len(transactions) == 2
