# -*- coding: utf-8 -*-
from django.test import TestCase

from ..forms import BookmarksAuthForm, BookmarksPasswordResetForm

from ..models import BookmarksUser

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class UsersFormTestCase(TestCase):
    def setUp(self):
        BookmarksUser.objects.create_user(
            email='foo@bar.bz',
            last_name='foo',
            first_name='bar',
            password='buz'
        )

    def test_auth_form(self):
        form = BookmarksAuthForm(data={'username': 'foo@bar.bz',
                                       'password': 'buz'})
        self.assertTrue(form.is_valid())

    def test_reset_form(self):
        form = BookmarksPasswordResetForm()
        self.assertFalse(form.is_valid())
        form = BookmarksPasswordResetForm({'password1': 'boo',
                                           'password2': 'zoo'})
        self.assertFalse(form.is_valid())
        self.assertEquals(u'Passwords do not match. Please check.',
                          form.errors['__all__'][0])

