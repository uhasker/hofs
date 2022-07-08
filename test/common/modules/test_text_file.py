from unittest import TestCase

import hofs as fs
from test.test_fs_values import B_TXT_PATH, EMPTY_TXT_PATH, A_TXT_PATH


class TextFileContentTest(TestCase):
    def test_content_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).content, "")

    def test_content(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).content, "line 2\nline 3")


class TextFileLinesTest(TestCase):
    def test_lines_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).lines.list(), [])

    def test_lines(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).lines.list(), ["line 2\n", "line 3"])


class TextFileWordsTest(TestCase):
    def test_words_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).words.list(), [])

    def test_words(self) -> None:
        self.assertEqual(
            fs.TextFile(B_TXT_PATH).words.list(), ["line", "2", "line", "3"]
        )


class TextFileCharCountTest(TestCase):
    def test_char_count_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).char_count, 0)

    def test_char_count(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).char_count, 13)

    def test_cc(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).cc, 13)


class TextFileWordCountTest(TestCase):
    def test_word_count_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).word_count, 0)

    def test_word_count(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).word_count, 4)

    def test_wc(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).wc, 4)


class TextFileLineCountTest(TestCase):
    def test_line_count_empty(self) -> None:
        self.assertEqual(fs.TextFile(EMPTY_TXT_PATH).line_count, 0)

    def test_line_count(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).line_count, 2)

    def test_lc(self) -> None:
        self.assertEqual(fs.TextFile(B_TXT_PATH).lc, 2)


class TextFileStrTest(TestCase):
    def test_str(self) -> None:
        self.assertEqual(str(fs.TextFile(A_TXT_PATH)), f"TextFile({A_TXT_PATH})")

    def test_repr(self) -> None:
        self.assertEqual(repr(fs.TextFile(A_TXT_PATH)), f"TextFile({A_TXT_PATH})")
