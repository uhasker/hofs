from test.test_fs_values import BASE_DIR_PATH
from unittest import TestCase

import hofs as fs


class TestExamples(TestCase):
    def test_cc_example(self) -> None:
        total_size = fs.Dir(BASE_DIR_PATH).files.filter_ext("txt2").t().map_cc().sum()
        self.assertEqual(total_size, 16)

    def test_wc_example(self) -> None:
        total_size = fs.Dir(BASE_DIR_PATH).files.filter_ext("txt2").t().map_wc().sum()
        self.assertEqual(total_size, 4)
