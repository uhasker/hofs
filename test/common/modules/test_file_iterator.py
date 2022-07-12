from unittest import TestCase

import hofs as fs
from test.test_fs_values import (
    BASE_DIR_PATH,
    A_TXT_PATH,
    B_TXT_PATH,
    E_TXT_PATH,
    EMPTY_TXT_PATH,
    D_TXT_PATH,
    C_TXT2_PATH,
    EMPTYBIN_PATH,
    RNDBIN1_PATH,
    RNDBIN2_PATH,
    SUB_DIR_PATH,
)


class TestFileIterator(TestCase):
    def test_map_path(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH).files.map_path().list(),
            [
                A_TXT_PATH,
                B_TXT_PATH,
                C_TXT2_PATH,
                EMPTYBIN_PATH,
                RNDBIN1_PATH,
                D_TXT_PATH,
                E_TXT_PATH,
                EMPTY_TXT_PATH,
                RNDBIN2_PATH,
            ],
        )

    def test_map_name(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH).files.map_name().list(),
            [
                "a.txt",
                "b.txt",
                "c.txt2",
                "emptybin",
                "rndbin1",
                "d.txt",
                "e.txt",
                "empty.txt",
                "rndbin2",
            ],
        )

    def test_filter_extension(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH).files.filter_extension("txt").map_path().list(),
            [A_TXT_PATH, B_TXT_PATH, D_TXT_PATH, E_TXT_PATH, EMPTY_TXT_PATH],
        )

    def test_filter_path_regex(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH)
            .files.filter_path_regex(r".+base_dir.+\.txt")
            .map_path()
            .list(),
            [A_TXT_PATH, B_TXT_PATH, D_TXT_PATH, E_TXT_PATH, EMPTY_TXT_PATH],
        )

    def test_filter_path_glob(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH).files.filter_path_glob(r"*/a.txt").map_path().list(),
            [A_TXT_PATH],
        )

    def test_filter_name(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH).files.filter_name(r".+\.txt").map_name().list(),
            ["a.txt", "b.txt", "d.txt", "e.txt", "empty.txt"],
        )

    def test_map_char_count(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH)
            .files.filter_extension("txt2")
            .t()
            .map_char_count()
            .list(),
            [16],
        )

    def test_map_word_count(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH)
            .files.filter_extension("txt")
            .t()
            .map_word_count()
            .list(),
            [2, 4, 6, 8, 0],
        )

    def test_map_line_count(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH)
            .files.filter_extension("txt")
            .t()
            .map_line_count()
            .list(),
            [1, 2, 3, 4, 0],
        )

    def test_include(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH).files.include([SUB_DIR_PATH]).map_path().list(),
            [D_TXT_PATH, E_TXT_PATH, EMPTY_TXT_PATH, RNDBIN2_PATH],
        )

    def test_exclude(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH).files.exclude([SUB_DIR_PATH]).map_path().list(),
            [A_TXT_PATH, B_TXT_PATH, C_TXT2_PATH, EMPTYBIN_PATH, RNDBIN1_PATH],
        )

    def test_exclude_or_include_true(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH)
            .files.include_or_exclude([SUB_DIR_PATH], True)
            .map_path()
            .list(),
            [D_TXT_PATH, E_TXT_PATH, EMPTY_TXT_PATH, RNDBIN2_PATH],
        )

    def test_exclude_or_include_false(self) -> None:
        self.assertEqual(
            fs.Dir(BASE_DIR_PATH)
            .files.include_or_exclude([SUB_DIR_PATH], False)
            .map_path()
            .list(),
            [A_TXT_PATH, B_TXT_PATH, C_TXT2_PATH, EMPTYBIN_PATH, RNDBIN1_PATH],
        )
