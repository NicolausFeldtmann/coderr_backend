from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from user_auth_app.models import UserProfile

class IsCustomer(BasePermission):
    """ Custompermission class to identify user type. """

    def has_permission(self, request, view):
        """ Grants permission if user-role is customer. """
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == "customer"
        except UserProfile.DoesNotExist:
            return False

class IsReviewAuthorOrReadOnly(BasePermission):
    """ Custompermission class allowns all user GET request. But only reviwe-author PATCH or DELETE requests. """

    def has_permission(self, request, view):
        """ Grants all authenticated and unauthenticated user GET request. """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """ Identifies review-author and grants PATCH and DELETE requests. """
        if request.method in SAFE_METHODS:
            return True

        return obj.reviewer.user == request.user