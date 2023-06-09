from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenViewBase

from user.models import Developer, ProjectManager
from user.serializers import DeveloperSerializer, ProjectManagerSerializer, DeveloperTokenObtainPairSerializer, \
    ProjectManagerTokenObtainPairSerializer


class DeveloperRegisterView(CreateModelMixin, GenericViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = DeveloperSerializer
    queryset = Developer.objects


class ProjectManagerRegisterView(CreateModelMixin, GenericViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ProjectManagerSerializer
    queryset = ProjectManager.objects


class DeveloperLogin(TokenViewBase):
    serializer_class = DeveloperTokenObtainPairSerializer


class ProjectManagerLogin(TokenViewBase):
    serializer_class = ProjectManagerTokenObtainPairSerializer
