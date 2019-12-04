from rest_framework import routers
from django.urls import path


app_name = "pipelines"

router = routers.DefaultRouter(trailing_slash=False)
urlpatterns = [
]

urlpatterns += router.urls
