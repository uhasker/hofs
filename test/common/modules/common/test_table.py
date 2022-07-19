from unittest import TestCase

import hofs as fs


class TestTable(TestCase):
    def setUp(self) -> None:
        self.table = fs.Table(cols=["Col1", "Col2", "Col3"])
        self.table.add_row({"Col1": "A", "Col2": "B", "Col3": "C"})
        self.table.add_row({"Col1": "D", "Col2": "E", "Col3": "F"})

    def test_table_zero_cols_exception(self) -> None:
        self.assertRaises(fs.HofsException, fs.Table, [])

    def test_col_name(self) -> None:
        self.assertEqual(self.table.col_name(1), "Col2")

    def test_col_names(self) -> None:
        self.assertEqual(self.table.col_names, ["Col1", "Col2", "Col3"])

    def test_col(self) -> None:
        self.assertEqual(self.table.col(2), ["C", "F"])

    def test_col_by_name(self) -> None:
        self.assertEqual(self.table.col_by_name("Col1"), ["A", "D"])

    def test_value(self) -> None:
        self.assertEqual(self.table.value(1, 2), "F")

    def test_value_by_name(self) -> None:
        self.assertEqual(self.table.value_by_name(1, "Col3"), "F")

    def test_row(self) -> None:
        self.assertEqual(self.table.row(1), ["D", "E", "F"])

    def test_row_dict(self) -> None:
        self.assertEqual(
            self.table.row_dict(0), {"Col1": "A", "Col2": "B", "Col3": "C"}
        )

    def test_n_rows(self) -> None:
        self.assertEqual(self.table.n_rows, 2)

    def test_n_cols(self) -> None:
        self.assertEqual(self.table.n_cols, 3)

    def test_add_row_wrong_len_exception(self) -> None:
        self.assertRaises(fs.HofsException, self.table.add_row, ["G", "H"])

    def test_add_row_wrong_type_exception(self) -> None:
        self.assertRaises(fs.HofsException, self.table.add_row, 3)

    def test_add_row_keys_diff_exception(self) -> None:
        self.assertRaises(fs.HofsException, self.table.add_row, {"Col1": "G"})

    def test_add_row_list(self) -> None:
        self.table.add_row(["G", "H", "I"])
        self.assertEqual(self.table.row(2), ["G", "H", "I"])

    def test_add_row_dict(self) -> None:
        self.table.add_row({"Col1": "G", "Col2": "H", "Col3": "I"})
        self.assertEqual(self.table.row(2), ["G", "H", "I"])

    def test_add_row_dict_other_order(self) -> None:
        self.table.add_row({"Col2": "H", "Col3": "I", "Col1": "G"})
        self.assertEqual(self.table.row(2), ["G", "H", "I"])

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
            "Col1 Col2 Col3 \nA    B    C    \nD    E    F    \n",
        )

    def test_table_from_rows(self) -> None:
        table = fs.table_from_rows(
            cols=["Col1", "Col2", "Col3"], rows=[["A", "B", "C"], ["D", "E", "F"]]
        )
        self.assertEqual(
            str(table), "Col1 Col2 Col3 \nA    B    C    \nD    E    F    \n"
        )
