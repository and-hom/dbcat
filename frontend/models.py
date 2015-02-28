from django.db import models
from model_utils.managers import InheritanceManager


class Filter(models.Model):
    code = models.CharField(null=False, blank=False, db_index=True, max_length=32, primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=128)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(null=False, default=10)

    objects = InheritanceManager()

    def initial(self):
        return {
            "filter_id": self.code
        }

    @classmethod
    def form_type(cls):
        from frontend.forms import SimpleDbParamForm

        return SimpleDbParamForm

    def sql_where_clauses(self, get):
        return ''

    def sql_rank(self, get):
        return self.sql_rank_clause() + ' THEN ' + self.sql_rank_value(get) if self.present(get) else None

    def sql_rank_clause(self):
        code = self.code
        return 'p.filter_id=\'%(code)s\'' %locals()

    def sql_rank_value(self, get):
        return ''

    def present(self, get):
        return get.get(self.code)


class IntRangeFilter(Filter):
    min = models.IntegerField()
    max = models.IntegerField()

    @classmethod
    def form_type(cls):
        from frontend.forms import IntRangeDbParamForm

        return IntRangeDbParamForm

    def sql_where_clauses(self, get):
        code=self.code
        _from = get.get('%s_from' % self.code)
        _to = get.get('%s_to' % self.code)

        if _from and _to:
           return  'p.filter_id=\'%(code)s\' AND sp.value BETWEEN %(_from)s AND %(_to)s' %locals()
        if _from:
           return  'p.filter_id=\'%(code)s\' AND sp.value >= %(_from)s' %locals()
        if _to:
           return  'p.filter_id=\'%(code)s\' AND sp.value <= %(_to)s' %locals()
        return None

    def sql_rank_value(self, get):
        return '100'

    def present(self, get):
        return get.get('%s_from' %self.code) or get.get('%s_to' %self.code)


class BooleanFilter(Filter):
    def sql_where_clauses(self, get):
        code=self.code
        lim=50

        if self.on(get):
           return  'p.filter_id=\'%(code)s\' AND sp.value>=%(lim)i' %locals()
        if self.off(get):
           return  'p.filter_id=\'%(code)s\' AND sp.value<=%(lim)i' %locals()
        return None


    def sql_rank_value(self, get):
        if self.on(get):
            return  'COALESCE(sp.value,0)'
        if self.off(get):
           return  '100-COALESCE(sp.value,0)'
        return '0'


    def on(self, get):
        return get.get(self.code) == 'on'

    def off(self, get):
        return get.get(self.code) == 'off'


class SelectFilter(Filter):
    required = models.BooleanField(default=False)

    def opts(self):
        return SelectOption.objects.filter(filter=self)

    @classmethod
    def form_type(cls):
        from frontend.forms import SelectDbParamForm

        return SelectDbParamForm


    def initial(self):
        initial_data = {
            "filter_id": self.code
        }
        for option in self.selectoption_set.all():
            initial_data[option.code] = 0
        return initial_data


    def sql_where_clauses(self, get):
        code=self.code
        selected_opts=self.get_selected_opts(get)
        lim=30

        if len(selected_opts)>0:
           return  'p.filter_id=\'%(code)s\' AND spo.option_id IN (%(selected_opts)s) AND spo.value>%(lim)i' %locals()

        return None


    def sql_rank_value(self, get):
        return  'COALESCE(spo.value,0)'


    def get_selected_opts(self,get):
        selected_opt_ids=[]
        selected = get.get(self.code)
        for option in self.selectoption_set.all().iterator():
            if selected and option.code in selected:
                selected_opt_ids.append(str(option.id))
        return ','.join(selected_opt_ids)


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
        return DbParam.objects.select_subclasses().filter(db_id=self.id).order_by('filter__priority', 'filter__code')

    @property
    def usefull_links(self):
        return DbUsefullLink.objects.filter(db_id=self.id).order_by('short_description')

    @classmethod
    def find_by_filters(cls, request):
        where_clauses = []
        rank = []
        filter_codes_arr = []
        filters = Filter.objects.select_subclasses().all()
        for filter in filters:
            where_clauses.append(filter.sql_where_clauses(request.GET))
            rank.append(filter.sql_rank(request.GET))
            if filter.present(request.GET):
                filter_codes_arr.append(filter.code)
        sql = Db.build_filter_query( where_clauses, rank, filter_codes_arr)
        return Db.objects.raw(sql)


    @classmethod
    def build_filter_query(cls, where_clauses_arr, rank_arr, filter_codes_arr):
        fields = 'db.id,db.name,db.short_description,db.description,homepage'
        db_table = cls.objects.model._meta.db_table
        db_param_table = DbParam.objects.model._meta.db_table
        simple_db_param_table = SimpleDbParam.objects.model._meta.db_table
        select_db_param_option_table = SelectDbParamOption.objects.model._meta.db_table

        rank_expr = cls.rank_expr(rank_arr)
        where_clauses = cls.where_expr(where_clauses_arr)
        all_filters_ok = cls.filter_code_expr(filter_codes_arr)

        return 'SELECT %(fields)s FROM (' \
               ' SELECT %(fields)s, p.filter_id AS filter_id,' \
               ' %(rank_expr)s AS rank' \
               ' FROM %(db_table)s db' \
               ' LEFT OUTER JOIN %(db_param_table)s p ON p.db_id=db.id ' \
               ' LEFT OUTER JOIN %(simple_db_param_table)s sp ON sp.dbparam_ptr_id=p.id' \
               ' LEFT OUTER JOIN %(select_db_param_option_table)s spo ON spo.param_id=p.id' \
               ' %(where_clauses)s' \
               ' ) db' \
               ' GROUP BY %(fields)s' \
               ' %(all_filters_ok)s' \
               ' ORDER BY sum(rank) DESC, name ASC' \
               % (locals())

    @classmethod
    def rank_expr(cls, rank_arr):
        rank_arr = list(filter(None, rank_arr))
        return ('CASE  WHEN ' + (' WHEN '.join(rank_arr)) + ' ELSE 0 END') if len(rank_arr) > 0 else '0'

    @classmethod
    def where_expr(cls, where_clauses_arr):
        where_clauses_arr = list(filter(None, where_clauses_arr))
        return ('WHERE ' + ' OR '.join(where_clauses_arr)) if len(where_clauses_arr) > 0 else ''

    @classmethod
    def filter_code_expr(cls, filter_codes_arr):
        if len(filter_codes_arr) == 0:
            return ''
        filter_codes_arr = list(map(lambda x: '\'%s\'::character varying' % x, filter_codes_arr))
        return ('HAVING array_agg(filter_id) @> ARRAY[' + ','.join(filter_codes_arr) + ']::character varying[]')


class DbParam(models.Model):
    db = models.ForeignKey(Db, null=False)
    filter = models.ForeignKey(Filter, null=False)
    objects = InheritanceManager()


class SimpleDbParam(DbParam):
    value = models.IntegerField(null=False)
    comment = models.TextField(null=True, blank=True, max_length=512)


class SelectDbParam(DbParam):
    @property
    def options(self):
        return self.selectdbparamoption_set.all()


class SelectDbParamOption(models.Model):
    param = models.ForeignKey(SelectDbParam, null=False)
    option = models.ForeignKey(SelectOption, null=False)
    value = models.IntegerField(null=False)
    comment = models.TextField(null=True, blank=True, max_length=512)


class DbUsefullLink(models.Model):
    db = models.ForeignKey(Db, null=False)
    short_description = models.CharField(null=False, blank=False, max_length=128)
    link = models.URLField()

