import pytest
import json

def load_js(fname):
    with open(fname) as fl:
        _js = json.load(fl)
    return _js

@pytest.fixture
def parsed_account_data():
    return load_js("output/out.json")

@pytest.fixture
def labels():
    return load_js("csv/labels.json")