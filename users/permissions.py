from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Разрешение, позволяющее пользователю редактировать только свой профиль.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user
