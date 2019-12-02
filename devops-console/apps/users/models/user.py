# -*- coding: utf-8 -*-
#
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from common.utils import date_expired_default
from orgs.models import Organization

__all__ = ['User']


class User(AbstractUser):
    SOURCE_LOCAL = 'local'
    SOURCE_LDAP = 'ldap'
    SOURCE_OPENID = 'openid'
    SOURCE_CHOICES = (
        (SOURCE_LOCAL, 'Local'),
        (SOURCE_LDAP, 'LDAP/AD'),
        (SOURCE_OPENID, 'OpenID'),
    )
    AUTHORITY_SUPERUSER = 'superuser'
    AUTHORITY_ADMIN = 'admin'
    AUTHORITY_USER = 'user'
    username = models.CharField(
        max_length=128, unique=True, verbose_name=_('Username')
    )
    name = models.CharField(null=True, max_length=128, verbose_name=_('Name'))
    email = models.EmailField(
        max_length=128, unique=True, verbose_name=_('Email')
    )
    avatar = models.ImageField(
        upload_to="avatar", null=True, verbose_name=_('Avatar')
    )
    wechat = models.CharField(
        max_length=128, blank=True, verbose_name=_('Wechat')
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_('Phone')
    )
    description = models.TextField(
        max_length=200, blank=True, verbose_name=_('Description')
    )
    is_first_login = models.BooleanField(default=True)
    date_expired = models.DateTimeField(
        default=date_expired_default, blank=True, null=True,
        db_index=True, verbose_name=_('Date expired')
    )
    created_by = models.CharField(
        max_length=30, default='', verbose_name=_('Created by')
    )
    source = models.CharField(
        max_length=30, default=SOURCE_LOCAL, choices=SOURCE_CHOICES,
        verbose_name=_('Source')
    )
    date_password_last_updated = models.DateTimeField(
        auto_now_add=True, blank=True, null=True,
        verbose_name=_('Date password last updated')
    )
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_('date_joined')
    )

    def __str__(self):
        return '{0.name}({0.username})'.format(self)

    @property
    def password_raw(self):
        # raise AttributeError('Password raw is not a readable attribute')
        return self.password_raw
        #: Use this attr to set user object password, example
        #: user = User(username='example', password_raw='password', ...)
        #: It's equal:
        #: user = User(username='example', ...)
        #: user.set_password('password')

    @password_raw.setter
    def password_raw(self, password_raw_):
        self.set_password(password_raw_)

    def set_password(self, raw_password):
        self._set_password = True
        if self.can_update_password():
            return super().set_password(raw_password)
        else:
            error = _("User auth from {}, go there change password").format(self.source)
            raise PermissionError(error)

    def can_update_password(self):
        return self.is_local

    def get_absolute_url(self):
        return reverse('users:user-detail', args=(self.id,))

    @property
    def is_expired(self):
        if self.date_expired and self.date_expired < timezone.now():
            return True
        else:
            return False

    @property
    def is_valid(self):
        if self.is_active and not self.is_expired:
            return True
        return False

    @property
    def admin_orgs(self):
        from orgs.models import Organization
        return Organization.get_user_admin_orgs(self)

    @property
    def user_orgs(self):
        return self.orgs.all()

    @property
    def is_org_admin(self):
        if self.is_superuser or self.admin_orgs.exists():
            return True
        else:
            return False

    @property
    def is_staff(self):
        if self.is_authenticated and self.is_valid:
            return True
        else:
            return False

    @property
    def is_local(self):
        return self.source == self.SOURCE_LOCAL

    @property
    def date_password_expired(self):
        interval = settings.SECURITY_PASSWORD_EXPIRATION_TIME
        date_expired = self.date_password_last_updated + timezone.timedelta(
            days=int(interval))
        return date_expired

    @property
    def password_expired_remain_days(self):
        date_remain = self.date_password_expired - timezone.now()
        return date_remain.days

    @property
    def password_has_expired(self):
        if self.is_local and self.password_expired_remain_days < 0:
            return True
        return False

    @property
    def password_will_expired(self):
        if self.is_local and self.password_expired_remain_days < 5:
            return True
        return False

    @property
    def authority(self):
        if self.is_superuser:
            return self.AUTHORITY_SUPERUSER
        elif self.admin_orgs.exists():
            return self.AUTHORITY_ADMIN
        else:
            return self.AUTHORITY_USER

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.username
        if self.username == 'admin':
            self.is_superuser = True
            self.is_active = True
        super().save(*args, **kwargs)

    def to_json(self):
        return OrderedDict({
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'groups': [group.name for group in self.groups.all()],
            'source': self.get_source_display(),
            'wechat': self.wechat,
            'phone': self.phone,
            'description': self.description,
            'date_expired': self.date_expired.strftime('%Y-%m-%d %H:%M:%S') \
                if self.date_expired is not None else None
        })

    def reset_password(self, new_password):
        self.set_password(new_password)
        self.date_password_last_updated = timezone.now()
        self.save()

    def avatar_url(self):
        admin_default = settings.STATIC_URL + "img/avatar/admin.png"
        user_default = settings.STATIC_URL + "img/avatar/user.png"
        if self.avatar:
            return self.avatar.url
        if self.is_superuser:
            return admin_default
        else:
            return user_default

    def delete(self, using=None, keep_parents=False):
        if self.pk == 1 or self.username == 'admin':
            return
        return super(User, self).delete()

    class Meta:
        ordering = ['username']
        verbose_name = _("User")

    #: Use this method initial user
    @classmethod
    def initial(cls):
        user = cls(username='admin',
                   email='admin@devops.org',
                   name=_('Administrator'),
                   password_raw='admin',
                   description=_('Administrator is the super user of system'),
                   created_by=_('System'))
        user.save()
        Organization.initial()
