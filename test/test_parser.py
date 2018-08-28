from bankparser.helpers import get_day


def test_get_day():
    dct = {}
    val = get_day(dct, "2017", "02", "12")
    assert isinstance(val, list)
    assert len(val) == 0
    assert dct == {"2017": {"02": {"12": []}}}

    val = get_day(dct, "2017", "04", "01")
    assert isinstance(val, list)
    assert dct == {"2017": {"02": {"12": []}, "04": {"01": []}}}
