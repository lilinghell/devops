from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from .models import User
from common.utils import get_object_or_none


def check_user_valid(**kwargs):
    password = kwargs.pop('password', None)
    username = kwargs.pop('username', None)

    if username:
        user = get_object_or_none(User, username=username)
    else:
        user = None

    if user is None:
        user = get_object_or_none(User, email=username)

    if user is None:
        return None, _("User not exist")
    elif not user.is_valid:
        return None, _("Disable or expired")

    if password and authenticate(username=user.username, password=password):
        return user, ''

    return None, _("Password invalid")
