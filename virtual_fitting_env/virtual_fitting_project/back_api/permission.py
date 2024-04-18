from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to edit objects.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow POST requests for authenticated users
        elif request.method == 'POST' and request.user.is_authenticated:
            return True
        # Allow PUT, PATCH, DELETE requests for admin users only
        return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, or OPTIONS requests for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow POST requests for authenticated users
        elif request.method == 'POST' and request.user.is_authenticated:
            return True
        # Allow PUT, PATCH, DELETE requests for the owner of the object
        return obj.user == request.user
