from django import template
from django.templatetags.static import static

from pagina46.utils import render_tag

register = template.Library()


@register.simple_tag
def p46_css():
    p46_css = dict(href=static('css/p46style.css'), rel="stylesheet")
    return render_tag("link", attrs=p46_css)
