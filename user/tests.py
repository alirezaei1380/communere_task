from django.test import TestCase
from rest_framework.test import APIRequestFactory

from user.models import Developer, ProjectManager
from user.views import DeveloperRegisterView, ProjectManagerRegisterView, DeveloperLogin, ProjectManagerLogin


class UserTestCase(TestCase):

    def setUp(self):
        Developer.objects.create(first_name='test', last_name='test', username='test3', password='test')
        ProjectManager.objects.create(first_name='test', last_name='test', username='test4', password='test')

    def test_developer_sign_up(self):
        factory = APIRequestFactory()
        request = factory.post('/api/v1/developer/register/', data={
            'first_name': 'test',
            'last_name': 'test',
            'username': 'test1',
            'password': 'test',
        })
        view = DeveloperRegisterView.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code, 201
        assert Developer.objects.filter(username='test1').exists(), True

    def test_developer_sign_up_invalid_username(self):
        factory = APIRequestFactory()
        request = factory.post('/api/v1/developer/register/', data={
            'first_name': 'test',
            'last_name': 'test',
            'username': 'test3',
            'password': 'test',
        })
        view = DeveloperRegisterView.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code, 400

    def test_developer_sign_up_invalid_data(self):
        factory = APIRequestFactory()
        request = factory.post('/api/v1/developer/register/', data={
            'last_name': 'test',
            'username': 'test1',
            'password': 'test',
        })
        view = DeveloperRegisterView.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code, 400

    def test_manager_sign_up(self):
        factory = APIRequestFactory()
        request = factory.post('/api/v1/manager/register/', data={
            'first_name': 'test',
            'last_name': 'test',
            'username': 'test2',
            'password': 'test',
        })
        view = ProjectManagerRegisterView.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code, 201
        assert ProjectManager.objects.filter(username='test2').exists(), True

    def test_developer_login(self):
        factory = APIRequestFactory()
        request = factory.post('/api/v1/developer/login/', data={
            'username': 'test3',
            'password': 'test',
        })
        view = DeveloperLogin.as_view()
        response = view(request)
        data = response.data
        assert response.status_code, 200
        assert 'refresh' in data, True
        assert 'access' in data, True

    def test_manager_login(self):
        factory = APIRequestFactory()
        request = factory.post('/api/v1/manager/login/', data={
            'username': 'test4',
            'password': 'test',
        })
        view = ProjectManagerLogin.as_view()
        response = view(request)
        data = response.data
        assert response.status_code, 200
        assert 'refresh' in data, True
        assert 'access' in data, True
