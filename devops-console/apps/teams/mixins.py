class TeamMemberSerializerMixin:
    def run_validation(self, initial_data=None):
        initial_data['source_id'] = str(self.context['source_id'])

        return super().run_validation(initial_data)


class TeamMemberModelViewSetMixin:
    """

    获取工作组ID
    """
    http_method_names = ['get', 'post', 'delete', 'put']

    def dispatch(self, request, *args, **kwargs):
        self.source_id = kwargs.get('source_id')
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['source_id'] = self.kwargs.get('source_id')
        return context


class TeamViewSetMixin:

    def dispatch(self, request, *args, **kwargs):
        self.team_id = kwargs.get('team_id')
        kwargs['partial'] = True
        return super().dispatch(request, *args, **kwargs)
