import unittest

from ..__version__ import __version__


class TestVersion(unittest.TestCase):
    def test_version(self) -> None:
        self.assertTrue(__version__)
