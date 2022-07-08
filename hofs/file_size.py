from enum import Enum
from typing import Any

from hofs import HofsException


class FileSizeUnit(Enum):
    AUTO = 0
    BYTE = 1
    KB = 2
    MB = 3
    GB = 4
    TB = 5
    KIB = 6
    MIB = 7
    GIB = 8
    TIB = 9

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        if self == FileSizeUnit.AUTO:
            raise HofsException("FileSizeUnit.AUTO has no string representation")

        return {
            FileSizeUnit.BYTE: "B",
            FileSizeUnit.KB: "KB",
            FileSizeUnit.MB: "MB",
            FileSizeUnit.GB: "GB",
            FileSizeUnit.TB: "TB",
            FileSizeUnit.KIB: "KiB",
            FileSizeUnit.MIB: "MiB",
            FileSizeUnit.GIB: "GiB",
            FileSizeUnit.TIB: "TiB",
        }[self]


class FileSize:
    ConversionValues = {
        FileSizeUnit.BYTE: 1,
        FileSizeUnit.KB: 1e3,
        FileSizeUnit.MB: 1e6,
        FileSizeUnit.GB: 1e9,
        FileSizeUnit.TB: 1e12,
        FileSizeUnit.KIB: 1024,
        FileSizeUnit.MIB: 1024**2,
        FileSizeUnit.GIB: 1024**3,
        FileSizeUnit.TIB: 1024**4,
    }

    def __init__(self, size_bytes: int) -> None:
        self.size_bytes = size_bytes

    def __int__(self) -> int:
        return self.size_bytes

    def __add__(self, other: Any) -> "FileSize":
        return FileSize(int(self) + int(other))

    def __radd__(self, other: Any) -> "int":
        return self + other

    def _unit(self, unit: FileSizeUnit) -> FileSizeUnit:
        if unit != FileSizeUnit.AUTO:
            return unit

        for k, v in FileSize.ConversionValues.items():
            if self.size_bytes < v:
                return k
        return FileSizeUnit.TB

    def size_f(self, unit: FileSizeUnit = FileSizeUnit.AUTO) -> float:
        """
        Get the size as float.

        :param unit: The unit to use.
        :return: The size.
        """
        return self.size_bytes / FileSize.ConversionValues[self._unit(unit)]

    def size(self, unit: FileSizeUnit = FileSizeUnit.AUTO, rounding: int = 3) -> str:
        """
        Get the size as a readable string.

        :param unit: The unit to use.
        :param rounding: The number of digits to round the size to.
        :return: The size.
        """
        unit = self._unit(unit)
        return f"{round(self.size_f(unit), rounding)}{str(unit)}"

    def __lt__(self, other: Any) -> bool:
        return int(self) < int(other)

    def __eq__(self, other: Any) -> bool:
        return int(self) == int(other)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return self.size()
