from unittest import TestCase

import hofs as fs


class TestFunctional(TestCase):
    def test_list(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).list()
        self.assertEqual(result, [1, 2, 3, 4])

    def test_filter(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).filter(lambda x: x % 2 == 0).list()
        self.assertEqual(result, [2, 4])

    def test_map(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).map(lambda x: x * 2).list()
        self.assertEqual(result, [2, 4, 6, 8])

    def test_reduce(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).reduce(lambda x, y: x + y, 0)
        self.assertEqual(result, 10)

    def test_len(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).len()
        self.assertEqual(result, 4)

    def test_sum(self) -> None:
        result = fs.FunctionalIterator([1, 2, 3, 4]).sum()
        self.assertEqual(result, 10)

    def test_min(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).max()
        self.assertEqual(result, 4)

    def test_max(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).min()
        self.assertEqual(result, 1)

    def test_sort_asc(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).sort_asc()
        self.assertEqual(result, [1, 2, 3, 4])

    def test_sort(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).sort()
        self.assertEqual(result, [1, 2, 3, 4])

    def test_sort_desc(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).sort_desc()
        self.assertEqual(result, [4, 3, 2, 1])

    def test_top_0(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).top_n(0)
        self.assertEqual(result, [])

    def test_top_n(self) -> None:
        result = fs.FunctionalIterator([2, 1, 4, 3]).top_n(2)
        self.assertEqual(result, [4, 3])

    def test_for_each(self) -> None:
        values = []
        fs.FunctionalIterator([2, 1, 4, 3]).for_each(lambda x: values.append(x * 2))
        self.assertEqual(values, [4, 2, 8, 6])
