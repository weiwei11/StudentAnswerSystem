# coding:utf-8
"""
@author:ww
@time:2018/3/23
@version:0.1
"""
from django import forms
from django.forms.widgets import TextInput


class TagsInput(TextInput):
    input_type = 'tagsinput'
    template_name = 'extend_util/tagsinput.html'

    # def render(self, name, value, attrs=None, renderer=None):
    #     if attrs:
    #         attrs.update({'data-role': 'tagsinput'})
    #     else:
    #         attrs = {'data-role': 'tagsinput'}
    #     return super(TagsInput, self).render(name, value, attrs, renderer)

    def _get_media(self):
        return forms.Media(css={'all': ('extend_util/tagsinput.css',)},
                           js=('extend_util/jquery.tagsinput.js', 'extend_util/tagsinput.active.js'))

    media = property(_get_media)


class RangeWidget(forms.MultiWidget):
    template_name = 'extend_util/rangewidget.html'

    def __init__(self, attrs=None):
        widgets = (forms.TextInput,)
        if attrs is None:
            attrs = dict()
        attrs['daterangepicker'] = 'daterangepicker'
        super(RangeWidget, self).__init__(widgets, attrs)

    # def format_output(self, rendered_widgets):
    #     # Method was removed in Django 1.11.
    #     return '-'.join(rendered_widgets)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        datelist = super(RangeWidget, self).value_from_datadict(data, files, name)
        data = datelist[0]
        if data is None:
            return []
        else:
            return data.split(' -- ')

    def _get_media(self):
        media = super(RangeWidget, self)._get_media()
        return media + forms.Media(css={'all': ('extend_util/daterangepicker/daterangepicker.css',)},
                                   js=(
                                       'extend_util/daterangepicker/moment.js',
                                       'extend_util/daterangepicker/date.js',
                                       'extend_util/daterangepicker/daterangepicker.js',
                                       'extend_util/daterangepicker.active.js'))

    media = property(_get_media)
