from django.db import models
from reviews_app.models import ReviewModel

""" Defines base-model class and containing infromations. """
class BaseInfoModel(models.Model):
    review_count = models.IntegerField()
    average_rating = models.FloatField()
    business_profile_count = models.IntegerField()
    offer_count = models.IntegerField()