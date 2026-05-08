from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ads.permissions import IsOwnerOrAdmin
from users.models import User
from users.serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UserSerializer,
)


class UserListAPIView(ListAPIView):
    """Получение списка пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserRetrieveAPIView(RetrieveAPIView):
    """Получение пользователя по ID."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class UserUpdateAPIView(UpdateAPIView):
    """Обновление пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class UserDestroyAPIView(DestroyAPIView):
    """Удаление пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    Просмотр и обновление собственного профиля.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Возвращает текущего пользователя."""
        return self.request.user


class PasswordResetRequestView(APIView):
    """Запрос восстановления пароля."""

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Отправляет ссылку восстановления пароля на email.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            url = settings.PASSWORD_RESET_CONFIRM_URL.format(uid=uid, token=token)

            send_mail(
                "Восстановление пароля",
                f"Ссылка: {url}",
                None,
                [user.email],
            )

        return Response(
            {"detail": "Инструкции отправлены на почту."}, status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    """Подтверждение восстановления пароля."""

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Проверяет токен и устанавливает новый пароль.
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Пароль изменен."}, status=status.HTTP_200_OK)

        return Response(
            {"error": "Неверный токен или ID."}, status=status.HTTP_400_BAD_REQUEST
        )
