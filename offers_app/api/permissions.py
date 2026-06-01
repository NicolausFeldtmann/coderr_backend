from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from user_auth_app.models import UserProfile

""" Custom permission class that grants admin or profile-user full authorization. """
class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        return obj.user == request.user or request.user.is_superuser

""" Custom permission class that garants admin or offer-user fullauthorization. """
class IsOfferAuthorOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            if not request.user or not request.user.is_authenticated:
                return False
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                return user_profile.role == 'business'
            except UserProfile.DoesNotExist:
                return False

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH']:
            return obj.user == request.user

        if request.method == "DELETE":
            return request.user.is_superuser or obj.user == request.user

        return False