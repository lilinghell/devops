"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import url, include
from .swagger import get_swagger_view
from rest_framework import documentation

...

api_urlpatterns = [
    path('api/', include([
        path('v1/', include('common.urls', namespace='api-common')),
        path('v1/', include('users.urls', namespace='api-users')),
        path('v1/', include('orgs.urls', namespace='api-orgs')),
        path('v1/', include('teams.urls', namespace='api-devops-teams')),
        path('v1/', include('designs.urls', namespace='api-designs')),  # sun yx
        path('v1/', include('projects.urls', namespace='api-devops-projects')),
        path('v1/', include('test.urls', namespace='api-devops-test')),
        path('v1/projects/<int:project_id>/', include('applications.urls', namespace='api-devops-apps')),
        path('v1/projects/<int:project_id>/', include('requirements.urls', namespace='api-devops-reqs')),
        path('v1/projects/<int:project_id>/', include('features.urls', namespace='api-devops-features')),
        path('v1/projects/<int:project_id>/', include('workitems.urls', namespace='api-devops-workitems')),
        path('v1/projects/<int:project_id>/', include('iterations.urls', namespace='api-devops-iterations')),
    ]))
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(api_urlpatterns))
]
if settings.DEBUG:
    urlpatterns += [
        re_path('^swagger(?P<format>\.json|\.yaml)$',
                get_swagger_view().without_ui(cache_timeout=1), name='schema-json'),
        path('docs/', get_swagger_view().with_ui('swagger', cache_timeout=1), name="docs"),
        url(r'^apidocs/', documentation.include_docs_urls(title='DEVOPS API title')),
        path('redoc/', get_swagger_view().with_ui('redoc', cache_timeout=1), name='redoc'),

    ]
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),

                      # For django versions before 2.0:
                      # url(r'^__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns
