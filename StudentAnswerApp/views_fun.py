# coding:utf-8
"""
@author:weiwei
@time:2018.01.27
@version:0.1
"""
import json

from braces.views._access import LoginRequiredMixin
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from notifications.models import Notification

from StudentAnswerApp.filters import ClassFilter
from StudentAnswerApp.formadmin import make_base_context_data, FormAdmin
from StudentAnswerApp.forms import UserCreationForm
from StudentAnswerApp.models import PersonInformation, Answer, Class, Question
from StudentAnswerApp.views import views
from StudentAnswerApp import filters, models


# Create your views here.

@csrf_protect
def register(request, template_name='registration/register.html'):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # if request.is_ajax():
            #     to_json_response = dict()
            #     to_json_response['status'] = 1
            #     to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
            #     to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
            #     return HttpResponse(json.dumps(to_json_response), content='application/json')
            return HttpResponseRedirect(reverse_lazy('saa:login'))
        else:
            # if request.is_ajax():
            #     to_json_response = dict()
            #     to_json_response['status'] = 0
            #     to_json_response['form_errors'] = form.errors
            #     to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
            #     to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
            #     return HttpResponse(json.dumps(to_json_response), content_type='application/json')

            return render(request, template_name, {'form': form})
    else:
        form = UserCreationForm()
        # t = loader.get_template('register.html')
        # c = RequestContext(request, {'form': form})
        # return t.render(c)
        # return render(RequestContext(request, {'form': form}), template_name='register.html')
        return render(request, template_name, {'form': form})


def home(request, **kwargs):
    # return render(request, template_name, context=make_base_context_data(request))
    # return views.HomeView.as_view(**kwargs)(request, **kwargs)
    # f = filters.QuestionFilter(request.GET)
    # return render(request, kwargs['template_name'], context=make_base_context_data(request, filter=f))
    return views.HomeView.as_view(**kwargs)(request, **kwargs)


def user_information(request, **kwargs):
    return views.UserInformationView.as_view(**kwargs)(request, **kwargs)


# def user_information(request, **kwargs):
#     user_fields = ('username', 'first_name', 'last_name', 'email', 'last_login')
#     user_form_admin = FormAdmin(User, fields=user_fields, extra=0)
#     # def get(self, request, **kwargs):
#     #     template_name = kwargs['template_name']
#     #     obj_id = kwargs['id']
#     #     # user = request.user
#     #     context = make_base_context_data(request)
#     #     # context.update(formsettree=self.get_form_set_tree(self.modelformset(queryset=User.objects.filter(pk=obj_id))))
#     #     context.update(formlist=self.get_form_list(self.modelformset(queryset=User.objects.filter(pk=obj_id))))
#     #     return render(request, template_name=template_name, context=context)
#     # user_form_admin.change_get_method(get)
#     user_id = request.user.id
#     user_form_admin.queryset = User.objects.filter(pk=user_id)
#     person_information_form_admin = FormAdmin(PersonInformation)
#     user_form_admin.add_inline_formadmins([person_information_form_admin], ['user'])
#     return user_form_admin.view_proxy(request, **kwargs)
#     # AuthorFormSet = modelformset_factory(User, fields=user_fields, extra=0)
#     # if request.method == "POST":
#     #     formset = AuthorFormSet(
#     #         request.POST, request.FILES,
#     #         queryset=User.objects.filter(pk=kwargs['id']),
#     #     )
#     #     if formset.is_valid():
#     #         formset.save()
#     #         # Do something.
#     # else:
#     #     formset = AuthorFormSet(queryset=User.objects.filter(pk=kwargs['id']))
#     # context = make_base_context_data(request)
#     # context.update(formlist=formset)
#     # return render(request, template_name=kwargs['template_name'], context=context)


