import os
import re
from test.test_fs_values import (
    A_TXT_PATH,
    BAD_F_TXT_PATH,
    BAD_OTHER_DIR_PATH,
    BASE_DIR_PATH,
    SUB_DIR_PATH,
    TEST_DIR_PATH,
)
from unittest import TestCase

import hofs as fs


class TestPath(TestCase):
    def test_file_exists_true_is_file(self) -> None:
        """
        Check that file_exists returns True if the provided path is a regular file path.
        """
        self.assertTrue(fs.file_like_exists(A_TXT_PATH))

    def test_file_exists_true_is_dir(self) -> None:
        """
        Check that file_exists returns True if the provided path is a directory path.
        """
        self.assertTrue(fs.file_like_exists(A_TXT_PATH))

    def test_file_exists_false(self) -> None:
        """
        Check that file_exists returns False if the file does not exist.
        """
        self.assertFalse(fs.file_like_exists(BAD_F_TXT_PATH))

    def test_regular_file_exists_true(self) -> None:
        """
        Check that regular_file_exists returns True if the file does exist.
        """
        self.assertTrue(fs.file_exists(A_TXT_PATH))

    def test_regular_file_exists_false(self) -> None:
        """
        Check that file_exists returns False if the file does not exist.
        """
        self.assertFalse(fs.file_exists(BAD_F_TXT_PATH))

    def test_regular_file_exists_false_is_dir(self) -> None:
        """
        Check that file_exists returns False if the provided path is a directory path.
        """
        self.assertFalse(fs.file_exists(SUB_DIR_PATH))

    def test_dir_exists(self) -> None:
        """
        Check that dir_exists returns True if the directory exists.
        """
        self.assertTrue(fs.dir_exists(SUB_DIR_PATH))

    def test_dir_exist_true(self) -> None:
        """
        Check that dir_exists returns False if the directory does not exist.
        """
        self.assertFalse(fs.dir_exists(BAD_OTHER_DIR_PATH))

    def test_dir_exist_false_is_file(self) -> None:
        """
        Check that file_exists returns False if the provided path is a file path.
        """
        self.assertFalse(fs.dir_exists(A_TXT_PATH))

    def test_path_is_absolute(self) -> None:
        self.assertTrue(fs.path_is_absolute(A_TXT_PATH))

    def test_path_is_relative(self) -> None:
        self.assertFalse(fs.path_is_relative(A_TXT_PATH))

    def test_path_matches(self) -> None:
        self.assertTrue(fs.path_matches(SUB_DIR_PATH, BASE_DIR_PATH))

    def test_path_matches_one_of(self) -> None:
        self.assertTrue(fs.path_matches(SUB_DIR_PATH, [BASE_DIR_PATH]))

    def test_path_matches_regex_str(self) -> None:
        self.assertTrue(fs.path_matches_regex(A_TXT_PATH, r".*a\.txt"))

    def test_path_matches_regex(self) -> None:
        self.assertTrue(fs.path_matches_regex(A_TXT_PATH, [r".*a\.txt"]))

    def test_path_matches_compiled_regex_pattern(self) -> None:
        self.assertTrue(
            fs.path_matches_compiled_regex(A_TXT_PATH, re.compile(r".*a\.txt"))
        )

    def test_path_matches_compiled_regex(self) -> None:
        self.assertTrue(
            fs.path_matches_compiled_regex(A_TXT_PATH, [re.compile(r".*a\.txt")])
        )

    def test_path_matches_glob_pattern(self) -> None:
        self.assertTrue(fs.path_matches_glob(A_TXT_PATH, "*/a.txt"))

    def test_path_matches_glob(self) -> None:
        self.assertTrue(fs.path_matches_glob(A_TXT_PATH, ["*/a.txt"]))

    def test_file_like_name_file(self) -> None:
        self.assertEqual(fs.file_like_name(A_TXT_PATH), "a.txt")

    def test_file_like_name_dir(self) -> None:
        self.assertEqual(fs.file_like_name(SUB_DIR_PATH), "sub_dir")

    def test_relative_path(self) -> None:
        self.assertEqual(fs.relative_path(A_TXT_PATH, BASE_DIR_PATH), "a.txt")

    def test_expand_path(self) -> None:
        """
        Check that expand_path correctly expands a path.
        """
        normal_path = fs.expand_path("a.txt")
        expected_path = os.path.join(TEST_DIR_PATH, normal_path)
        self.assertEqual(normal_path, expected_path)
