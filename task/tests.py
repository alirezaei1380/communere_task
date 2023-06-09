from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from task.models import Project, Task
from task.views import DeveloperTaskView, ProjectView, ManagerTaskView
from user.models import ProjectManager, Developer


class DeveloperTaskTestCase(TestCase):

    def setUp(self):
        self.manager = ProjectManager.objects.create(first_name='test', last_name='test', username='test1', password='test')
        self.developer = Developer.objects.create(first_name='test', last_name='test', username='test1', password='test')
        self.developer2 = Developer.objects.create(first_name='test', last_name='test', username='test2', password='test')
        self.project = Project.objects.create(name='test', cost=1000, manager=self.manager)

    def test_developer_create_task_fail(self):
        factory = APIRequestFactory()
        request = factory.post('/api/v1/task/developer/', data={
            'title': 'test1',
            'description': 'test',
            'project': self.project.id
        })
        force_authenticate(request, user=self.developer)
        view = DeveloperTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        assert response.status_code, 400

    def test_developer_create_task(self):
        factory = APIRequestFactory()
        task = Task.objects.create(title='test1', description='test', project=self.project)
        task.assignees.set((self.developer,))
        request = factory.post('/api/v1/task/developer/', data={
            'title': 'test2',
            'description': 'test',
            'project': self.project.id
        })
        force_authenticate(request, user=self.developer)
        view = DeveloperTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        assert response.status_code, 201
        assert Task.objects.filter(assignees=self.developer, project=self.project, title='test2').exists(), True

    def test_developer_get_tasks(self):
        factory = APIRequestFactory()
        task1 = Task.objects.create(title='test1', description='test', project=self.project)
        task2 = Task.objects.create(title='test2', description='test', project=self.project)
        task1.assignees.set((self.developer,))
        task2.assignees.set((self.developer2,))
        request = factory.get(f'/api/v1/task/developer/?project_id={self.project.id}')
        force_authenticate(request, user=self.developer)
        view = DeveloperTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        data = response.data
        assert response.status_code, 200
        assert len(data), 2

    def test_developer_get_my_tasks(self):
        factory = APIRequestFactory()
        task1 = Task.objects.create(title='test1', description='test', project=self.project)
        task2 = Task.objects.create(title='test2', description='test', project=self.project)
        task1.assignees.set((self.developer,))
        task2.assignees.set((self.developer2,))
        request = factory.get(f'/api/v1/task/developer/?project_id={self.project.id}&my_tasks=True')
        force_authenticate(request, user=self.developer)
        view = DeveloperTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        data = response.data
        assert response.status_code, 200
        assert len(data), 1

    def test_developer_get_tasks_without_project(self):
        factory = APIRequestFactory()
        task1 = Task.objects.create(title='test1', description='test', project=self.project)
        task2 = Task.objects.create(title='test2', description='test', project=self.project)
        task1.assignees.set((self.developer,))
        task2.assignees.set((self.developer2,))
        request = factory.get(f'/api/v1/task/developer/')
        force_authenticate(request, user=self.developer)
        view = DeveloperTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        assert response.status_code, 400

    def test_developer_get_tasks_unauthenticated(self):
        factory = APIRequestFactory()
        task1 = Task.objects.create(title='test1', description='test', project=self.project)
        task2 = Task.objects.create(title='test2', description='test', project=self.project)
        task1.assignees.set((self.developer,))
        task2.assignees.set((self.developer2,))
        request = factory.get(f'/api/v1/task/developer/?project_id={self.project.id+1}')
        view = DeveloperTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        assert response.status_code, 401

    def test_developer_get_tasks_unautherized(self):
        factory = APIRequestFactory()
        task1 = Task.objects.create(title='test1', description='test', project=self.project)
        task2 = Task.objects.create(title='test2', description='test', project=self.project)
        task1.assignees.set((self.developer,))
        task2.assignees.set((self.developer2,))
        request = factory.get(f'/api/v1/task/developer/?project_id={self.project.id+1}')
        force_authenticate(request, user=self.manager)
        view = DeveloperTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        assert response.status_code, 403


