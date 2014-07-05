import logging
import os

import webapp2
import jinja2

from front.pages import MainPage, FilterChangeRequestPage
from filter import SelectFilter, IntRangeFilter, BooleanFilter
from util import filter_type


global JINJA_ENVIRONMENT
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/front/templates/"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
JINJA_ENVIRONMENT.filters['filter_type'] = filter_type


frontend = webapp2.WSGIApplication([
                                       ('/', MainPage),
                                       ('/filter', FilterChangeRequestPage),
                                   ], debug=True)
