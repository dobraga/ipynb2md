from json import loads
from pathlib import Path
from logging import getLogger

from ipynb2md.render.content import parse_content


def ipynb2md(input, output, show_code=True) -> None:
    input = Path(input)
    LOG.debug(f'Reading content from "{input}"')

    output = Path(output, input.with_suffix('.md').name)

    contents = []
    for cell in loads(input.read_text())['cells']:
        contents.append(parse_content(cell))

    plotly_add = False
    with open(output, 'w') as f:
        for content in contents:
            html = content.render(show_code=show_code)
            if getattr(content, 'plotly', False) and not plotly_add:
                f.write(PLOTLY)
                plotly_add = True
            f.write(html)

    LOG.info(f'"{input}" -> "{output}"')


PLOTLY = '<script src="https://cdn.plot.ly/plotly-2.18.0.min.js"></script>\n'
LOG = getLogger(__name__)
