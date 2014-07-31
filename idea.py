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
    idea_num = ndb.IntegerProperty()

class Idea(ndb.Model):
    # Models an idea with name description requirements and author. Key is author
    number = ndb.IntegerProperty()
    author = ndb.StringProperty()
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    requirements = ndb.TextProperty()
    tag = ndb.StringProperty()
    reply_num = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Reply(ndb.Model):
    idea_author = ndb.StringProperty()
    respond = ndb.IntegerProperty()
    idea_name = ndb.StringProperty()
    i_number = ndb.IntegerProperty()
    solution = ndb.TextProperty()
    image = ndb.StringProperty()
    author = ndb.StringProperty()
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
        reply_query = Reply.query(Reply.author == users.get_current_user().email())
        reply = reply_query.fetch()
        template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
                'ideas': idea,
                'replies': reply
            }
        template = jinja_environment.get_template('logged.html')
        self.response.out.write(template.render(template_values))

class Login (webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('login.html')
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
        parent = ndb.Key('Authors',users.get_current_user().email())
        author = parent.get()
        if author == None:
            author = Authors(id=users.get_current_user().email())
            author.idea_num = 1
            author.reply_num = 1

        idea = Idea(parent=parent, id=str(author.idea_num))
        idea.number = author.idea_num
        idea.author = users.get_current_user().email()
        idea.name = self.request.get("name")
        idea.description = self.request.get("description")
        idea.requirements = self.request.get("requirements")
        idea.tag = self.request.get("tags")
        idea.reply_num = 0
        author.idea_num +=1
        author.put()
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
            idea = ndb.Key('Authors', users.get_current_user().email(), 'Idea', self.request.get('number'))
            idea.delete()
            self.redirect('/logged/main')

class Edit1(webapp2.RequestHandler):
    def post(self):
            idea_key = ndb.Key('Authors', users.get_current_user().email(), 'Idea', self.request.get('number'))
            ideareal = idea_key.get()
            idea_query = Idea.query(Idea.author == users.get_current_user().email())
            idea_query2 = idea_query.filter(Idea.number == ideareal.number)
            idea = idea_query2.fetch()
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
                'ideas': idea
            }
            template = jinja_environment.get_template('edit.html')
            self.response.out.write(template.render(template_values))

class Edit2(webapp2.RequestHandler):
    def post(self):
        idea_key = ndb.Key('Authors', users.get_current_user().email(), 'Idea', self.request.get('number'))
        idea = idea_key.get()
        idea.name = self.request.get("name")
        idea.description = self.request.get("description")
        idea.requirements = self.request.get("requirements")
        idea.tag = self.request.get("tags")
        idea.put()
        self.redirect('/logged/main')

class Search(webapp2.RequestHandler):
    def get(self):
        self.show()

    def show(self):
        template_values = {
            'user_mail': users.get_current_user().email(),
            'logout': users.create_logout_url(self.request.host_url),
        }
        template = jinja_environment.get_template('search.html')
        self.response.out.write(template.render(template_values))

class Result(webapp2.RequestHandler):
    def post(self):
        idea_query = Idea.query(Idea.tag == self.request.get('tags'))
        idea = idea_query.fetch()
        template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
                'ideas': idea,
                }
        if idea_query.count(1):
            template = jinja_environment.get_template('result.html')
        else:
            template = jinja_environment.get_template('no.html')
        self.response.out.write(template.render(template_values))

class Display(webapp2.RequestHandler):
    def post(self):
        idea_key = ndb.Key('Authors', self.request.get('submitter'), 'Idea', self.request.get('index'))
        ideareal = idea_key.get()
        if ideareal is not None:

            idea_query = Idea.query(Idea.author == ideareal.author)
            idea_query2 = idea_query.filter(Idea.number == ideareal.number)
            idea = idea_query2.fetch()

        #Have to make it idea specific
            reply_query = Reply.query().order(Reply.date)
            reply_query2 = reply_query.filter(Reply.respond == ideareal.number)
            reply_info = reply_query2.fetch()
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
                'ideas': idea,
                'replies': reply_info
            }
            template = jinja_environment.get_template('individual.html')
            self.response.out.write(template.render(template_values))
        else:
            idea_query = Idea.query(Idea.author == users.get_current_user().email())
            idea = idea_query.fetch()
            reply_query = Reply.query(Reply.author == users.get_current_user().email())
            reply = reply_query.fetch()
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
                'ideas': idea,
                'replies': reply
            }
            template = jinja_environment.get_template('deleted.html')
            self.response.out.write(template.render(template_values))

class AddReply(webapp2.RequestHandler):

    def post(self):
        parent = ndb.Key('Authors', self.request.get('submitter'), 'Idea', self.request.get('index'))
        idea = parent.get()

        reply = Reply(parent=parent, id=str(idea.reply_num))
        reply.idea_author = idea.author
        reply.idea_name = idea.name
        reply.respond = idea.number
        reply.i_number = idea.reply_num
        reply.solution = self.request.get('solution_description')
        reply.author = users.get_current_user().email()
        reply.image = self.request.get('photo')
        idea.reply_num += 1
        idea.put()
        reply.put()
        self.redirect('/logged/main')

class DeleteReply(webapp2.RequestHandler):
        def post(self):
            reply = ndb.Key('Authors', self.request.get('parenta'), 'Idea', self.request.get('number'),'Reply', self.request.get('index'))
            reply.delete()
            self.redirect('/logged/main')

class EditReply1(webapp2.RequestHandler):
    def post(self):
            reply_key = ndb.Key('Authors', self.request.get('parenta'), 'Idea', self.request.get('number'),'Reply', self.request.get('index'))
            replyreal = reply_key.get()
            reply_query = Reply.query(Reply.author == users.get_current_user().email())
            reply_query2 = reply_query.filter(Reply.i_number == replyreal.i_number)
            reply = reply_query2.fetch()
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
                'replies': reply
            }
            template = jinja_environment.get_template('reply.html')
            self.response.out.write(template.render(template_values))

class EditReply2(webapp2.RequestHandler):
    def post(self):
        reply_key = ndb.Key('Authors', self.request.get('parenta'), 'Idea', self.request.get('number'),'Reply', self.request.get('index'))
        reply = reply_key.get()
        reply.solution = self.request.get("description")
        reply.image = self.request.get("photo")
        reply.put()
        self.redirect('/logged/main')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/login', Login),
                               ('/GoogleOpenId', GoogleOpenId),
                               ('/NUSOpenId', NUSOpenId),
                               ('/YahooOpenId', YahooOpenId),
                               ('/_ah/login_required', HandleOpenId),
                               ('/logged/main', LoggedMain),
                               ('/logged/add', Add),
                               ('/logged/browse', Browse),
                               ('/logged/search', Search),
                               ('/logged/search2', Result),
                               ('/about', About),
                               ('/reply', Display),
                               ('/add_reply', AddReply),
                               ('/delete', Delete),
                               ('/deletereply',DeleteReply),
                               ('/editreply1', EditReply1),
                               ('/editreply2', EditReply2),
                               ('/edit1', Edit1),
                               ('/edit2', Edit2),
                               ],
                              debug=True)
