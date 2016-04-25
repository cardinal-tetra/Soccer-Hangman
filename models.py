# import modules and methods
from google.appengine.ext import ndb
from protorpc import messages

# define entity classes
class User(ndb.Model):
    """stores user records"""
    username = ndb.StringProperty()
    email = ndb.StringProperty()

class Game(ndb.Model):
    """stores game information and functions for gameflow"""
    username = ndb.KeyProperty(required = True, kind = 'User')
    answer = ndb.JsonProperty()
    moves_left = ndb.IntegerProperty()
    guesses_made = ndb.IntegerProperty()

    @classmethod
    def new_game(cls, username, answer, moves_left, guesses_made):
        """stores a new game entity"""
        game = Game(username = username, answer = answer,
                    moves_left = moves_left, guesses_made = guesses_made)
        game.put()
        return game

    def to_form(self, message, hint):
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.message = message
        form.moves_left = self.moves_left
        form.hint = hint
        return form


# define message classes
class StringMessage(messages.Message):
    """outbound string messages"""
    message = messages.StringField(1, required=True)

class GameForm(messages.Message):
    """outbound game information"""
    urlsafe_key = messages.StringField(1, required=True)
    message = messages.StringField(2, required=True)
    moves_left = messages.IntegerField(3, required=True)
    hint = messages.StringField(4, required=True)
    
    
