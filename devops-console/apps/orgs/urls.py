# -*- coding: utf-8 -*-
#
from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import OrgAdminSetOrgView
from .views import OrgMembershipAdminsViewSet, OrgViewSet, SwitchOrgView, OrgProductAdminView, LogoDetailView

app_name = 'orgs'

router = DefaultRouter(trailing_slash=False)
router.register(r'admin/orgs', OrgViewSet, 'orgs')

router.register(r'admin/orgs/(?P<org_id>[^/.]+)/users',
                OrgMembershipAdminsViewSet, 'org-membership')
router.register(r'products/(?P<product>[^/.]+)/admins', OrgProductAdminView, "product-admin")
urlpatterns = [
    path('admin/orgs/<int:pk>/switch/', SwitchOrgView.as_view(), name="orgs-switch"),
    path('admin/orgs/<int:pk>/logo/', LogoDetailView.as_view(), name="logo-detail"),
    path('org', OrgAdminSetOrgView.as_view(), name='org-admin-set-org'),
]

urlpatterns += router.urls
