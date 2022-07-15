from unittest import TestCase
import hofs as fs


class FileSizeUnitTest(TestCase):
    def test_exception(self) -> None:
        self.assertRaises(fs.HofsException, repr, fs.FileSizeUnit.AUTO)
