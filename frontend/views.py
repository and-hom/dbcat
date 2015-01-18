from functools import reduce

from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response


# Create your views here.
from django.template.context import RequestContext
from frontend.forms import DbForm, FilterFormFactory, SelectFilterOptionFormSet
from frontend.models import Filter, SelectFilter, Db


def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request, {
                                  "filters": Filter.objects.select_subclasses(),
                                  "search_result": Db.find_by_filters(request)
                              }))

def boolean_filter(request):
    return filter(request, 'boolean_filter')


def int_range_filter(request):
    return filter(request, 'int_range_filter')


def filter(request, type):
    if request.method == 'POST':
        form = FilterFormFactory(request.POST).form(type)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = FilterFormFactory([]).form(type)

    template_name = 'filters/%s_edit.html' % (type)
    return render_to_response(template_name, context_instance=RequestContext(request, {
        'form': form,
    }))


def select_filter(request):
    type = 'select_filter'
    if request.method == 'POST':
        form = FilterFormFactory(request.POST).form(type)
        options_formset = SelectFilterOptionFormSet(request.POST)

        if form.is_valid():
            filter = form.save()
            options_formset.instance = filter
            if options_formset.is_valid():
                options_formset.save()
                return HttpResponseRedirect('/')
    else:
        form = FilterFormFactory([]).form(type)
        options_formset = SelectFilterOptionFormSet(instance=SelectFilter())

    template_name = 'filters/%s_edit.html' % (type)
    return render_to_response(template_name, context_instance=RequestContext(request, {
        'form': form,
        'options_formset': options_formset,
    }))


def set_filter_links(param_formset):
    for form in param_formset:
        id = form['filter_id'].value()
        filter = Filter.objects.select_subclasses().get(code=id)
        form.instance.filter = filter


def db(request):
    if request.method == 'POST':
        form = DbForm(request.POST)
        param_formsets = db_param_formsets(request.POST)
        if save_if_valid(form, param_formsets):
            return HttpResponseRedirect('/')
    else:
        form = DbForm()
        param_formsets = db_param_formsets()

    return render_to_response('add_db.html', context_instance=RequestContext(request, {
        'form': form,
        'param_formsets': param_formsets,
    }))


def save_if_valid(form, param_formsets):
    if form.is_valid():
        formsets_are_all_valid = all_valid(form, param_formsets)
        if formsets_are_all_valid:
            db = form.save()
            save_formsets(param_formsets, db)
            return True
    return False


def all_valid(form, param_formsets):
    result = True
    for param_formset in param_formsets:
        param_formset.instance = form.instance
        set_filter_links(param_formset)
        if not param_formset.is_valid():
            result = False
    return result


def save_formsets(param_formsets, db):
    for param_formset in param_formsets:
        for form in param_formset.forms:
            form.instance.db = db
        param_formset.save()


def db_param_formsets(post=None):
    """
    Список форм для параметров базы
    :return:
    """
    filters = Filter.objects.select_subclasses()
    by_type = filters_by_type(filters)
    return create_formsets(by_type, post).values()


def filters_by_type(filters):
    def add_to_dict(dict, filter):
        key = filter.__class__
        old_val = dict.get(key, [])
        new_val = old_val + [filter]
        dict[key] = new_val
        return dict

    return reduce(add_to_dict, filters, {})


def create_formsets(by_type, post=None):
    result = {}
    for type, filters in by_type.items():
        forms = formset(type.form_type(), type.__name__, filters, post)
        result[type] = forms
    return result


def formset(form_type, prefix, filters, post=None):
    size = len(filters) if filters else 0
    param_type = form_type.Meta.model
    formset_type = inlineformset_factory(Db, param_type, extra=size, can_delete=False, form=form_type)

    if post:
        _formset = formset_type(post, instance=Db(), prefix=prefix)
    else:
        _formset = formset_type(instance=Db(), prefix=prefix)

    for subform, filter in zip(_formset.forms, filters):
        subform.initial = filter.initial()
        subform.filter = filter
        subform.filter_id = filter.code
        subform.after_filter_set()
    return _formset

