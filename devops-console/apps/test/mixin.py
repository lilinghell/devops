# author: Sun Yaxing
# datetime:2019/10/23 15:00


class TestViewSetMixin:

    """
    获取项目ID
    """
    http_method_names = ['get', 'post', 'delete', 'put']

    def dispatch(self, request, *args, **kwargs):
        self.case_id = kwargs.get('case_id')
        kwargs['partial'] = True
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['case_id'] = self.kwargs.get('case_id')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(case_id=self.kwargs.get('case_id'))
        return queryset
