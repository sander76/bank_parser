from pathlib import Path

from bankparser.constants import KEY_OTHER, KEY_DESC, KEY_AMOUNT, KEY_NAME
from bankparser.helpers import get_daily_transations, make_mutation, load_json
from bankparser.post_processors import PostProcessor


class Extract(PostProcessor):
    """A postprocessor which extracts transactions based on account nr

    This is used to manage internal bookings and keep the amount on the
    internal balance.... or something."""

    def __init__(
        self,
        bank_data: dict,
        base_folder: Path,
        account_file_name="accounts.json",
    ):
        super().__init__(bank_data, base_folder)
        self._account_file_name = account_file_name
        self._accounts = None

    def setup(self):
        self._accounts = load_json(
            self._base_folder.joinpath(self._account_file_name)
        )

    def process(self):
        """Extract the transaction based on the counter account nr and
        add it as a personal account nr. To keep balance intact the
        amount is inverted."""
        for year, month, day, transactions in get_daily_transations(
            self._bank_data
        ):
            extracted = []
            for transaction in transactions:
                if transaction[KEY_OTHER] in self._accounts:
                    extracted.append(
                        make_mutation(
                            transaction[KEY_OTHER],
                            -1 * transaction[KEY_AMOUNT],  # invert balance
                            "",
                            transaction[KEY_NAME],
                            transaction[KEY_DESC],
                        )
                    )
            if extracted:
                transactions.extend(extracted)


#
# def extract_accounts(bank_data: dict, accounts: dict):
#     """currently the post processor runs through account data looking
#     for accounts to extract."""
#
#     for year, month, day, transactions in get_daily_transations(bank_data):
#         extracted = []
#         for transaction in transactions:
#             if transaction[KEY_OTHER] in accounts:
#                 extracted.append(
#                     make_mutation(
#                         transaction[KEY_OTHER],
#                         transaction[KEY_ACCOUNT],
#                         "",
#                         transaction[KEY_DESC],
#                     )
#                 )
#         if extracted:
#             transactions.extend(extracted)
