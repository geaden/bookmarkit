# -*- coding: utf-8 -*-
import os
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from ..models import BookmarksUser


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class UsersLiveTestCase(LiveServerTestCase):
    def setUp(self):
        self.user = BookmarksUser.objects.\
            create_user(
                email='foo@bar.bz',
                last_name='foo',
                first_name='bar',
                password='buz'
        )
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(20)
        self.login_url = reverse('users:login')
        self.register_url = reverse('users:register')

    def tearDown(self):
        self.browser.close()

    def before_test(self):
        self.browser.get(self.live_server_url + self.login_url)

        body = self.browser.find_element_by_tag_name('body')

        self.assertIn('Please Sign In', body.text,
                      msg='Login should be present in page')

        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        return username_field, password_field

    def test_login_view(self):
        username_field, password_field = self.before_test()
        username_field.send_keys('foo@bar.bz')
        password_field.send_keys('buz')
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('bar', body.text)

    def test_fail_login(self):
        username_field, password_field = self.before_test()

        username_field.send_keys('fooz@bar.bz')
        password_field.send_keys('buz')
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        self.assertIn('Invalid login!', body.text)
        self.assertIn('Forgot your password?', body.text)

    def test_empty_login(self):
        self.before_test()
        password_field = self.browser.find_element_by_id(
            'id_password')
        password_field.send_keys(Keys.RETURN)

        errors = self.browser.find_elements_by_class_name(
            'has-error')
        self.assertEquals(2, len(errors))

    def test_register(self):
        self.browser.get(self.live_server_url + self.register_url)
        os.environ['RECAPTCHA_TESTING'] = 'True'

        username_field = self.browser.find_element_by_id('id_username')
        last_name_field = self.browser.find_element_by_id('id_last_name')
        first_name_field = self.browser.find_element_by_id('id_first_name')
        password1_field = self.browser.find_element_by_id('id_password1')
        password2_field = self.browser.find_element_by_id('id_password2')
        recaptcha_response_field = self.browser.\
            find_element_by_id('recaptcha_response_field')

        username_field.send_keys('boo@bar.bz')
        last_name_field.send_keys('boo')
        first_name_field.send_keys('buz')
        password1_field.send_keys('boz')
        password2_field.send_keys('boz')
        recaptcha_response_field.send_keys('PASSED')
        recaptcha_response_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        self.assertIn('Please check your email', body.text)
        self.assertEquals(len(mail.outbox), 1)
