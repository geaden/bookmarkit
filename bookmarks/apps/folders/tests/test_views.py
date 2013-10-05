# -*- coding: utf-8 -*-
import json
from urllib import urlencode
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Folder

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class FoldersViewTestCase(TestCase):
    fixtures = ['../fixtures/folders.json']

    def setUp(self):
        self.list_create_url = reverse(
            'folders:list_create')
        self.retrieve_update_destroy_url = reverse(
            'folders:retrieve_update_destroy', kwargs={'pk': 1}
        )

    def test_folder_list_view(self):
        response = self.client.get(self.list_create_url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['name'], u'foo')
        self.assertEquals(data[0]['icon'], 'default')

    def test_folder_update_view(self):
        data = urlencode({
            'name': u'boo',
            'icon': 'default'
        })
        response = self.client.put(
            self.retrieve_update_destroy_url,
            data=data,
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEquals(200, response.status_code)
        folder = Folder.objects.all()[0]
        self.assertEquals(folder.name, u'boo')

