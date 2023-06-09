from django.urls import path

from task.views import DeveloperTaskView, ProjectView, ManagerTaskView

urlpatterns = [
    path('developer/', DeveloperTaskView.as_view({'post': 'create', 'get': 'list'})),
    path('project/', ProjectView.as_view({'post': 'create', 'get': 'list'})),
    path('manager/', ManagerTaskView.as_view({'post': 'create', 'get': 'list'})),
    path('manager/<int:pk>/', ManagerTaskView.as_view({'patch': 'partial_update'})),
]