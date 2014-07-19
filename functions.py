__author__ = 'adamsimon'

from google.appengine.api import users
from google.appengine.ext import ndb


def guestbook2_key(guestbook_name='default_guestbook'):
	"""Constructs a Datastore key for a Guestbook entity with guestbook_name."""
	return ndb.Key("Guestbook", guestbook_name)


def return_current_user():
	if (users.get_current_user()):
		return {'user': users.get_current_user().nickname()}
	else:
		return {}