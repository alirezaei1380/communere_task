from django.contrib import admin

from user.models import Developer, ProjectManager


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectManager)
class ProjectManagerAdmin(admin.ModelAdmin):
    pass
