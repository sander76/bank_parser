from bankparser.constants import (
    KEY_ACCOUNT,
    KEY_LABEL,
    KEY_OTHER,
    KEY_DESC,
    KEY_TAGS,
    KEY_LABELS)
from bankparser.helpers import get_transactions
from bankparser.post_processors import PostProcessor


class Label(PostProcessor):

    def __init__(self, bank_data: dict, base_folder, label_file="labels.csv"):
        super().__init__(bank_data, base_folder)
        self._label_file = label_file
        self._labels = None

    def setup(self):
        def get_item_from_list(list, idx, alt=None):
            try:
                if list[idx] == '':
                    return alt
                else:
                    return list[idx]
            except IndexError:
                return alt

        self._labels = []
        with open(self._base_folder.joinpath(self._label_file)) as fl:
            next(fl)
            for line in fl:
                cols = [val.strip() for val in line.split(',')]

                label = {}
                label[KEY_ACCOUNT] = get_item_from_list(cols, 0)
                label[KEY_DESC] = get_item_from_list(cols, 1)
                label[KEY_LABEL] = get_item_from_list(cols, 2)
                label[KEY_TAGS] = get_item_from_list(cols, 3)

                self._labels.append(label)
        self._bank_data[KEY_LABELS] = self._labels

    def process(self):
        for year, month, day, transaction in get_transactions(self._bank_data):
            self.label_mutation(transaction)

    def label_mutation(self, mutation: dict):
        """Checks for labels.

        If no match in account is found a match in description
        is searched, but only for labels without an account defined."""
        for label in self._labels:
            if label[KEY_ACCOUNT]:
                if label[KEY_ACCOUNT] == mutation[KEY_OTHER]:
                    mutation[KEY_LABEL] = label[KEY_LABEL] or label[KEY_DESC]
                    return
        for label in self._labels:
            if label[KEY_ACCOUNT] is None:
                if label[KEY_DESC] in mutation[KEY_DESC]:
                    mutation[KEY_LABEL] = label[KEY_LABEL] or label[KEY_DESC]
                    return
