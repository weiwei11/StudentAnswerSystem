# coding:utf-8
"""
@author:weiwei
@time:2018.01.30
@version:0.1
"""

# import re

# from django.core.exceptions import ValidationError
# from django.db import models
# from django.utils.translation import ugettext_lazy as _

# def parse_hand(hand_string):
#     """Takes a string of cards and splits into a full hand."""
#     p1 = re.compile('.{26}')
#     p2 = re.compile('..')
#     args = [p2.findall(x) for x in p1.findall(hand_string)]
#     if len(args) != 4:
#         raise ValidationError(_("Invalid input for a Score instance"))
#     return Hand(*args)

# class ScoreField(models.PositiveSmallIntegerField):

#     def __init__(self, *args, **kwargs):
#         super(ScoreField, self).__init__(*args, **kwargs)

#     def from_db_value(self, value, expression, connection, context):
#         if value is None:
#             return value
#         return value

#     def to_python(self, value):
#         if isinstance(value, ScoreField):
#             return value

#         if value is None:
#             return value

#         return parse_hand(value)

#     def get_prep_value(self, value):
#         return ''.join([''.join(l) for l in (value.north,
#                 value.east, value.south, value.west)])

