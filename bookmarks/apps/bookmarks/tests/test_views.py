# -*- coding: utf-8 -*-
from urlparse import urlparse

from django.core.urlresolvers import reverse
from django.test import TestCase

from ...users.models import BookmarksUser
from ..models import Bookmark, Link
from ...tags.models import Tag


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BookmarksViewsTestCase(TestCase):
    def setUp(self):
        self.user = BookmarksUser.objects.create_user(
            email='foo@bar.bz',
            password='bar',
            first_name='foo',
            last_name='bar'
        )
        self.client.login(username=self.user.email,
                          password='bar')
        self.create_bookmark_url = reverse('bookmarks:save')

    def test_create_bookmark_view(self):
        self.assertEquals(self.create_bookmark_url, '/save/')
        response = self.client.post(self.create_bookmark_url,
                                    data={'url': 'http://www.nba.com',
                                          'title': 'Foo',
                                          'tags': 'foo,bar'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(urlparse(response['Location']).path, '/')
        self.assertEquals(Link.objects.count(), 1)
        self.assertEquals(Bookmark.objects.count(), 1)
        self.assertEquals(Tag.objects.count(), 2)
        bookmark = Bookmark.objects.get(link=Link.objects.get(url='http://www.nba.com/').pk)
        self.assertEquals(bookmark.favicon, 'http://www.google.com/s2/favicons?domain_url=http://www.nba.com/')

    def test_edit_bookmark_view(self):
        bookmark = Bookmark.objects.create(
            link=Link.objects.create(url='http://foo.bar'),
            user=self.user
        )
        response = self.client.post('{0}?url={1}'.format(
            self.create_bookmark_url, bookmark.link),
            data={'url': 'http://www.foo.bar',
                  'title': 'Foo',
                  'tags': 'foo,bar'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(urlparse(response['Location']).path, '/')
        # TODO: fix to edit bookmark
        self.assertEquals(Bookmark.objects.count(), 2)
        self.assertEquals(Tag.objects.count(), 2)


