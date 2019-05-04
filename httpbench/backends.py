from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UsernameBackend:
    def authenticate(self, request, username):
        if not username:
            return None
        try:
            return UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
