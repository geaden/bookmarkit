# -*- coding: utf-8 -*-
from django.db import models

from ..users.models import BookmarksUser
from ..bookmarks.models import SharedBookmark

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class Comment(models.Model):
    user = models.ForeignKey(BookmarksUser)
    bookmark = models.ForeignKey(SharedBookmark)
    text = models.TextField()
    published = models.DateTimeField(auto_now_add=True)