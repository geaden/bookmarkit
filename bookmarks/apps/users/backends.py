# -*- coding: utf-8 -*-

from .models import BookmarksUser

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class GoogleOAuthBackend(object):
    supports_inactive_user = False

    def authenticate(self, **kwargs):
        """
        Authenticates according to authentication method.
        Whether `password` and `username` provided, or
        `google_user`

        :params kwargs: dictionary with `username` and `password` or `google_user`
            information
        :returns: user
        """
        authenticated = False
        if 'password' and 'username' in kwargs:
            try:
                user = BookmarksUser.objects.get_by_natural_key(
                    kwargs.get('username'))
                authenticated = user.check_password(kwargs.get('password'))
            except BookmarksUser.DoesNotExist:
                pass
        elif 'google_user' in kwargs:
            google_user = kwargs.get('google_user')
            email = google_user['email']
            try:
                user = BookmarksUser.objects.get_by_natural_key(email)
                authenticated = True
            except BookmarksUser.DoesNotExist:
                email = google_user['email']
                try:
                    user = BookmarksUser.objects.get_by_natural_key(email)
                    authenticated = True
                except BookmarksUser.DoesNotExist:
                    pass
        if authenticated:
            return user
        return None

    def get_user(self, user_id):
        try:
            return BookmarksUser.objects.get(pk=user_id)
        except BookmarksUser.DoesNotExist:
            return None