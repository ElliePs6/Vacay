from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            print("User with email '{}' does not exist.".format(username))
            return None
        else:
            if user.check_password(password):
                print("User '{}' authenticated successfully.".format(username))
                return user
            else:
                print("Authentication failed for user '{}'.".format(username))
        return None
