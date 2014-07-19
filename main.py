# figure out templates

__author__ = 'adamsimon'

# TODO move forms code to separate template
# TODO Figure out how to serve straight html page
# TODO Create introductory page

import os
import urllib
from models import *
from functions import *

from google.appengine.api import users

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(
		os.path.join(os.path.dirname(__file__), 'templates')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class StartPage(webapp2.RequestHandler):

	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'logout'
			template_values = {'user': users.get_current_user().nickname()}
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'login'
			template_values = {}

		guestbooks = Guestbook.query()

		template_values.update({'guestbooks': guestbooks,
		                        'url': url,
		                        'url_linktext': url_linktext,
		})

		template = JINJA_ENVIRONMENT.get_template('start.html')
		self.response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):

	def get(self):
		guestbook_name = self.request.query_string
		guestbook = Guestbook.get_by_id(guestbook_name)

		greetings_query = Greeting.query(
			ancestor=guestbook.key).order(-Greeting.date)
		greetings = greetings_query.fetch(10)

		template_values = return_current_user()

		template_values.update({'greetings': greetings,
		                        'guestbook_name': urllib.quote_plus(guestbook_name),
		                       })

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

	def post(self):
		guestbook_name = self.request.get('guestbook_name',
		                                  default_value='default_guestbook')
		guestbook = Guestbook.get_or_insert(guestbook_name)

		greetings_query = Greeting.query(
			ancestor=guestbook.key).order(-Greeting.date)
		greetings = greetings_query.fetch(10)

		template_values = return_current_user()

		template_values.update({'greetings': greetings,
		                        'guestbook_name': urllib.quote_plus(guestbook_name),
		})

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))


class GuestbookPage(webapp2.RequestHandler):

	def post(self):
		# We set the same parent key on the 'Greeting' to ensure each Greeting
		# is in the same entity group. Queries across the single entity group
		# will be consistent. However, the write rate to a single entity group
		# should be limited to ~1/second.
		guestbook_name = self.request.get('guestbook_name')
		guestbook = Guestbook.get_by_id(guestbook_name)
		greeting = Greeting(parent=guestbook.key)

		if users.get_current_user():
			greeting.author = users.get_current_user()

		if self.request.get('content'):
			greeting.content = self.request.get('content')
			greeting.put()

		self.redirect('/main?' + guestbook_name)


app = webapp2.WSGIApplication([
	('/main', MainPage),
	('/sign', GuestbookPage),
	('/', StartPage)
], debug=True)

