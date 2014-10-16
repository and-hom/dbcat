from django.db import models
from model_utils.managers import InheritanceManager


class Filter(models.Model):
    code = models.CharField(null=False, blank=False, db_index=True, max_length=32, primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=128)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(null=False, default=10)

    objects = InheritanceManager()


    def param_form_objects(self):
        return [{
                    'filter': self,
                    'filter_id': self.code,
                    'code': self.code,
                    'name': self.name,
                }]


class IntRangeFilter(Filter):
    min = models.IntegerField()
    max = models.IntegerField()


class BooleanFilter(Filter):
    pass


class SelectFilter(Filter):
    required = models.BooleanField(default=False)

    def opts(self):
        return SelectOption.objects.filter(filter=self)

    def param_form_objects(self):
        return list(map(self.option_to_db_param_form, self.opts()))

    def option_to_db_param_form(self, option):
        return {
            'filter': self,
            'filter_id': self.code,
            'code': option.code,
            'name': option.name,
        }


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
        return self.dbparam_set.order_by('filter__priority','filter__code')


class DbParam(models.Model):
    db = models.ForeignKey(Db, null=False)
    filter = models.ForeignKey(Filter, null=True)
    code = models.CharField(null=True, blank=True, max_length=32)
    value = models.IntegerField()

    @property
    def select_option_name(self):
        option = SelectOption.objects.get(code=self.code)
        return option.name if option else 'Undefined'
