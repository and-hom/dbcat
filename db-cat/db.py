from google.appengine.ext import ndb

class DBManager:
    def list(self):
        return DB.query().fetch()

class DB(ndb.Model):
    name = ndb.StringProperty(indexed=True, required=True)
    short_description = ndb.TextProperty(indexed=False, required=True)
    description = ndb.TextProperty(indexed=False, required=False)
    homepage = ndb.StringProperty(indexed=False, required=True)
    filter_matching_map = ndb.JsonProperty()