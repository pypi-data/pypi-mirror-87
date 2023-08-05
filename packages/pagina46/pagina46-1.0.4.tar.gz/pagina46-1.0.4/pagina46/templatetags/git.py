import subprocess

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def git_revisions_hash():
    if settings.DEBUG:
        try:
            return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode("utf-8")
        except:
            return 'Any commit found'
    else:
        return ''


@register.simple_tag
def git_branch():
    if settings.DEBUG:
        try:
            return subprocess.check_output(['git', 'branch', '--show-current']).decode("utf-8")
        except:
            return 'Not a branch'
    else:
        return ''
