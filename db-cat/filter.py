from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
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
        return {self.code: req.get(self.code)}


class IntRangeFilter(Filter):
    min = ndb.IntegerProperty(indexed=False, required=False)
    max = ndb.IntegerProperty(indexed=False, required=False)

    def from_request(self, req):
        super(IntRangeFilter, self).from_request(req)
        self.min = int(req.get('min'))
        self.max = int(req.get('max'))

class BooleanFilter(Filter):
    pass

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


    def db_params_from_request(self, req):
        option_correlation_map = {}
        for opt in self.options:
            param_name = '%s_%s' % (self.code, opt)
            option_correlation_map[param_name] = req.get(param_name)
        return option_correlation_map


class FilterChangeRequest:
    pass