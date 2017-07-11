from django import template
import time
import os

register = template.Library()

@register.simple_tag
def GED_url():
    return "http://demoged.datasystems.fr:8080"

