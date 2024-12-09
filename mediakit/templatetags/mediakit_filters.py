from django import template

register = template.Library()

@register.filter
def abbreviate_number(value):
    if value >= 1000000:
        return f"{value/1000000:.1f}M"
    elif value >= 1000:
        return f"{value/1000:.1f}K"
    else:
        return value