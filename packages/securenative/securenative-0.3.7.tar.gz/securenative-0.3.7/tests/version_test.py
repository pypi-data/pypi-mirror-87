import unittest

from securenative.utils.version_utils import VersionUtils


class VersionTest(unittest.TestCase):

    def test_version(self):
        version = VersionUtils.get_version()

        self.assertIsNotNone(version)
