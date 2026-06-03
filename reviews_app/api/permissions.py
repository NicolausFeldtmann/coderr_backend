from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from user_auth_app.models import UserProfile

class IsCustomer(BasePermission):
    """ Custompermission class to identify user type. """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == "customer"
        except UserProfile.DoesNotExist:
            return False

class IsReviewAuthorOrReadOnly(BasePermission):
    """ Custompermission class allowns all user GET reqauest. But onyl reviwe author PATCH or DELETE requests. """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.reviewer.user == request.user