import webapp2
import frontend

class BasePage(webapp2.RequestHandler):
    def get(self):
        template_values={}
        template = frontend.JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class MainPage(BasePage):
    pass
