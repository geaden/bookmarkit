# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from django.db import models
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.utils.translation \
    import ugettext_lazy as _
from django.core import mail

from ..users.models import BookmarksUser

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class Friendship(models.Model):
    from_friend = models.ForeignKey(BookmarksUser, related_name='friend_set')
    to_friend = models.ForeignKey(BookmarksUser, related_name='to_friend_set')

    def __unicode__(self):
        return "{0}, {1}".format(self.from_friend.get_full_name(),
                                 self.to_friend.get_full_name())

    class Meta:
        unique_together = (('to_friend', 'from_friend'), )
        permissions = (('can_list_friend_bookmarks', 'Can list friend bookmarks'), )


class Invitation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    sender = models.ForeignKey(BookmarksUser)

    def __unicode__(self):
        return "{0}, {1}".format(self.sender.get_full_name(), self.email)

    def send(self):
        subject = _(u'Invitation to join Bookmark.It')
        link = reverse('friends:accept', args=[self.code])
        template = get_template('emails/invitation_email.txt')
        context = Context({
            'name': self.name,
            'host': settings.SITE_HOST,
            'link': link,
            'sender': self.sender.get_full_name(),
        })
        message = template.render(context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])