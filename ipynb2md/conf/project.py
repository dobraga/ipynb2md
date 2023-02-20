from yaml import dump
from toml import loads
from pathlib import Path
from logging import getLogger


def project_config(files: list[str]):
    depth = 0
    pwd = '.'
    while not (Path(pwd)/'pyproject.toml').is_file():
        if depth > 3:
            return
        pwd += '/..'
        depth += 1

    conf_dir = (Path(pwd)/'pyproject.toml').resolve()
    LOG.info(f'Reading config from "{conf_dir}"')
    conf = loads(conf_dir.read_text())['tool']['poetry']
    conf['project'] = conf['name']
    for k in list(conf.keys()):
        if k not in ['project', 'version', 'description', 'authors']:
            conf.pop(k, None)
    conf['name'] = 'ipynb2md'
    conf['files'] = {'path': files}
    conf = {'default_context': conf}

    LOG.info(f'config: "{conf}"')
    Path('/tmp/ipynb2md.yml').write_text(dump(conf))


LOG = getLogger(__name__)
