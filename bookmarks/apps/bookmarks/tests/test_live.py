# -*- coding: utf-8 -*-
import time

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from ..models import Bookmark
from ...users.models import BookmarksUser
from ...tags.models import Tag


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BookmarksLiveTestCase(LiveServerTestCase):
    def setUp(self):
        self.user = BookmarksUser.objects.\
            create_user(
                email='foo@bar.bz',
                last_name='foo',
                first_name='bar',
                password='buz')
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(20)
        self.client.login(username=self.user.email,
                          password='buz')
        self.create_bookmark_url = reverse('bookmarks:save')

    def tearDown(self):
        self.browser.quit()

    def test_create_bookmark_view(self):
        self.browser.get(self.live_server_url + self.create_bookmark_url)
        body = self.browser.find_element_by_tag_name('body')

        self.assertIn('Please Sign In', body.text,
                      msg='Login should be present in page')

        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys('foo@bar.bz')
        password_field.send_keys('buz')
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        self.assertIn('Create bookmark', body.text,
                      msg='Title `Create bookmark` should be present')

        url_field = self.browser.find_element_by_id('id_url')
        title_field = self.browser.find_element_by_id('id_title')
        tags_field = self.browser.find_element_by_id('id_tags_tag')

        url_field.send_keys('http://www.foo.bz')
        title_field.send_keys('Foo')
        tags_field.send_keys('foo,')
        time.sleep(3)
        tags_field.send_keys('bar,')
        time.sleep(3)
        self.browser.find_element_by_css_selector('input[type=submit]').click()

        self.assertEquals(Bookmark.objects.count(), 1)
        self.assertEquals(Tag.objects.count(), 2)




