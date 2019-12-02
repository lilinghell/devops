from django.urls import path
from rest_framework import routers
from .views import IterationViewSet, IterationPlanViewSet

app_name = "features"

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'iterations', IterationViewSet, 'iterations')
urlpatterns = [
    path('iteration/<int:pk>/plan', IterationPlanViewSet.as_view(), name='iteration-plan'),
]

urlpatterns += router.urls
