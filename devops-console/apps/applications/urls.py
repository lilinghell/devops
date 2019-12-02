from django.urls import path
from rest_framework import routers

from .views import RepositoryAPIView, ApplicationViewSet, BranchAPIView, CommitAPIView

app_name = "applications"

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'apps', ApplicationViewSet, 'apps')

urlpatterns = [
    path('apps/<int:application_id>/repos', RepositoryAPIView.as_view(), name='apps-repo'),
    path('apps/<int:application_id>/git_branchs', BranchAPIView.as_view(), name='apps-branch'),
    path('apps/<int:application_id>/commits', CommitAPIView.as_view(), name='apps-commit'),
]

urlpatterns += router.urls
