import webapp2
import jinja2
import os
from front.pages import MainPage

global JINJA_ENVIRONMENT
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


frontend = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
