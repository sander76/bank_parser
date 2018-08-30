from pathlib import Path


class PostProcessor():
    def __init__(self, bank_data: dict, base_folder: Path):
        self._bank_data = bank_data
        self._base_folder = base_folder

    def setup(self):
        raise NotImplemented

    def process(self):
        raise NotImplemented
