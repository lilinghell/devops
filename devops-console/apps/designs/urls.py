from rest_framework import routers
from django.urls import path

from .views import DictionaryView, GroupView, InterfaceView, InterfaceTestView, EsbInterfaceView,InterfaceYamlView

app_name = "designs"

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'designs/dictionary', DictionaryView, 'designs-dictionary')
router.register(r'designs/(?P<project_id>[^/.]+)/groups', GroupView, 'designs-group')
router.register(r'designs/(?P<project_id>[^/.]+)/interfaces', InterfaceView, 'designs-interfaces')
router.register(r'designs/(?P<project_id>[^/.]+)/(?P<interface_id>[^/.]+)/test', InterfaceTestView, 'designs-interface-test')
router.register(r'designs/esb/interfaces', EsbInterfaceView, 'designs-esb-interfaces')
urlpatterns = [
    path('designs/interface_yaml/query', InterfaceYamlView.as_view(), name='interface-yaml'),
]

urlpatterns += router.urls
