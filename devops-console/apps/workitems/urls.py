from django.urls import path
from rest_framework import routers
from .views import WorkItemViewSet, WorkItemCommentViewSet

app_name = "workitems"

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'workItems', WorkItemViewSet, 'workItem')

# 项目标签
router.register(r'workItems/(?P<w_id>[^/.]+)/comments',
                WorkItemCommentViewSet, 'workitems-comments')
urlpatterns = [

]

urlpatterns += router.urls
