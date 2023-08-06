![Django Draft.js Tools CI](https://github.com/renderbox/django-draftjs-tools/workflows/Django%20Draft.js%20Tools%20CI/badge.svg)

![Django Draft.js Tools Develop](https://github.com/renderbox/django-draftjs-tools/workflows/Django%20Draft.js%20Tools%20Develop/badge.svg?branch=develop)

# Django Draft.js Tools

Django Tools around DraftJS format


## Installation

```shell
> pip install django-draftjs-tools
```

Add it to your list of apps in Django

```python
INSTALLED_APPS = [
    ...
    'draftjstools',
    ...
]
```

## Template Tag

At the top of your template make sure to include this after the 'extends' tag if used.

```html
{% load draftjs_tools %}
```

Now pass in the draft.js data to the tag to see it render on the screen in HTML.

```html
{% draftjs_render object.data %}
```
