from django.contrib.auth import backends


class CustomModelBackend(backends.ModelBackend):
    # It authenticates the inactive users also
    def user_can_authenticate(self, user):
        return True
