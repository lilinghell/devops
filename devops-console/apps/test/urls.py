from rest_framework import routers

from .views import TestEnvViewSet, TestGroupView, TestCaseView, TestCasesView, TestPlanView, TestAutoPlanView

app_name = "test"

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'test/(?P<project_id>[^/.]+)/env', TestEnvViewSet, 'test-env')
router.register(r'test/(?P<project_id>[^/.]+)/group', TestGroupView, 'test-group')
router.register(r'test/(?P<project_id>[^/.]+)/cases', TestCasesView, 'test-case')
router.register(r'test/(?P<project_id>[^/.]+)/(?P<case_id>[^/.]+)/test', TestCaseView, 'test-test')
router.register(r'test/(?P<project_id>[^/.]+)/plan', TestPlanView, 'test-plan')
router.register(r'test/(?P<project_id>[^/.]+)/auto_plan', TestAutoPlanView, 'test-auto-plan')

urlpatterns = []

urlpatterns += router.urls

