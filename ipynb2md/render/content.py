from dataclasses import dataclass
from logging import getLogger
from re import compile
from uuid import uuid4
from json import dumps


def parse_content(content: dict):
    if content['cell_type'] == 'code':
        return Code(content)

    if content['cell_type'] == 'markdown':
        return Markdown(content)

    LOG.warning(f'Type of "{content}" not detected')
    return NoContent()


@dataclass
class Markdown:
    content: dict

    def render(self, **kwargs):
        return '{}\n\n'.format(''.join(self.content["source"]))


@ dataclass
class Code:
    content: dict
    plotly: bool = False

    def render(self, **kwargs):
        output = ''
        if kwargs.get('show_code', True) and self.content['source']:
            output += '```python\n{}\n```\n\n'.format(
                ''.join(self.content['source']))

        if 'outputs' in self.content:
            for o in self.content['outputs']:
                if 'text' in o:
                    output += '{}\n\n'.format(''.join(o['text']))
                elif 'data' in o:
                    data = o['data']

                    if 'application/vnd.plotly.v1+json' in data:
                        self.plotly = True
                        plotly_data = data['application/vnd.plotly.v1+json']
                        output += plotly(plotly_data)

                    elif 'text/html' in data:
                        html = ''.join(data['text/html']).replace('\n', '')
                        html = STYLE.sub('', html)
                        output += '{}\n\n'.format(html)

                    elif 'image/png' in data:
                        output += '<img src="data:image/png;base64,{}"/>\n\n'.format(
                            data['image/png'])

                    elif 'text/plain' in data:
                        output += ''.join(data['text/plain']) + '\n\n'

                    else:
                        LOG.warning(
                            f'Data content not detected {str(data)[:100]}')
                else:
                    LOG.warning(f'Content not detected {str(o)[:100]}')

        return output


@ dataclass
class NoContent:
    def render(self, **kwargs):
        return '\n'


def plotly(d: dict) -> str:
    id = str(uuid4())
    return '''
<div id="plotly_{id}"></div>
<script>
var figure = JSON.parse(`{data}`);
Plotly.newPlot('plotly_{id}', figure.data, figure.layout, figure.config);
</script>\n\n'''.format(data=dumps(d).replace('\\', ''), id=id)


LOG = getLogger(__name__)
STYLE = compile(r'<style.+>.*<\/style>')
