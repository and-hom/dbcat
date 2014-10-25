from django.forms.fields import CharField, IntegerField
from django.forms.models import ModelForm, inlineformset_factory
from django.forms.util import ErrorList
from django.forms.widgets import HiddenInput, TextInput

from frontend.models import Db, BooleanFilter, SelectFilter, IntRangeFilter, SelectOption, DbParam, SimpleDbParam, \
    SelectDbParam
from frontend.util import underscore_to_camel


class RangeInput(TextInput):
    input_type = 'range'


class ValueFieldLabelRetriever:
    def __init__(self, instance):
        self.instance = instance

    def __repr__(self, *args, **kwargs):
        try:
            return self.instance.filter.name
        except:
            return '######'


class DbForm(ModelForm):
    class Meta:
        model = Db


class DbParamForm(ModelForm):
    def after_filter_set(self):
        pass

    @property
    def as_custom_layout(self):
        return self.as_table()


class SimpleDbParamForm(DbParamForm):
    filter_id = CharField(max_length=32, widget=HiddenInput())

    class Meta:
        model = SimpleDbParam
        fields = ('value', )
        widgets = {
            'value': RangeInput(attrs={'min': 0, 'max': 100, 'value': 0, 'label': '######'}),
        }

    def as_custom_layout(self):
        return self.as_p()


    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance)
        self.fields['value'].label = ''


class SelectDbParamForm(DbParamForm):
    class Meta:
        model = SelectDbParam
        fields = ()


    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance)

    def after_filter_set(self):
        for option in self.filter.selectoption_set.all():
            self.fields[option.code] = IntegerField(min_value=0, max_value=100,
                                                    widget=RangeInput(attrs={'label': option.name}))
    #
    # def as_custom_layout(self):
    #     return '<table>' + self.as_table() + '</table>'


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