def answer_history(request, **kwargs):
    # answer_fields = ('question', 'created_date_time')
    # answer_form_admin = FormAdmin(Answer, fields=answer_fields)
    # user_id = request.user.id
    # context = make_base_context_data(request, answer_list=Answer.objects.filter(creator=user_id))
    # # answer_form_admin.queryset = Answer.objects.filter(creator=user_id)
    # # return answer_form_admin.view_proxy(request, **kwargs)
    # return render(request, template_name=kwargs['template_name'], context=context)
    return views.AnswerHistoryView.as_view(template_name=kwargs['template_name'])(request, **kwargs)


def answer_create(request, **kwargs):
    return views.AnswerCreateView.as_view(template_name=kwargs['template_name'])(request, **kwargs)


def question_and_answer(request, **kwargs):
    return views.QuestionAnswerView.as_view(template_name=kwargs['template_name'])(request, **kwargs)


def question_list(request, **kwargs):
    return views.QuestionListView.as_view(**kwargs)(request, **kwargs)


def question_detail(request, **kwargs):
    return views.QuestionDetailView.as_view(template_name=kwargs['template_name'])(request, **kwargs)


def question_history(request, **kwargs):
    return views.QuestionHistoryView.as_view(**kwargs)(request, **kwargs)


def question_create(request, **kwargs):
    return views.QuestionCreateView.as_view(**kwargs)(request, **kwargs)


def class_in(request, **kwargs):
    # user = request.user
    # f = ClassFilter(data=request.GET, queryset=Class.objects.filter(Q(class_members=user) | Q(creator=user)))
    # context = make_base_context_data(request, title='Class In', obj_list=f.qs, filter=f)
    # context = make_base_context_data(request, class_list=request.user.class_set)
    # return render(request, template_name=kwargs['template_name'], context=context)
    return views.ClassInView.as_view(**kwargs)(request, **kwargs)


def class_create(request, **kwargs):
    return views.ClassCreateView.as_view(**kwargs)(request, **kwargs)


def class_join(request, **kwargs):
    return views.ClassJoinView.as_view(**kwargs)(request, **kwargs)


def class_join_do(request, **kwargs):
    _class = models.Class.objects.get(id=kwargs.pop('pk'))
    _class.class_members.add(request.user)
    return views.ClassJoinView.as_view(**kwargs)(request, **kwargs)


def class_detail(request, **kwargs):
    return views.ClassDetailView.as_view(template_name=kwargs['template_name'])(request, **kwargs)


def notification(request, **kwargs):
    # user_id = request.user.id
    # context = make_base_context_data(request, message_list=Message.objects.filter(to_user=user_id))
    # return render(request, template_name=kwargs['template_name'], context=context)
    # return render(request, template_name=kwargs['template_name'], context=make_base_context_data(request))
    return views.NotificationView.as_view(**kwargs)(request, **kwargs)


def mark_as_read_or_unread(request, **kwargs):
    return views.NotificationMarkView.as_view(**kwargs)(request, **kwargs)


def favorite(request, **kwargs):
    return views.FavoriteView.as_view(**kwargs)(request, **kwargs)


def favorite_mark(request, **kwargs):
    return views.FavoriteMarkView.as_view(**kwargs)(request, **kwargs)


def recommend(request, **kwargs):
    return render(request, template_name=kwargs['template_name'], context=make_base_context_data(request))


def search(request, **kwargs):
    return render(request, template_name=kwargs['template_name'], context=make_base_context_data(request))

# from django.contrib.auth.decorators import login_required
# from django.widgets.decorators import method_decorator
# from django.views.generic import TemplateView
# decorators = [never_cache, login_required]
#
# @method_decorator(decorators, name='dispatch')
# class ProtectedView(TemplateView):
#     template_name = 'secret.html'

# from django.db.models.signals import post_save
# from notifications.signals import notify
# from StudentAnswerApp.models import Examination
#
#
# def my_handler(sender, instance, created, **kwargs):
#     notify.send(instance, verb='was saved')
#
# post_save.connect(my_handler, sender=Examination)
#
# from notifications.signals import notify
# notify.send(user, recipient=user, verb='you reached level 10')
