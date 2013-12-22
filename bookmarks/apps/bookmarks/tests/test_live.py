# -*- coding: utf-8 -*-
import time

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from ..models import Bookmark, Link
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
        pass

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
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('No bookmarks yet', body.text,
                      msg='No bookmarks should be disappeared.')
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
        time.sleep(2)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Saved successfully', body.text,
                      msg='Bookmark should be successfully saved.')
        close_button = self.browser.find_element_by_css_selector('button[data-dismiss="modal"]')
        close_button.click()
        time.sleep(2)
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Save bookmark', body.text,
                         msg='Title `Save bookmark` should be present')
        self.assertIn('foo', body.text, msg='Tag `foo` should be present')
        self.assertIn('bar', body.text, msg='Tag `bar` should be present')
