from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import PasswordResetRequestView, PasswordResetConfirmView, UserCreateAPIView, UserListAPIView, \
    UserProfileAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("create/", UserCreateAPIView.as_view(), name="user_create"),
    path("list/", UserListAPIView.as_view(), name="user_list"),

    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=[AllowAny]),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=[AllowAny]),
        name="token_refresh",
    ),

    path("me/", UserProfileAPIView.as_view(), name="user_me"),

    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user-delete"),

    path(
        "reset_password/",
        PasswordResetRequestView.as_view(),
        name="reset_password"
    ),
    path(
        "reset_password_confirm/",
        PasswordResetConfirmView.as_view(),
        name="reset_password_confirm"
    ),
]
