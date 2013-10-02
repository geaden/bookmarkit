# -*- coding: utf-8 -*-

from django.db import models


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BaseFolder(models.Model):
    """Base class for folders"""
    name = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Folder(BaseFolder):
    """Folders"""

    def __unicode__(self):
        formated_name = u'<Folder: {0}>'.format(self.name)
        if self.parents.exists():
            return '/'.join([folder.parent_folder.__unicode__()
                            for folder in self.parents.all()] +
                            [formated_name]
            )
        return formated_name


class FolderSystem(models.Model):
    """Folder system for organizing bookmarks"""
    parent_folder = models.ForeignKey(Folder, related_name='children')
    child_folder = models.ForeignKey(Folder, related_name='parents')
