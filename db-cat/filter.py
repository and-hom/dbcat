from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
import util


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


class IntRangeFilter(Filter):
    min = ndb.IntegerProperty(indexed=False, required=False)
    max = ndb.IntegerProperty(indexed=False, required=False)


class BooleanFilter(Filter):
    pass


class SelectFilter(Filter):
    required = ndb.BooleanProperty(indexed=False, required=True, default=False)
    options = ndb.StringProperty(indexed=False, repeated=True)
