from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.html import format_html
from django.utils.safestring import mark_safe

def text_value(value):
    """Force a value to text, render None as an empty string."""
    if value is None:
        return ""
    return force_str(value)


def render_tag(tag, attrs=None, content=None, close=True):
    """Render a HTML tag."""
    builder = "<{tag}{attrs}>{content}"
    if content or close:
        builder += "</{tag}>"
    return format_html(builder, tag=tag, attrs=mark_safe(flatatt(attrs)) if attrs else "", content=text_value(content))