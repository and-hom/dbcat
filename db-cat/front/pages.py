import logging
import webapp2
from db import Db, DbManager
from filter import FilterManager, Filter
import frontend
from util import camel_to_underscore, underscore_to_camel


class BasePage(webapp2.RequestHandler):
    filter_manager = FilterManager()
    db_manager = DbManager()

    def get(self):
        template_values = self.model()
        templte_filename = self.template_name() + '.html'
        template = frontend.JINJA_ENVIRONMENT.get_template(templte_filename)
        self.response.write(template.render(template_values))

    def model(self):
        return {}

    def template_name(self):
        return 'index'


class MainPage(BasePage):
    def model(self):
        return {
            "filters": self.filter_manager.list(),
            "search_result": self.db_manager.query(self.criteria())
        }

    def criteria(self):
        return reduce(self.one_filter_criteria, self.filter_manager.list(), [])

    def one_filter_criteria(self, total_criteria, filter):
        filter_criteria = filter.criteria(self.request)
        if not filter_criteria:
            return total_criteria
        if isinstance(filter_criteria, (list, tuple)):
            return total_criteria + filter_criteria
        return total_criteria + [filter_criteria]


class ChangeRequestPage(BasePage):
    pass


class FilterChangeRequestPage(ChangeRequestPage):
    def template_name(self):
        return 'add_filter'

    def model(self):
        return {
            "filter_types": self.filter_types()
        }

    def filter_types(self):
        return map(self.class_to_name, Filter.__subclasses__())

    def class_to_name(self, clazzz):
        return camel_to_underscore(clazzz.__name__)

    def filter_class(self):
        f_type = self.request.get('type')
        print(self.request)
        filter_class_name = underscore_to_camel(f_type)
        filter_package = __import__('filter')
        return getattr(filter_package, filter_class_name)

    def post(self):
        filter = self.filter_class()()
        filter.from_request(self.request)
        self.filter_manager.create(filter)
        self.redirect('/')


class DbChangeRequestPage(ChangeRequestPage):
    def template_name(self):
        return 'add_db'

    def model(self):
        return {
            'filters': self.filter_manager.list()
        }

    def db_filter_opts(self):
        db_opts = {}
        for filter in self.filter_manager.list():
            db_opts.update(filter.db_params_from_request(self.request))
        return db_opts

    def post(self):
        db = Db()
        db.from_request(self.request)
        db.add_params(self.db_filter_opts())
        self.db_manager.create(db)
        self.redirect('/')

