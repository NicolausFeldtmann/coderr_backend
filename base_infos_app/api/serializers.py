from rest_framework import serializers

""" Convert needed data for base info requests. """
class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    business_profile_count = serializers.IntegerField(read_only=True)
    offer_count = serializers.IntegerField(read_only=True)