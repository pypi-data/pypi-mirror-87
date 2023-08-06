from django import template
from django.utils.safestring import mark_safe

from draftjs_exporter.html import HTML

from draftjstools.config import DRAFTJS_RENDER_CONFIG

exporter = HTML(DRAFTJS_RENDER_CONFIG)

register = template.Library()

@register.simple_tag(takes_context=True)        # Untested Tag
def draftjs_render(context, obj):
    data = exporter.render(obj)
    return mark_safe(data)
