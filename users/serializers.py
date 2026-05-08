from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя."""

    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "phone",
            "image",
            "role",
            "first_name",
            "last_name",
        )
        read_only_fields = ("role",)

    def create(self, validated_data):
        """Создает пользователя с хешированием пароля."""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Обновляет пользователя и корректно изменяет пароль."""
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class PasswordResetRequestSerializer(serializers.Serializer):
    """Сериализатор запроса восстановления пароля."""

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Сериализатор подтверждения восстановления пароля."""

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
