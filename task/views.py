from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from task.models import Task, Project
from task.serializers import DeveloperTaskSerializer, ManagerTaskSerializer, ProjectSerializer
from user.authentication import UserAuthentication
from user.permissions import IsDeveloper, IsManager


class DeveloperTaskView(CreateModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (IsDeveloper,)
    serializer_class = DeveloperTaskSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        if not Task.objects.filter(assignees=self.request.user, project=data['project']).exists():
            raise ValidationError('developer doesn\'t have access to this project')
        serializer.save(assignees=(self.request.user,))

    def get_queryset(self):
        params = self.request.GET
        project_id = params.get('project_id')
        if not project_id:
            raise ValidationError('project_id is not provided')

        my_tasks = params.get('my_tasks')

        queryset = Task.objects.filter(project_id=project_id)
        if my_tasks:
            queryset = queryset.filter(assignees=self.request.user)
        return queryset


class ProjectView(CreateModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (IsManager,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        my_projects = self.request.GET.get('my_projects')

        queryset = Project.objects.all()
        if my_projects:
            queryset = queryset.filter(manager=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


class ManagerTaskView(CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    authentication_classes = (UserAuthentication,)
    permission_classes = (IsManager,)
    serializer_class = ManagerTaskSerializer

    def get_object(self):
        obj = super(ManagerTaskView, self).get_object()
        if obj.project.manager != self.request.user:
            raise ValidationError('project is not yours')
        return obj

    def get_queryset(self):
        if self.request.method != 'GET':
            return Task.objects.filter(project__manager=self.request.user)

        project_id = self.request.GET.get('project_id')
        if not project_id:
            raise ValidationError('project_id is not provided')

        project = Project.objects.filter(id=project_id).first()
        if not project or project.manager != self.request.user:
            raise ValidationError('project is not yours')

        return Task.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        if serializer.validated_data['project'].manager != self.request.user:
            raise ValidationError('project is not yours')
        super(ManagerTaskView, self).perform_create(serializer)
