import os
from abc import ABC, abstractmethod
from typing import Any

from hofs.paths.paths import expand_path, file_like_name


class FileLike(ABC):
    def __init__(self, path: str) -> None:
        self.path = expand_path(path)
        assert os.path.isabs(self.path)

        self.name = file_like_name(self.path)

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError  # pragma: no cover

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FileLike):
            return False
        return self.path == other.path
