from django import template
import math
register = template.Library()

@register.filter
def tb_value(num):
    return math.floor(num/1024)

@register.filter
def gb_value(num):
    return num % 1024