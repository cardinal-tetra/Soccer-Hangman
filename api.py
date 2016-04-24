# import modules and methods
import logging
import endpoints
from protorpc import remote, messages

from models import User, StringMessage

# resource containers
USER_REQUEST = endpoints.ResourceContainer(
    username = messages.StringField(1, required=True),
    email = messages.StringField(2))

# define endpoints
@endpoints.api(name='soccerhangman', version='v1')
class soccerhangman(remote.Service):
    """Game API where user plays hangman for soccer players"""

    @endpoints.method(USER_REQUEST, StringMessage, path='user',
                      name='create_user', http_method='POST')
    def create_user(self, request):
        """creating new users method"""
        # check that username doesn't already exist
        if User.query(User.username == request.username):
            endpoints.ConflictException('Username already exists')
        # store a new user profile entity
        user = User(username = request.username, email = request.email)
        user.put()
        # alert the user of success
        return StringMessage(message = 'We have successfully registered %s!'
                             % request.username)
 

# launch endpoints API
api = endpoints.api_server([soccerhangman])
