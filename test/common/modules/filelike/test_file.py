import datetime
import os
from test.test_fs_values import (
    A_TXT_PATH,
    B_TXT_PATH,
    BAD_F_TXT_PATH,
    BASE_DIR_PATH,
    EMPTYBIN_PATH,
    RNDBIN1_PATH,
)
from unittest import TestCase

import hofs as fs


class FileExceptionTest(TestCase):
    def test_exception(self) -> None:
        self.assertRaises(fs.HofsException, fs.File, BAD_F_TXT_PATH)


class FilePathTest(TestCase):
    def test_path(self) -> None:
        self.assertEqual(fs.File(A_TXT_PATH).path, A_TXT_PATH)


class FileBytesTest(TestCase):
    def test_bytes_empty(self) -> None:
        self.assertEqual(fs.File(EMPTYBIN_PATH).bytes, b"")

    def test_bytes(self) -> None:
        self.assertEqual(
            fs.File(RNDBIN1_PATH).bytes,
            b"\x4c\xd0\x89\x5e\x2f\x36\x1f\x56\x74\x42\xff\xb1",
        )


class FileDirTest(TestCase):
    def test_dir(self) -> None:
        self.assertEqual(fs.File(A_TXT_PATH).dir.path, BASE_DIR_PATH)


class FileExtensionTest(TestCase):
    def test_extension(self) -> None:
        self.assertEqual(fs.File(A_TXT_PATH).extension, "txt")

    def test_ext(self) -> None:
        self.assertEqual(fs.File(A_TXT_PATH).ext, "txt")

    def test_empty_extension(self) -> None:
        self.assertEqual(fs.File(RNDBIN1_PATH).extension, "")


class FileSizeTest(TestCase):
    def test_size_empty(self) -> None:
        self.assertEqual(int(fs.File(EMPTYBIN_PATH).size), 0)

    def test_size(self) -> None:
        self.assertEqual(int(fs.File(A_TXT_PATH).size), 6)


class FileAccessTimeTest(TestCase):
    def test_access_time(self) -> None:
        timestamp = datetime.datetime(2022, 1, 1, 10, 2, 50).timestamp()
        os.utime(A_TXT_PATH, (timestamp, timestamp))
        self.assertEqual(
            fs.File(A_TXT_PATH).access_time, datetime.datetime(2022, 1, 1, 10, 2, 50)
        )

    def test_atime(self) -> None:
        timestamp = datetime.datetime(2022, 1, 1, 10, 2, 50).timestamp()
        os.utime(A_TXT_PATH, (timestamp, timestamp))
        self.assertEqual(
            fs.File(A_TXT_PATH).atime, datetime.datetime(2022, 1, 1, 10, 2, 50)
        )


class FileModTimeTest(TestCase):
    def test_mod_time(self) -> None:
        timestamp = datetime.datetime(2022, 1, 1, 10, 2, 50).timestamp()
        os.utime(A_TXT_PATH, (timestamp, timestamp))
        self.assertEqual(
            fs.File(A_TXT_PATH).mod_time, datetime.datetime(2022, 1, 1, 10, 2, 50)
        )

    def test_mtime(self) -> None:
        timestamp = datetime.datetime(2022, 1, 1, 10, 2, 50).timestamp()
        os.utime(A_TXT_PATH, (timestamp, timestamp))
        self.assertEqual(
            fs.File(A_TXT_PATH).mtime, datetime.datetime(2022, 1, 1, 10, 2, 50)
        )


class FileTextFileTest(TestCase):
    def test_text_file(self) -> None:
        self.assertEqual(fs.File(A_TXT_PATH).text_file().content, "line 1")

    def test_t(self) -> None:
        self.assertEqual(fs.File(A_TXT_PATH).t().content, "line 1")


class FileOperatorsTest(TestCase):
    def test_equals(self) -> None:
        self.assertTrue(fs.File(A_TXT_PATH) == fs.File(A_TXT_PATH))

    def test_not_equals(self) -> None:
        self.assertFalse(fs.File(A_TXT_PATH) == A_TXT_PATH)

    def test_less_than(self) -> None:
        self.assertTrue(fs.File(A_TXT_PATH) < fs.File(B_TXT_PATH))


class FileStrTest(TestCase):
    def test_str(self) -> None:
        self.assertEqual(str(fs.File(A_TXT_PATH)), f'File("{A_TXT_PATH}")')

    def test_repr(self) -> None:
        self.assertEqual(repr(fs.File(A_TXT_PATH)), f'File("{A_TXT_PATH}")')
