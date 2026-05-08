from rest_framework import permissions
from rest_framework.generics import ListAPIView


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission-класс для проверки владельца объекта или администратора.

    Доступ:
    - admin: полный доступ
    - owner: доступ только к своим объектам
    - anonymous: только чтение, если разрешено view
    """

    def has_object_permission(self, request, view, obj):
        """Проверка объектных прав доступа."""

        is_admin = request.user.is_authenticated and request.user.role == "admin"

        if is_admin:
            return True

        if obj == request.user:
            return True

        return hasattr(obj, "author") and obj.author == request.user

    def has_permission(self, request, view):
        """Проверка общих прав доступа."""

        action = getattr(view, "action", None)

        if action == "list" or isinstance(view, ListAPIView):
            return request.user.is_authenticated and request.user.role == "admin"
        return request.user.is_authenticated
