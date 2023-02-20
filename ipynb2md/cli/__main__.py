from logging import basicConfig, getLogger
from cookiecutter.main import cookiecutter
from os import makedirs, rename, system
from rich.logging import RichHandler
from argparse import ArgumentParser
from shutil import rmtree
from pathlib import Path

from ipynb2md.render import render_files
from ipynb2md.conf import project_config


def cli():
    input, output, remove_code, keep_files = parser()
    LOG.debug(f'Running from "{input}" -> "{output}"')
    files = render_files(input, output, remove_code)

    project_config(files)

    cookiecutter(str(Path(PROJECT, 'template')),
                 no_input=True, output_dir=str(output),
                 config_file='/tmp/ipynb2md.yml')

    for file in output.glob('*.md'):
        dst = Path(file.parent, 'ipynb2md', file.name)
        LOG.debug(f'Moving from "{file}" to "{dst}"')
        rename(file, dst)

    command = f'sphinx-build {output}/ipynb2md {output}/output -b zundler'
    LOG.info(f'Running "{command}"')
    system(command)

    rename(output/'output'/'index.html', output/'..'/'index.html')

    if not keep_files:
        rmtree(output)


def parser():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', help='Input path', required=True)
    parser.add_argument('-o', '--output', help='Output path', required=False)
    parser.add_argument('-rc', '--remove_code', help='Remove code in output file',
                        action='store_false')
    parser.add_argument('-k', '--keep', help='Keep intermediary files',
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='Show more output in logs', action='store_true')
    args = parser.parse_args()
    basicConfig(
        format='%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level='DEBUG' if args.verbose else 'INFO',
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    input = Path(args.input).absolute()
    output = Path(input, 'rendered')

    rmtree(output, ignore_errors=True)
    makedirs(output, exist_ok=True)

    return input, output, args.remove_code, args.keep


LOG = getLogger(__name__)
PROJECT = Path(__file__, '..', '..').resolve()
