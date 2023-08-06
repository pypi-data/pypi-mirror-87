import os

import pytest


def pytest_assertrepr_compare(op, left, right):
    """
    It's quite common that we compare string representation of documents.
    Native pytest's comparison failure representation is at least unreadable for this purpose.
    Printing the content in case of failure makes development and debug cycle longer.
    This prints compared strings only in case of test's failure.
    """
    if op == "==" and isinstance(left, str) and isinstance(right, str):
        print('left: ---\n' + left + '\n---')
        print('right: ---\n' + right + '\n---')


@pytest.fixture
def local_file():
    this_dir = os.path.dirname(os.path.abspath(__file__))

    class LocalFile:

        def __init__(self, *path_parts: str):
            self.path = os.path.join(this_dir, *path_parts)

        def contents(self) -> str:
            with open(self.path, encoding='utf-8') as f:
                return f.read()

        def store(self, text: str):
            with open(self.path, 'w') as f:
                return f.write(text)

        def add_suffix(self, suffix: str) -> 'LocalFile':
            return LocalFile(self.path + suffix)

    return LocalFile
