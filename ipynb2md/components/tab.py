from dataclasses import dataclass, field


@dataclass
class Tab:
    _names: list[str] = field(default_factory=list)
    _contents: list[str] = field(default_factory=list)

    def add(self, name: str, content: str):
        self._names.append(name)
        self._contents.append(content)

    def _repr_html_(self):
        contents = []
        pills = []

        for i, name in enumerate(self._names):
            active = i == 0
            id = name.replace(' ', '_').replace('-', '_')
            content = self._contents[i]

            pills.append(PILL.format(
                id=id, name=name, active='active' if active else ''))
            contents.append(CONTENT.format(
                id=id, content=content,
                active='display: block' if active else ''))

        pill = ''.join(pills)
        content = ''.join(contents)

        return BASE.format(pills=pill, contents=content)


BASE = '''
<div class="tabs_ipynb2md" role="tablist">
    {pills}
</div>

<div class="tabs_content_ipynb2md">
    {contents}
</div>
'''

PILL = '''
<button class="tab_link_ipynb2md {active}" onclick="showTab(event, '{id}')">{name}</button>
'''

CONTENT = '''
<div id="{id}" class="tab_content_ipynb2md" style="{active}">
  {content}
</div>
'''
