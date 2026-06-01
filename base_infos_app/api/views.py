from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.db.models import Avg

from reviews_app.models import ReviewModel
from offers_app.models import OfferModel
from user_auth_app.models import UserProfile

""" View to handle GET requests for base informations. """
class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    """ Calculates all needed numbers. """
    def get(self, request):
        review_count = ReviewModel.objects.count()
        average_rating = ReviewModel.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        business_profile_count = UserProfile.objects.filter(role='business').count()
        offer_count = OfferModel.objects.count()

        data = {
            'review_count': review_count,
            'average_rating': round(average_rating, 1) if average_rating else 0,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count
        }
        return Response(data, status=status.HTTP_200_OK)