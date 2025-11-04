import re
from django import template

register = template.Library()

@register.filter
def digits(value):
    """Renvoie uniquement les chiffres d'une chaîne"""
    if not value:
        return ''
    return re.sub(r'\D', '', str(value))
