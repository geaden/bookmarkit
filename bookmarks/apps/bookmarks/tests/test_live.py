# -*- coding: utf-8 -*-
from StringIO import StringIO
import os
import time

from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.test import LiveServerTestCase
from django.test.utils import override_settings
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from ..models import Bookmark, Link, SharedBookmark
from ...users.models import BookmarksUser
from ...tags.models import Tag


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


def create_fixture(app_name, filename):
    buf = StringIO()
    call_command('dumpdata', app_name, stdout=buf)
    buf.seek(0)
    with open(filename, 'w') as f:
        f.write(buf.read())


@override_settings(SECRET_KEY='FooBar')
class BookmarksLiveTestCase(LiveServerTestCase):
    fixtures = map(lambda x: os.path.join(os.path.dirname(__file__), x),
                   ['users.json', 'bookmarks_paginated.json'])
    bookmarks = 25
    tags = 71

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(20)
        self.user = BookmarksUser.objects.get(pk=1)
        self.create_bookmark_url = reverse('bookmarks:save')
        self.popular_url = reverse('bookmarks:popular')
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
        super(BookmarksLiveTestCase, self).tearDown()

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

        self.assertEquals(Bookmark.objects.count(), self.bookmarks + 1)
        self.assertEquals(Tag.objects.count(), self.tags + 2)

    def test_bookmarks_pagination(self):
        self.assertEquals(Bookmark.objects.count(), self.bookmarks,
                          msg='Fixtures should be loaded {0}.'.format(Bookmark.objects.count()))
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(u'\n1\n2\n', body.text,
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
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.find_element_by_css_selector('.alert')
        )
        time.sleep(1)
        alert = self.browser.find_element_by_css_selector('.alert')
        self.assertTrue(alert.is_displayed())
        body = self.browser.find_element_by_tag_name('body')
        table = self.browser.find_element_by_xpath('//table[@class="table table-hover"]')
        # Count rows
        count_rows = 0
        for tr in table.find_elements_by_tag_name('tr'):
            count_rows += 1
        # TODO: fix pagination (no more than 20 bookmarks per page)
        self.assertEquals(count_rows, 22)
        self.assertIn('Foo', body.text)
        self.assertEquals(Bookmark.objects.count(), self.bookmarks + 1)
        self.assertEquals(Tag.objects.count(), self.tags + 2)

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
        time.sleep(1)
        alert = self.browser.find_element_by_css_selector('.alert')
        self.assertTrue(alert.is_displayed())
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('foo', body.text, msg='Tag `foo` should be present')
        self.assertIn('bar', body.text, msg='Tag `bar` should be present')

    def test_bookmark_search(self):
        # positive search results
        search_field = self.browser.find_element_by_id('bookmarkSearch')
        search_field.send_keys('XrgEdk')
        search_field.send_keys(Keys.RETURN)
        body = self.browser.find_element_by_tag_name('body')
        WebDriverWait(self.browser, 10).until(
            lambda s: s.find_element_by_tag_name('h3'))
        self.assertIn('Search results for "XrgEdk":', body.text)
        table = self.browser.find_element_by_xpath('//table[@class="table table-hover"]')
        # Number of search results should be 1
        count_rows = 0
        for tr in table.find_elements_by_tag_name('tr'):
            count_rows += 1
        self.assertEquals(count_rows, 2)

    def test_shared_bookmarks(self):
        trs = self.browser.find_elements_by_tag_name('tr')
        hover = ActionChains(self.browser).move_to_element(trs[1])
        hover.perform()
        share = self.browser.find_element_by_class_name('bookmark-share')
        share.click()
        time.sleep(1)
        alert = self.browser.find_element_by_css_selector('.alert')
        self.assertTrue(alert.is_displayed())
        self.assertIn('has been successfully shared', alert.text)
        self.assertEquals(SharedBookmark.objects.count(), 1)
        hover = ActionChains(self.browser).move_to_element(trs[2])
        hover.perform()
        hover = ActionChains(self.browser).move_to_element(trs[1])
        hover.perform()
        time.sleep(3)
        share.click()
        time.sleep(1)
        alert = self.browser.find_element_by_css_selector('.alert')
        self.assertTrue(alert.is_displayed())
        self.assertIn('not', alert.text)
        # Test shared bookmarks layout
        popular = self.browser.find_element_by_link_text('Popular')
        popular.click()
        count_rows = 0
        table = self.browser.find_element_by_tag_name('table')
        for tr in table.find_elements_by_tag_name('tr'):
            count_rows += 1
        self.assertEquals(2, count_rows)
        self.assertIn('No one has shared any bookmarks yet', table.text)

    def test_vote_for_bookmarks(self):
        bookmark = Bookmark.objects.get(pk=1)
        SharedBookmark.objects.create(bookmark=bookmark)
        self.browser.get(self.live_server_url + self.popular_url)
        count_rows = 0
        table = self.browser.find_element_by_tag_name('table')
        for tr in table.find_elements_by_tag_name('tr'):
            count_rows += 1
        self.assertEquals(count_rows, 2)
        self.assertNotIn('No one has shared any bookmarks yet', table.text)
        trs = self.browser.find_elements_by_tag_name('tr')
        hover = ActionChains(self.browser).move_to_element(trs[1])
        hover.perform()
        vote_up = self.browser.find_element_by_class_name('vote-up')
        vote_up.send_keys(Keys.ENTER)
        ActionChains(self.browser).move_to_element(vote_up).click(vote_up).\
            perform()
        time.sleep(2)
        alert = self.browser.find_element_by_css_selector('.alert')
        self.assertTrue(alert.is_displayed())
        self.assertIn('You voted for', alert.text)
        time.sleep(4)
        trs = self.browser.find_elements_by_tag_name('tr')
        hover = ActionChains(self.browser).move_to_element(trs[1])
        hover.perform()
        vote_up = self.browser.find_element_by_class_name('vote-up')
        vote_up.send_keys(Keys.ENTER)
        ActionChains(self.browser).move_to_element(vote_up).click(vote_up).\
            perform()
        self.assertEquals(SharedBookmark.objects.all()[0].votes, 2)
        badge = self.browser.find_element_by_class_name('badge')
        self.assertEquals(u'2', badge.text, msg='Number of votes should be 2')
        time.sleep(2)
        alert = self.browser.find_element_by_css_selector('.alert')
        self.assertTrue(alert.is_displayed())
        self.assertIn('can\'t', alert.text)

    def test_bookmark_page(self):
        bookmark = Bookmark.objects.get(pk=1)
        sb = SharedBookmark.objects.create(bookmark=bookmark)
        bookmark_page_url = reverse('bookmarks:page', kwargs={'pk': sb.pk})
        self.browser.get(self.live_server_url + bookmark_page_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(sb.bookmark.title, body.text)
        # TODO: tests comments
