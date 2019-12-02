from django.urls import path
from rest_framework import routers
from .views import RequirementViewSet

app_name = "requirements"

router = routers.DefaultRouter()

router.register(r'requirements', RequirementViewSet, 'requirement')

urlpatterns = [
]

urlpatterns += router.urls
