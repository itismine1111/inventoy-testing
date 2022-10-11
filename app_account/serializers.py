import base64
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from drf_extra_fields.fields import HybridImageField
from django.core.files import File


class CustomBase64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if "data:" in data and ";base64," in data:
                header, data = data.split(";base64,")

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (
                file_name,
                file_extension,
            )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(CustomBase64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class CreateUserSerializer(serializers.ModelSerializer):
    profile_picture = HybridImageField(required=False)  # From DRF Extra Fields
    # profile_picture = CustomBase64ImageField(required=False, max_length=None, use_url=True)

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "gender",
            "dob",
            "profile_picture",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        MyUser = get_user_model()
        password = validated_data.pop("password")
        profile_picture = validated_data.pop(
            "profile_picture"
        )  # returns a SimpleUploadedFile obj
        user = MyUser.objects.create(**validated_data)

        if profile_picture is not None:
            user.profile_picture = profile_picture

        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        print(instance.email)
        user = instance.partial_update(**validated_data, email=instance.email)
        return user

    def validate(self, data):
        errors = []

        MyUser = get_user_model()
        instance = MyUser(**data)
        try:
            instance.clean()
        except Exception as e:
            print(e)
            raise errors.append(e.args[0])

        # E-Mail Validations
        data["email"] = data["email"].lower()
        email = data["email"]
        if email is not None:
            # check if any users already exists with this email
            try:
                match = MyUser.objects.get(email=email)
            except MyUser.DoesNotExist:
                pass
            else:
                errors.append({"email": "This email is already is in use"})

        if errors:
            raise serializers.ValidationError(errors)

        return data


class UserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "phone_number_confirmed",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "dob",
            "is_active",
            "is_admin",
            "is_superuser",
            "profile_picture_url",
        )

    def get_image_url(self, obj):
        try:
            MyUser = get_user_model()
            user_obj = MyUser.objects.get(id=obj.id)
            # print(image_obj)
        except MyUser.DoesNotExist:
            return ""

        return user_obj.profile_picture.url


class LoginUserSerializer(serializers.Serializer):
    errors = []
    email = serializers.CharField()
    password = serializers.CharField()
    device_type = serializers.CharField()
    device_token = serializers.CharField()

    def validate(self, data):
        errors = []
        email = data["email"]
        password = data["password"]
        device_type = data["device_type"]
        device_token = data["device_token"]

        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials Passed.")


class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    # model = get_user_model()

    """
    Serializer for password change endpoint.
    """
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        errors = []

        # checking both password and confirm_password are same
        password = data["password"]
        confirm_password = data["confirm_password"]

        if password != confirm_password:
            errors.append({"password": "Password and Confirm Password do not match "})

        if errors:
            raise serializers.ValidationError(errors)

        return data
