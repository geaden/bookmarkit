# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Invitation

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class FriendAcceptView(View):
    def get(self, request, **kwargs):
        invitation = get_object_or_404(Invitation,
                                       code__exact=kwargs.get('code'))
        request.session['invitation'] = invitation.id
        return HttpResponseRedirect(
            reverse_lazy('users:register'))