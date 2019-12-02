from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TeamViewSet, TeamMemberViewSet, TeamOwnerAPIView, TeamListAPIView, TeamChildListView

app_name = "teams"

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'teams', TeamViewSet, 'team')
router.register(r'teams/(?P<source_id>[^/.]+)/members',
                TeamMemberViewSet, 'teams-membership')
urlpatterns = [
    path('teams/<int:pk>/owner/', TeamOwnerAPIView.as_view(), name='teams-change-owner'),
    path('teams/<int:pk>/children/', TeamChildListView.as_view(), name='teams-children'),
    path('user/teams', TeamListAPIView.as_view(), name='user-teams'),
]

urlpatterns += router.urls
