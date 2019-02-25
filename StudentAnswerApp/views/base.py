# coding:utf-8
"""
@author:ww
@time:2018/3/9
@version:0.1
"""

from braces import views
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView


def make_base_context_data(request, **kwargs):
    context = {
        # 'user': request.user,
        # 'has_permission': request.user.is_authenticated,
    }
    context.update(kwargs)
    return context


class LoginRequiredMixin(views.LoginRequiredMixin):
    login_url = reverse_lazy('saa:login')

    def get_context_data(self, **kwargs):
        context = super(LoginRequiredMixin, self).get_context_data(**kwargs)
        title = self.__class__.__name__.replace('View', '')
        return make_base_context_data(self.request, title=title, **context)


class LoginRequiredListView(LoginRequiredMixin, ListView):
    context_object_name = 'obj_list'
    paginate_by = 6
    filter = None

    def get_context_data(self, **kwargs):
        context = super(LoginRequiredListView, self).get_context_data(**kwargs)
        # f = filters.ClassFilter(data=self.request.GET, queryset=self.get_queryset())
        context['filter'] = self.filter
        # context['obj_list'] = f.qs
        return context


class LoginRequiredCreateView(LoginRequiredMixin, CreateView):
    pass


class LoginRequiredUpdateView(LoginRequiredMixin, UpdateView):
    pass


class LoginRequiredTemplateView(LoginRequiredMixin, TemplateView):
    pass


class LoginRequiredDetailView(LoginRequiredMixin, DetailView):
    pass


def _get_next(request):
    """
    The part that's the least straightforward about views in this module is
    how they determine their redirects after they have finished computation.

    In short, they will try and determine the next place to go in the
    following order:

    1. If there is a variable named ``next`` in the *POST* parameters, the
       view will redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters,
       the view will redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers,
       the view will redirect to that previous page.
    """
    next = request.POST.get('next', request.GET.get('next',
                            request.META.get('HTTP_REFERER', None)))
    if not next:
        next = request.path
    return next