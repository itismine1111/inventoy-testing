from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import IntegrityError
from django.forms import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics

from knox.models import AuthToken
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from knox.views import LoginView as KnoxLoginView
from knox.settings import CONSTANTS

from .serializers import (
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    CreateUserSerializer,
    LoginUserSerializer,
    UserSerializer,
)
from .tokens import myuser_email_confirmation_token
from .helpers import generateOTP
from .models import LoginHistory, MyUser


class CreateUser(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:

            data = {}
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()

                """Sending email to user to verification"""
                mail_subject = "Confirm your email."
                message = render_to_string(
                    "email_confirmation_template.html",
                    {
                        "user": user,
                        "domain": get_current_site(request).domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": myuser_email_confirmation_token.make_token(user),
                    },
                )
                email_sent = send_email(user.email, mail_subject, message)

                data["user_verification_email_sent"] = email_sent

                """Sending email to all the admin users who can approve this user"""
                MyUser = get_user_model()
                admin_users = MyUser.objects.filter(is_admin=True)

                for admin_user in admin_users:
                    mail_subject_approve_user = (
                        "New user added. Click on the link to approve the user"
                    )
                    message_approve_user = render_to_string(
                        "email_approve_user_by_admin.html",
                        {
                            "admin_user": admin_user,
                            "user_id": user.id,
                            "user_email": user.email,
                            "user_name": f"{user.first_name} {user.last_name}",
                            "user_gender": user.gender,
                            "user_dob": user.dob,
                            "user_creation_date": user.created_on,
                            "domain": get_current_site(request).domain,
                        },
                    )
                    email_sent_approve_user = send_email(
                        admin_user.email,
                        mail_subject_approve_user,
                        message_approve_user,
                    )

                data["user_approval_by_admin_email_sent"] = email_sent_approve_user

                return Response(
                    {
                        "success": True,
                        "message": "Registered user successfully. Waiting for approval by admin",
                        "data": data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            else:
                error_list = serializer.errors.values()
                return Response(
                    {
                        "status": 400,
                        "data": serializer.errors,
                        "message": "Error occured while registering user",
                    }
                )

        # I don't know what this code is doing
        except IntegrityError as e:
            MyUser = get_user_model()
            user = MyUser.objects.get(username="")
            user.delete()
            raise ValidationError({"400": f"{str(e)}"})

        except KeyError as e:
            print(e)
            raise ValidationError({"400": f"Field {str(e)} missing"})


def send_email(to_email, mail_subject, message):

    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

    return True


def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        MyUser = get_user_model()
        user = MyUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and myuser_email_confirmation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        return HttpResponse("Email successfully confirmed")

    else:
        return HttpResponse("Email confirmation link expired")


@csrf_exempt
@api_view(["POST"])
@permission_classes(
    (
        IsAuthenticated,
        IsAdminUser,
    )
)
def activate_user_account_by_admin(request, pk):
    # id = request.data.get("id")
    MyUser = get_user_model()
    user = MyUser.objects.get(id=pk)

    if user is not None:
        if user.is_active:
            return Response(
                {
                    "success": False,
                    "message": f"User {user.username} account is already active",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        user.save()
        return Response(
            {
                "success": True,
                "message": f"User {user.first_name} account has been activated successfully",
                "data": {},
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {
            "success": False,
            "message": f"User account does not exist",
            "data": {},
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        email = request.data.get("email").lower()
        password = request.data.get("password")
        device_type = request.data.get("device_type")
        device_token = request.data.get("device_token")

        if email is None or password is None:
            return Response(
                {
                    "success": False,
                    "message": "Both email and password are required",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)

        if not user:
            return Response(
                {
                    "success": False,
                    "message": "Invalid username or password",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not user.is_active:
            return Response(
                {
                    "success": False,
                    "message": "Pending authentication by admin",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = AuthToken.objects.create(user)

        login_history_obj = LoginHistory.objects.create(
            user=user,
            auth_token_key=token[1][: CONSTANTS.TOKEN_KEY_LENGTH],
            signin_time=now(),
            is_signed_in=True,
            device_token=device_token,
            device_type=device_type,
        )
        login_history_obj.save()

        user_serializer = UserSerializer(user)

        return Response(
            {
                "success": True,
                "message": "Login Successful",
                "data": {"token": token[1], "user": user_serializer.data},
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    authentication_classes = (KnoxTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        token_key = request._auth.token_key
        # print(request._auth)
        login_history_obj = LoginHistory.objects.filter(
            auth_token_key=token_key
        ).update(signout_time=now(), is_signed_in=False)
        print(f"Login History: {login_history_obj}")
        # login_history_obj.update(signout_time = now(), is_signed_in = False)
        # login_history_obj.signout_time = now()
        # login_history_obj.is_signed_in = False
        # login_history_obj.save()

        request._auth.delete()

        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(None, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get("email").lower()
    try:
        MyUser = get_user_model()
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            user = None

        if user is not None:
            otp = generateOTP()
            user.forgot_password_otp = otp
            user.save()

            mail_subject = "Forgot Password"
            message = render_to_string(
                "forgot_password_otp_template.html",
                {
                    "user": user,
                    "otp": otp,
                },
            )
            email_sent = send_email(user.email, mail_subject, message)

            return Response(
                {
                    "success": True,
                    "message": "OTP sent successfully to the email",
                    "data": {"email_sent": email_sent},
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "success": False,
                "message": "Email does not exist",
                "data": {"email_sent": False},
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def confirm_otp_forgot_password(request):
    email = request.data.get("email", "").lower()
    otp = request.data.get("otp")
    device_type = request.data.get("device_type")
    device_token = request.data.get("device_token")

    try:
        MyUser = get_user_model()
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            user = None

        if user is not None:
            if user.forgot_password_otp == otp:
                token = AuthToken.objects.create(user)
                login(request, user)
                user.otp = ""
                user.save()

                login_history_obj = LoginHistory.objects.create(
                    user=user,
                    auth_token_key=token[1][: CONSTANTS.TOKEN_KEY_LENGTH],
                    signin_time=now(),
                    is_signed_in=True,
                    device_token=device_token,
                    device_type=device_type,
                )
                login_history_obj.save()

                return Response(
                    {
                        "success": True,
                        "message": "Otp confirmed. You can now change your password",
                        "data": {
                            "username": user.username,
                            "email": user.email,
                            "token": token[1],
                        },
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "Wrong OTP Entererd or it is already expired",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": False,
                "message": "Email does not exist",
                "data": {},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        print(e)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def reset_password(request):
    auth_obj = request._auth
    user = auth_obj.user
    serializer = ResetPasswordSerializer(data=request.data)

    data = {}
    if serializer.is_valid():
        user.set_password(request.data.get("password"))
        user.save()

        return Response(
            {
                "success": True,
                "message": "Password Changed Successfully",
                "data": {"id": user.id, "email": user.email},
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {
            "success": False,
            "message": "Password and Confirm Password do not match",
            "data": serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {
                        "success": False,
                        "message": "Old Password entered is wrong",
                        "data": {},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response(
                {
                    "success": True,
                    "message": "Password Chagned Successfully",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "success": False,
                "message": "Error occured while changing password",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class PartialUpdateUser(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        try:
            data = {}
            user_id = request.data.get("user_id")
            MyUser = get_user_model()
            user = MyUser.objects.filter(id=user_id)
            serializer = self.get_serializer(
                instance=user, data=request.data, partial=True
            )

            if serializer.is_valid():
                user = serializer.save()

        # I don't know what this code is doing
        except IntegrityError as e:
            MyUser = get_user_model()
            user = MyUser.objects.get(username="")
            user.delete()
            raise ValidationError({"400": f"{str(e)}"})

        except KeyError as e:
            print(e)
            raise ValidationError({"400": f"Field {str(e)} missing"})


class GetLoginUserDetails(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserSerializer(request.user)

        return Response(
            {
                "success": True,
                "message": "Login User Detils",
                "data": serializer.data,
            },
            status=200,
        )


# There is some error in this API
class GetAllUsers(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        cur_user = request.user
        if cur_user.is_admin == False:
            return Response(
                {
                    "success": False,
                    "message": "You don't have permission to access this end point",
                    "data": {},
                },
                status=400,
            )

        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(
            {
                "success": True,
                "message": "Login User Detils",
                "data": {"count": len(serializer.data), "list": serializer.data},
            },
            status=200,
        )


class GetUserDetails(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        # Users should be authenticated
        if not (request.user and request.user.is_authenticated):
            return Response(
                {
                    "success": False,
                    "message": "Authentication failed",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        cur_user = request.user
        if cur_user.is_admin == False:
            return Response(
                {
                    "success": False,
                    "message": "You don't have permission to access this end point",
                    "data": {},
                },
                status=400,
            )

        try:
            user = MyUser.objects.get(id=pk)
        except MyUser.DoesNotExist:
            user = None

        if not user:
            return Response(
                {
                    "success": False,
                    "message": "User does not exist",
                    "data": {},
                },
                status=400,
            )

        serializer = UserSerializer(user)

        return Response(
            {
                "success": True,
                "message": "User details",
                "data": serializer.data,
            },
            status=200,
        )
