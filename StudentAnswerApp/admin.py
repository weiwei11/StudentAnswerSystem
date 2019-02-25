# coding:utf-8
"""
@author:weiwei
@time:2018.01.30
@version:0.1
"""

from django.contrib.admin import ModelAdmin
from django.contrib import admin
from StudentAnswerApp.models import *

# Register your models here.


admin.site.register(PersonInformation)
admin.site.register(Question)
admin.site.register(SubQuestion)
# admin.site.register(ExaminationPaper)
# admin.site.register(ExaminationQuestionGroup)
# admin.site.register(ExaminationQuestion)
# admin.site.register(SubExaminationQuestion)
# admin.site.register(Examination)
admin.site.register(Answer)
admin.site.register(SubAnswer)
# admin.site.register(ExaminationAnswerPaper)
# admin.site.register(ExaminationAnswerGroup)
# admin.site.register(ExaminationAnswer)
# admin.site.register(SubExaminationAnswer)
# admin.site.register(UserExaminationRecord)
admin.site.register(Class)
# admin.site.register(Discussion)


# from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User

# from my_user_profile_app.models import Employee

# # Define an inline admin descriptor for Employee model
# # which acts a bit like a singleton
# class EmployeeInline(admin.StackedInline):
#     model = Employee
#     can_delete = False
#     verbose_name_plural = 'employee'

# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (EmployeeInline, )

# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
