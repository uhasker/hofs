import datetime
import os
import re
from enum import Enum
from typing import Iterator, List, Union, Any

from hofs.common.functional import FunctionalIterator
from hofs.exceptions.exceptions import HofsException
from hofs.filelike.file_like import FileLike
from hofs.filesize.file_size import FileSize
from hofs.paths.paths import (
    dir_exists,
    file_exists,
    path_matches,
    path_matches_compiled_regex,
    path_matches_glob,
)


class File(FileLike):
    def __init__(self, path: str) -> None:
        if not file_exists(path):
            raise HofsException(f"There is no (regular) file at {path}")

        super(File, self).__init__(path)

    @property
    def bytes(self) -> bytes:
        """
        The content of the file.

        :return: The content bytes.
        """
        with open(self.path, "rb") as file:
            return file.read()

    @property
    def dir(self) -> "Dir":
        """
        The directory containing this file.

        :return: A Dir object representing the directory.
        """
        return Dir(os.path.dirname(self.path))

    @property
    def extension(self) -> str:
        """
        The extension of this file.

        :return: The extension. If the file has no extension, an empty string will be
            returned. Otherwise, the extension *without* the preceding dot will be returned
            (e.g. "txt", *not* ".txt").
        """
        _, ext = os.path.splitext(self.path)
        return ext[1:] if len(ext) > 0 else ext

    ext = extension

    @property
    def size(self) -> FileSize:
        """
        The size of this file.

        :return: A FileSize object representing the size of this file (in bytes).
        """
        return FileSize(os.path.getsize(self.path))

    @property
    def access_time(self) -> datetime.datetime:
        """
        The last access time of this file.

        :return: A datetime object representing the last access time.
        """
        atime = os.path.getatime(self.path)
        return datetime.datetime.fromtimestamp(atime)

    atime = access_time

    @property
    def mod_time(self) -> datetime.datetime:
        """
        The last modification time of this file.

        :return: A datetime object representing the last modification time.
        """
        mtime = os.path.getmtime(self.path)
        return datetime.datetime.fromtimestamp(mtime)

    mtime = mod_time

    def __lt__(self, other: "File") -> bool:
        return self.size < other.size

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f'File("{self.path}")'

    t: Any
    text_file: Any


class _FileTreeWalkIteratorKind(Enum):
    BOTH = 0
    REGULAR_FILES_ONLY = 1
    DIRS_ONLY = 2


class _FileTreeWalkIterator(Iterator):
    def __init__(self, path: str, kind: _FileTreeWalkIteratorKind) -> None:
        self.it = os.walk(path)
        self.path = path

        self.kind = kind

        self.sub_dir_path, _, file_names = next(self.it)
        self.sub_dir_processed = False
        self.file_names = sorted(file_names)

    def __next__(self) -> FileLike:
        if not self.sub_dir_processed and (
            self.kind == _FileTreeWalkIteratorKind.BOTH
            or self.kind == _FileTreeWalkIteratorKind.DIRS_ONLY
        ):
            self.sub_dir_processed = True
            return Dir(self.sub_dir_path)

        if len(self.file_names) != 0 and (
            self.kind == _FileTreeWalkIteratorKind.BOTH
            or self.kind == _FileTreeWalkIteratorKind.REGULAR_FILES_ONLY
        ):
            file_name, *self.file_names = self.file_names
            return File(os.path.join(self.sub_dir_path, file_name))

        try:
            self.sub_dir_path, _, file_names = next(self.it)
            self.file_names = sorted(file_names)
            self.sub_dir_processed = False
            return next(self)
        except StopIteration:
            raise StopIteration


class Dir(FileLike):
    def __init__(self, path: str) -> None:
        if not dir_exists(path):
            raise HofsException(f"There is no directory at {path}")

        super(Dir, self).__init__(path)

    def file(self, file_name: str) -> "File":
        """
        The file with the given name located in this directory.

        :param file_name: The file name.
        :return: A File object representing the given file.
        """
        return File(os.path.join(self.path, file_name))

    def dir(self, subdir_name: str) -> "Dir":
        return Dir(os.path.join(self.path, subdir_name))

    @property
    def file_likes(self) -> FunctionalIterator[FileLike]:
        """
        An iterator of file-like objects present in this directory and all subdirectories.

        :return: The iterator.
        """
        return FunctionalIterator(
            _FileTreeWalkIterator(self.path, _FileTreeWalkIteratorKind.BOTH)
        )

    @property
    def files(self) -> "FileIterator":
        """
        An iterator of (regular) files present in this directory and all subdirectories.

        :return: The iterator.
        """
        return FileIterator(
            _FileTreeWalkIterator(
                self.path, _FileTreeWalkIteratorKind.REGULAR_FILES_ONLY
            )
        )

    @property
    def dirs(self) -> FunctionalIterator["Dir"]:
        """
        An iterator of all directories present in this directory and all subdirectories.

        :return: The iterator.
        """
        return FunctionalIterator(
            _FileTreeWalkIterator(self.path, _FileTreeWalkIteratorKind.DIRS_ONLY)
        )

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f'Dir("{self.path}")'


