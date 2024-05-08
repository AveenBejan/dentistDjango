from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()
register.filter(intcomma)

@register.filter
def remove_quotes(value):
    return value.replace("'", "")


@register.filter
def split_by_comma(value):
    return value.split(',')


@register.filter
def format_with_commas(value):
    if value is not None:
        return "{:,}".format(value)
    return None