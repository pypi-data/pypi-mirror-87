# -*- coding: utf-8 -*-

def get_project_dir() -> str:
    """
    Returns absolute project dir.
    """
    return '/app'


def get_fixture_path(path: str) -> str:
    """
    Returns absolute fixture file path.

    :param path: Relative path to the file
    """
    return get_project_dir() + "/tests/fixtures/" + path
