from unittest import TestCase

import hofs as fs
from test.test_fs_values import (
    E_TXT_PATH,
    D_TXT_PATH,
    SUB_DIR_PATH,
    BASE_DIR_PATH,
    RNDBIN2_PATH,
    RNDBIN1_PATH,
    C_TXT2_PATH,
    B_TXT_PATH,
    A_TXT_PATH,
    BAD_OTHER_DIR_PATH,
    EMPTYBIN_PATH,
    EMPTY_TXT_PATH,
)


class DirExceptionTest(TestCase):
    def test_exception(self) -> None:
        self.assertRaises(fs.HofsException, fs.Dir, BAD_OTHER_DIR_PATH)


class DirFileTest(TestCase):
    def test_file(self) -> None:
        file = fs.Dir(BASE_DIR_PATH).file("a.txt")
        self.assertEqual(file.path, A_TXT_PATH)


class DirDirTest(TestCase):
    def test_dir(self) -> None:
        dir = fs.Dir(BASE_DIR_PATH).dir("sub_dir")
        self.assertEqual(dir.path, SUB_DIR_PATH)


class DirFileLikesTest(TestCase):
    def test_file_likes(self) -> None:
        file_paths = [file_like.path for file_like in fs.Dir(BASE_DIR_PATH).file_likes]
        self.assertEqual(
            file_paths,
            [
                BASE_DIR_PATH,
                A_TXT_PATH,
                B_TXT_PATH,
                C_TXT2_PATH,
                EMPTYBIN_PATH,
                RNDBIN1_PATH,
                SUB_DIR_PATH,
                D_TXT_PATH,
                E_TXT_PATH,
                EMPTY_TXT_PATH,
                RNDBIN2_PATH,
            ],
        )


class DirFilesTest(TestCase):
    def test_files(self) -> None:
        regular_file_paths = [file.path for file in fs.Dir(BASE_DIR_PATH).files]
        self.assertEqual(
            regular_file_paths,
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


class DirDirsTest(TestCase):
    def test_dirs(self) -> None:
        dir_paths = [dir.path for dir in fs.Dir(BASE_DIR_PATH).dirs]
        self.assertEqual(dir_paths, [BASE_DIR_PATH, SUB_DIR_PATH])


class DirStrTest(TestCase):
    def test_str(self) -> None:
        self.assertEqual(str(fs.Dir(BASE_DIR_PATH)), f"Dir({BASE_DIR_PATH})")

    def test_repr(self) -> None:
        self.assertEqual(repr(fs.Dir(BASE_DIR_PATH)), f"Dir({BASE_DIR_PATH})")
