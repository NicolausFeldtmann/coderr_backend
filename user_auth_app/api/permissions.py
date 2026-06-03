from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """ Custom permission class that grants admin or profile-user full authorization. """

    def has_object_permission(slef, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "DELETE":
            return request.user == obj.user or request.user.is_superuser

        if request.method in ["PATCH", "PUT"]:
            return request.user == obj.user

        return False