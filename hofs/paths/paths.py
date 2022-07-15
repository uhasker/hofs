import fnmatch
import os
import re
from typing import List, Union


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


def path_matches(path: str, base_paths: Union[str, List[str]]) -> bool:
    """
    Check whether a path matches one of the file-like paths.

    :param path: The given path.
    :param base_paths: The file-like paths.
    :return: True, if the path matches, False otherwise.
    """
    if isinstance(base_paths, str):
        base_paths = [base_paths]

    base_paths = expand_paths(base_paths)
    for base_path in base_paths:
        if os.path.commonpath([path, base_path]) == base_path:
            return True
    return False


def path_matches_regex(path: str, regexes: Union[str, List[str]]) -> bool:
    """
    Check whether a path matches a regular expression.

    :param path: The given path.
    :param regexes: The regular expression.
    :return: True, if the path matches, False otherwise.
    """
    if isinstance(regexes, str):
        regexes = [regexes]

    compiled_regexes = [re.compile(regex) for regex in regexes]
    return path_matches_compiled_regex(path, compiled_regexes)


def path_matches_compiled_regex(
    path: str, compiled_regexes: Union[re.Pattern, List[re.Pattern]]
) -> bool:
    """
    Check whether a path matches a compiled regular expression.

    :param path: The given path.
    :param compiled_regexes: The compiled regular expression.
    :return: True, if the path matches, False otherwise.
    """
    if isinstance(compiled_regexes, re.Pattern):
        compiled_regexes = [compiled_regexes]

    for compiled_regex in compiled_regexes:
        if compiled_regex.fullmatch(path):
            return True
    return False


def path_matches_glob(path: str, patterns: Union[str, List[str]]) -> bool:
    """
    Check whether a path matches a glob pattern.

    :param path: The given path.
    :param patterns: The glob pattern.
    :return: True, if the path matches, False otherwise.
    """
    if isinstance(patterns, str):
        patterns = [patterns]

    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


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


def expand_paths(paths: List[str]) -> List[str]:
    return [expand_path(path) for path in paths]
