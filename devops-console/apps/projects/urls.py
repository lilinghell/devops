from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from .views import ProjectViewSet, ProjectMemberViewSet, ProjectOwnerAPIView, ProjectListAPIView, ProjectLabelViewSet, \
    ProjectModuleViewSet

app_name = "projects"

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'projects', ProjectViewSet, 'projects¬')
# 项目成员
router.register(r'projects/(?P<project_id>[^/.]+)/members',
                ProjectMemberViewSet, 'projects-membership')
# 项目标签
router.register(r'projects/(?P<project_id>[^/.]+)/labels',
                ProjectLabelViewSet, 'projects-label')
# 项目模块
router.register(r'projects/(?P<project_id>[^/.]+)/modules',
                ProjectModuleViewSet, 'projects-module')

urlpatterns = [
    path('projects/<int:pk>/owner/', ProjectOwnerAPIView.as_view(), name='projects-change-owner'),
    path('user/projects', ProjectListAPIView.as_view(), name='user-projects'),
]

urlpatterns += router.urls
