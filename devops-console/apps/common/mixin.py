# coding: utf-8

from django.db import models
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from orgs.models import Organization
from users.models import User
from orgs.utils import get_current_org, get_current_user


# 基础db对象
class BaseModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET(-999))

    class Meta:
        abstract = True
        managed = False

    def save(self, *args, **kwargs):
        # 默认注入机构字段
        self.org = get_current_org()
        self.created_by = get_current_user()
        super().save(*args, **kwargs)


class NoDeleteQuerySet(models.query.QuerySet):

    def delete(self):
        return self.update(is_discard=True, discard_time=timezone.now())


class NoDeleteManager(models.Manager):

    def get_all(self):
        return NoDeleteQuerySet(self.model, using=self._db)

    def get_queryset(self):
        return NoDeleteQuerySet(self.model, using=self._db).filter(is_discard=False)

    def get_deleted(self):
        return NoDeleteQuerySet(self.model, using=self._db).filter(is_discard=True)


class NoDeleteModelMixin(models.Model):
    is_discard = models.BooleanField(verbose_name=_("is discard"), default=False)
    discard_time = models.DateTimeField(verbose_name=_("discard time"), null=True, blank=True)

    objects = NoDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.is_discard = True
        self.discard_time = timezone.now()
        return self.save()


class JSONResponseMixin(object):
    """JSON mixin"""

    @staticmethod
    def render_json_response(context):
        return JsonResponse(context)


class IDInFilterMixin(object):
    def filter_queryset(self, queryset):
        queryset = super(IDInFilterMixin, self).filter_queryset(queryset)
        id_list = self.request.query_params.get('id__in')
        if id_list:
            import json
            try:
                ids = json.loads(id_list)
            except Exception as e:
                return queryset
            if isinstance(ids, list):
                queryset = queryset.filter(id__in=ids)
        return queryset


class DatetimeSearchMixin:
    date_format = '%Y-%m-%d'
    date_from = date_to = None

    def get_date_range(self):
        date_from_s = self.request.GET.get('date_from')
        date_to_s = self.request.GET.get('date_to')

        if date_from_s:
            date_from = timezone.datetime.strptime(date_from_s, self.date_format)
            tz = timezone.get_current_timezone()
            self.date_from = tz.localize(date_from)
        else:
            self.date_from = timezone.now() - timezone.timedelta(7)

        if date_to_s:
            date_to = timezone.datetime.strptime(
                date_to_s + ' 23:59:59', self.date_format + ' %H:%M:%S'
            )
            self.date_to = date_to.replace(
                tzinfo=timezone.get_current_timezone()
            )
        else:
            self.date_to = timezone.now()

    def get(self, request, *args, **kwargs):
        self.get_date_range()
        return super().get(request, *args, **kwargs)
