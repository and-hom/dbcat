from django import template

from frontend.models import Filter
from frontend.util import camel_to_underscore


register = template.Library()


@register.filter
def template_name(value):
    filter_code = camel_to_underscore(value.__class__.__name__)
    return 'filters/%s.html' % filter_code


@register.filter
def template_name_db(form):
    value = get_filter_from_form(form)
    filter_code = camel_to_underscore(value.__class__.__name__)
    return 'filters/%s_db.html' % filter_code


@register.filter
def filter_name(form):
    return get_filter_from_form(form).name


@register.filter
def request_get_param(name, req):
    return req.GET.get(name)

@register.filter
def get_field_val(form, name):
    return form[name].value()

@register.filter
def get_item(dictionary, key):
    return dictionary[key]


@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name)


@register.filter
def get_filter_from_form(form):
    filter_id = get_field_val(form, 'filter_id')
    return get_filter_by_id(filter_id)


@register.filter
def get_filter_by_id(id):
    return Filter.objects.select_subclasses().get(code=id)