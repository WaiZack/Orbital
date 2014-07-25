import urllib
import webapp2
import jinja2
import os
import datetime

from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/pages"))

class Authors(ndb.Model):
    next = ndb.IntegerProperty()

class Idea(ndb.Model):
    # Models an idea with name description requirements and author. Key is author
    number = ndb.IntegerProperty()
    author = ndb.StringProperty()
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    requirements = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    """ Handler for the front page."""
    def get(self):
        template = jinja_environment.get_template('index2.html')
        self.response.out.write(template.render())

class About(webapp2.RequestHandler):
    """ Handler for the about page."""
    def get(self):
        template = jinja_environment.get_template('about.html')
        self.response.out.write(template.render())

class LoggedMain(webapp2.RequestHandler):
    """ Handler for the post login page"""
    def get(self):

        idea_query = Idea.query(Idea.author == users.get_current_user().email())
        idea = idea_query.fetch()
        template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
                'ideas': idea
            }
        template = jinja_environment.get_template('logged.html')
        self.response.out.write(template.render(template_values))

class Old (webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('old.html')
        self.response.out.write(template.render())

class Add(webapp2.RequestHandler):
    def show(self):
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('add.html')
            self.response.out.write(template.render(template_values))

    def get(self):
        self.show()

    def post(self):
         = ndb.Key('Ideastore',users.get_current_user().email())
        idea = Idea(parent=parent)
        idea.number = author.number
        idea.author = users.get_current_user().email()
        idea.name = self.request.get("name")
        idea.description = self.request.get("description")
        idea.requirements = self.request.get("requirements")
        author.number +=1
        idea.put()
        self.show()

class Browse(webapp2.RequestHandler):

    def get(self):
        self.show()

    def show(self):
        idea_query = Idea.query().order(Idea.date)
        idea = idea_query.fetch()
        template_values = {
            'user_mail': users.get_current_user().email(),
            'logout': users.create_logout_url(self.request.host_url),
            'ideas': idea
        }
        template = jinja_environment.get_template('browse.html')
        self.response.out.write(template.render(template_values))


class GoogleOpenId(webapp2.RequestHandler):
    """ Handler for Google Login."""
    def post(self):
        openId = "https://www.google.com/accounts/o8/id"
        self.redirect(users.create_login_url('/logged/main', None, federated_identity=openId))

class NUSOpenId(webapp2.RequestHandler):
    """ Handler for NUS Login."""
    def post(self):
        openId = "https://openid.nus.edu.sg/"
        self.redirect(users.create_login_url('/logged/main', None, federated_identity=openId))

class YahooOpenId(webapp2.RequestHandler):
    """ Handler for Yahoo Login."""
    def post(self):
        openId = "yahoo.com"
        self.redirect(users.create_login_url('/logged/main', None, federated_identity=openId))

class HandleOpenId(webapp2.RequestHandler):
    """ Handler for pages that require login."""
    def get(self):
        self.redirect(self.request.host_url)

class Delete(webapp2.RequestHandler):
        def post(self):
            idea = ndb.Key('Ideastore', users.get_current_user().email())
            idea.delete()
            self.redirect('/logged/main')




app = webapp2.WSGIApplication([('/', MainPage),
                               ('/old',Old),
                               ('/GoogleOpenId', GoogleOpenId),
                               ('/NUSOpenId', NUSOpenId),
                               ('/YahooOpenId', YahooOpenId),
                               ('/_ah/login_required', HandleOpenId),
                               ('/logged/main', LoggedMain),
                               ('/logged/add', Add),
                               ('/logged/browse', Browse),
                               ('/about', About),
                               ('/delete',Delete),
                              ],
                              debug=True)
