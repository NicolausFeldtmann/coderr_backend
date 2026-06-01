from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, NumberFilter, CharFilter
from offers_app.models import OfferModel

class CustomOfferFilter(FilterSet):
    price = NumberFilter(field_name='details__price', lookup_expr='exact')
    price_min = NumberFilter(field_name='details__price', lookup_expr='gte')
    price_max = NumberFilter(field_name='details__price', lookup_expr='lte')
    min_price = NumberFilter(field_name='details__price', lookup_expr='gte')
    max_price = NumberFilter(field_name='details__price', lookup_expr='lte')
    max_delivery_time = NumberFilter(field_name='details__delivery_time', lookup_expr='exact')
    offer_type = CharFilter(field_name='details__offer_type', lookup_expr='icontains')

    class Meta:
        model = OfferModel
        fields = ['user', 'title', 'description', 'price', 'price_min', 'price_max', 'min_price', 'max_delivery_time', 'offer_type', 'user']