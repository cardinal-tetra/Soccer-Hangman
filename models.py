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
    game_status = ndb.StringProperty()

    @classmethod
    def new_game(cls, username, answer, moves_left, guesses_made, game_status):
        """stores a new game entity"""
        game = Game(username = username, answer = answer,
                    moves_left = moves_left, guesses_made = guesses_made,
                    game_status = game_status)
        game.put()
        return game

    def to_form(self, message, hint, game_status):
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.message = message
        form.moves_left = self.moves_left
        form.hint = hint
        form.game_status = game_status
        return form

class Score(ndb.Model):
    """stores score records"""
    user = ndb.KeyProperty(required = True, kind = 'User')
    date = ndb.DateProperty()
    won = ndb.BooleanProperty()
    guesses = ndb.IntegerProperty()

    def to_form(self):
        form = ScoreForm()
        form.user_name = self.user.get().username
        form.date = str(self.date)
        form.won = self.won
        form.guesses = self.guesses
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
    game_status = messages.StringField(5, required=True)

class GameForms(messages.Message):
    """outbound game information for multiple games"""
    items = messages.MessageField(GameForm, 1, repeated=True)
    
class ScoreForm(messages.Message):
    """outbound score information"""
    user_name = messages.StringField(1)
    date = messages.StringField(2)
    won = messages.BooleanField(3)
    guesses = messages.IntegerField(4)

class ScoreForms(messages.Message):
    """outbound score information for multiple games"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)
