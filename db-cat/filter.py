from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
import util

MAX_SELECT_OPTS = 1000


class FilterManager:
    def list(self):
        return Filter.query().fetch()


class Filter(polymodel.PolyModel):
    code = ndb.StringProperty(indexed=True, required=True)
    name = ndb.StringProperty(indexed=True, required=True)
    description = ndb.TextProperty(indexed=False, required=False)

    def id(self):
        return self.key.id()

    def template(self):
        return util.camel_to_underscore(self.__class__.__name__)

    def from_request(self, req):
        self.name = req.get('name')
        self.code = req.get('code')
        self.description = req.get('desc')


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


class FilterChangeRequest:
    pass