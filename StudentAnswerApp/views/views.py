# coding:utf-8
"""
@author:ww
@time:2018/3/9
@version:0.1
"""
# Create your views here.
from braces.views._access import UserPassesTestMixin
from braces.views._ajax import JSONResponseMixin, AjaxResponseMixin
from braces.views._queries import SelectRelatedMixin, PrefetchRelatedMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.db.models import Count, Sum
from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from notifications.models import Notification

from StudentAnswerApp import forms, models, filters
from StudentAnswerApp.views.base import LoginRequiredCreateView, LoginRequiredListView, make_base_context_data, \
    LoginRequiredUpdateView, LoginRequiredTemplateView, LoginRequiredDetailView


class NotificationView(LoginRequiredListView):
    context_object_name = 'message_list'

    def get_context_data(self, **kwargs):
        context = super(NotificationView, self).get_context_data(**kwargs)
        f = filters.NotificationFilter(data=self.request.GET, queryset=self.get_queryset())
        context['filter'] = f
        return context

    def get_queryset(self):
        return self.request.user.notifications.all()


class NotificationMarkView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        notification_id = request.GET.get('id')
        mark_as_read_or_unread = request.GET.get('read_or_unread')
        if notification_id and mark_as_read_or_unread:
            if mark_as_read_or_unread == 'read':
                Notification.objects.get(id=notification_id).mark_as_read()
            else:
                Notification.objects.get(id=notification_id).mark_as_unread()
            json_dict = {'info': 'success'}
        else:
            json_dict = {'info': 'fail'}
        return self.render_json_response(json_dict)


class FavoriteView(LoginRequiredListView):
    # def get_context_data(self, **kwargs):
    #     context = super(FavoriteView, self).get_context_data(**kwargs)
    #     f = filters.QuestionFilter(data=self.request.GET, queryset=self.get_queryset())
    #     context['filter'] = f
    #     context['obj_list'] = f.qs
    #     return context

    def get_queryset(self):
        qs = models.Question.objects.filter(favorite_users=self.request.user)
        f = filters.QuestionFilter(data=self.request.GET, queryset=qs)
        self.filter = f
        return f.qs


class FavoriteMarkView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        question_id = request.GET.get('id')
        mark = request.GET.get('mark')
        if question_id and mark:
            if mark == '1':
                models.Question.objects.get(id=question_id).favorite_users.add(request.user)
            else:
                models.Question.objects.get(id=question_id).favorite_users.remove(request.user)
            json_dict = {'info': 'success'}
        else:
            json_dict = {'info': 'fail'}
        return self.render_json_response(json_dict)


class HomeView(ListView):
    # context_object_name = 'question_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return make_base_context_data(self.request, filter=self.filter, **context)

    def get_queryset(self):
        qs = models.Question.objects.all().annotate(favorite_users_total=Count('favorite_users')).order_by('-favorite_users_total')
        f = filters.QuestionFilter(data=self.request.GET, queryset=qs)
        self.filter = f
        return f.qs


class UserInformationView(LoginRequiredUpdateView):
    model = User
    form_class = forms.UserForm
    success_url = reverse_lazy('saa:user_information')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserInformationView, self).get_context_data(**kwargs)
        context = make_base_context_data(self.request, user_information=forms.PersonInformationForm(
            instance=self.get_object().person_information), **context)
        return context

    def post(self, request, *args, **kwargs):
        user_information = forms.PersonInformationForm(data=self.request.POST,
                                                       instance=self.get_object().person_information)
        if user_information.is_valid():
            user_information.save()
        return super(UserInformationView, self).post(request, *args, **kwargs)


class AnswerHistoryView(LoginRequiredListView):
    # def get_context_data(self, **kwargs):
    #     context = super(AnswerHistoryView, self).get_context_data(**kwargs)
    #     f = filters.AnswerFilter(data=self.request.GET, queryset=self.get_queryset())
    #     context['filter'] = f
    #     context['obj_list'] = f.qs
    #     return context

    def get_queryset(self):
        question = self.kwargs.get('pk')
        if question:
            qs = models.Answer.objects.filter(creator=self.request.user, question=question)
        else:
            qs = models.Answer.objects.filter(creator=self.request.user)
        f = filters.AnswerFilter(data=self.request.GET, queryset=qs)
        self.filter = f
        return f.qs


