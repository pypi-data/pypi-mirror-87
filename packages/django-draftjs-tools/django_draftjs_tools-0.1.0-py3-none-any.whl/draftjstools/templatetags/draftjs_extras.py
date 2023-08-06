from django import template
# from django.utils.html import format_html
from django.utils.safestring import mark_safe

from draftjs_exporter.html import HTML

register = template.Library()

config = {}

exporter = HTML(config)

@register.simple_tag(takes_context=True)        # Untested Tag
def draftjs_render(context, obj):
    return mark_safe(exporter.render(obj))


"""
html = exporter.render({
    'entityMap': {},
    'blocks': [{
        'key': '6mgfh',
        'text': 'Hello, world!',
        'type': 'unstyled',
        'depth': 0,
        'inlineStyleRanges': [],
        'entityRanges': []
    }]
})
"""
