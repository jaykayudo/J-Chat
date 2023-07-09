from django import template
register = template.Library()

@register.filter(name = 'short')
def splicestring(value):
    return value[0:2]