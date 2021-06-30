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

@register.filter
def shrink_num(value):
    """
    Shrinks number rounding
    123456  > 123,5K
    123579  > 123,6K
    1234567 > 1,2M
    """
    value = str(value)

    if value.isdigit():
        value_int = int(value)

        if value_int > 1000000:
            value = "%.1f%s" % (value_int/1000000.00, 'm')
        else:
            if value_int > 1000:
                value = "%.1f%s" % (value_int/1000.0, 'k')

    return value