# coding:utf-8
"""
@author:weiwei
@time:2018.02.01
@version:0.1
"""
from captcha.fields import CaptchaField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth import forms as auth_forms
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.widgets import HiddenInput
from django.forms.models import ModelForm

from StudentAnswerApp.models import *
from extend_util.widgets import TagsInput

PersonInformationFormSet = modelformset_factory(PersonInformation, fields='__all__')
QuestionFormSet = modelformset_factory(Question, fields='__all__')
SubQuestionFormSet = modelformset_factory(SubQuestion, fields='__all__')
# ExaminationPaperFormSet = modelformset_factory(ExaminationPaper, fields='__all__')
# ExaminationQuestionGroupFormSet = modelformset_factory(ExaminationQuestionGroup, fields='__all__')
# ExaminationQuestionFormSet = modelformset_factory(ExaminationQuestion, fields='__all__')
# SubExaminationQuestionFormSet = modelformset_factory(SubExaminationQuestion, fields='__all__')
# ExaminationFormSet = modelformset_factory(Examination, fields='__all__')
AnswerFormSet = modelformset_factory(Answer, fields='__all__')
SubAnswerFormSet = modelformset_factory(SubAnswer, fields='__all__')
# ExaminationAnswerPaperFormSet = modelformset_factory(ExaminationAnswerPaper, fields='__all__')
# ExaminationAnswerGroupFormSet = modelformset_factory(ExaminationAnswerGroup, fields='__all__')
# ExaminationAnswerFormSet = modelformset_factory(ExaminationAnswer, fields='__all__')
# SubExaminationAnswerFormSet = modelformset_factory(SubExaminationAnswer, fields='__all__')
# UserExaminationRecordFormSet = modelformset_factory(UserExaminationRecord, fields='__all__')
ClassFormSet = modelformset_factory(Class, fields='__all__')
# DiscussionFormSet = modelformset_factory(Discussion, fields='__all__')
UserInformationInlineModelSet = inlineformset_factory(User, PersonInformation, fields='__all__')


class CaptchaFormMixin(ModelForm):
    captcha = CaptchaField()


class UserCreationForm(CaptchaFormMixin, auth_forms.UserCreationForm):
    # captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class PersonInformationForm(ModelForm):
    class Meta:
        model = PersonInformation
        fields = ('nickname', 'gender', 'age')


class QuestionForm(ModelForm):

    # share_classes = ModelMultipleChoiceField(widget=BootstrapSelect(choices={
    #     1: '23', 2: '33'
    # }), queryset=Question.objects.all())

    class Meta:
        model = Question
        fields = ('content_description', 'accessible_groups', 'share_classes', 'tags')
        widgets = {'tags': TagsInput, 'content_description': CKEditorUploadingWidget()}

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['accessible_groups'].required = False
        self.fields['share_classes'].required = False


class SubQuestionForm(ModelForm):
    class Meta:
        model = SubQuestion
        fields = ('order_number', 'content', 'kind', 'auto_correction')


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('question',)
        widgets = {
            # 'creator': HiddenInput,
            'question': HiddenInput,
        }


class SubAnswerForm(ModelForm):
    class Meta:
        model = SubAnswer
        fields = ('order_number', 'content')


class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ('name', 'tags', 'description')
        widgets = {'tags': TagsInput}
