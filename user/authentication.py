from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
User = get_user_model()

class EmailAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None,**kwargs):
        roleBassedAuthentication = {'role_id__in': [1,2]} if kwargs['role_id'] == 1 else {'role_id': 3}
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs,**roleBassedAuthentication)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
