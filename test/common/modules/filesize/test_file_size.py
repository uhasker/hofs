from unittest import TestCase

import hofs as fs


class FileSizeBytesTest(TestCase):
    def test_size_f_auto(self) -> None:
        self.assertEqual(fs.FileSize(size_bytes=64).size_f(), 64.0)


class FileSizeTest(TestCase):
    def setUp(self) -> None:
        self.file_size = fs.FileSize(size_bytes=2000)

    def test_int(self) -> None:
        self.assertEqual(int(self.file_size), 2000)

    def test_add_int(self) -> None:
        self.assertEqual(self.file_size + 450, fs.FileSize(2450))

    def test_add_file_size(self) -> None:
        self.assertEqual(self.file_size + fs.FileSize(450), fs.FileSize(2450))

    def test_radd_int(self) -> None:
        self.assertEqual(450 + self.file_size, fs.FileSize(2450))

    def test_radd_file_size(self) -> None:
        self.assertEqual(fs.FileSize(450) + self.file_size, fs.FileSize(2450))

    def test_size_f_auto(self) -> None:
        self.assertEqual(self.file_size.size_f(fs.FileSizeUnit.AUTO), 2.0)

    def test_size_f_kb(self) -> None:
        self.assertEqual(self.file_size.size_f(fs.FileSizeUnit.KB), 2.0)

    def test_size_f_tb(self) -> None:
        self.assertEqual(
            fs.FileSize(int(1e15)).size_f(fs.FileSizeUnit.AUTO),
            1000.0,
        )

    def test_size_auto(self) -> None:
        self.assertEqual(self.file_size.size(fs.FileSizeUnit.AUTO), "2.0KB")

    def test_size_kb(self) -> None:
        self.assertEqual(self.file_size.size(fs.FileSizeUnit.KB), "2.0KB")

    def test_lt_int(self) -> None:
        self.assertTrue(self.file_size < 3000)

    def test_lt(self) -> None:
        self.assertTrue(self.file_size < fs.FileSize(3000))

    def test_eq_int(self) -> None:
        self.assertTrue(self.file_size == 2000)

    def test_eq(self) -> None:
        self.assertTrue(self.file_size == fs.FileSize(2000))

    def test_str(self) -> None:
        self.assertEqual(str(self.file_size), "2.0KB")

    def test_repr(self) -> None:
        self.assertEqual(repr(self.file_size), "2.0KB")
