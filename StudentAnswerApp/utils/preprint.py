# coding:utf-8
"""
@author:weiwei
@time:2018.02.01
@version:0.1
"""

models = [
    'PersonInformation',
    'Question',
    'SubQuestion',
    'ExaminationPaper',
    'ExaminationQuestionGroup',
    'ExaminationQuestion',
    'SubExaminationQuestion',
    'Examination',
    'Answer',
    'SubAnswer',
    'ExaminationAnswerPaper',
    'ExaminationAnswerGroup',
    'ExaminationAnswer',
    'SubExaminationAnswer',
    'UserExaminationRecord',
    'Class',
    'Discussion',
]

s = []
for model in models:
    s.append(model + 'FormSet() = modelformset_factory(' + model + ', fields=\'__all__\')' + '\n')
with open('preprint.txt', 'w') as f:
    f.writelines(s)
