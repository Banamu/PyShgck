""" Utilities to work with Twython (https://pypi.python.org/pypi/twython). """

import logging

try:
    from twython import Twython
    from twython.exceptions import TwythonError
except ImportError:
    print("Can't import Twython.")

from pyshgck.log import get_logger


class CommandLineAuthorizer(object):
    """ Provide a command-line interface to authorize an account to use
    a desktop Twitter app."""

    def __init__(self, app_key, app_secret, log=None,
                 log_level=logging.WARNING):
        self.app_tokens = app_key, app_secret
        self.user_tokens = ("", "")
        self.log = log or get_logger("pyshgck.libs.twython", level=log_level)

    def get_twython_api(self):
        try:
            self.authenticate()
            app_key, app_secret = self.app_tokens
            token, token_secret = self.user_tokens
            return Twython(app_key, app_secret, token, token_secret)
        except TwythonError as exc:
            self.log.error("Error while connecting to Twitter: " + str(exc))
            return None

    def authenticate(self):
        """ Performs the authentication and authorization of the app through
        a command-line interface. Return the OAuth token and secret on success,
        or None on error. """
        app_key, app_secret = self.app_tokens
        first_step_api = Twython(app_key, app_secret)
        try:
            auth_tokens = first_step_api.get_authentication_tokens()
        except TwythonError as exc:
            self.log.error("Couldn't get authentication tokens: " + str(exc))
            return None
        self.log.debug("authentication tokens: " + str(auth_tokens))

        url = auth_tokens["auth_url"]
        print("Please visit '{}' to get your PIN.".format(url))
        oauth_verifier = input("Enter PIN: ")

        token = auth_tokens["oauth_token"]
        token_secret = auth_tokens["oauth_token_secret"]
        second_step_api = Twython(app_key, app_secret, token, token_secret)
        try:
            new_tokens = second_step_api.get_authorized_tokens(oauth_verifier)
        except TwythonError as exc:
            self.log.error("Couldn't get authorization tokens: " + str(exc))
            return None
        self.log.debug("authorized tokens: " + str(new_tokens))

        return new_tokens["oauth_token"], new_tokens["oauth_token_secret"]
