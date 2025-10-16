from rest_framework import permissions

class IsDoctorUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Admin can update any doctor
        if request.user.is_staff:
            return True
        # Doctor can update only their own profile
        return obj.user == request.user
