from rest_framework import serializers
from django.contrib.auth.models import User
from reviews_app.models import ReviewModel
from user_auth_app.models import UserProfile

class ReviewSerializer(serializers.ModelSerializer):
    """ Conferts data to handle reives requests. """

    class Meta:
        model = ReviewModel
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "reviewer",
            "created_at",
            "updated_at"
        ]

    def validate(self, data):
        request = self.context.get("request")
        if request and request.method == "POST":
            user = request.user
            reviewer_profile = UserProfile.objects.get(user=user)
            business_user = data.get('business_user')

            if ReviewModel.objects.filter(reviewer=reviewer_profile, business_user=business_user).exists():
                raise serializers.ValidationError({"error": "Review already added."})
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        reviewer_profile = UserProfile.objects.get(user=user)
        return ReviewModel.objects.create(user=user, reviewer=reviewer_profile, **validated_data)

class UpdateSerializer(serializers.ModelSerializer):
    """ Converts data to handle PATCH requests for reviews. """

    class Meta:
        model = ReviewModel
        fields = ["rating", "description"]

        def update(self, instance, validated_data):
            instance.rating = validated_data.get('rating', instance.rating)
            instance.description = validated_data.get('description', instance.description)
            instance.save()
            return instance