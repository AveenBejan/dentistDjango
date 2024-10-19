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
    """
    Custom template filter to format a number with commas for thousands separators.
    Remove unnecessary decimals and trailing zeros.
    """
    try:
        value = float(value)
        formatted_value = "{:,.2f}".format(value).rstrip('0').rstrip('.')
        return formatted_value if '.' in formatted_value else "{:,.0f}".format(value)
    except (TypeError, ValueError):
        return value

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)