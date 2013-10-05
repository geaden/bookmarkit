# -*- coding: utf-8 -*-
import os
from django.core import serializers
from django.test import TestCase

from ...folders.models import Folder

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BaseTestCase(TestCase):
    """
    Base test case
    """
    # TODO: complete base test case class
    model = None
    appname = None

    def setUp(self):
        self.create_fixture(self.model, self.model)

    def create_fixture(self):
        """Creates fixtures for Folders"""
        Folder.objects.create(
            name=u'foo')
        with open(os.path.join(os.path.dirname(__file__), '..', 'fixtures/folders.json'), 'w') as f:
            f.write(serializers.serialize('json', Folder.objects.all()))
        return ['../fixtures/folders.json']