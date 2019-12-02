# -*- coding: utf-8 -*-
#

from django.utils.six import text_type
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework import authentication, exceptions
from rest_framework.authentication import CSRFCheck

from common.models import PrivateToken


def get_request_date_header(request):
    date = request.META.get('HTTP_DATE', b'')
    if isinstance(date, text_type):
        # Work around django test client oddness
        date = date.encode(HTTP_HEADER_ENCODING)
    return date


class PrivateTokenAuthentication(authentication.TokenAuthentication):
    model = PrivateToken


class SessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        reason = CSRFCheck().process_view(request, None, (), {})
        if reason:
            raise exceptions.AuthenticationFailed(reason)
