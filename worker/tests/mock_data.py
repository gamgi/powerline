# Exposes json test data from a folder through
# the variable "data". Eg. data.example_data
import json
from pathlib import Path

test_data_dir = Path('tests/mock_data/')


class MockData:
    def __init__(self):
        self.data = {}
        for file_name in test_data_dir.glob('*.json'):
            with open(file_name, "r") as json_file:
                key = Path(file_name).stem
                self.data[key] = json.load(json_file)

    @property
    def keys(self):
        return self.data.keys

    def __getattr__(self, name):
        return self.data[name]


data = MockData()
