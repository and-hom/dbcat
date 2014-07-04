import logging
import os

import webapp2
import jinja2

from front.pages import MainPage
from filter import SelectFilter, IntRangeFilter, BooleanFilter


global JINJA_ENVIRONMENT
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/front/templates/"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def fake_filters():
    logging.debug('Creating fake filters')
    sf1 = SelectFilter()
    sf1.name = 'Selector1'
    sf1.description = 'Selector1'
    sf1.options = ['v1', 'v2']
    sf1.put()

    rf1 = IntRangeFilter()
    rf1.name = 'Some val'
    rf1.min = 0
    rf1.max = 10
    rf1.put()

    bf1 = BooleanFilter()
    bf1.name = 'Flag'
    bf1.put()


# fake_filters()

frontend = webapp2.WSGIApplication([
                                       ('/', MainPage),
                                   ], debug=True)
