from django_filters import compat
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.inspectors import SwaggerAutoSchema

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys):
        if len(operation_keys) > 2 and operation_keys[1].startswith('v'):
            return [operation_keys[2]]
        if "devops" in operation_keys:
            return [operation_keys[1]]
        return super().get_tags(operation_keys)


def get_swagger_view(version='v1'):
    schema_view = get_schema_view(
        openapi.Info(
            title="devops API Docs",
            default_version=version,
            description="devops Restful api docs",
            terms_of_service="",
            contact=openapi.Contact(email=""),
            license=openapi.License(name=""),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    return schema_view


class CustomDjangoFilterBackend(DjangoFilterBackend):
    """
    Overrides get_schema_fields() to show filter_fields in Swagger.
    """

    def get_schema_fields(self, view):
        assert (
                compat.coreapi is not None
        ), "coreapi must be installed to use `get_schema_fields()`"
        assert (
                compat.coreschema is not None
        ), "coreschema must be installed to use `get_schema_fields()`"

        # append filter fields to existing fields
        fields = view.filter_fields
        # if hasattr(view, "filter_fields"):
        #     fields += view.filter_fields

        return [
            compat.coreapi.Field(
                name=field,
                location='query',
                required=False,
                schema=compat.coreschema.String(description=str('')),
            ) for field in fields
        ]
