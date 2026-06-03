from django.db import models
from reviews_app.models import ReviewModel

class BaseInfoModel(models.Model):
    """ Defines base-model class and containing infromations. """
    review_count = models.IntegerField()
    average_rating = models.FloatField()
    business_profile_count = models.IntegerField()
    offer_count = models.IntegerField()