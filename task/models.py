from django.db import models

from user.models import ProjectManager, Developer


class Project(models.Model):
    name = models.CharField(max_length=127)
    cost = models.PositiveIntegerField()
    manager = models.ForeignKey(ProjectManager, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignees = models.ManyToManyField(Developer, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
