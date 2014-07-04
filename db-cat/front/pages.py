import webapp2
from filter import FilterManager, Filter
import frontend
from util import camel_to_underscore, underscore_to_camel


class BasePage(webapp2.RequestHandler):

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
    filter_manager = FilterManager()


    def model(self):
        return {"filters": self.filter_manager.list()}


class ChangeRequestPage(BasePage):
    pass


class FilterChangeRequestPage(ChangeRequestPage):
    def template_name(self):
        return 'add_filter'

    def model(self):
        return {
            "filter_types":self.filter_types()
        }

    def filter_types(self):
        return map(self.class_to_name,Filter.__subclasses__())

    def class_to_name(self,clazzz):
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
        filter.put()
        self.redirect('/')
