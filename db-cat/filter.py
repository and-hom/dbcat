from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
import logging
import util
from util import BaseManager

MAX_SELECT_OPTS = 1000


class FilterManager(BaseManager):
    def __init__(self):
        BaseManager.__init__(self, Filter)


class Filter(polymodel.PolyModel):
    code = ndb.StringProperty(indexed=True, required=True)
    name = ndb.StringProperty(indexed=True, required=True)
    description = ndb.TextProperty(indexed=False, required=False)

    def template(self):
        return util.camel_to_underscore(self.__class__.__name__)

    def from_request(self, req):
        self.name = req.get('name')
        self.code = req.get('code')
        self.description = req.get('desc')

    def db_params_from_request(self, req):
        return {self.code: int(req.get(self.code))}

    def criteria(self, request):
        return ndb.GenericProperty(self.code) == request.get(self.code)


class IntRangeFilter(Filter):
    min = ndb.IntegerProperty(indexed=False, required=False)
    max = ndb.IntegerProperty(indexed=False, required=False)

    def from_request(self, req):
        super(IntRangeFilter, self).from_request(req)
        self.min = int(req.get('min'))
        self.max = int(req.get('max'))

    def parse_int(self, str_val):
        try:
            return int(str_val)
        except:
            return None

    def criteria(self, request):
        _from = request.get('%s_from' % self.code)
        _to = request.get('%s_to' % self.code)
        return [ndb.GenericProperty(self.code) >= self.parse_int(_from) if _from else None,
                ndb.GenericProperty(self.code) <= self.parse_int(_to) if _to else None]


class BooleanFilter(Filter):
    def criteria(self, request):
        return ndb.GenericProperty(self.code) >= 50 if request.get(self.code) else None


class SelectFilter(Filter):
    required = ndb.BooleanProperty(indexed=False, required=True, default=False)
    options = ndb.JsonProperty(indexed=False, repeated=False)

    def options_from_request(self, req):
        options = {}
        i = 0
        while i < MAX_SELECT_OPTS:
            code = req.get('code_%i' % i)
            name = req.get('name_%i' % i)
            if code and name:
                i += 1
                options[code] = name
            else:
                break
        return options

    def from_request(self, req):
        super(SelectFilter, self).from_request(req)
        self.required = (req.get('required') == 'true')
        options = self.options_from_request(req)
        self.options = options


    def opt_param_name(self, opt):
        return '%s_%s' % (self.code, opt)

    def db_params_from_request(self, req):
        option_correlation_map = {}
        for opt in self.options:
            param_name = self.opt_param_name(opt)
            option_correlation_map[param_name] = int(req.get(param_name))
        return option_correlation_map


    def criteria(self, req):
        def option_or(or_cr, opt):
            return self.or_criterion(or_cr, self.option_criteria(req, opt))

        return reduce(option_or, self.options, None)

    def or_criterion(self, a, b):
        if a and b:
            return ndb.OR(a, b)
        return a or b

    def option_criteria(self, req, opt):
        param_name = self.opt_param_name(opt)
        return ndb.GenericProperty(param_name) >= 50 if req.get(param_name) else None


class FilterChangeRequest:
    pass