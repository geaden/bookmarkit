# -*- coding: utf-8 -*-

from django.db import models

from ..bookmarks.models import Bookmark

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    bookmarks = models.ManyToManyField(Bookmark)

    def __unicode__(self):
        return self.name