from django import template

from frontend.models import Filter
from frontend.util import camel_to_underscore
import re


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
def template_name_value(filter_id):
    filter = get_filter_by_id(filter_id)
    filter_code = camel_to_underscore(filter.__class__.__name__)
    return 'filters/%s_value.html' % filter_code


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
def count_opts_more_then_x_grade(lst, min):
    return len(list(filter(lambda x: x.value>=min, lst)))


@register.filter
def get_filter_by_id(id):
    return Filter.objects.select_subclasses().get(code=id)

class SetVarNode(template.Node):
    def __init__(self, new_val, var_name):
        self.new_val = new_val
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = self.new_val
        return ''

@register.tag(name="setvar")
def setvar(parser,token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])

    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    new_val, var_name = m.groups()
    if not (new_val[0] == new_val[-1] and new_val[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return SetVarNode(new_val[1:-1], var_name)

@register.inclusion_tag(name="help", file_name="tags/help_tag.html")
def help_tag(msg):
    return {'msg':msg}