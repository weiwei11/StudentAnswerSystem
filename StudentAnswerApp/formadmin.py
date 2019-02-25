# coding:utf-8
"""
@author:weiwei
@time:2018.02.20
@version:0.1
"""

import types

from django.forms.models import ModelForm, BaseModelFormSet, BaseInlineFormSet, modelformset_factory, \
    inlineformset_factory
from django.http.response import HttpResponseNotFound
from django.shortcuts import render

from StudentAnswerApp.views.base import make_base_context_data


class FormAdmin(object):
    def __init__(self, model, model_form=ModelForm, formset=BaseModelFormSet, inlineformset=BaseInlineFormSet,
                 formfield_callback=None, extra=0, can_delete=False,
                 can_order=False, max_num=None, fields=None, exclude=None,
                 widgets=None, validate_max=False, localized_fields=None,
                 labels=None, help_texts=None, error_messages=None,
                 min_num=None, validate_min=False, field_classes=None):
        super(FormAdmin, self).__init__()

        self.model = model
        self.model_form = model_form
        self.formset = formset
        self.inlineformset = inlineformset
        self.formfield_callback = formfield_callback
        self.extra = extra
        self.can_delete = can_delete
        self.can_order = can_order
        self.max_num = max_num
        self.min_num = min_num
        self.fields = fields if fields is not None else '__all__'
        self.exclude = exclude
        self.localized_fields = localized_fields
        self.widgets = widgets
        self.field_classes = field_classes
        self.labels = labels
        self.help_texts = help_texts
        self.error_messages = error_messages
        self.validate_max = validate_max
        self.validate_min = validate_min

        self.modelformset = self.get_modelformset()
        self.queryset = None
        self.inlines = []

    def get_modelformset(self):
        return modelformset_factory(self.model, form=self.model_form, formset=self.formset,
                                    formfield_callback=self.formfield_callback, extra=self.extra,
                                    can_delete=self.can_delete, can_order=self.can_order, max_num=self.max_num,
                                    min_num=self.min_num, fields=self.fields, exclude=self.exclude,
                                    localized_fields=self.localized_fields, widgets=self.widgets,
                                    field_classes=self.field_classes, labels=self.labels, help_texts=self.help_texts,
                                    error_messages=self.error_messages, validate_max=self.validate_max,
                                    validate_min=self.validate_min)

    def get_inline_modelformset(self, parent_formadmin, fk_name):
        return inlineformset_factory(parent_formadmin.model, self.model, self.model_form, formset=self.inlineformset,
                                     fk_name=fk_name, formfield_callback=self.formfield_callback, extra=self.extra,
                                     can_delete=self.can_delete, can_order=self.can_order, max_num=self.max_num,
                                     min_num=self.min_num, fields=self.fields, exclude=self.exclude,
                                     localized_fields=self.localized_fields, widgets=self.widgets,
                                     field_classes=self.field_classes, labels=self.labels, help_texts=self.help_texts,
                                     error_messages=self.error_messages, validate_max=self.validate_max,
                                     validate_min=self.validate_min
                                     )

    def add_inline_formadmins(self, formadmin_list, fk_name_list):
        for formadmin, fk_name in zip(formadmin_list, fk_name_list):
            inline_modelformset = formadmin.get_inline_modelformset(parent_formadmin=self, fk_name=fk_name)
            self.inlines.append({'formadmin': formadmin, 'modelformset': inline_modelformset, 'fk_name': fk_name})

    def get_form_set_tree(self, form_set):
        modelform_set_tree = list()
        if form_set:
            for form in form_set:
                form_set_tree_childs = []
                if self.inlines:
                    for inline in self.inlines:
                        form_instance = form.instance
                        inline_formset = inline['modelformset'](instance=form_instance)
                        form_set_tree_child = inline['formadmin'].get_form_set_tree(inline_formset)
                        form_set_tree_childs.append(form_set_tree_child)
                modelform_set_tree.append({'current_form': form, 'formsettree_childs': form_set_tree_childs})
        return modelform_set_tree

    def get_form_list(self, form_set):
        form_list = list()
        if form_set:
            for form in form_set:
                form_list.append(form)
                if self.inlines:
                    for inline in self.inlines:
                        form_instance = form.instance
                        inline_formset = inline['modelformset'](instance=form_instance)
                        sub_form_list = inline['formadmin'].get_form_list(inline_formset)
                        form_list.extend(sub_form_list)
        return form_list

    def get_formset_list(self, form_set):
        formset_list = list()
        if form_set:
            formset_list.append(form_set)
            for form in form_set:
                if self.inlines:
                    for inline in self.inlines:
                        form_instance = form.instance
                        inline_formset = inline['modelformset'](instance=form_instance)
                        sub_formset_list = inline['formadmin'].get_formset_list(inline_formset)
                        formset_list.extend(sub_formset_list)
        return formset_list

    def get_queryset(self):
        return self.queryset if self.queryset is not None else self.model.objects.all()

    def get(self, request, **kwargs):
        template_name = kwargs['template_name']
        # context = make_base_context_data(request)
        queryset = self.get_queryset()
        # context.update(formsetlist=self.get_formset_list(self.modelformset(queryset=queryset)))
        context = make_base_context_data(request,
                                         formsetlist=self.get_formset_list(self.modelformset(queryset=queryset)))
        return render(request, template_name=template_name, context=context)

    def change_get_method(self, get_method):
        if hasattr(get_method, '__call__'):
            self._get = self.get
            self.get = types.MethodType(get_method, self)

    def save_as_inline(self, request, instance, inline_modelformset):
        form_set = inline_modelformset(data=request.POST, files=request.FILES, instance=instance)
        if form_set.is_valid():
            form_set.save()
            for form in form_set:
                if self.inlines:
                    for inline in self.inlines:
                        self.save_as_inline(request, form.instance, inline['modelformset'])

    def save(self, request, queryset):
        form_set = self.modelformset(data=request.POST, files=request.FILES, queryset=queryset)
        if form_set.is_valid():
            form_set.save()
            for form in form_set:
                if self.inlines:
                    for inline in self.inlines:
                        inline['formadmin'].save_as_inline(request, form.instance, inline['modelformset'])

    def post(self, request, **kwargs):
        template_name = kwargs['template_name']
        # context = make_base_context_data(request)
        queryset = self.get_queryset()
        # formset = self.modelformset(data=request.POST, files=request.FILES, queryset=queryset)
        # if formset.is_valid():
        #     formset.save()
        self.save(request, queryset=queryset)
        # context.update(formsetlist=self.get_formset_list(self.modelformset(queryset=queryset)))
        context = make_base_context_data(request,
                                         formsetlist=self.get_formset_list(self.modelformset(queryset=queryset)))
        return render(request, template_name=template_name, context=context)

    def change_post_method(self, post_method):
        if hasattr(post_method, '__call__'):
            self._post = self.post
            self.post = types.MethodType(post_method, self)

    def view_proxy(self, request, **kwargs):
        request_method_map = {
            'POST': self.post,
            'GET': self.get,
        }

        request_method = request_method_map.get(request.method, None)
        if request_method is not None:
            return request_method(request, **kwargs)
        else:
            return HttpResponseNotFound()
