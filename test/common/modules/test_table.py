from unittest import TestCase

import hofs as fs


class TestTable(TestCase):
    def setUp(self) -> None:
        self.table = fs.Table(cols=["Col1", "Col2", "Col3"])
        self.table.add_row({"Col1": "A", "Col2": "B", "Col3": "C"})
        self.table.add_row({"Col1": "D", "Col2": "E", "Col3": "F"})

    def test_exception(self) -> None:
        self.assertRaises(fs.HofsException, self.table.add_row, {"Col1": "G"})

    def test_getitem(self) -> None:
        self.assertEqual(self.table[1], {"Col1": "D", "Col2": "E", "Col3": "F"})

    def test_len(self) -> None:
        self.assertEqual(len(self.table), 2)

    def test_str(self) -> None:
        self.assertEqual(
            str(self.table), "Col1 Col2 Col3 \nA    B    C    \nD    E    F    \n"
        )

    def test_repr(self) -> None:
        self.assertEqual(
            repr(self.table),
            '{"cols": {"Col1": ["A", "D"], "Col2": ["B", "E"], "Col3": ["C", "F"]}}',
        )
