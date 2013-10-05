# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation \
    import ugettext_lazy as _


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


ICON_CHOICES = (
    ('default', _('Default')),
    ('red', _('Red')),
    ('blue', _('Blue')),
    ('pink', _('Pink')),
    ('orange', _('Orange')),
)


class BaseFolder(models.Model):
    """Base class for folders"""
    name = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Folder(BaseFolder):
    """Folders"""
    icon = models.CharField(max_length=20,
                            choices=ICON_CHOICES,
                            default='default')

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
