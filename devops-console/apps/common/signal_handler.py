# -*- coding: utf-8 -*-
#

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction

from devops.utils import current_request
from common.utils import get_request_ip
from .models import OperateLog

MODELS_NEED_RECORD = (
    'User', 'Organization', 'Team', 'Member', 'Project', 'Module',
    'Label', 'Comment', 'Application', 'Feature', 'FeatureBranch', 'WorkItem', 'Iteration'
)
PATH_NOT_NEED_RECORD = (
    '/api/v1/login',
)
PROJECT_RECORD = (
    'Module',
    'Label', 'Comment', 'Application', 'Feature', 'FeatureBranch', 'WorkItem', 'Iteration'
)


def create_operate_log(action, sender, resource):
    if not current_request:
        return
    path = current_request.path
    if path in PATH_NOT_NEED_RECORD:
        return
    user = current_request.user if current_request else None
    if not user or not user.is_authenticated:
        return
    model_name = sender._meta.object_name
    if model_name not in MODELS_NEED_RECORD:
        return
    resource_type = sender._meta.db_table
    remote_addr = get_request_ip(current_request)
    project_id = None
    resource_id = None
    if model_name in PROJECT_RECORD:
        project_id = current_request.resolver_match.kwargs.get('project_id')
    if model_name == 'Project':
        project_id = current_request.resolver_match.kwargs.get('pk')
    if resource:
        resource_id = resource.id
    with transaction.atomic():
        OperateLog.objects.create(
            user=user, action=action, resource_type=resource_type,
            resource_id=resource_id, remote_addr=remote_addr, project_id=project_id
        )


@receiver(post_save, dispatch_uid="my_unique_identifier")
def on_object_created_or_update(sender, instance=None, created=False, **kwargs):
    if created:
        action = OperateLog.ACTION_CREATE
    else:
        action = OperateLog.ACTION_UPDATE
    create_operate_log(action, sender, instance)


@receiver(post_delete, dispatch_uid="my_unique_identifier")
def on_object_delete(sender, instance=None, **kwargs):
    create_operate_log(OperateLog.ACTION_DELETE, sender, instance)
