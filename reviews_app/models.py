from django.db import models
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile

class ReviewModel(models.Model):
    """ Model-class to define review and containing fields. """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews_written')
    rating = models.IntegerField()
    description = models.TextField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['reviewer', 'business_user']