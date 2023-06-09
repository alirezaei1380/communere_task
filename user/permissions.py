from rest_framework.permissions import BasePermission

from user.models import Developer, ProjectManager


class IsDeveloper(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.__class__ == Developer


class IsManager(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.__class__ == ProjectManager
