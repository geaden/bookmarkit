# -*- coding: utf-8 -*-
import os
import random
from string import letters
import time

from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from ..models import Bookmark, Link
from ...users.models import BookmarksUser
from ...tags.models import Tag


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class BookmarksLiveTestCase(LiveServerTestCase):
    items = 25
    tags = 71

    @classmethod
    def setUpClass(cls):
        BookmarksUser.objects.\
            create_user(
                email='foo@bur.bz',
                last_name='foo',
                first_name='bar',
                password='buz')
        fixture_file = os.path.join(os.path.dirname(__file__), 'bookmarks_paginated.json')
        call_command("loaddata", "{0}".format(fixture_file),
                     verbosity=0)
        super(BookmarksLiveTestCase, cls).setUpClass()

    def setUp(self):
        self.user = BookmarksUser.objects.\
            create_user(
                email='foo@bar.bz',
                last_name='foo',
                first_name='bar',
                password='buz')
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(20)
        self.create_bookmark_url = reverse('bookmarks:save')
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Please Sign In', body.text,
                      msg='Login should be present in page')
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        username_field.send_keys('foo@bar.bz')
        password_field.send_keys('buz')
        password_field.send_keys(Keys.RETURN)

    def tearDown(self):
        self.browser.quit()

    def test_create_bookmark_view(self):
        self.browser.get(self.live_server_url + self.create_bookmark_url)
        body = self.browser.find_element_by_tag_name('body')

        self.assertIn('Save bookmark', body.text,
                      msg='Title `Save bookmark` should be present')

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

    def test_bookmarks_pagination(self):
        self.assertEquals(Bookmark.objects.count(), self.items,
                          msg='Fixtures should be loaded {0}.'.format(Bookmark.objects.count()))
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(u'\xab\n1\n2\n\xbb', body.text,
                      msg='Pagination should be present.')

    def test_save_bookmark_ajax(self):
        add_bookmark = self.browser.find_element_by_link_text('Add bookmark')
        add_bookmark.click()
        time.sleep(2)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Save bookmark', body.text,
                      msg='Title `Save bookmark` should be present')
        url_field = self.browser.find_element_by_id('id_url')
        title_field = self.browser.find_element_by_id('id_title')
        tags_field = self.browser.find_element_by_id('id_tags_tag')
        url_field.send_keys('http://www.foo.bz')
        title_field.send_keys('Foo')
        tags_field.send_keys('foo,')
        tags_field.send_keys('bar,')
        self.browser.find_element_by_css_selector('input[type=submit]').click()
        # Alert message should be shown
        alert = self.browser.find_element_by_css_selector('.alert')
        self.assertTrue(alert.is_displayed())
        body = self.browser.find_element_by_tag_name('body')
        table = self.browser.find_element_by_xpath('//table[@class="table table-hover"]')
        # Count rows
        count_rows = 0
        for tr in table.find_elements_by_tag_name('tr'):
            count_rows += 1
        self.assertEquals(count_rows, 2)
        self.assertIn('Foo', body.text)
        self.assertEquals(Bookmark.objects.count(), 1)
        self.assertEquals(Tag.objects.count(), 2)

    def test_update_bookmark_ajax(self):
        Bookmark.objects.create(
            link=Link.objects.create(url='http://www.foo.bz/'),
            user=self.user,
            title='Foo'
        )
        self.browser.get(self.live_server_url)
        edit_link = self.browser.find_element_by_class_name('bookmark-edit')
        edit_link.click()
        time.sleep(2)
        url_field = self.browser.find_element_by_id('id_url')
        self.assertEquals('http://www.foo.bz/', url_field.get_attribute('value'))
        title_field = self.browser.find_element_by_id('id_title')
        self.assertEquals('Foo', title_field.get_attribute('value'))
        tags_field = self.browser.find_element_by_id('id_tags_tag')
        tags_field.send_keys('foo,')
        tags_field.send_keys('bar,')
        self.browser.find_element_by_css_selector('input[type=submit]').click()
        # Alert message should be shown
        alert = self.browser.find_element_by_css_selector('.alert')
        self.assertTrue(alert.is_displayed())
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('foo', body.text, msg='Tag `foo` should be present')
        self.assertIn('bar', body.text, msg='Tag `bar` should be present')
