from django.urls import path
from .views import AttachmentCreateView, AttachmentDeleteView, OperationLogListView

app_name = 'common'

urlpatterns = [
    path('attachments', AttachmentCreateView.as_view(), name="attatch-create"),
    path('attachments/<int:attachment_id>', AttachmentDeleteView.as_view(), name="attatch-delete"),
    path('logs', OperationLogListView.as_view(), name="logs"),
]
