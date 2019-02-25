# coding:utf-8
"""
@author:ww
@time:2018/3/9
@version:0.1
"""
from django import template
from django.template.defaultfilters import date
from django.utils.translation import ugettext as _

register = template.Library()


@register.filter('render_creator_and_date_time')
def render_creator_and_date_time(value, *args, **kwargs):
    at = _('at')
    created_by = _('created by')
    return '' + at + ' ' + str(date(value.created_date_time, 'Y-m-d H:i')) + ' ' + created_by + ' ' + str(value.creator)