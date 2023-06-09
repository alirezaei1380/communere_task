from django.contrib import admin

from task.models import Task, Project


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
