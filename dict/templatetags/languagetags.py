from django import template

from dict.models import DictEntry

register = template.Library()

@register.simple_tag
def get_language_direction(m):
    return DictEntry.get_ordered_languages()[m-1].direction.lower()