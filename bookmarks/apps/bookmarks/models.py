# -*- coding: utf-8 -*-

from django.db import models

from ..users.models import BookmarksUser
from ..folders.models import Folder


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class Link(models.Model):
    url = models.URLField(unique=True)

    def __unicode__(self):
        return self.url


class Bookmark(models.Model):
    user = models.ForeignKey(BookmarksUser)
    link = models.ForeignKey(Link)
    title = models.CharField(max_length=200)
    folder = models.ForeignKey(Folder, null=True, blank=True)

    def __unicode__(self):
        return u'{user}, {link}'.format(user=self.user.email,
                                        link=self.link.url)

    def get_absolute_url(self):
        return self.link.url


class SharedBookmark(models.Model):
    bookmark = models.ForeignKey(Bookmark, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=1)
    user_voted = models.ManyToManyField(BookmarksUser)

    def __unicode__(self):
        return '{bookmark}, {votes}'.format(bookmark=self.bookmark,
                                           votes=self.votes)

