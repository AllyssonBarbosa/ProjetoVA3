from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **extra_fields):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):

                user.custom_param = extra_fields.get('custom_param', None)
                return user
        except UserModel.DoesNotExist:
            return None
