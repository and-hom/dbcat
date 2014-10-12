from django.forms.models import ModelForm, inlineformset_factory

from frontend.models import Db, BooleanFilter, SelectFilter, IntRangeFilter, SelectOption, DbParam
from frontend.util import underscore_to_camel


class DbForm(ModelForm):
    class Meta:
        model = Db


class DbParamForm(ModelForm):
    class Meta:
        model = DbParam
        fields = ('value',)


DbParamFormSet = inlineformset_factory(Db, DbParam, can_delete=False, form=DbParamForm)


class BooleanFilterForm(ModelForm):
    class Meta:
        model = BooleanFilter


class SelectFilterForm(ModelForm):
    class Meta:
        model = SelectFilter


SelectFilterOptionFormSet = inlineformset_factory(SelectFilter, SelectOption, can_delete=False)


class IntRangeFilterForm(ModelForm):
    class Meta:
        model = IntRangeFilter


class FilterFormFactory:
    def __init__(self, req_post):
        super().__init__()
        self.req_post = req_post

    def form(self, f_type):
        return self.form_class(f_type)(self.req_post)

    def form_class(self, f_type):
        filter_class_name = underscore_to_camel(f_type) + 'Form'
        filter_package = __import__('frontend', fromlist=['frontend'])
        filter_package = getattr(filter_package, 'forms')
        return getattr(filter_package, filter_class_name)
