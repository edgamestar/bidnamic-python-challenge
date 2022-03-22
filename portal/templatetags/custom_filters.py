__author__ = 'Edward'
"""
Usage: custom_filters.py

This holds all template helper functions that can be used across the project.
"""

from django import template

register = template.Library()


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)
