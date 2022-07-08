import os
import re
import fnmatch
from typing import List


def file_like_exists(path: str) -> bool:
    """
    Check whether a file-like object (i.e. a file or directory) is present at the given path.

    :param path: The given path.
    :return: True, if a file-like object is present, False otherwise.
    """
    return os.path.exists(path)


def file_exists(path: str) -> bool:
    """
    Check whether a (regular) file is present at the given path.

    :param path: The given path.
    :return: True, if a file is present. False if the path does not exist at all or
        if the path represents a directory.
    """
    return os.path.isfile(path)


def dir_exists(path: str) -> bool:
    """
    Check whether a directory is present at the given path.

    :param path: The given path.
    :return: True, if a directory is present. False if the path does not exist at all or
        if the path represents a (regular) file.
    """
    return os.path.isdir(path)


def path_is_absolute(path: str) -> bool:
    """
    Check whether a given path is absolute.

    :param path: The given path.
    :return: True, if the path is absolute, False otherwise.
    """
    return os.path.isabs(path)


def path_is_relative(path: str) -> bool:
    """
    Check whether a given path is relative.

    :param path: The given path.
    :return: True, if the path is relative, False otherwise.
    """
    return not path_is_absolute(path)


def path_matches(path: str, file_like_path: str) -> bool:
    """
    Check whether a path matches a file-like path (i.e. is either equal or is contained in the path).

    :param path: The given path.
    :param file_like_path: The file-like path.
    :return: True, if the path matches, False otherwise.
    """
    return os.path.commonpath([path, file_like_path]) == file_like_path


def path_matches_one_of(path: str, file_like_paths: List[str]) -> bool:
    """
    Check whether a path matches one of the file-like paths.

    :param path: The given path.
    :param file_like_paths: The file-like paths.
    :return: True, if the path matches, False otherwise.
    """
    for base_path in file_like_paths:
        if path_matches(path, base_path):
            return True
    return False


def path_matches_regex(path: str, regex: str) -> bool:
    """
    Check whether a path matches a regular expression.

    :param path: The given path.
    :param regex: The regular expression.
    :return: True, if the path matches, False otherwise.
    """
    compiled_regex = re.compile(regex)
    return path_matches_compiled_regex(path, compiled_regex)


def path_matches_compiled_regex(path: str, compiled_regex: re.Pattern) -> bool:
    """
    Check whether a path matches a compiled regular expression.

    :param path: The given path.
    :param compiled_regex: The compiled regular expression.
    :return: True, if the path matches, False otherwise.
    """
    return bool(compiled_regex.fullmatch(path))


def path_matches_glob(path: str, pattern: str) -> bool:
    """
    Check whether a path matches a glob pattern.

    :param path: The given path.
    :param pattern: The glob pattern.
    :return: True, if the path matches, False otherwise.
    """
    return fnmatch.fnmatch(path, pattern)


def file_like_name(path: str) -> str:
    """
    Get the name of a file-like object.

    :param path: The path of the file-like object.
    :return: The name of the file-like object.
    """
    return os.path.basename(path)


def relative_path(path: str, base_path: str) -> str:
    """
    Get the relative path relative to a base path.

    :param path: The given path.
    :param base_path: The base path.
    :return: The relative path.
    """
    return os.path.relpath(path, base_path)


def expand_path(path: str) -> str:
    """
    Maximally expand a path.

    :param path: The given path.
    :return: The absolute path corresponding to the given path with special characters
        (like ~) and environment variables expanded.
    """
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return os.path.abspath(path)
