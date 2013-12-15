# -*- coding: utf-8 -*-

from django.test import TestCase
from ..models import Tag
from ...bookmarks.models import Bookmark, Link
from ...users.models import BookmarksUser


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TagsTestCase(TestCase):
    def setUp(self):
        self.user = BookmarksUser.objects.create_user(
            email='foo@bar.bz',
            password='bar',
            first_name='foo',
            last_name='bar'
        )
        self.bookmark = Bookmark.objects.create(
            link=Link.objects.create(url='http://www.foo.bar'),
            user=self.user
        )

    def test_add_tags(self):
        tag_foo = Tag.objects.create(name='foo')
        tag_bar = Tag.objects.create(name='bar')
        tag_foo.bookmarks.add(self.bookmark)
        tag_foo.save()
        tag_bar.bookmarks.add(self.bookmark)
        tag_bar.save()
        self.assertEquals(self.bookmark.tag_set.count(), 2)
