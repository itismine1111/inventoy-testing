from django.urls import URLPattern, path
from knox import views as knox_views

from .views import (
    CreateUser,
    LoginView,
    LogoutView,
    confirm_email,
    forgot_password,
    confirm_otp_forgot_password,
    ChangePasswordView,
    reset_password,
    activate_user_account_by_admin,
    PartialUpdateUser,
    GetUserDetails,
    GetAllUsers,
    GetLoginUserDetails,
)

app_name = "app_account"

urlpatterns = [
    path("register/", CreateUser.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    # path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "activate-user-account_by_admin/<int:pk>/",
        activate_user_account_by_admin,
        name="activate-user-account_by_admin",
    ),
    path(
        "confirm-email/<str:uidb64>/<str:token>/", confirm_email, name="confirm-email"
    ),
    path("forgot-password/", forgot_password, name="forgot-password"),
    path(
        "confirm-otp-forgot-password/",
        confirm_otp_forgot_password,
        name="confirm-otp-forgot-password",
    ),
    path("reset-password/", reset_password, name="reset-password"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("update/", PartialUpdateUser.as_view(), name="update"),
    path("get-login-user-details/", GetLoginUserDetails.as_view(), name ="get-login-user-details"),
    path("get-all-users/", GetAllUsers.as_view(), name ="get-all-users"),
    path("get-user-details/<int:pk>/", GetUserDetails.as_view(), name ="get-user-details"),

]
