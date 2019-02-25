# coding:utf-8
"""
@author:weiwei
@time:2018.01.30
@version:0.1
"""

from django.test import TestCase
from StudentAnswerApp.forms import *
from django.shortcuts import render

# Create your tests here.


def test_forms(request):
    forms_set = [
        PersonInformationFormSet(queryset=PersonInformation.objects.all()),
        # QuestionFormSet(),
        # SubQuestionFormSet(),
        # ExaminationPaperFormSet(),
        # ExaminationQuestionGroupFormSet(),
        # ExaminationQuestionFormSet(),
        # SubExaminationQuestionFormSet(),
        # ExaminationFormSet(),
        # AnswerFormSet(),
        # SubAnswerFormSet(),
        # ExaminationAnswerPaperFormSet(),
        # ExaminationAnswerGroupFormSet(),
        # ExaminationAnswerFormSet(),
        # SubExaminationAnswerFormSet(),
        # UserExaminationRecordFormSet(),
        # ClassFormSet(),
        # DiscussionFormSet(),
        UserInformationInlineModelSet(instance=request.user)
    ]
    return render(request, 'test/testforms.html', {'formsset': forms_set})

# class MyTestCase(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         super(MyTestCase, cls).setUpClass()
#
#     @classmethod
#     def tearDownClass(cls):
#         super(MyTestCase, cls).tearDownClass()
#
#     @classmethod
#     def setUpTestData(cls):
#         # Set up data for the whole TestCase
#         cls.foo = Foo.objects.create(bar="Test")
