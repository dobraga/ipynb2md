from pathlib import Path

from .file import render


def render_files(input: Path, output: Path, remove_code: bool) -> list[str]:
    files = []
    for file in input.glob('**/*.ipynb'):
        if '/.ipynb_checkpoints/' in str(file):
            continue

        o = Path(output, file.with_suffix('.md').name)
        render(file, o, remove_code)
        files.append(file.with_suffix('').name)

    return sorted(files)
