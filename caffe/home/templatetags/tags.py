import re

from django import template
from django.core.urlresolvers import NoReverseMatch, reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    """Check if pattern matches in URL.

    Args:
        context (str): Context which has to be checked.
        pattern_or_urlname (url): Pattern which is searched in context request.

    Returns:
        str('active') if pattern matches, str('') otherwise.
    """
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.filter(name='field_type')
def field_type(field):
    """Get field type from field."""

    return field.field.widget.__class__.__name__
