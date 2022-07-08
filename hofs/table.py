import json
from typing import List, Dict, Any

from hofs import HofsException


class Table:
    def __init__(self, cols: List[str]) -> None:
        self.columns: Dict[str, List] = {col: [] for col in cols}

    def add_row(self, row: Dict[str, str]) -> None:
        cols_diff = set(row.keys()).symmetric_difference(set(self.columns.keys()))
        if len(cols_diff) != 0:
            raise HofsException(cols_diff)

        for k, v in row.items():
            self.columns[k].append(v)

    def __getitem__(self, item: int) -> Dict[str, Any]:
        return {k: self.columns[k][item] for k in self.columns.keys()}

    def __len__(self) -> int:
        key = list(self.columns.keys())[0]
        return len(self.columns[key])

    def __str__(self) -> str:
        ljust_values = {}
        for col_name, col in self.columns.items():
            ljust_values[col_name] = (
                max([len(str(v)) for v in col] + [len(col_name)]) + 1
            )

        s = ""
        s += (
            "".join(
                [
                    str(col_name).ljust(ljust_values[col_name])
                    for col_name in self.columns.keys()
                ]
            )
            + "\n"
        )
        for i in range(len(self)):
            s += (
                "".join(
                    [
                        str(col).ljust(ljust_values[col_name])
                        for col_name, col in self[i].items()
                    ]
                )
                + "\n"
            )
        return s

    def __repr__(self) -> str:
        return json.dumps({"cols": self.columns})
