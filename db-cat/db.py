from google.appengine.ext import ndb
from util import BaseManager


class DbManager(BaseManager):
    def __init__(self):
        BaseManager.__init__(self, Db)


class Db(ndb.Model):
    name = ndb.StringProperty(indexed=True, required=True)
    short_description = ndb.TextProperty(indexed=False, required=True)
    description = ndb.TextProperty(indexed=False, required=False)
    homepage = ndb.StringProperty(indexed=False, required=True)
    filter_matching_map = ndb.JsonProperty()

    def from_request(self, request):
        self.name = request.get('name')
        self.short_description = request.get('short_description')
        self.description = request.get('description')
        self.homepage = request.get('homepage')