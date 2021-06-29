import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import urlize as urlize_impl

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def urlize_target_blank(text, autoescape=None):
    return re.sub("<a([^>]+)(?<!target=)>",'<a target="_blank"\\1 class="caption-url">',text)
url_target_blank = register.filter(urlize_target_blank, is_safe = True)