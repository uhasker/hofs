from test.test_fs_values import BASE_DIR_PATH
from unittest import TestCase

import hofs as fs


class TestReadme(TestCase):
    def test_readme_short_example(self) -> None:
        total_size = fs.Dir(BASE_DIR_PATH).files.filter_ext("txt").t().map_lc().sum()
        self.assertEqual(total_size, 10)

    def test_readme_long_example(self) -> None:
        total_size = (
            fs.Dir(BASE_DIR_PATH)
            .files.filter_extension("txt")
            .t()
            .map_line_count()
            .sum()
        )
        self.assertEqual(total_size, 10)

    def test_readme_explicit_short_example(self) -> None:
        total_size = (
            fs.Dir(BASE_DIR_PATH)
            .files.filter(lambda f: f.ext == "txt")
            .map(lambda f: f.t().lc)
            .sum()
        )
        self.assertEqual(total_size, 10)

    def test_readme_explicit_long_example(self) -> None:
        total_size = (
            fs.Dir(BASE_DIR_PATH)
            .files.filter(lambda f: f.extension == "txt")
            .map(lambda f: f.text_file().line_count)
            .sum()
        )
        self.assertEqual(total_size, 10)
