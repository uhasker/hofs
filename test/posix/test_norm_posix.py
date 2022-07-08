from unittest import TestCase

import hofs as fs


class TestNormWin(TestCase):
    def test_posix_path(self) -> None:
        """
        Check that normalize_path creates the correct absolute path from a relative path.
        """
        normal_path = fs.expand_path("/home/user")
        self.assertEqual(normal_path, r"/home/user")
