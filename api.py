# import modules and methods
import logging
import random
import endpoints
from protorpc import remote, messages

from models import User, Game, Score
from models import StringMessage, GameForm, ScoreForm
from helpers import produce_hint, moves_gone, reveal_answer, get_by_urlsafe
from helpers import update, game_won, game_over, wrong_guess, correct_guess

# resource containers
USER_REQUEST = endpoints.ResourceContainer(
    username = messages.StringField(1, required=True),
    email = messages.StringField(2))

NEW_GAME = endpoints.ResourceContainer(
    username = messages.StringField(1, required=True),)

GET_GAME = endpoints.ResourceContainer(
    urlsafe_game_key = messages.StringField(1, required=True),)

MOVE = endpoints.ResourceContainer(
    urlsafe_game_key = messages.StringField(1, required=True),
    guess = messages.StringField(2, required=True))


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

        # randomly generate answer and convert to nested list 
        players = ['ronaldo', 'messi', 'bale', 'rooney', 'suarez', 'fabregas',
                   'cech', 'sanchez', 'aguero', 'hazard', 'benzema', 'neymar']
        answer = list(random.choice(players))
        answer = [[x, False] for x in answer] # boolean for whether letter guessed

        # store a game entity where user starts with 6 moves and 0 guesses
        game = Game.new_game(user.key, answer, 6, 0, 'ongoing')

        # produce message
        message = 'A new game has been created for you %s' % request.username

        # produce hint
        hint = produce_hint(answer)

        # make form and return to user
        return game.to_form(message, hint, 'ongoing')

    @endpoints.method(GET_GAME, GameForm, path='game/{urlsafe_game_key}',
                      name='get_game', http_method='GET')
    def get_game(self, request):
        """retrieves game information"""
        # retrieve game entity by urlsafe key
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if not game:
            raise endpoints.NotFoundException('Game not found')

        # make message and hint for the user
        message = 'Here is the game information!'
        hint = produce_hint(game.answer)

        # make form and return to user
        return game.to_form(message, hint, game.game_status)

    @endpoints.method(MOVE, GameForm, path='game/{urlsafe_game_key}',
                      name='make_move', http_method='PUT')
    def make_move(self, request):
        """guess the player"""
        # retrieve game entity by urlsafe key
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if not game:
            raise endpoints.NotFoundException('No such game')

        # check if game is already over
        if game.game_status != 'ongoing':
            raise endpoints.BadRequestException('Game is already over')

        # if the user is guessing an entire word
        if len(request.guess) > 1 and request.guess.isalpha():
            # update moves left and guesses made
            game = update(game)
            # check if the user has guessed correctly
            if request.guess == reveal_answer(game.answer):
                return game_won(game)
            else:
                # if the user guessed wrong, check if they have moves left
                if moves_gone(game.moves_left):
                    return game_over(game)
                else:
                    return wrong_guess(game)
        # if user's word guess is malformed
        elif len(request.guess) > 1 and not request.guess.isalpha():
            raise endpoints.BadRequestException('Word has to be all letters')

        # if the user is guessing letter by letter
        if len(request.guess) == 1 and not request.guess.isalpha():
            raise endpoints.BadRequestException('Provide just one single letter!')

        guess = request.guess.lower()           

        # update moves left and guesses made
        game = update(game)

        # iterate through entire answer to see if user guessed correctly
        correct = False
        for letter in game.answer:
            if letter[0] == guess and letter[1] == False:
                letter[1] = True
                correct = True

        # if the user has guessed correctly
        if correct == True:
            # differentiate between cases where they won the game or not
            for letter in game.answer:
                if letter[1] == False: # they have not won the game
                    # check if moves exhausted
                    if moves_gone(game.moves_left) == True:
                        return game_over(game, 'Correct, however ...')
                    else:
                        return correct_guess(game)
            # user has won the game
            return game_won(game)
        # user has not guessed correctly
        else:
            # check if they have run out of moves
            if moves_gone(game.moves_left) == True:
                return game_over(game, 'Wrong! ')
            else:
                return wrong_guess(game)


                                      
# launch endpoints API
api = endpoints.api_server([soccerhangman])
