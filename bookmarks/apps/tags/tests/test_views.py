# -*- coding: utf-8 -*-
import json
import os
from urlparse import urlparse
from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test.utils import override_settings

from ..models import Tag
from ...bookmarks.models import Bookmark, Link
from ...users.models import BookmarksUser


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


@override_settings(SECRET_KEY='FooBar')
class TagsViewTestCase(TestCase):
    fixtures = [os.path.join(os.path.dirname(__file__),
                             '../../bookmarks/tests/users.json'),
                os.path.join(os.path.dirname(__file__), 'tag_cloud_data.json')]

    def setUp(self):
        self.tag_autocomplete_url = reverse('tags:autocomplete')
        self.tag_url = lambda t: reverse('tags:page', kwargs={'tag_name': t})
        self.tag_cloud_url = reverse('tags:cloud')

    def test_autocomplete_url(self):
        self.assertEquals(self.tag_autocomplete_url, '/tags/autocomplete/')
        call_response = lambda t: self.client.get('{0}?term={1}'.format(
            self.tag_autocomplete_url, t))
        response = call_response('foo')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(urlparse(response['Location']).path, '/users/login')
        self.client.login(username='foo@bar.bz',
                          password='buz')
        response = call_response('foo')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)

    def tag_name_bookmarks(self, tag_name, bookmarks):
        self.assertEquals(self.tag_url(tag_name), '/tags/{0}/'.format(tag_name))
        response = self.client.get(self.tag_url(tag_name))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['tag_name'], tag_name)
        self.assertTemplateUsed(response, 'tags/tag_list.html')
        self.assertEquals(len(response.context['bookmark_list']), bookmarks)

    def test_tag_page_view(self):
        self.client.login(username='foo@bar.bz',
                          password='buz')
        # In fixtures we have 10 bookmarks for tag foo
        self.tag_name_bookmarks('foo', 10)
        # In fixtures we have 5 bookmarks for tag bar
        self.tag_name_bookmarks('bar', 5)
        # In fixtures we have 2 bookmarks for tag buz
        self.tag_name_bookmarks('buz', 2)

    def test_tag_cloud_page(self):
        self.assertEquals(self.tag_cloud_url, '/tags/',
                          msg='URL should be /tags/')
        self.client.login(username='foo@bar.bz',
                          password='buz')
        response = self.client.get(self.tag_cloud_url)
        self.assertEquals(200, response.status_code)
        self.assertTemplateUsed(response, 'tags/tag_cloud.html')
        tags = response.context['tag_list']
        self.assertEquals(len(tags), 3)
        # Test weights
        for tag in tags:
            if tag.name == 'foo':
                self.assertEquals(tag.weight, 22)
            elif tag.name == 'bar':
                self.assertEquals(tag.weight, 8)
            elif tag.name == 'buz':
                self.assertEquals(tag.weight, 8)
