# coding:utf-8
"""
@author:ww
@time:2018/3/19
@version:0.1
"""
import django_filters
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_filters import filters
from notifications.models import Notification

from StudentAnswerApp import models
from extend_util.widgets import RangeWidget


class QuestionFilter(django_filters.FilterSet):
    # created_date_time = filters.DateFilter(field_name='created_date_time', label='date')
    order = filters.OrderingFilter(fields=(('created_date_time', 'date time'),
                                           ('id', 'question id')))
    datetime_range = filters.DateFromToRangeFilter(name='created_date_time', widget=RangeWidget)
    tags = filters.AllValuesMultipleFilter(name='tags')
    creator = filters.ModelMultipleChoiceFilter(name='creator', to_field_name='id', queryset=User.objects.all())
    content = filters.CharFilter(name='content_description', lookup_expr='contains')

    class Meta:
        model = models.Question
        fields = []


class AnswerFilter(django_filters.FilterSet):
    order = filters.OrderingFilter(fields=(('created_date_time', 'date time'),
                                           ('id', 'answer id')))
    datetime_range = filters.DateTimeFromToRangeFilter(name='created_date_time', widget=RangeWidget)
    # creator = filters.ModelMultipleChoiceFilter(name='creator', to_field_name='id', queryset=)
    question_content = filters.CharFilter(name='question__content_description', lookup_expr='contains')

    class Meta:
        model = models.Answer
        fields = []


class ClassFilter(django_filters.FilterSet):
    order = filters.OrderingFilter(fields=(('created_date_time', 'date time'),
                                           ('id', 'class id'),
                                           ('name', 'name')))
    datetime_range = filters.DateTimeFromToRangeFilter(name='created_date_time', widget=RangeWidget)
    class_description = filters.CharFilter(name='description', lookup_expr='contains')
    creator = filters.ModelMultipleChoiceFilter(name='creator', to_field_name='id', queryset=User.objects.all())
    tags = filters.MultipleChoiceFilter(name='tags')

    class Meta:
        model = models.Class
        fields = []


class NotificationFilter(django_filters.FilterSet):
    unread_choices = (
        (True, _('unread')),
        (False, _('read'))
    )

    all = filters.ChoiceFilter(name='unread', choices=unread_choices, empty_label=_('All'))
    level = filters.ChoiceFilter(name='level', choices=Notification.LEVELS, empty_label=_('Level'))
    description = filters.CharFilter(name='description', lookup_expr='contains')
    timestamp = filters.DateFromToRangeFilter(name='timestamp', widget=RangeWidget)

    class Meta:
        model = Notification
        fields = []
