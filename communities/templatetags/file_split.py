from django import template

register = template.Library()


@register.filter(name="split")
def file_split(value, arg):
    value = str(value)
    return value.split(arg)[1]
