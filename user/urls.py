from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import DeveloperRegisterView, ProjectManagerRegisterView, DeveloperLogin, ProjectManagerLogin

urlpatterns = [
    path('developer/login/', DeveloperLogin.as_view(), name='developer_login'),
    path('developer/register/', DeveloperRegisterView.as_view({'post': 'create'}), name='developer_register'),
    path('manager/login/', ProjectManagerLogin.as_view(), name='manager_login'),
    path('manager/register/', ProjectManagerRegisterView.as_view({'post': 'create'}), name='manager_register'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
]
