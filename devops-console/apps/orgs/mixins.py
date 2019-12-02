from .models import Organization


class OrgMembershipSerializerMixin:
    def run_validation(self, initial_data=None):
        initial_data['organization'] = str(self.context['org'].id)
        return super().run_validation(initial_data)


class OrgMembershipModelViewSetMixin:
    """

    处理前获取机构信息，返回上下文增加机构信息
    """
    org = None
    http_method_names = ['get', 'post', 'delete', 'put']

    def dispatch(self, request, *args, **kwargs):
        self.org = Organization.objects.get(pk=kwargs.get('org_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['org'] = self.org
        return context
