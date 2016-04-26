# a whole load of helper functions
import logging
from google.appengine.ext import ndb
import endpoints

def get_by_urlsafe(urlsafe, model):
    """returns entity corresponding to urlsafe key, code based on that in 'make a number'"""
    try:
        key = ndb.Key(urlsafe=urlsafe)
    except TypeError:
        raise endpoints.BadRequestException('Invalid Key')
    except Exception, e:
        if e.__class__.__name__ == 'ProtocolBufferDecodeError':
            raise endpoints.BadRequestException('Invalid Key')
        else:
            raise

    entity = key.get()
    if not entity:
        return None
    if not isinstance(entity, model):
        raise ValueError('Incorrect Kind')
    return entity

def produce_hint(answer):
        """make string partially revealing answer where user guessed correctly"""
        hint = []

        for letter in answer:
            if letter[1] == True:
                hint.append(letter[0])
            else:
                hint.append('_ ')

        return ''.join(hint)

def reveal_answer(answer):
    """show the entire answer"""
    entire_answer = []

    for letter in answer:
        entire_answer.append(letter[0])

    return ''.join(entire_answer)
    
def moves_gone(moves_left):
    """This checks if there are still moves left in the game"""
    if moves_left < 1:
        return True

def update(game):
    game.moves_left -= 1
    game.guesses_made += 1
    return game

def game_won(game):
    game.game_status = 'won'
    message = 'You have won the game!'
    hint = reveal_answer(game.answer)
    game.put()
    return game.to_form(message, hint, 'won')

def game_over(game, msg=''):
    game.game_status = 'lost'
    message = msg + 'You have lost the game!'
    hint = reveal_answer(game.answer)
    game.put()
    return game.to_form(message, hint, 'lost')

def wrong_guess(game):
    message = 'Wrong guess! Try again!'
    hint = produce_hint(game.answer)
    game.put()
    return game.to_form(message, hint, 'ongoing')

def correct_guess(game):
    message = 'Correct! Keep going!'
    hint = produce_hint(game.answer)
    game.put()
    return game.to_form(message, hint, 'ongoing')
    
