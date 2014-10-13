from functools import reduce
from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

# Create your views here.
from django.template.context import RequestContext
from frontend.forms import DbForm, FilterFormFactory, SelectFilterOptionFormSet, DbParamFormSet, DbParamForm
from frontend.models import Filter, SelectFilter, Db, DbParam


def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request, {
                                  "filters": Filter.objects.select_subclasses(),
                                  "search_result": Db.objects.all()
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


def db(request):
    if request.method == 'POST':
        form = DbForm(request.POST)
        param_formset = DbParamFormSet(request.POST)
        if form.is_valid():
            param_formset.instance = form.instance
            if param_formset.is_valid():
                form.save()
                param_formset.save()
                return HttpResponseRedirect('/')
    else:
        form = DbForm()
        param_formset = db_param_formset()

    return render_to_response('add_db.html', context_instance=RequestContext(request, {
        'form': form,
        'param_formset': param_formset,
    }))


# Список форм для параметров базы
def db_param_formset():
    filters = Filter.objects.select_subclasses()
    param_form_objects = reduce(lambda pfo, filter: pfo + filter.param_form_objects(), filters, [])

    param_formset = inlineformset_factory(Db, DbParam, extra=len(param_form_objects), can_delete=False,
                                          form=DbParamForm)(instance=Db())

    for subform, form in zip(param_formset.forms, param_form_objects):
        subform.initial = form
        subform.filter = form['filter']
        subform.filter_id = form['filter_id']
    return param_formset


def db_param_form_count(filters):
    """
    Каждый фильтр может порождать более чем одну характеристику базы. Например, select порождает
    столько характеристик, сколько у него опций.
    :param filters:
    :return:
    """
    return reduce(lambda sum, filter: sum + filter.db_param_count(), filters)
