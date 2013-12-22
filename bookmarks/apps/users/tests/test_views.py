# -*- coding: utf-8 -*-
import os
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import BookmarksUser
from ..forms import BookmarksAuthForm

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class UsersViewsTestCase(TestCase):
    def setUp(self):
        self.user = BookmarksUser.objects.create_user(
            email='foo@bar.bz',
            last_name='foo',
            first_name='bar',
            password='buz'
        )
        self.login_url = reverse('users:login')
        self.register_url = reverse('users:register')
        self.reset_url = reverse('users:reset')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEquals(200, response.status_code,
                          msg='Status code should be 200')
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertTrue(isinstance(response.context['form'],
                                   BookmarksAuthForm))
        response = self.client.post(self.login_url,
            {'username': 'foo@bar.bz', 'password': 'buz'})
        self.assertRedirects(response, reverse('bookmarks:main'))

    def test_register_view(self):
        os.environ['RECAPTCHA_TESTING'] = 'True'

        response = self.client.get(self.register_url)
        self.assertEqual(
            response.status_code,
            200
        )
        response = self.client.post(
            self.register_url,
            {
                'last_name': 'foo',
                'first_name': 'bar',
                'username': 'boo@bar.bz',
                'password1': 'baz',
                'password2': 'baz',
                'recaptcha_response_field': 'PASSED'
             }
        )
        self.assertRedirects(response, reverse('users:register-success'))
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(2, BookmarksUser.objects.count())
        user = BookmarksUser.objects.get(email='boo@bar.bz')
        self.assertFalse(user.is_active)
        self.assertEquals(response.context['activation_key'],
                          user.activation_key)

        registration_confirm_url = reverse('users:registration-confirm',
                                           args=[response.context['activation_key']])
        response = self.client.get(registration_confirm_url)
        self.assertEquals(200, response.status_code)
        user = BookmarksUser.objects.get(email='boo@bar.bz')
        self.assertTrue(user.is_active)

    def test_reset_password(self):
        data = {'password1': 'bar', 'password2': 'bar'}
        response = self.client.post(self.reset_url,
                                    data)
        # TODO: test password forgot
        # You can't reset your password if you're not logged in
        self.assertEquals(response.status_code, 302)
        self.client.login(username='foo@bar.bz', password='buz')
        response = self.client.post(self.reset_url,
            data)
        self.assertEquals(response.status_code, 302)
        self.client.logout()
        # Password changed successfully
        self.client.login(username='foo@bar.bz', password='bar')
        self.assertTrue(self.user.is_authenticated)



