import random
from django import template

register = template.Library()

@register.simple_tag
def random_int():
    # r = lambda: random.randint(0,255)
    # print('#%02X%02X%02X' % (r(),r(),r()))
    color = "#%06x" % random.randint(0, 0xFFFFFF)
    return color