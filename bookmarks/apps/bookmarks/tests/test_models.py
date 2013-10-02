# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import Link, Bookmark, SharedBookmark
from ...users.models import BookmarksUser
from ...folders.models import Folder, FolderSystem

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BookmarksTestCase(TestCase):
    def setUp(self):
        self.user = BookmarksUser.objects.create_user(
            email='foo@bar.bz',
            last_name='foo',
            first_name='baz',
            password='bz'
        )
        self.link = Link.objects.create(
            url='http://www.foo.bar'
        )
        self.bookmark = Bookmark.objects.create(
            link=self.link,
            user=self.user,
            title=u'foo'
        )
        self.shared = SharedBookmark.objects.create(
            bookmark=self.bookmark
        )

    def test_bookmark_created(self):
        self.assertEquals(Bookmark.objects.count(), 1)
        self.assertEquals(self.bookmark.title, u'foo')
        self.assertEquals(self.bookmark.__unicode__(),
                          u'foo@bar.bz, http://www.foo.bar')

    def test_link_created(self):
        self.assertEquals(Link.objects.count(), 1)

    def test_shared_created(self):
        self.assertEquals(SharedBookmark.objects.count(), 1)
        self.assertEquals(self.shared.__unicode__(),
                          u'foo@bar.bz, http://www.foo.bar,1')

    def test_bookmark_to_folder(self):
        folder = Folder.objects.create(
            name=u'foo'
        )
        self.bookmark.folder = folder
        self.bookmark.save()
        self.assertEquals(folder.bookmark_set.count(), 1)


