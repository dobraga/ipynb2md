try:
    from IPython.display import display
    from IPython.core.display import HTML
except:
    HTML = None

from pathlib import Path


def init_notebook():
    if HTML is None:
        raise ImportError('Need IPython/Jupyter deps.')

    css = []
    js = []

    for file in STATIC.glob('**/*'):
        suffix = file.suffix

        if suffix == '.js':
            js.append(file.read_text())
        elif suffix == '.css':
            css.append(file.read_text())

    return display(HTML('<style>' + '\n'.join(css) + '</style>\n\n' + '<script>' + '\n'.join(js) + '</script>'))


STATIC = Path(__file__, '..', '..', 'template',
              '{{ cookiecutter.name }}', '_static').resolve()
