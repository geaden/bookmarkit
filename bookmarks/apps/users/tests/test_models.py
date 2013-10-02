# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import BookmarksUser


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class UsersModelsTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_super_user(self):
        super_user = BookmarksUser.objects.create_superuser(
            email='foo@bar.bz',
            first_name='foo',
            last_name='bar',
            password='buz'
        )
        self.assertEquals(BookmarksUser.objects.all().count(),
                          1, msg='Number of users should be 1')
        self.assertTrue(super_user.is_superuser,
                        msg='User should be super user')

    def test_create_regular_user(self):
        user = BookmarksUser.objects.create_user(
            email='foo@bar.bz',
            first_name='foo',
            last_name='bar',
            password='baz'
        )
        self.assertEquals(BookmarksUser.objects.all().count(),
                          1, msg='Number of users should be 1')
        self.assertFalse(user.is_superuser,
                         msg='User shouldn\'t be super user')

