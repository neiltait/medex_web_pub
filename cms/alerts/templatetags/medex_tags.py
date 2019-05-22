from urllib.parse import urlencode

from django import template

from medexCms.utils import get_code_version

register = template.Library()


@register.simple_tag
def code_version():
    return get_code_version()


@register.simple_tag
def queryparams(*_, **kwargs):
    safe_args = {key: value for key, value in kwargs.items() if value is not None}
    if safe_args:
        return '?{}'.format(urlencode(safe_args))
    return ''
