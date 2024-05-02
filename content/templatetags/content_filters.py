from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="cut")
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")

@register.filter
def lower(value):
    """Converts a string into all lowercase"""
    return value.lower()

@register.filter(name='format_time')
def format_time(value):
    hrs, rem = divmod(value.seconds, 3600)
    mins, secs = divmod(rem, 60)
    time = ''
    
    if (hrs > 0):
        time += f'{hrs}:'
        if (mins < 10):
            time += f'0'

    if (secs < 10):
        return time + f'{mins}:0{secs}'
    
    return time + f'{mins}:{secs}'
    
@register.filter(name='format_thousand_num')
def format_thousand_num(value):
    try:
        return f'{int(value):,}'
    except:
        return value
