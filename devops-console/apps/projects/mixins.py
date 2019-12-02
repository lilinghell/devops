class ProjectValidateSerializerMixin:
    def run_validation(self, initial_data=None):
        initial_data['project_id'] = str(self.context['project_id'])

        return super().run_validation(initial_data)


class ProjectViewSetMixin:
    """

    获取项目ID
    """
    http_method_names = ['get', 'post', 'delete', 'put']

    def dispatch(self, request, *args, **kwargs):
        self.project_id = kwargs.get('project_id')
        kwargs['partial'] = True
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project_id'] = self.kwargs.get('project_id')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(project_id=self.kwargs.get('project_id'))
        return queryset


class ProjectMemberViewSetMixin:
    """

    获取项目ID
    """
    http_method_names = ['get', 'post', 'delete', 'put']

    def dispatch(self, request, *args, **kwargs):
        self.source_id = kwargs.get('project_id')
        kwargs['partial'] = True
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['source_id'] = self.kwargs.get('project_id')
        return context


class ProjectSerializerMixin:
    def create(self, validated_data):
        validated_data['project_id'] = self.context['view'].project_id
        instance = super().create(validated_data)
        return instance
