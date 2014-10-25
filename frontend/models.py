from django.db import models
from model_utils.managers import InheritanceManager


class Filter(models.Model):
    code = models.CharField(null=False, blank=False, db_index=True, max_length=32, primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=128)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(null=False, default=10)

    objects = InheritanceManager()

    def create_db_param(self):
        return SimpleDbParam()

    def initial(self):
        return {}

    @classmethod
    def form_type(cls):
        from frontend.forms import SimpleDbParamForm

        return SimpleDbParamForm


class IntRangeFilter(Filter):
    min = models.IntegerField()
    max = models.IntegerField()


class BooleanFilter(Filter):
    pass


class SelectFilter(Filter):
    required = models.BooleanField(default=False)

    def opts(self):
        return SelectOption.objects.filter(filter=self)

    def create_db_param(self):
        param = SelectDbParam()
        for option in self.selectoption_set:
            param_option = SelectDbParamOption()
            param_option.param = param
            param_option.option = option
            param.selectdbparamoption_set.add(param_option)
        return param


    @classmethod
    def form_type(cls):
        from frontend.forms import SelectDbParamForm

        return SelectDbParamForm

    def initial(self):
        initial_data = {}
        for option in self.selectoption_set.all():
            initial_data[option.code] = 0
        return initial_data


class SelectOption(models.Model):
    filter = models.ForeignKey(SelectFilter)
    code = models.CharField(null=False, blank=False, db_index=True, max_length=32)
    name = models.CharField(null=False, blank=False, max_length=64)


class Db(models.Model):
    name = models.CharField(null=False, blank=False, max_length=64)
    short_description = models.TextField(null=False, blank=False, max_length=512)
    description = models.TextField()
    homepage = models.URLField()

    @property
    def sorted_param_set(self):
        return self.dbparam_set.order_by('filter__priority', 'filter__code')


class DbParam(models.Model):
    db = models.ForeignKey(Db, null=False)
    filter = models.ForeignKey(Filter, null=False)


class SimpleDbParam(DbParam):
    value = models.IntegerField(null=False)


class SelectDbParam(DbParam):
    pass


class SelectDbParamOption(models.Model):
    param = models.ForeignKey(SelectDbParam, null=False)
    option = models.ForeignKey(SelectOption, null=False)
    value = models.IntegerField(null=False)
