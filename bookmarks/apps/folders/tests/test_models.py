# -*- coding: utf-8 -*-

from django.test import TestCase

from ..models import Folder, FolderSystem

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class FoldersTestCase(TestCase):
    def setUp(self):
        self.folder = Folder.objects.create(
            name=u'foo'
        )

    def test_create_folder(self):
        self.assertEquals(Folder.objects.count(), 1)
        self.assertEquals(self.folder.name, u'foo')
        self.assertEquals(self.folder.__unicode__(),
                          u'<Folder: foo>')

    def test_create_subfolder(self):
        folder_2 = Folder.objects.create(
            name=u'boo'
        )
        FolderSystem.objects.create(
            parent_folder=self.folder,
            child_folder=folder_2
        )
        self.assertEquals(self.folder.parents.count(), 0)
        self.assertEquals(self.folder.children.count(), 1)
        self.assertEquals(self.folder.__unicode__(), u'<Folder: foo>')
        self.assertEquals(folder_2.__unicode__(),
                          u'<Folder: foo>/<Folder: boo>')

        folder_3 = Folder.objects.create(
            name=u'bar'
        )
        FolderSystem.objects.create(
            parent_folder=folder_2,
            child_folder=folder_3
        )
        self.assertEquals(str(folder_3),
                          u'<Folder: foo>/<Folder: boo>/<Folder: bar>')
