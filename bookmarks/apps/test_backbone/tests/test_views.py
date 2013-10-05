# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BackboneTestView(TestCase):
    def test_app_view(self):
        url = reverse('backbone:main')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)