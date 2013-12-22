# -*- coding: utf-8 -*-
import json
from urlparse import urlparse
from django.core.urlresolvers import reverse

from django.test import TestCase


from ..models import Tag
from ...bookmarks.models import Bookmark, Link
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
        self.tag_foo = Tag.objects.create(name='foo')
        Tag.objects.create(name='bar')
        Tag.objects.create(name='buz')
        self.tag_autocomplete_url = reverse('tags:autocomplete')
        self.tag_url = lambda t: reverse('tags:page', kwargs={'tag_name': t})

    def test_autocomplete_url(self):
        self.assertEquals(self.tag_autocomplete_url, '/tags/autocomplete/')
        call_response = lambda t: self.client.get('{0}?term={1}'.format(
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

    def test_tag_page_view(self):
        self.client.login(username=self.user.email,
                          password='buz')
        bookmark = Bookmark.objects.create(
            link=Link.objects.create(url='http://www.foo.bar/'),
            title='Foo', user=self.user)
        bookmark.tag_set.add(self.tag_foo)
        bookmark.save()
        tag_name = 'foo'
        self.assertEquals(self.tag_url(tag_name), '/tags/{0}/'.format(tag_name))
        response = self.client.get(self.tag_url(tag_name))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['tag_name'], 'foo')
        self.assertTemplateUsed(response, 'tags/tag_list.html')
        self.assertEquals(len(response.context['bookmark_list']), 1)



