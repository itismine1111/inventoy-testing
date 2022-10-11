from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class MyUserTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, MyUser, timestamp):
        return (
            six.text_type(MyUser.pk) + six.text_type(timestamp) +
            six.text_type(MyUser.email_confirmed)
        )

myuser_email_confirmation_token = MyUserTokenGenerator()