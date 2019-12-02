from django.urls import path
from rest_framework import routers

from .views import UserAuthApi, UserViewSet, UserLogoutView, UserProfileView, UserProfileUpdatePassword, \
    UserChangePasswordApi, CreaterWorkItemAPIView, OwnerWorkItemAPIView, AssigneeWorkItemAPIView, WorkItemAPIView

app_name = "users"

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, 'user')

urlpatterns = [
    path('login', UserAuthApi.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('user/profile', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/password', UserChangePasswordApi.as_view(), name='user-change-password'),
    path('user/profile/password', UserProfileUpdatePassword.as_view(), name='user-password-update'),
    path('user/create/workitems', CreaterWorkItemAPIView.as_view(), name='user-create-workitem'),
    path('user/own/workitems', OwnerWorkItemAPIView.as_view(), name='user-own-workitem'),
    path('user/assignee/workitems', AssigneeWorkItemAPIView.as_view(), name='user-assign-workitem'),
    path('user/workItems', WorkItemAPIView.as_view(), name='user-assign-workitem'),
]

urlpatterns += router.urls
