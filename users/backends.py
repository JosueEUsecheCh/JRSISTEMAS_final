from django.contrib.auth.backends import BaseBackend
from .models import User_register

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User_register.objects.get(email=username)
            if user.check_password(password):  # Usa el método check_password del modelo
                return user
        except User_register.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User_register.objects.get(pk=user_id)
        except User_register.DoesNotExist:
            return None
