from rest_framework import viewsets
from rest_framework.response import Response

from common.checkmsg import CheckMsg
from common.exception import DevException
from common.utils import get_object_or_none
from designs.models import InterfaceDictionary, InterfaceGroup, Interfaces, InterfaceTest, EsbInterfaces
from applications.models import Application
from applications.serializers import ApplicationSerializer
from .serializers import DictionarySerializer, GroupSerializer, InterfaceSerializer, InterfaceReadSerializer, \
    InterfaceTestSerializer, GroupReadSerializer, EsbInterfaceSerializer, EsbInterfaceReadSerializer
from applications.models import Repository
from common.utils import git


class DictionaryView(viewsets.ModelViewSet):
    filter_fields = ('name', 'type', 'description')  # 查询条件
    serializer_class = DictionarySerializer
    # 指定关键字参数可以只查询(join)指定的对象，节省资源
    queryset = InterfaceDictionary.objects.all().filter()

    def create(self, request, *args, **kwargs):
        """

        重写创建字典方法，重复数据返回错误：数据已存在
        :return:
        """
        dictionary, msg = self.check_dictionary_valid(request)
        if dictionary:
            raise DevException(CheckMsg.DESIGNS_OBJECT_EXIST)
        else:
            response = super().create(request, *args, **kwargs)
            instance = response.data
            return Response(InterfaceDictionary(instance).data)

    @staticmethod
    def check_dictionary_valid(request):
        name = request.data.get('name', '')
        type = request.data.get('type', '')

        if name and type:
            dictionary = get_object_or_none(
                InterfaceDictionary, name=name, type=type)
        else:
            dictionary = None

        if dictionary is None:
            return None, "Dictionary not exist"

        return dictionary, "Dictionary exist"


class GroupView(viewsets.ModelViewSet):
    """
    分组组信息
    """

    queryset = InterfaceGroup.objects.select_related("application", "project")
    serializer_class = GroupSerializer

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve'):
            return GroupReadSerializer
        return self.serializer_class


class InterfaceView(viewsets.ModelViewSet):
    """
    接口信息
    """

    queryset = Interfaces.objects.select_related(
        "application", "group", "project")
    serializer_class = InterfaceSerializer

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve'):
            return InterfaceReadSerializer
        return self.serializer_class


class InterfaceTestView(viewsets.ModelViewSet):
    """
    接口测试
    """

    queryset = InterfaceTest.objects.all()
    serializer_class = InterfaceTestSerializer


class EsbInterfaceView(viewsets.ModelViewSet):
    """
    ESB接口
    """
    queryset = EsbInterfaces.objects.all()
    serializer_class = EsbInterfaceSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return EsbInterfaceReadSerializer
        return self.serializer_class


class InterfaceYamlView(viewsets.generics.RetrieveAPIView):
    """

    获取应用某个yaml接口文件信息
    """

    def get(self, request, *args, **kwargs):
        app_id = request.query_params.get('application_id')
        yaml_path = request.query_params.get('yaml_path')
        a = yaml_path.split("/", 1)
        if len(a) < 2:
            raise DevException(CheckMsg.VALIDATION_YAML_PATH_ERROR)
        repository = Repository.objects.get(application_id=app_id)
        yaml = ""
        if repository.scm_url != '':
            try:
                gl = git(repository.scm_url, repository.auth_token)
                project = gl[0].projects.get(gl[1])
                f = project.files.get(
                    file_path=a[1], ref=a[0])
                # decode获得bytes格式的内容
                content = f.decode()
                # 再次decode获得str
                yaml = content.decode()
            except:
                raise DevException(CheckMsg.VALIDATION_SCM_URL_ERROR)
        return Response(yaml)
