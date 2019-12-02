from rest_framework import routers

from .views import FeatureViewSet, FeatureBranchViewSet

app_name = "features"

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'features', FeatureViewSet, 'features')
router.register(r'features/(?P<feature_id>[^/.]+)/branchs',
                FeatureBranchViewSet, 'features-branch')
urlpatterns = [
]

urlpatterns += router.urls