class ProjectTestCase(TestCase):

    def setUp(self):
        self.manager = ProjectManager.objects.create(first_name='test', last_name='test', username='test1', password='test')
        self.manager2 = ProjectManager.objects.create(first_name='test', last_name='test', username='test2', password='test')

    def test_create_project(self):
        factory = APIRequestFactory()
        request = factory.post(f'/api/v1/task/project/', data={
            'name': 'test1',
            'cost': 1000,
        })
        force_authenticate(request, user=self.manager)
        view = ProjectView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        assert response.status_code, 201
        assert Project.objects.filter(manager=self.manager, name='test1').exists(), True

    def test_get_projects(self):
        Project.objects.create(name='test1', cost=1000, manager=self.manager)
        Project.objects.create(name='test2', cost=1000, manager=self.manager2)
        factory = APIRequestFactory()
        request = factory.get(f'/api/v1/task/project/')
        force_authenticate(request, user=self.manager)
        view = ProjectView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        data = response.data
        assert response.status_code, 200
        assert len(response.data), 2

    def test_get_my_projects(self):
        Project.objects.create(name='test1', cost=1000, manager=self.manager)
        Project.objects.create(name='test2', cost=1000, manager=self.manager2)
        factory = APIRequestFactory()
        request = factory.get(f'/api/v1/task/project/?my_projects=True')
        force_authenticate(request, user=self.manager)
        view = ProjectView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        data = response.data
        assert response.status_code, 200
        assert len(response.data), 1


class ManagerTaskTestCase(TestCase):

    def setUp(self):
        self.manager = ProjectManager.objects.create(first_name='test', last_name='test', username='test1', password='test')
        self.developer = Developer.objects.create(first_name='test', last_name='test', username='test1', password='test')
        self.project = Project.objects.create(name='test1', cost=1000, manager=self.manager)

    def test_create_task(self):
        factory = APIRequestFactory()
        request = factory.post(f'/api/v1/task/manager/', data={
            'title': 'test1',
            'description': 'test',
            'project': self.project.id,
            'assignees': [self.developer.id,]
        })
        force_authenticate(request, user=self.manager)
        view = ManagerTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        assert response.status_code, 201
        assert Task.objects.filter(assignees=self.developer, project=self.project, title='test1').exists(), True

    def test_create_task_fail(self):
        factory = APIRequestFactory()
        new_manager = ProjectManager.objects.create(first_name='test', last_name='test', username='test2', password='test')
        new_project = Project.objects.create(name='test2', cost=1000, manager=new_manager)
        request = factory.post(f'/api/v1/task/manager/', data={
            'title': 'test1',
            'description': 'test',
            'project': new_project.id,
            'assignees': [self.developer.id,]
        })
        force_authenticate(request, user=self.manager)
        view = ManagerTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        assert response.status_code, 400

    def test_get_tasks(self):
        factory = APIRequestFactory()
        task = Task.objects.create(project=self.project, title='test1', description='test')
        task.assignees.set((self.developer,))
        request = factory.get(f'/api/v1/task/manager/')
        force_authenticate(request, user=self.manager)
        view = ManagerTaskView.as_view({'post': 'create', 'get': 'list'})
        response = view(request)
        data = response.data
        assert response.status_code, 200
        assert len(data), 1

    def test_update_task(self):
        factory = APIRequestFactory()
        task = Task.objects.create(project=self.project, title='test1', description='test')
        task.assignees.set((self.developer,))
        new_developer = Developer.objects.create(first_name='test', last_name='test', username='test2', password='test')
        request = factory.patch(f'/api/v1/task/manager/', data={
            'assignees': [new_developer.id,]
        })
        force_authenticate(request, user=self.manager)
        view = ManagerTaskView.as_view({'patch': 'partial_update'})
        response = view(request, pk=task.id)
        assert response.status_code, 200
        assert Task.objects.filter(assignees=new_developer, project=self.project, title='test1').exists(), True

    def test_update_task_fail(self):
        factory = APIRequestFactory()
        new_manager = ProjectManager.objects.create(first_name='test', last_name='test', username='test2', password='test')
        new_project = Project.objects.create(name='test2', cost=1000, manager=new_manager)
        task = Task.objects.create(project=new_project, title='test1', description='test')
        task.assignees.set((self.developer,))
        new_developer = Developer.objects.create(first_name='test', last_name='test', username='test2', password='test')
        request = factory.patch(f'/api/v1/task/manager/', data={
            'assignees': [new_developer.id,]
        })
        force_authenticate(request, user=self.manager)
        view = ManagerTaskView.as_view({'patch': 'partial_update'})
        response = view(request, pk=task.id)
        assert response.status_code, 400
