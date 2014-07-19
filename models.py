__author__ = 'adamsimon'

from google.appengine.ext import ndb

class Greeting(ndb.Model):
	"""Models an individual guestbook entry with author, content, and date."""
	author = ndb.UserProperty()
	content = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)


class Guestbook(ndb.Model):
	date = ndb.DateTimeProperty(auto_now_add=True)
