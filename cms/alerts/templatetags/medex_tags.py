from urllib.parse import urlencode

from django import template

from medexCms import settings
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


@register.simple_tag
def logout_period():
    return settings.LOGOUT_IF_IDLE_PERIOD


@register.simple_tag
def refresh_period():
    return settings.REFRESH_PERIOD
