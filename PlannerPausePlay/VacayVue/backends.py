from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(email, password)
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            print("User with email '{}' does not exist.".format(email))
            return None
        else:
            if user.check_password(password):
                print("User '{}' authenticated successfully.".format(email))
                return user
            else:
                print("Authentication failed for user '{}'.".format(email))
        return None