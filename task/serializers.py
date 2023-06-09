from rest_framework import serializers

from task.models import Task, Project
from user.models import Developer


class AssigneeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = ('first_name', 'last_name', 'id')


class DeveloperTaskSerializer(serializers.ModelSerializer):
    assignees_details = AssigneeSerializer(source='assignees', many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('title', 'description', 'created_at', 'assignees', 'assignees_details', 'project', 'id')
        read_only_fields = ('created_at', 'assignees_details', 'id', 'assignees')


class ManagerTaskSerializer(serializers.ModelSerializer):
    assignees_details = AssigneeSerializer(source='assignees', many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('title', 'description', 'created_at', 'assignees', 'assignees_details', 'project', 'id')
        read_only_fields = ('created_at', 'assignees_details', 'id')


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('name', 'cost', 'manager', 'created_at', 'id')
        read_only_fields = ('manager', 'created_at', 'id')
