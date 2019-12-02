# -*- coding: utf-8 -*-
#
from django.db.models import Subquery
from rest_framework import status, mixins, generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import Response, APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from common import permissions
from common.checkmsg import CheckMsg
from common.exception import DevException
from common.permissions import IsSuperUser, IsOrgAdmin
from common.utils import get_logger
from orgs.utils import current_org, set_current_org, get_current_org
from users.models import User
from users.serializers import UserSerializer
from .mixins import OrgMembershipModelViewSetMixin
from .models import Organization, ProductRole
from .serializers import OrgSerializer, OrgReadSerializer, OrgMembershipAdminSerializer, ProductRoleSerializer, \
    ProductRoleReadSerializer, LogoSerializer

logger = get_logger(__file__)


class SwitchOrgView(APIView):
    """

    post:
    切换机构，超级管理可切换机构之后进行操作
    """

    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        oid = kwargs.get('pk')
        self.org = Organization.objects.get(id=oid)
        request.session['oid'] = self.org.id.__str__()
        set_current_org(self.org)
        return Response(OrgSerializer(get_current_org()).data)


class OrgViewSet(ModelViewSet):
    """
    retrieve:
    描述:获取组织详情
    权限:超级管理员

    list:
    描述:获取组织列表
    权限:超级管理员

    create:
    描述:获取单个组织详情
    权限:超级管理员

    delete:
    描述:获取单个组织详情
    权限:超级管理员
    """
    queryset = Organization.objects.all()
    serializer_class = OrgSerializer
    permission_classes = (IsSuperUser,)
    search_fields = ('name',)
    org = None

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OrgReadSerializer
        else:
            return self.serializer_class

    def get_data_from_model(self, model):
        if model == User:
            data = model.objects.filter(orgs__id=self.org.id)
        return data

    def destroy(self, request, *args, **kwargs):
        self.org = self.get_object()
        models = [
            User,
        ]
        for model in models:
            data = self.get_data_from_model(model)
            if data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if str(current_org) == str(self.org):
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            self.org.delete()
            return Response({'msg': True}, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id__gt=-1)
        return queryset


class OrgMembershipAdminsViewSet(OrgMembershipModelViewSetMixin, ModelViewSet):
    """
    retrieve:
    描述:获取指定组织下单个成员详情
    权限:超级管理员

    list:
    描述:获取指定组织下所有成员
    权限:超级管理员

    create:
    描述:新建指定组织下用户，区分管理员和非管理员
    权限:超级管理员

    delete:
    描述:删除指定组织下单个用户
    权限:超级管理员
    """
    serializer_class = OrgMembershipAdminSerializer
    permission_classes = (IsSuperUser,)
    queryset = User.objects.all()
    search_fields = ('email', 'name', 'username')

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve', 'update'):
            return UserSerializer
        return self.serializer_class

    def get_queryset(self):
        if not self.org:
            return None
        if self.request.query_params.get('type') == 'user':
            return self.org.get_org_users()
        elif self.request.query_params.get('type') == 'admin':
            return self.org.get_org_admins()
        else:
            return self.org.get_org_users() | self.org.get_org_admins()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class OrgProductAdminView(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """

    list:
    查看产品管理员列表

    create:
    新增产品管理员

    delete:

    """
    serializer_class = ProductRoleSerializer
    permission_classes = (IsOrgAdmin,)
    queryset = ProductRole.objects.all()

    def get_serializer_class(self):
        if self.action in ("list",):
            return ProductRoleReadSerializer
        return self.serializer_class

    def dispatch(self, request, *args, **kwargs):
        self.product = kwargs.get('product')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(product=self.product, role=ProductRole.ADMIN)
        return queryset

    def create(self, request, *args, **kwargs):
        self.product = kwargs.get('product')
        productrole = ProductRole(product=self.product, role=ProductRole.ADMIN, user_id=request.data.get("user"))
        productrole.save()
        return Response(self.serializer_class(instance=productrole).data, status=201)


class LogoDetailView(generics.RetrieveUpdateAPIView):
    """

    get:
    获取LOGO信息

    put:
    更新LOGO信息
    """

    queryset = Organization.objects.all()
    serializer_class = LogoSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsSuperUser,)

    def get(self, request, *args, **kwargs):
        # raise DevException(CheckMsg.VALIDATION_REQUIRED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
