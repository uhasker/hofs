import os
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
    :return: The maximally expanded path, i.e. the absolute path corresponding to the
        given path with special characters (like ~) and environment variables expanded.
    """
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return os.path.abspath(path)


def expand_paths(paths: List[str]) -> List[str]:
    """
    Maximally expand a list of paths.

    :param paths: The list of paths.
    :return: The expanded paths (see expand_path for more information).
    """
    return [expand_path(path) for path in paths]
