import pytest

from bankparser.constants import (
    KEY_ACCOUNT,
    KEY_DESC,
    KEY_LABEL,
    KEY_TAGS,
    KEY_LABELS,
)
from bankparser.helpers import make_mutation
from bankparser.post_processors.label import Label
from bankparser.reports.monthly_report import make_unique
from configuration import ROOT_DIR


@pytest.fixture
def labels(parsed_account_data):
    label = Label(parsed_account_data, ROOT_DIR.joinpath("test/csv"))

    return label


def test_setup(labels):
    assert labels._labels is None
    labels.setup()

    assert isinstance(labels._labels, list)
    first_label = labels._labels[0]
    assert first_label[KEY_ACCOUNT] == "NL59INGB03032"
    assert first_label[KEY_LABEL] == "NNederlanden"

    last_label = labels._labels[3]
    assert last_label[KEY_LABEL] == "a label"

    last_label = labels._labels[4]
    assert last_label[KEY_ACCOUNT] is None
    # assert last_label[KEY_TAGS] is None


def test_make_unique(labels):
    labels.setup()
    lst = make_unique(labels._bank_data[KEY_LABELS])
    assert len(lst[0]) == 5


def test_label_mutation(labels):
    labels._labels = [
        {
            KEY_ACCOUNT: "1NL12345",
            KEY_DESC: "description",
            KEY_LABEL: "description",
        },
        {KEY_ACCOUNT: "2NL12345", KEY_DESC: "desc", KEY_LABEL: "haslabel"},
        {KEY_ACCOUNT: None, KEY_DESC: "desc1", KEY_LABEL: "label_by_desc"},
        {KEY_ACCOUNT: "4NL12345", KEY_DESC: "desc1", KEY_LABEL: "labelled"},
    ]

    mutation = make_mutation("NL123453345", 10, "1NL12345", "name1", "desc1")

    labels.label_mutation(mutation)
    assert mutation[KEY_LABEL] == "description"

    mutation = make_mutation("NL123453345", 10, "2NL12345", "name2", "desc1")
    labels.label_mutation(mutation)
    assert mutation[KEY_LABEL] == "haslabel"

    mutation = make_mutation("NL123453345", 10, "3NL12345", "name3", "desc1")
    labels.label_mutation(mutation)
    assert mutation[KEY_LABEL] == "label_by_desc"

    mutation = make_mutation("NL123453345", 10, "4NL12345", "name4", "desc1")
    labels.label_mutation(mutation)
    assert mutation[KEY_LABEL] == "labelled"
