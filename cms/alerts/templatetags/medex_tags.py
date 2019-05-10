from django import template

from medexCms.utils import get_code_version

register = template.Library()


@register.simple_tag
def code_version():
    return get_code_version()
