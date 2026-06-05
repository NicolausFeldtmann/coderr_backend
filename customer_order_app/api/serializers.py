from rest_framework import serializers,status
from customer_order_app.models import OrderModel
from offers_app.models import OfferDetails
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from reviews_app.models import ReviewModel

class OrderSerializer(serializers.ModelSerializer):
    """ Validated data needed for POST or GET order requests """

    class Meta:
        model = OrderModel
        fields = '__all__'
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at"
        ]

    def get_business_user(self, obj):
        return obj.business_user.id

class CreateOrderSerializer(serializers.Serializer):
    """ Converts needed data to handle POST request. """
    offer_detail_id = serializers.IntegerField()

    def create(self, validated_data):
        """ Function to validate offer_detail and create order if offer_detail is valid. """

        offer_detail_id = validated_data.pop("offer_detail_id")
        user = self.context["request"].user
        offer_detail = get_object_or_404(OfferDetails, id=offer_detail_id)
        order = OrderModel.objects.create(
            offer_detail=offer_detail,
            customer_user=user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='pending'
        )
        return order

class UpdateSerializer(serializers.ModelSerializer):
    """ Converts needed data to handle PATCH order requests. """

    class Meta:
        model = OrderModel
        fields = ["status"]

    def update(self, instance, validated_data):
        """ Handels order update via PATCH request. """
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance