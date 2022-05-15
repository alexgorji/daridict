from django import template
from django.forms import CharField

register = template.Library()


@register.filter()
def as_p_with_autofocus(form):
    for key in form.fields:
        field = form.fields[key]
        if isinstance(field, CharField):
            field.widget.attrs.update({'autofocus': ''})
            break
    return form.as_p()


@register.filter
def subtract(value1, value2):
    if value1 is None or value1 == '':
        value1 = 0
    if value2 is None or value2 == '':
        value2 = 0
    return value1 - value2


@register.filter()
def add_placeholder(boundfield, placeholder):
    if placeholder is None:
        return boundfield
    else:
        boundfield.field.widget.attrs.update({'placeholder': placeholder})
        return boundfield
