from django import template

from frontend.util import camel_to_underscore


register = template.Library()


@register.filter
def template_name(value):
    filter_code = camel_to_underscore(value.__class__.__name__)
    return 'filters/%s.html' % filter_code


@register.filter
def template_name_db(value):
    filter_code = camel_to_underscore(value.__class__.__name__)
    return 'filters/%s_db.html' % filter_code


@register.filter
def request_get_param(name, req):
    return req.GET.get(name)


@register.filter
def get_item(dictionary, key):
    return dictionary[key]


@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name)