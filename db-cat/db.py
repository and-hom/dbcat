from google.appengine.ext import ndb
import logging
from util import BaseManager


class DbManager(BaseManager):
    def __init__(self):
        BaseManager.__init__(self, Db)

    def query(self, criteria):
        logging.info(criteria)
        return reduce(lambda q, cr: q.filter(cr) if cr else q, criteria, Db.query()).fetch()


class Db(ndb.Expando):
    name = ndb.StringProperty(indexed=True, required=True)
    short_description = ndb.TextProperty(indexed=False, required=True)
    description = ndb.TextProperty(indexed=False, required=False)
    homepage = ndb.StringProperty(indexed=False, required=True)

    def from_request(self, request):
        self.name = request.get('name')
        self.short_description = request.get('short_description')
        self.description = request.get('description')
        self.homepage = request.get('homepage')

    def add_params(self, params):
        for p in params:
            setattr(self, p, params[p])