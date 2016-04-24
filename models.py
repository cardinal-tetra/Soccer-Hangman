# import modules and methods
from google.appengine.ext import ndb
from protorpc import messages

# define entity classes
class User(ndb.Model):
    """for storing information about users"""
    username = ndb.StringProperty()
    email = ndb.StringProperty()

# define message classes
class StringMessage(messages.Message):
    """outbound string messages"""
    message = messages.StringField(1, required=True)
    
