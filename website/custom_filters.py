from django import template

register = template.Library()


@register.filter
def remove_quotes(value):
    return value.replace("'", "")


@register.filter
def split_by_comma(value):
    return value.split(',')
