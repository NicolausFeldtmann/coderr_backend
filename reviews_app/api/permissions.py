from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from user_auth_app.models import UserProfile

""" Custompermission class to identify user type. """
class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == "customer"
        except UserProfile.DoesNotExist:
            return False

""" Custompermission class allowns all user GET reqauest. But onyl reviwe author PATCH or DELETE requests. """
class IsReviewAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.reviewer.user == request.user