# import modules and methods
import logging
import random
import endpoints
from protorpc import remote, messages

from models import User, Game
from models import StringMessage, GameForm
from helpers import produce_hint

# resource containers
USER_REQUEST = endpoints.ResourceContainer(
    username = messages.StringField(1, required=True),
    email = messages.StringField(2))

NEW_GAME = endpoints.ResourceContainer(
    username = messages.StringField(1, required=True),)

# define endpoints
@endpoints.api(name='soccerhangman', version='v1')
class soccerhangman(remote.Service):
    """Game API where user plays hangman for soccer players"""

    @endpoints.method(USER_REQUEST, StringMessage, path='user',
                      name='create_user', http_method='POST')
    def create_user(self, request):
        """register new user"""
        # check that username doesn't already exist
        if User.query(User.username == request.username):
            endpoints.ConflictException('Username already exists')
        # store a new user profile entity
        user = User(username = request.username, email = request.email)
        user.put()
        # alert the user of success
        return StringMessage(message = 'We have successfully registered %s!'
                             % request.username)

    @endpoints.method(NEW_GAME, GameForm, path='game',
                      name='new_game', http_method='POST')
    def new_game(self, request):
        """create new game"""
        # check if username exists
        user = User.query(User.username == request.username).get()
        
        if not user:
            raise endpoints.NotFoundException('No such user is registered!')

        # randomly generate answer and convert to nested list for storage
        players = ['ronaldo', 'messi', 'bale', 'rooney', 'suarez', 'fabregas',
                   'cech', 'sanchez', 'aguero', 'hazard', 'benzema', 'neymar']
        
        answer = list(random.choice(players))

        answer = [[x, False] for x in answer]

        # store a game entity where user starts with 6 moves and 0 guesses
        game = Game.new_game(user.key, answer, 6, 0)

        # produce message
        message = 'A new game has been created for you %s' % request.username

        # produce hint
        hint = produce_hint(answer)

        # make form and return to user
        return game.to_form(message, hint)
    

# launch endpoints API
api = endpoints.api_server([soccerhangman])
