import webapp2
from filter import FilterManager
import frontend


class BasePage(webapp2.RequestHandler):
    def get(self):
        template_values = self.model()
        template = frontend.JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def model(self):
        return {}


class MainPage(BasePage):
    filter_manager = FilterManager()


    def model(self):
        return {"filters": self.filter_manager.list()}