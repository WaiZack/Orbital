import urllib
import webapp2
import jinja2
import os
import datetime

from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/pages"))


class MainPage(webapp2.RequestHandler):
    """ Handler for the front page."""

    def get(self):
        template = jinja_environment.get_template('index2.html')
        self.response.out.write(template.render())

class About(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('about.html')
        self.response.out.write(template.render())

class GoogleOpenId(webapp2.RequestHandler):
    def post(self):
        openId = "https://www.google.com/accounts/o8/id"
        self.redirect(users.create_login_url('/', None, federated_identity=openId))

class NUSOpenId(webapp2.RequestHandler):
    def post(self):
        openId = "https://openid.nus.edu.sg/"
        self.redirect(users.create_login_url('/', None, federated_identity=openId))

class YahooOpenId(webapp2.RequestHandler):
    def post(self):
        openId = "yahoo.com"
        self.redirect(users.create_login_url('/', None, federated_identity=openId))

class HandleOpenId(webapp2.RequestHandler):
    def get(self):
        self.redirect(self.request.host_url)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/GoogleOpenId', GoogleOpenId),
                               ('/NUSOpenId', NUSOpenId),
                               ('/YahooOpenId', YahooOpenId),
                               ('/_ah/login_required', HandleOpenId),
                               ('/about',About),
                              ],
                              debug=True)
