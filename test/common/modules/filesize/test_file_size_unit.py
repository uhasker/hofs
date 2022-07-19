from unittest import TestCase

import hofs as fs
from hofs import FileSizeUnit


class FileSizeUnitTest(TestCase):
    def test_exception(self) -> None:
        self.assertRaises(fs.HofsException, repr, fs.FileSizeUnit.AUTO)

    def test_file_size_unit(self) -> None:
        self.assertEqual(str(FileSizeUnit.KB), "KB")
