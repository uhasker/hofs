import fnmatch
import os
import re
from typing import List, Union

from hofs.paths.paths import expand_path, expand_paths


def path_matches_base(path: str, base_paths: Union[str, List[str]]) -> bool:
    """
    Check whether a path matches one of the given base paths.

    The paths and base paths will be maximally expanded.

    :param path: The given path.
    :param base_paths: Either a single base path or a list of base paths.
    :return: True, if the path matches one of the base paths, False otherwise.
    """
    if isinstance(base_paths, str):
        base_paths = [base_paths]

    path = expand_path(path)
    base_paths = expand_paths(base_paths)

    for base_path in base_paths:
        if os.path.commonpath([path, base_path]) == base_path:
            return True
    return False


def path_matches_regex(path: str, regexes: Union[str, List[str]]) -> bool:
    """
    Check whether a path matches one of the given regular expressions.

    :param path: The given path.
    :param regexes: Either a single regular expression or a list of regular expressions.
    :return: True, if the path matches one of the regular expressions, False otherwise.
    """
    if isinstance(regexes, str):
        regexes = [regexes]

    compiled_regexes = [re.compile(regex) for regex in regexes]
    return path_matches_compiled_regex(path, compiled_regexes)


def path_matches_compiled_regex(
    path: str, compiled_regexes: Union[re.Pattern, List[re.Pattern]]
) -> bool:
    """
    Check whether a path matches one of the given compiled regular expressions.

    :param path: The given path.
    :param compiled_regexes: Either a single compiled regular expression or a list
        of compiled regular expressions.
    :return: True, if the path matches one of the compiled regular expressions,
        False otherwise.
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
