from rest_framework import permissions


class IsAuthenticatedStaff(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.profile.is_staff

    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False
        return request.user.profile.is_staff


class IsStaffWriteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        authenticated = bool(request.user and request.user.is_authenticated)
        if not authenticated:
            return False
        if not request.user.profile.is_staff:
            return False
        return True
