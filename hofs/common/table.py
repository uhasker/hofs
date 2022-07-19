from typing import Dict, List, Union

from hofs.exceptions.exceptions import HofsException


class Table:
    def __init__(self, cols: List[str]) -> None:
        if len(cols) == 0:
            raise HofsException("table must have at least one column")

        self._cols: Dict[str, List[str]] = {col: [] for col in cols}

    def col_name(self, idx: int) -> str:
        """
        Get the name of a column from its index.

        :param idx: The column index.
        :return: The column name.
        """
        return self.col_names[idx]

    @property
    def col_names(self) -> List[str]:
        """
        The names of the table columns.
        """
        return list(self._cols.keys())

    def col(self, idx: int) -> List[str]:
        """
        Get a column by index.

        This is equivalent to col_by_name(col_name(idx)).

        :param idx: The column index.
        :return: A list containing the values of the column.
        """
        return self.col_by_name(self.col_name(idx))

    def col_by_name(self, name: str) -> List[str]:
        """
        Get a column by name.

        :param name: The column name.
        :return: A list containing the values of the column.
        """
        return self._cols[name]

    def value(self, row_idx: int, col_idx: int) -> str:
        """
        Get a value from the table.

        :param row_idx: The index of the row.
        :param col_idx: The index of the column.
        :return: The value residing at row with index row_idx and column with index col_index.
        """
        return self.col(col_idx)[row_idx]

    def value_by_name(self, row_idx: int, col_name: str) -> str:
        """
        Get a value from the table.

        :param row_idx: The index of the row.
        :param col_name: The name of the column.
        :return: The value residing at row with index row_idx and column with name col_name.
        """
        return self.col_by_name(col_name)[row_idx]

    def row(self, idx: int) -> List[str]:
        """
        Get a row.

        :param idx: The row index.
        :return: A list containing the row values.
        """
        return list(self.row_dict(idx).values())

    def row_dict(self, idx: int) -> Dict[str, str]:
        """
        Get a row.

        :param idx: The row index.
        :return: A dictionary containing the columns along with their values for the respective row.
        """
        return {
            col_name: self.value_by_name(idx, col_name) for col_name in self.col_names
        }

    @property
    def n_rows(self) -> int:
        """
        The number of rows.
        """
        assert self.n_cols != 0

        first_col = self.col(0)
        return len(first_col)

    @property
    def n_cols(self) -> int:
        """
        The number of columns.
        """
        return len(self.col_names)

    def add_row(self, row: Union[Dict[str, str], List[str]]) -> None:
        """
        Add a row to the table.

        :param row: The row. It must be either a list of values
        :return:
        """
        if isinstance(row, List):
            if len(row) != self.n_cols:
                raise HofsException(
                    "the number of row values must be equal to the number of columns"
                )

            row_dict = {
                col_name: row[row_idx]
                for row_idx, col_name in enumerate(self.col_names)
            }
        elif isinstance(row, Dict):
            row_dict = row
        else:
            raise HofsException(
                f"row must be either a dictionary or a list, but was {type(row)} instead"
            )

        cols_diff = set(row_dict.keys()).symmetric_difference(set(self._cols.keys()))
        if len(cols_diff) != 0:
            raise HofsException(
                f"the row keys must be the column names, but the following keys differed: {cols_diff!r}"
            )

        for k, v in row_dict.items():
            self._cols[k].append(v)

    def __getitem__(self, i: int) -> Dict[str, str]:
        return self.row_dict(i)

    def __len__(self) -> int:
        return self.n_rows

    def __header(self, col_ljust_vals: Dict[str, int]) -> str:
        return (
            "".join(
                [
                    str(col_name).ljust(col_ljust_vals[col_name])
                    for col_name in self.col_names
                ]
            )
            + "\n"
        )

    def __col_str(self, col_ljust_vals: Dict[str, int], row_idx: int) -> str:
        return (
            "".join(
                [
                    str(col).ljust(col_ljust_vals[col_name])
                    for col_name, col in self[row_idx].items()
                ]
            )
            + "\n"
        )

    def __repr__(self) -> str:
        col_ljust_vals = {}
        for col_name, col in self._cols.items():
            values = self.col_by_name(col_name) + [col_name]
            col_ljust_vals[col_name] = len(max(values, key=len)) + 1

        s = self.__header(col_ljust_vals)
        for row_idx in range(len(self)):
            s += self.__col_str(col_ljust_vals, row_idx)
        return s


def table_from_rows(cols: List[str], rows: List[List[str]]) -> Table:
    table = Table(cols)
    for row in rows:
        table.add_row(row)
    return table
