"""Contains handlers that are called by cronjobs"""

import logging
import webapp2
from google.appengine.api import mail, app_identity
from api import soccerhangman
from models import User, Game


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each user with incomplete games and an email account.
        Called every three hours using a cron job"""
        app_id = app_identity.get_application_id()

        # get a list of user keys
        keys = []
        games = Game.query(Game.game_status == "ongoing").fetch()
        for game in games:
            keys.append(game.username)

        # remove duplicate values from the list
        keys = set(keys)
        keys = list(keys)

        # use list to obtain user entities
        users = []
        for key in keys:
            user = key.get()
            users.append(user)

        # send out emails
        for user in users:
            subject = "This is a reminder!"
            body = "Hello {}, you have a game to complete!".format(user.username)
            # the arguments to send_mail are: from, to, subject, body
            mail.send_mail(
                "noreply@{}.appspotmail.com".format(app_id), user.email, subject, body
            )


app = webapp2.WSGIApplication([("/crons/send_reminder", SendReminderEmail)], debug=True)

