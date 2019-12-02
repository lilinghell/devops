#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = ['LoginLog']


class LoginLog(models.Model):
    LOGIN_TYPE_CHOICE = (
        ('W', 'Web'),
    )

    MFA_DISABLED = 0
    MFA_ENABLED = 1
    MFA_UNKNOWN = 2

    MFA_CHOICE = (
        (MFA_DISABLED, _('Disabled')),
        (MFA_ENABLED, _('Enabled')),
        (MFA_UNKNOWN, _('-')),
    )

    REASON_NOTHING = 0
    REASON_PASSWORD = 1
    REASON_MFA = 2
    REASON_NOT_EXIST = 3
    REASON_PASSWORD_EXPIRED = 4

    REASON_CHOICE = (
        (REASON_NOTHING, _('-')),
        (REASON_PASSWORD, _('Username/password check failed')),
        (REASON_MFA, _('MFA authentication failed')),
        (REASON_NOT_EXIST, _("Username does not exist")),
        (REASON_PASSWORD_EXPIRED, _("Password expired")),
    )

    STATUS_CHOICE = (
        (True, _('Success')),
        (False, _('Failed'))
    )
    username = models.CharField(max_length=128, verbose_name=_('Username'))
    type = models.CharField(choices=LOGIN_TYPE_CHOICE, max_length=2, verbose_name=_('Login type'))
    ip = models.GenericIPAddressField(verbose_name=_('Login ip'))
    reason = models.SmallIntegerField(default=REASON_NOTHING, choices=REASON_CHOICE, verbose_name=_('Reason'))
    status = models.BooleanField(max_length=2, default=True, choices=STATUS_CHOICE, verbose_name=_('Status'))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Date login'))

    class Meta:
        ordering = ['-datetime', 'username']
