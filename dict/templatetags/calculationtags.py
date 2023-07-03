from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return int(value) * int(arg)

@register.filter
def add(value, arg):
    return int(value) + int(arg)
