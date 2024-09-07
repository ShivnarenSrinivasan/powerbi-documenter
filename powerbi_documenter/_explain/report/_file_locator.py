import pathlib


def definition_file(root: pathlib.Path) -> pathlib.Path:
    return root.joinpath('definition.pbir')


def definition_dir(root: pathlib.Path) -> pathlib.Path:
    return root.joinpath('definition')


def pages(root: pathlib.Path) -> pathlib.Path:
    return root.joinpath()
