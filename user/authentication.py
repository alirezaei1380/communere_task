from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from user.models import Developer, ProjectManager


class UserAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        if 'type' not in validated_token or 'user_id' not in validated_token:
            raise InvalidToken("Token contained no recognizable user identification")

        class_type = validated_token['type']
        user_id = validated_token['user_id']
        user_class = Developer if class_type == 'Developer' else ProjectManager

        try:
            return user_class.objects.get(id=user_id)
        except user_class.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")
