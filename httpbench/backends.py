from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UsernameBackend:
    def authenticate(self, request, username):
        if not username:
            return None
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            user = UserModel(username=username)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
