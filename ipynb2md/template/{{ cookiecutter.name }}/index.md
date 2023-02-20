Welcome to {{ cookiecutter.project }}'s documentation!
=================================

{{ cookiecutter.description }}

```{toctree}
:maxdepth: 2
:caption: Contents

{% for file in cookiecutter.files.path %}
{{ file }}
{% endfor %}
```