class FileIterator(FunctionalIterator["File"]):
    def filter_extension(self, extension: str) -> "FileIterator":
        """
        Filter the files by extension.

        This function is equivalent to filter(lambda file: file.extension == extension).

        :param extension: The extension (must be given without the preceding dot).
        :return: A file iterator containing the files that have the given extension.
        """
        return FileIterator(self.filter(lambda file: file.extension == extension))

    def filter_path_regex(self, regex: str) -> "FileIterator":
        compiled_regex = re.compile(regex)
        return FileIterator(
            self.filter(
                lambda file: path_matches_compiled_regex(file.path, compiled_regex)
            )
        )

    def filter_path_glob(self, glob: str) -> "FileIterator":
        return FileIterator(
            self.filter(lambda file: path_matches_glob(file.path, glob))
        )

    def filter_name(self, regex: str) -> "FileIterator":
        compiled_regex = re.compile(regex)
        return FileIterator(
            self.filter(lambda file: bool(compiled_regex.fullmatch(file.name)))
        )

    filter_ext = filter_extension

    def map_path(self) -> FunctionalIterator[str]:
        """
        Map the files to their paths.

        :return: A functional iterator containing the file path.
        """
        return self.map(lambda file: file.path)

    def map_name(self) -> FunctionalIterator[str]:
        """
        Map the files to their names.

        :return: A functional iterator containing the file name.
        """
        return self.map(lambda file: file.name)

    def include(self, file_likes: Union[str, List[str]]) -> "FileIterator":
        """
        Include all files that match a given list of file-like objects.

        All files that don't match the list are thereby excluded.

        :param file_likes: The list of file-like objects.
        :return: A file iterator containing the included files.
        """
        return FileIterator(
            self.filter(lambda file: path_matches(file.path, file_likes))
        )

    def exclude(self, file_likes: Union[str, List[str]]) -> "FileIterator":
        """
        Exclude all files that match a given list of file-like objects.

        :param file_likes: The list of file-like objects.
        :return: A file iterator containing the non-excluded files.
        """
        return FileIterator(
            self.filter(lambda file: not path_matches(file.path, file_likes))
        )

    def include_or_exclude(
        self, file_likes: Union[str, List[str]], include: bool
    ) -> "FileIterator":
        """
        Include or exclude all files that match a given list of file-like objects.

        This is useful e.g. if you have a scenario where you are given a bunch of directories
        along with a flag specifying whether they should be excluded or included.
        Without this function you would potentially have to construct two different function chains.

        :param file_likes: The list of file-like objects.
        :param include: True, if file_likes should be included, False otherwise.
        :return: A file iterator containing the non-excluded files.
        """
        return self.include(file_likes) if include else self.exclude(file_likes)

    def include_glob(self, patterns: Union[str, List[str]]) -> "FileIterator":
        return FileIterator(
            self.filter(lambda file: path_matches_glob(file.path, patterns))
        )

    def exclude_glob(self, patterns: Union[str, List[str]]) -> "FileIterator":
        return FileIterator(
            self.filter(lambda file: not path_matches_glob(file.path, patterns))
        )

    def include_or_exclude_glob(
        self, patterns: Union[str, List[str]], include: bool
    ) -> "FileIterator":
        return self.include_glob(patterns) if include else self.exclude_glob(patterns)

    def include_regex(self, regexes: Union[str, List[str]]) -> "FileIterator":
        compiled_regexes = [re.compile(regex) for regex in regexes]
        return FileIterator(
            self.filter(
                lambda file: path_matches_compiled_regex(file.path, compiled_regexes)
            )
        )

    def exclude_regex(self, regexes: Union[str, List[str]]) -> "FileIterator":
        compiled_regexes = [re.compile(regex) for regex in regexes]
        return FileIterator(
            self.filter(
                lambda file: not path_matches_compiled_regex(
                    file.path, compiled_regexes
                )
            )
        )

    def include_or_exclude_regex(
        self, regexes: Union[str, List[str]], include: bool
    ) -> "FileIterator":
        return self.include_regex(regexes) if include else self.exclude_regex(regexes)

    text_file_iterator: Any
    t: Any
