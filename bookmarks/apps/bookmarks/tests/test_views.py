# -*- coding: utf-8 -*-
import json
import os
from urlparse import urlparse

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.core.management import call_command

from ...users.models import BookmarksUser
from ..models import Bookmark, Link, SharedBookmark
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
        self.list_bookmark_url = reverse('bookmarks:main')

    def test_list_bookmark_view(self):
        fixture_file = os.path.join(os.path.dirname(__file__), 'bookmarks.json')
        items = 7
        call_command("loaddata", "{0}".format(fixture_file),
                     verbosity=0)
        self.assertEquals(Bookmark.objects.count(), items,
                          msg='Fixture should be'
                          ' successfully loadded.')
        self.assertEquals(self.list_bookmark_url, '/')
        response = self.client.get(self.list_bookmark_url)
        self.assertEquals(len(response.context['bookmark_list']), items)
        self.assertEquals(response.context['bookmark_list'][0].id, items,
                          msg='The first item should'
                          ' be last added one.')
        self.assertEquals(response.context['bookmark_list'][6].id, 1)

    def test_save_bookmark_view(self):
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

    def test_edit_bookmark_ajax_view(self):
        bookmark = Bookmark.objects.create(
            link=Link.objects.create(url='http://foo.bar/'),
            title='Foo',
            user=self.user
        )
        before = Bookmark.objects.count();
        response = self.client.post('{0}?ajax&url={1}'.format(
            self.create_bookmark_url, bookmark.link.url),
            data={'url': bookmark.link.url,
                  'title': 'Bar',
                  'tags': 'foo,bar'})
        self.assertEquals(200, response.status_code)
        data = json.loads(response.content)
        self.assertEquals(data['title'], 'Bar')
        self.assertEquals(data['url'], bookmark.link.url)
        self.assertEquals(data['tags'], [u'foo', u'bar'])
        self.assertEquals(before, Bookmark.objects.count())
        self.assertEquals(data['created'], False)
        self.assertEquals(data['pk'], bookmark.pk)
        self.assertFalse(data['shared'])

        # Not valid data provided
        response = self.client.post('{0}?ajax&url={1}'.format(
            self.create_bookmark_url, bookmark.link.url),
            data={'url': bookmark.link.url,
                  'title': 'Bar'})
        self.assertEquals(400, response.status_code)
        data = json.loads(response.content)
        self.assertEquals(data['tags'], [u'This field is required.'])

    def test_bookmarks_search(self):
        bookmark_foo = Bookmark.objects.create(
            link=Link.objects.create(
                url='http://www.foo.bz'
            ),
            title='Foo',
            user=self.user
        )
        bookmark_boo = Bookmark.objects.create(
            link=Link.objects.create(
                url='http://www.boo.bz'
            ),
            title='Boo',
            user=self.user
        )
        bookmark_zoo = Bookmark.objects.create(
            link=Link.objects.create(
                url='http://www.zoo.bz'
            ),
            title='Zoo',
            user=self.user
        )
        tag_foo = Tag.objects.create(name='foo')
        tag_boo = Tag.objects.create(name='boo')
        tag_zoo = Tag.objects.create(name='zoo')
        tag_bz = Tag.objects.create(name='bz')
        bookmark_foo.tag_set.add(tag_foo, tag_bz)
        bookmark_boo.tag_set.add(tag_boo, tag_bz)
        bookmark_zoo.tag_set.add(tag_zoo, tag_bz)
        search_url = reverse('bookmarks:search')
        self.assertEquals(search_url, '/search/')
        query_url = lambda q: '{0}?query={1}'.format(search_url, q)
        response = self.client.get(query_url('Foo'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['bookmark_list']), 1)
        self.assertIn('Search results for "Foo"', response.content)
        self.assertNotIn('Add bookmark', response.content)

    def test_share_bookmark_ajax(self):
        bm = Bookmark.objects.create(
            title='foo',
            link=Link.objects.create(url='http://www.foo.bar/'),
            user=self.user
        )
        # Bookmark is not shared yet
        self.assertFalse(bm.is_shared)
        share_url = reverse('bookmarks:share')
        self.assertEquals(share_url, '/ajax/share/')
        response = self.client.post(share_url,
                                    data={'bookmark': bm.pk})
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(SharedBookmark.objects.count(), 1)
        self.assertEquals(data['pk'], bm.pk)
        self.assertTrue(data['shared'])
        self.assertEquals(bm.is_shared, data['shared'])
        # Bookmark is shared now
        self.assertTrue(bm.is_shared)
        # Lets share this bookmark one more time
        response = self.client.post(share_url,
                                    data={'bookmark': bm.pk})
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        # Now bookmark is marked as not shared
        self.assertFalse(data['shared'])
        self.assertEquals(data['pk'], bm.pk)
        self.assertEquals(SharedBookmark.objects.count(), 0)

    def test_shared_bookmark_vote_ajax(self):
        bm = Bookmark.objects.create(
            title='foo',
            link=Link.objects.create(url='http://www.foo.bar/'),
            user=self.user
        )
        shared_bm = SharedBookmark.objects.create(bookmark=bm)
        vote_url = reverse('bookmarks:vote')
        self.assertEquals(vote_url, '/ajax/vote/')
        response = self.client.post(vote_url, data={'bookmark': shared_bm.id})
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['votes'], 2)
        self.assertEquals(data['bookmark']['pk'], bm.pk)
        self.assertTrue(data['bookmark']['shared'])
        response = self.client.post(vote_url, data={'bookmark': shared_bm.id})
        # User can't vote one more time
        self.assertEquals(response.status_code, 400)
        # Pass not existing bookmark
        response = self.client.post(vote_url, data={'bookmark': 100})
        self.assertEquals(response.status_code, 404)
        # Logout user
        self.client.logout()
        response = self.client.post(vote_url, data={'bookmark': shared_bm.id})
        self.assertEquals(403, response.status_code)

    def test_popular_page(self):
        self.client.logout()
        bookmark_foo = Bookmark.objects.create(
            title='Foo',
            link=Link.objects.create(url='http://www.foo.bz/'),
            user=self.user
        )
        bookmark_bar = Bookmark.objects.create(
            title='Bar',
            link=Link.objects.create(url='http://www.bar.bz/'),
            user=self.user
        )
        SharedBookmark.objects.create(bookmark=bookmark_foo)
        SharedBookmark.objects.create(bookmark=bookmark_bar)
        popular_url = reverse('bookmarks:popular')
        self.assertEquals(popular_url, '/popular/')
        response = self.client.get(popular_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['bookmark_list']), 2)
        self.assertTemplateUsed(response, 'bookmarks/popular_list.html')

    def test_bookmark_page(self):
        bm = Bookmark.objects.create(
            title='foo',
            link=Link.objects.create(url='http://www.foo.bar/'),
            user=self.user
        )
        shared_bm = SharedBookmark.objects.create(bookmark=bm)
        bookmark_page_url = reverse('bookmarks:page',
                                    kwargs={'pk': shared_bm.pk})
        self.assertEquals(bookmark_page_url, '/{0}/'.format(shared_bm.pk))
        response = self.client.get(bookmark_page_url)
        self.assertEquals(200, response.status_code)
        self.assertIsInstance(response.context['shared_bookmark'], SharedBookmark)