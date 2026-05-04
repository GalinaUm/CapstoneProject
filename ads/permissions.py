from rest_framework import permissions
from rest_framework.generics import ListAPIView


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    1. Аноним: Только чтение (если разрешено во View).
    2. Владелец: Полный доступ к своему объекту.
    3. Админ: Полный доступ ко всему.
    """

    def has_object_permission(self, request, view, obj):
        is_admin = request.user.is_authenticated and request.user.role == 'admin'

        if is_admin:
            return True

        if obj == request.user:
            return True

        return hasattr(obj, 'author') and obj.author == request.user

    def has_permission(self, request, view):
        action = getattr(view, "action", None)

        if action == 'list' or isinstance(view, ListAPIView):
            return request.user.is_authenticated and request.user.role == 'admin'
        return request.user.is_authenticated
