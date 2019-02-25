# coding:utf-8
"""
@author:weiwei
@time:2018.01.27
@version:0.1
"""
import permission
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

import StudentAnswerApp
from StudentAnswerApp import views_fun as views
from StudentAnswerApp import tests
from django.conf import settings

from StudentAnswerApp.views.views import UserInformationView

app_name = 'saa'
urlpatterns = [
    # registration
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logged_out.html', 'next_page': 'saa:index'},
        name='logout'),
    url(r'^password_reset_done/$', auth_views.password_reset_done,
        {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': 'registration/password_reset_form.html',
         'post_reset_redirect': reverse_lazy('saa:password_reset_done')
         },
        name='password_reset'),
    url(r'^password_change_done/$', auth_views.password_change_done,
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),
    url(r'^password_change/$', auth_views.password_change,
        {'template_name': 'registration/password_change_form.html',
         'post_change_redirect': reverse_lazy('saa:password_change_done')},
        name='password_change'),
    url(r'^register/$', views.register, {'template_name': 'registration/register.html'}, name='register'),

    # main page
    url(r'^home/', views.home, {'template_name': 'saa/home.html'}, name='index'),
    # url(r'^user_information/$', views.user_information, {'template_name': 'saa/user_information.html'},
    #     name='user_information'),
    url(r'^user_information/$', UserInformationView.as_view(template_name='saa/user_information.html'),
        name='user_information'),
    # notification
    url(r'^notification/$', views.notification, {'template_name': 'saa/notification.html'}, name='notification'),
    url(r'^notification/mark_as_read_or_unread/$', views.mark_as_read_or_unread, name='mark_as_read_or_unread'),

    url(r'^search/$', views.search, {'template_name': 'saa/search_widget.html'}, name='search'),

    # url(r'^answer_history/$', render, {'template_name': 'saa/answer_history_without_login.html'},
    # name='answer_history_without_login'),
    # answer
    url(r'^answer/history/$', views.answer_history, {'template_name': 'saa/answer_list.html'},
        name='answer_history'),
    url(r'^answer/create/(?P<pk>[0-9]+)/', views.answer_create, {'template_name': 'saa/answer_create.html'},
        name='answer_create'),
    url(r'^answer/question/(?P<pk>[0-9]+)/$', views.answer_history, {'template_name': 'saa/answer_list.html'},
        name='answer_for_question'),

    url(r'^question/answer/(?P<question_id>[0-9]+)/(?P<answer_id>[0-9]+)/', views.question_and_answer,
        {'template_name': 'saa/question_and_answer.html'}, name='question_and_answer'),
    # question
    url(r'^question/list/$', views.question_list, {'template_name': 'saa/question_list.html'}, name='question_list'),
    url(r'^question/history/$', views.question_history, {'template_name': 'saa/question_list.html'},
        name='question_history'),
    url(r'^question/create/$', views.question_create, {'template_name': 'saa/question_create.html'},
        name='question_create'),
    url(r'^question/detail/(?P<pk>[0-9]+)/', views.question_detail, {'template_name': 'saa/question_detail.html'},
        name='question_detail'),

    # class
    url(r'^class/in/$', views.class_in, {'template_name': 'saa/class_list.html'}, name='class_in'),
    url(r'^class/create/$', views.class_create, {'template_name': 'saa/class_create.html'}, name='class_create'),
    url(r'^class/join/$', views.class_join, {'template_name': 'saa/class_list.html'}, name='class_join'),
    url(r'^class/join/do/(?P<pk>[0-9]+)/$', views.class_join_do, {'template_name': 'saa/class_list.html'},
        name='class_join_do'),
    url(r'^class/detail/(?P<pk>[0-9]+)/', views.class_detail, {'template_name': 'saa/class_detail.html'}, name='class_detail'),

    url(r'^favorite/mark/$', views.favorite_mark, name='favorite_mark'),
    url(r'^favorite/$', views.favorite, {'template_name': 'saa/question_list.html'}, name='favorite'),

    # recommend
    url(r'^recommend/$', views.recommend, {'template_name': 'saa/recommend.html'}, name='recommend'),

]

if settings.DEBUG is True:
    urlpatterns += [
        url(r'testforms/$', tests.test_forms),
    ]
