from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=63, unique=True)
    password = models.CharField(max_length=63)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.password = make_password(self.password, 'Salt')
        return super(User, self).save(force_insert, force_update, using, update_fields)

    @classmethod
    def authenticate(cls, username, password):
        return cls.objects.get(username=username, password=make_password(password, 'Salt'))

    class Meta:
        abstract = True


class Developer(User):
    pass


class ProjectManager(User):
    pass
