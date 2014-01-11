# -*- coding: utf-8 -*-
import os
from django.test import TestCase
from django.test.utils import override_settings

from ..models import Comment
from ...bookmarks.models import Bookmark, SharedBookmark
from ...users.models import BookmarksUser

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


path = lambda x: os.path.join(
    os.path.dirname(__file__),
    '..', '..', 'bookmarks', 'tests', x)

@override_settings(SECRET_KEY='FooBar')
class CommentsModelsTestCase(TestCase):
    fixtures = map(path, ['users.json', 'bookmarks.json'])

    def setUp(self):
        self.user = BookmarksUser.objects.all()[0]
        self.bookmark = Bookmark.objects.all()[0]
        self.sb = SharedBookmark.objects.create(
            bookmark=self.bookmark)

    def test_create_comment(self):
        comment = Comment.objects.create(
            bookmark=self.sb,
            user=self.user,
            text='Cool!'
        )
        self.assertEquals(Comment.objects.count(), 1)
        self.assertEquals(self.sb.comment_set.count(), 1)
