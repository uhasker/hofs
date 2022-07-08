from unittest import TestCase

import hofs as fs


class TestNormWin(TestCase):
    def test_win_path_backslash(self) -> None:
        """
        Check that normalize_path doesn't change a Windows path if it is already normalized.
        """
        normal_path = fs.expand_path(r"C:\Users\Example\a.txt")
        self.assertEqual(normal_path, r"C:\Users\Example\a.txt")

    def test_win_path_slash(self) -> None:
        """
        Check that normalize_path changes slashes to backward slashes on Windows path.
        """
        normal_path = fs.expand_path("C:/Users/Example/a.txt")
        self.assertEqual(normal_path, r"C:\Users\Example\a.txt")
