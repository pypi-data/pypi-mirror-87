from pathlib import Path

from itsicli.use_cases.files import UseCaseConfig


def root_path():
    """
    Returns the best-guess root path for the use case pack, starting from the current working directory.

    :return: the root path for the given path
    :rtype: Workspace or None
    """
    curr = Path.cwd()

    while curr != curr.parent:
        config = curr.joinpath(UseCaseConfig.file_name)

        if config.exists():
            return curr

        curr = curr.parent

    return None
