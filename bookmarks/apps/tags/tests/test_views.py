# -*- coding: utf-8 -*-
import json
from urlparse import urlparse
from django.core.urlresolvers import reverse

from django.test import TestCase


from ..models import Tag
from ...users.models import BookmarksUser


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TagsViewTestCase(TestCase):
    def setUp(self):
        self.user = BookmarksUser.objects.create_user(
            email='foo@bar.bz',
            first_name='foo',
            last_name='bar',
            password='buz'
        )

        Tag.objects.create(name='foo')
        Tag.objects.create(name='bar')
        Tag.objects.create(name='buz')
        self.tag_autocomplete_url=reverse('tags:autocomplete')

    def test_autocomplete_url(self):
        self.assertEquals(self.tag_autocomplete_url, '/tags/autocomplete/')
        call_response = lambda t : self.client.get('{0}?term={1}'.format(
            self.tag_autocomplete_url, t))
        response = call_response('foo')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(urlparse(response['Location']).path, '/users/login')
        self.client.login(username=self.user.email,
                          password='buz')
        response = call_response('foo')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)