class AnswerCreateView(LoginRequiredCreateView):
    success_url = reverse_lazy('saa:index')
    model = models.Answer
    form_class = forms.AnswerForm
    inline_sub_answer_set = inlineformset_factory(model, models.SubAnswer, forms.SubAnswerForm,
                                                  fk_name='belong_to_answer', extra=1)

    def get_context_data(self, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(**kwargs)
        context['question'] = models.Question.objects.get(id=self.kwargs['pk'])
        context['sub_answers'] = self.inline_sub_answer_set()
        return make_base_context_data(self.request, **context)

    # def get(self, request, *args, **kwargs):
    #     return super(AddAnswerView, self).get(request, *args, **kwargs)

    def get_initial(self):
        cur_initial = super(AnswerCreateView, self).get_initial()
        cur_initial['question'] = self.kwargs['pk']
        return cur_initial

    def post(self, request, *args, **kwargs):
        question_ins = models.Question.objects.get(id=kwargs['pk'])
        # question_ins = question_ins.instance
        answer_ins = self.model.objects.create(question=question_ins, creator=request.user)
        answer = self.get_form_class()(data=request.POST, instance=answer_ins)
        sub_answers = self.inline_sub_answer_set(data=request.POST, instance=answer_ins)
        if sub_answers.is_valid():
            sub_answers.save()
            return self.form_valid(answer)
        else:
            # self.model.objects.filter(id=answer_ins.id).delete()
            return self.form_invalid(answer)


class QuestionAnswerView(LoginRequiredTemplateView):
    def get_context_data(self, **kwargs):
        context = super(QuestionAnswerView, self).get_context_data(**kwargs)
        question = models.Question.objects.get(id=kwargs['question_id'])
        answer = models.Answer.objects.get(id=kwargs['answer_id'])
        sub_questions_and_answers = zip(question.sub_questions.all(), answer.sub_answers.all())
        return make_base_context_data(self.request, question=question, answer=answer,
                                      sub_questions_and_answers=sub_questions_and_answers, **context)

    def get_queryset(self):
        return None


class QuestionListView(LoginRequiredListView):
    # def get_context_data(self, **kwargs):
    #     context = super(QuestionListView, self).get_context_data(**kwargs)
    #     f = filters.QuestionFilter(data=self.request.GET, queryset=self.get_queryset())
    #     context['filter'] = f
    #     context['obj_list'] = f.qs
    #     return context

    def get_queryset(self):
        qs = models.Question.objects.all()
        f = filters.QuestionFilter(data=self.request.GET, queryset=qs)
        self.filter = f
        return f.qs


class QuestionHistoryView(LoginRequiredListView):
    # def get_context_data(self, **kwargs):
    #     context = super(QuestionHistoryView, self).get_context_data(**kwargs)
    #     f = filters.QuestionFilter(data=self.request.GET, queryset=self.get_queryset())
    #     context['filter'] = f
    #     context['obj_list'] = f.qs
    #     return context

    def get_queryset(self):
        qs = models.Question.objects.filter(creator=self.request.user)
        f = filters.QuestionFilter(data=self.request.GET, queryset=qs)
        self.filter = f
        return f.qs


class QuestionDetailView(DetailView):
    model = models.Question

    # def get_context_data(self, **kwargs):
    #     context = super(QuestionDetailView, self).get_context_data(**kwargs)
    #     # context['sub_questions'] = models.SubQuestion.objects.filter(belong_to_question=self.get_object()).order_by(
    #     #     'order_number')
    #     # context['comment_object'] = context['question']
    #     return make_base_context_data(self.request, **context)


class QuestionCreateView(LoginRequiredCreateView):
    model = models.Question
    form_class = forms.QuestionForm
    answer_model = models.Answer
    success_url = reverse_lazy('saa:index')
    inline_sub_question_set = inlineformset_factory(model, models.SubQuestion, forms.SubQuestionForm,
                                                    fk_name='belong_to_question', extra=1)
    inline_sub_answer_set = inlineformset_factory(answer_model, models.SubAnswer, forms.SubAnswerForm,
                                                  fk_name='belong_to_answer', extra=1)

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        context['question'] = context['form']
        # self.inline_sub_queston_set = inlineformset_factory(self.model, models.SubQuestion, forms.SubQuestionForm,
        #                                                  fk_name='belong_to_question', extra=1)
        if self.request.method == 'POST':
            context['sub_questions'] = self.inline_sub_question_set(data=self.request.POST)
            context['sub_answers'] = self.inline_sub_answer_set(data=self.request.POST)
        else:
            context['sub_questions'] = self.inline_sub_question_set()
            context['sub_answers'] = self.inline_sub_answer_set()
        # context['sub_questions_management'] = context['sub_questions'].management_form
        # context['sub_answers_management'] = context['sub_answers'].management_form
        context['sub_questions_and_answers'] = zip(context['sub_questions'], context['sub_answers'])
        return make_base_context_data(self.request, **context)

    def get_object(self, queryset=None):
        return super(QuestionCreateView, self).get_object(queryset)

    # def get(self, request, *args, **kwargs):
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     return super(CreateQuestionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        question = forms.QuestionForm(data=request.POST)
        question.instance.creator = request.user
        if question.is_valid():
            question_ins = question.save()
            answer_ins = self.answer_model.objects.create(question=question_ins, creator=request.user)
            sub_questions = self.inline_sub_question_set(data=request.POST, instance=question_ins)
            sub_answers = self.inline_sub_answer_set(data=request.POST, instance=answer_ins)
            if sub_questions.is_valid() and sub_answers.is_valid():
                sub_answers.save()
                for sub_answer, sub_question in zip(sub_answers, sub_questions):
                    sub_question.instance.standard_answer = sub_answer.instance
                sub_questions.save()
                return self.form_valid(question)
            else:
                self.answer_model.objects.filter(id=answer_ins.id).delete()
                return self.form_invalid(question)
        else:
            self.object = None
            return self.form_invalid(question)

    def form_valid(self, form):
        return super(QuestionCreateView, self).form_valid(form)


class ClassCreateView(LoginRequiredCreateView):
    model = models.Class
    form_class = forms.ClassForm
    success_url = reverse_lazy('saa:class_in')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        form.instance.creator = request.user
        # form.instance.class_members.add(request.user)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ClassInView(LoginRequiredListView):
    # def get_context_data(self, **kwargs):
    #     context = super(ClassInView, self).get_context_data(**kwargs)
    #     # f = filters.ClassFilter(data=self.request.GET, queryset=self.get_queryset())
    #     context['filter'] = self.filter
    #     # context['obj_list'] = f.qs
    #     return context

    def get_queryset(self):
        qs = models.Class.objects.filter(Q(creator=self.request.user) | Q(class_members=self.request.user))
        f = filters.ClassFilter(data=self.request.GET, queryset=qs)
        self.filter = f
        return f.qs


class ClassJoinView(LoginRequiredListView):
    # def get_context_data(self, **kwargs):
    #     context = super(ClassJoinView, self).get_context_data(**kwargs)
    #     f = filters.ClassFilter(data=self.request.GET, queryset=self.get_queryset())
    #     context['filter'] = f
    #     context['obj_list'] = f.qs
    #     return context

    def get_queryset(self):
        qs = models.Class.objects.exclude(Q(creator=self.request.user) | Q(class_members=self.request.user))
        f = filters.ClassFilter(data=self.request.GET, queryset=qs)
        self.filter = f
        return f.qs


class ClassDetailView(LoginRequiredDetailView):
    model = models.Class

    def test_func(self):
        return self.request.user in self.get_object().class_members.all()

    def get(self, request, *args, **kwargs):
        if self.test_func():
            return super(ClassDetailView, self).get(request, *args, **kwargs)
        else:
            messages.warning(request,
                             _('You isn\'t in this class. so you haven\'t permission view this class of detail.'))
            return redirect(reverse_lazy('saa:class_join'), *args, **kwargs)
