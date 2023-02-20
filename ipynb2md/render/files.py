from pathlib import Path

from .file import ipynb2md


def render_files(input: Path, output: Path, remove_code: bool) -> list[str]:
    files = []
    for file in input.glob('**/*.ipynb'):
        ipynb2md(file, output, remove_code)
        files.append(file.with_suffix('').name)

    return sorted(files)
