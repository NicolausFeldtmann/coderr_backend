from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, NumberFilter, CharFilter, OrderingFilter
from offers_app.models import OfferModel

class CustomOfferFilter(FilterSet):
    min_price = NumberFilter(field_name='details__price', lookup_expr='gte')
    max_price = NumberFilter(field_name='details__price', lookup_expr='lte')
    max_delivery_time = NumberFilter(field_name='details__delivery_time', lookup_expr='lte')
    creator_id = NumberFilter(field_name='user__id', lookup_expr='exact')
    ordering = OrderingFilter(
        fields=(
            ('updated_at', 'updated_at'),
            ('details__price', 'min_price'),
        ),
        label='Sortierung'
    )

    class Meta:
        model = OfferModel
        fields = ['created_at', 'min_price', 'max_price', 'max_delivery_time']