from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

class IsCustomer(BasePermission):
    """ Custompermission class to detect user type. """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == "customer"

        except UserProfile.DoesNotExist:
            return False

class IsOrderOwner(BasePermission):
    """ Custompermission class to detect if user is order business-user. """

    def has_permission(self, request, view):
        """ Checks if user is authenticated. """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """ Handles permissions depending of user-role and request-type. """
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        return obj.business_user == request.user