from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import Developer, ProjectManager


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    user_class = None

    def validate(self, attrs):
        try:
            user = self.user_class.authenticate(username=attrs['username'], password=attrs['password'])
        except self.user_class.DoesNotExist:
            raise ValidationError('username or password is incorrect')

        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_token(self, user):
        token = super().get_token(user)
        token['type'] = self.user_class.__name__
        return token


class DeveloperTokenObtainPairSerializer(UserTokenObtainPairSerializer):
    user_class = Developer


class ProjectManagerTokenObtainPairSerializer(UserTokenObtainPairSerializer):
    user_class = ProjectManager


class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = ('first_name', 'last_name', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ProjectManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectManager
        fields = ('first_name', 'last_name', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }
