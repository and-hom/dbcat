from django.forms.fields import CharField, IntegerField
from django.forms.models import ModelForm, inlineformset_factory
from django.forms.util import ErrorList
from django.forms.widgets import HiddenInput, TextInput

from frontend.models import Db, BooleanFilter, SelectFilter, IntRangeFilter, SelectOption, SimpleDbParam, \
    SelectDbParam, Filter
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
    filter_id = CharField(max_length=32, widget=HiddenInput())

    def after_filter_set(self):
        pass

    @property
    def as_custom_layout(self):
        return self.as_table()


class SimpleDbParamForm(DbParamForm):

    class Meta:
        model = SimpleDbParam
        fields = ('value', 'filter_id', )
        widgets = {
            'value': RangeInput(attrs={'value': 0, 'label': '######'}),
        }

    def as_custom_layout(self):
        return self.as_p()


    def after_filter_set(self):
        self.fields['value'].label = ''

class IntRangeDbParamForm(SimpleDbParamForm):
    def after_filter_set(self):
        super().after_filter_set()
        self.fields['value'].widget.attrs['min']=self.filter.min
        self.fields['value'].widget.attrs['max']=self.filter.max


class SelectDbParamForm(DbParamForm):
    class Meta:
        model = SelectDbParam
        fields = ('filter_id',)

    def after_filter_set(self):
        for option in self.filter.selectoption_set.all():
            self.fields[option.code] = IntegerField(min_value=0, max_value=100,
                                                    widget=RangeInput(attrs={'label': option.name}))


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

