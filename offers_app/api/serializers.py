from rest_framework import serializers
from django.contrib.auth.models import User
from offers_app.models import OfferModel, OfferDetails
from django.urls import reverse

class UserDetailsSerializer(serializers.ModelSerializer):
    """ Serializers for user details. """
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class DetailsListSerializer(serializers.ModelSerializer):
    """ Converts data needed to list all offer details. """

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetails
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/api/offerdetails/{obj.id}/"

class DetailSerializer(serializers.ModelSerializer):
    """ Converts data needed to list all fields of specific offer detail. """

    delivery_time_in_days = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = OfferDetails
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type"
        ]
        read_only_fields = ["id"]
        extra_kwargs = {'offer_type': {'required': True}}

    def validate(self, attrs):
        """ Konverts an validates data to delivery_time. """
        if "delivery_time_in_days" in attrs:
            attrs["delivery_time"] = attrs.pop("delivery_time_in_days")
        return attrs

    def to_representation(self, instance):
        """ Konverts data to delivery_time_in_days for representation. """
        from collections import OrderedDict
        return OrderedDict([
            ('id', instance.id),
            ('title', instance.title),
            ('revisions', instance.revisions),
            ('delivery_time_in_days', instance.delivery_time),
            ('price', instance.price),
            ('features', instance.features),
            ('offer_type', instance.offer_type)
        ])

class OfferListSerializer(serializers.ModelSerializer):
    """ Converts data needed for offer list requests. """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = OfferModel
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_details(self, obj):
        """ Filtering of OfferDetails without seperate endpoints """
        details_qs = obj.details.all()
        request = self.context.get('request')
        return DetailsListSerializer(details_qs, many=True).data

    def get_user_details(self, obj):
        """ Return all user-data. """
        user_serializer = UserDetailsSerializer(obj.user, read_only=True)
        return user_serializer.data

    def get_min_price(self, obj):
        """ Returns lowes price in OfferDetails. """
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """ Returns lowes delivery_time in OfferDetails. """
        times = obj.details.values_list('delivery_time', flat=True)
        return min(times) if times else None

class OfferSerializer(serializers.ModelSerializer):
    """ Main offer serializer to create and update. """

    details = DetailSerializer(many=True, required=False)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = OfferModel
        fields = ["id", "title", "image", "description", "details"]

    def validate_details(self, value):
        """ Validates data for POST or PATCH purposes. """

        if self.instance is None and not value:
            raise serializers.ValidationError({"error": "Details required"})

        for detail in value:
            if not detail.get("offer_type") or detail.get("offer_type").strip() == "":
                raise serializers.ValidationError({"error": "Offer-type is required"})
        return value

    def update(self, instance, validated_data):
        """ Updates given offer_fields. """

        details_data = validated_data.pop("details", None)

        for field in ("title", "description", "image"):
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

        if details_data:
            existing_by_type = {detail.offer_type: detail for detail in instance.details.all()}
            for detail_data in details_data:
                if (detail := existing_by_type.get(detail_data.get("offer_type"))):
                    for attr, value in detail_data.items():
                        setattr(detail, attr, value)
                    detail.save()
        return instance

class OfferRetriveSerializer(serializers.ModelSerializer):
    """ OfferSerializer to handle GET request. """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = DetailsListSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = OfferModel
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time"
        ]

    def get_min_price(self, obj):
        """ Returns lowest price in offer_detail """

        prices = obj.details.values_list("price", flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        """ Returns lowes delivery_time in offer_details. """

        times = obj.details.values_list("delivery_time", flat=True)
        return min(times) if times else None