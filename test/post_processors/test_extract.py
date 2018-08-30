import pytest

from bankparser.constants import KEY_ACCOUNT, KEY_AMOUNT
from bankparser.helpers import get_transactions
from bankparser.post_processors.extract import Extract
from configuration import ROOT_DIR


@pytest.fixture
def extract_processor(parsed_account_data):
    label = Extract(parsed_account_data, ROOT_DIR.joinpath("test/csv"))

    return label


def test_setup(extract_processor):
    assert extract_processor._accounts is None
    extract_processor.setup()
    assert isinstance(extract_processor._accounts, dict)


def test_process(extract_processor):
    extract_processor.setup()
    extract_processor.process()

    found_transaction = None
    for year, month, day, transaction in get_transactions(
        extract_processor._bank_data
    ):
        if transaction[KEY_ACCOUNT] == "NL304RIO0254649718":
            found_transaction = transaction
            break

    assert found_transaction is not None
    assert found_transaction[KEY_AMOUNT] == 5.67
