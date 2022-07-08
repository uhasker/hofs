import datetime
import os
import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Iterator, Any

from hofs.exceptions import HofsException
from hofs.file_size import FileSize
from hofs.functional import FunctionalIterator
from hofs.paths import (
    expand_path,
    file_exists,
    dir_exists,
    path_matches_one_of,
    file_like_name,
    path_matches_glob,
    path_matches_compiled_regex,
)


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

    def text_file(self, encoding: str = "utf-8") -> "TextFile":
        """
        Get a TextFile object for this file.

        Note that you are responsible to ensure that the underlying file is a valid
        text file (since this is very expensive to ensure automatically). This function
        will always succeed, even if the underlying file is not a valid text file.
        However, when calling functions on the resulting TextFile object, errors will occur.

        :param encoding: The encoding to use.
        :return: The obtained TextFile object.
        """
        return TextFile(self.path, encoding)

    t = text_file

    def __lt__(self, other: "File") -> bool:
        return self.size < other.size

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"File({self.path})"


class TextFile(File):
    def __init__(self, path: str, encoding: str = "utf-8"):
        super().__init__(path)

        self.encoding = encoding

    @property
    def content(self) -> str:
        """
        The content of the file.

        :return: The content.
        """
        with open(str(self.path), "r", encoding=self.encoding) as file:
            return file.read()

    @property
    def lines(self) -> FunctionalIterator[str]:
        """
        The lines of this file.

        :return: A list of lines.
        """
        with open(str(self.path), "r", encoding=self.encoding) as file:
            return FunctionalIterator(file.readlines())

    @property
    def words(self) -> FunctionalIterator[str]:
        """
        The words of this file. It is assumed that words are separated by whitespace.

        :return: A list of words.
        """
        return FunctionalIterator(self.content.split())

    @property
    def char_count(self) -> int:
        """
        The number of characters of this file.

        :return: The number of characters.
        """
        return len(self.content)

    cc = char_count

    @property
    def word_count(self) -> int:
        """
        The number of words of this file.

        :return: The number of words.
        """
        return self.words.len()

    wc = word_count

    @property
    def line_count(self) -> int:
        """
        The number of lines of this file.

        :return: The number of lines.
        """
        return self.lines.len()

    lc = line_count

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"TextFile({self.path})"


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
        return f"Dir({self.path})"


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

    def exclude(self, file_likes: List[str]) -> "FileIterator":
        """
        Exclude all files that match a given list of file-like objects.

        :param file_likes: The list of file-like objects.
        :return: A file iterator containing the non-excluded files.
        """
        return FileIterator(
            self.filter(lambda file: not path_matches_one_of(file.path, file_likes))
        )

    def text_file_iterator(self) -> "TextFileIterator":
        return TextFileIterator(self.map(lambda file: file.text_file()))

    t = text_file_iterator


class TextFileIterator(FunctionalIterator[TextFile]):
    def map_char_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their character counts.

        Note that it is implicitly assumed that all the files are valid text files.
        This function is equivalent to map(lambda file: file.text_file().char_count).

        :return: A functional iterator containing the character counts.
        """
        return self.map(lambda file: file.char_count)

    map_cc = map_char_count

    def map_word_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their word counts.

        Note that it is implicitly assumed that all the files are valid text files.
        This function is equivalent to map(lambda file: file.text_file().word_count).

        :return: A functional iterator containing the word counts.
        """
        return self.map(lambda file: file.word_count)

    map_wc = map_word_count

    def map_line_count(self) -> FunctionalIterator[int]:
        """
        Map the files to their line counts.

        Note that it is implicitly assumed that all the files are valid text files.
        This function is equivalent to map(lambda file: file.text_file().line_count).

        :return: A functional iterator containing the line counts.
        """
        return self.map(lambda file: file.line_count)

    map_lc = map_line_count
