from bankparser.constants import KEY_ACCOUNT, KEY_DESC, KEY_LABEL
from bankparser.helpers import get_day, make_mutation
from bankparser.readers.parser import Parser


def test_get_day():
    dct = {}
    val = get_day(dct, "2017", "02", "12")
    assert isinstance(val, list)
    assert len(val) == 0
    assert dct == {"2017": {"02": {"12": []}}}

    val = get_day(dct, "2017", "04", "01")
    assert isinstance(val, list)
    assert dct == {"2017": {"02": {"12": []}, "04": {"01": []}}}


extract_accounts = {"NL13ABNA3505417344": {"name": "savings"}}


# # todo: test the post processor.
# def test_post_processor(parsed_account_data):
#     transactions = parsed_account_data["2018"]["04"]["19"]
#     post_processor(parsed_account_data, extract_accounts)
#     assert transactions[-1][KEY_ACCOUNT] == "NL13ABNA3505417344"



