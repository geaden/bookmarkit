# -*- coding: utf-8 -*-
from django.core import mail
from django.test import TestCase

from ..models import Friendship, Invitation
from ...users.models import BookmarksUser

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class FriendsTestCase(TestCase):
    def setUp(self):
        self.user_1 = BookmarksUser.objects.create_user(
            email=u'foo@bar.bz',
            last_name=u'foo',
            first_name=u'bar',
            password='buz'
        )
        self.user_2 = BookmarksUser.objects.create_user(
            email=u'boo@bar.bz',
            last_name=u'boo',
            first_name=u'zoo',
            password='goo'
        )
        self.friendship = Friendship.objects.create(
            from_friend=self.user_1,
            to_friend=self.user_2
        )
        self.invitation = Invitation.objects.create(
            name='foo',
            email='bar@bar.bz',
            code='zoo',
            sender=self.user_1
        )

    def test_friendship_created(self):
        self.assertEquals(Friendship.objects.count(), 1)
        self.assertEquals(self.friendship.__unicode__(),
                          u'bar foo (foo@bar.bz),'
                          u' zoo boo (boo@bar.bz)')

    def test_invitation_created(self):
        self.assertEquals(Invitation.objects.count(), 1)
        self.assertEquals(self.invitation.__unicode__(),
                          u'bar foo (foo@bar.bz), bar@bar.bz')
        # Send message.
        self.invitation.send()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]

        # Verify that the subject of the first message is correct.
        self.assertEqual(unicode(email.subject),
                         u'Invitation to join Bookmark.It')

        self.assertEquals(email.body, u'\n\nHi foo,\nbar foo (foo@bar.bz) invited you to join '
                                      u'Bookmark.It, a website where you can post and share'
                                      u' your bookmarks with friends!\nTo accept the invitation, '
                                      u'please click the link below:\nfoo.bar/friend/accept/zoo\n--'
                                      u' Bookmark.It Team\n')


