from django.utils.datastructures import MultiValueDict

from orgs.utils import get_current_org
from .models import Attachment, OperateLog
from .serializers import AttachmentSerializer, OperateLogSerializer
from rest_framework import views, status, generics
from rest_framework.response import Response
from django.db import transaction
import os
# Create your views here.
from rest_framework.parsers import MultiPartParser, FormParser


class AttachmentCreateView(generics.CreateAPIView):
    parser_classes = (FormParser, MultiPartParser,)
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def create(self, request, *args, **kwargs):
        files = request.FILES
        if isinstance(files, MultiValueDict):
            for key in files:
                file = files[key]
                instance = Attachment(file=file, filename=file.name, filesize=file.size)
                instance.save()
            return Response(status=status.HTTP_200_OK, data=AttachmentSerializer(instance).data)


class AttachmentDeleteView(views.APIView):
    def delete(self, request, *args, **kwargs):
        instance = Attachment.objects.get(id=kwargs.get("attachment_id"))
        if os.path.isfile(instance.file.path):
            with transaction.atomic():
                instance.file.delete(save=False)
                instance.delete()
                return Response(status=status.HTTP_200_OK, data=AttachmentSerializer(instance).data)


class OperationLogListView(generics.ListAPIView):
    queryset = OperateLog.objects.select_related("created_by")
    serializer_class = OperateLogSerializer
    filter_fields = ('resource_id', 'resource_type', 'project_id')

    def get_queryset(self):
        return super().get_queryset().filter(org=get_current_org())
