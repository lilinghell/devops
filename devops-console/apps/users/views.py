# ~*~ coding: utf-8 ~*~
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_condition import Or
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from common import permissions
from common.checkmsg import CheckMsg
from common.exception import DevException
from common.mixin import IDInFilterMixin
from common.permissions import IsOrgAdmin
from common.utils import get_logger, get_request_ip
from orgs import serializers
from orgs.models import Organization
from orgs.serializers import OrgSerializer
from orgs.utils import set_current_org, current_org, set_to_root_org
from users.serializers import UserSerializer, UserLoginSerializer, UserProfileSerializer, ChangeUserPasswordSerializer, \
    UserProfilePasswordUpdateSerializer, UserCreateSerializer
from workitems.models import WorkItem
from workitems.serializers import WorkItemSerializer
from .models import User, LoginLog
from .utils import check_user_valid

logger = get_logger(__name__)


class UserAuthApi(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserLoginSerializer

    def post(self, request):
        auth_logout(request)
        ip = request.data.get("remote_addr", None)
        ip = ip or get_request_ip(request)
        user, msg = self.check_user_valid(request)

        if not user:
            username = request.data.get('username', '')
            exist = User.objects.filter(username=username).first()
            reason = LoginLog.REASON_PASSWORD if exist else LoginLog.REASON_NOT_EXIST
            data = {
                'username': username,
                'reason': reason,
                'status': False
            }
            self.write_login_log(request, data, ip)
            raise DevException(CheckMsg.VALIDATION_UNAMEORPASS_WRONG)
            # return Response({'msg': msg})

        if user.password_has_expired:
            data = {
                'username': user.username,
                'reason': LoginLog.REASON_PASSWORD_EXPIRED,
                'status': False
            }
            self.write_login_log(request, data, ip)
            msg = _("The user {} password has expired, please update.".format(
                user.username))
            logger.info(msg)
            raise DevException(CheckMsg.VALIDATION_UNAMEORPASS_WRONG)
            # return Response({'msg': msg}, status=401)
        # 登陆后设置机构信息
        org = None
        if user.is_superuser:
            request.session['oid'] = Organization.root().id.__str__()
            set_to_root_org()
        else:
            if user.is_org_admin:
                org = user.admin_orgs.first()
            else:
                org = user.user_orgs.first()

            request.session['oid'] = org.id
            set_current_org(org)

        auth_login(request, user)

        data = {
            'username': user.username,
            'reason': LoginLog.REASON_NOTHING,
            'status': True
        }

        self.write_login_log(request, data, ip)
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user).data,
                'org': serializers.OrgSerializer(org).data
            }
        )

    @staticmethod
    def check_user_valid(request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user, msg = check_user_valid(
            username=username, password=password
        )
        return user, msg

    @staticmethod
    def write_login_log(request, data, ip):
        login_type = request.data.get('login_type', '')
        tmp_data = {
            'ip': ip,
            'type': login_type,
        }
        data.update(tmp_data)
        # TODO 修改为异步
        LoginLog.objects.create(**data)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        context = {
            'title': _('Logout success'),
            'messages': _('Logout success, return login page'),
        }
        return Response(context)


class UserProfileView(RetrieveUpdateAPIView):
    """

    获取修改登陆用户信息
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserProfileUpdatePassword(UpdateAPIView):
    """

    用户修改密码
    """
    serializer_class = UserProfilePasswordUpdateSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = self.get_object()
        old_password = serializer.validated_data['old_password']
        if not user.check_password(old_password):
            return Response(status=status.HTTP_409_CONFLICT)
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']
        if new_password != confirm_password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.reset_password(new_password=new_password)
        auth_logout(self.request)


class UserChangePasswordApi(UpdateAPIView):
    """

    管理员重置密码
    """
    permission_classes = (IsOrgAdmin,)
    queryset = User.objects.all()
    serializer_class = ChangeUserPasswordSerializer

    def perform_update(self, serializer):
        user = self.get_object()
        user.password_raw = serializer.validated_data["password"]
        user.save()


class UserViewSet(IDInFilterMixin, ModelViewSet):
    filter_fields = ('username', 'email', 'name', 'id')
    search_fields = filter_fields
    queryset = User.objects.all().filter()
    serializer_class = UserCreateSerializer
    permission_classes = [Or(permissions.IsValidUserAndReadonly, permissions.IsOrgAdmin), ]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve', 'update'):
            return UserSerializer
        return self.serializer_class

    def get_queryset(self):
        if current_org:
            self.queryset = super(UserViewSet, self).get_queryset().filter(
                Q(orgs=current_org.id) | Q(admin_orgs=current_org.id))
            return self.queryset
        return None

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = (IsOrgAdmin,)
        return super().get_permissions()


class AssigneeWorkItemAPIView(ListAPIView):
    """

    查看用户被分配的工作项
    """
    serializer_class = WorkItemSerializer

    def get_queryset(self):
        user = self.request.user
        return user.user_workitems


class CreaterWorkItemAPIView(ListAPIView):
    """

        查看用户被分配的工作项
        """
    serializer_class = WorkItemSerializer

    def get_queryset(self):
        user = self.request.user
        return WorkItem.objects.filter(created_by=user)


class OwnerWorkItemAPIView(ListAPIView):
    """

    查看用户负责的工作项
    """
    serializer_class = WorkItemSerializer

    def get_queryset(self):
        user = self.request.user
        return WorkItem.objects.filter(owner=user)


class OrgAdminSetOrgView(UpdateAPIView):
    """

    put:
    企业管理员：更新企业信息
    """
    queryset = ''
    serializer_class = OrgSerializer
    permission_classes = (IsOrgAdmin,)

    # parser_classes = (FormParser, MultiPartParser)

    def get_object(self):
        return current_org


class WorkItemAPIView(ListAPIView):
    """

    查看用户被分配、用户负责的工作项
    """
    serializer_class = WorkItemSerializer

    def get_queryset(self):
        user = self.request.user
        assignee = WorkItem.objects.filter(assignee_users=user)
        owner = WorkItem.objects.filter(owner=user)
        return assignee.union(owner)
