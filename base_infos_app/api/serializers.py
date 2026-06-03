from rest_framework import serializers

class BaseInfoSerializer(serializers.Serializer):
    """ Convert needed data for base info requests. """
    review_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    business_profile_count = serializers.IntegerField(read_only=True)
    offer_count = serializers.IntegerField(read_only=True)