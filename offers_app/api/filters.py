from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, NumberFilter, CharFilter, OrderingFilter
from offers_app.models import OfferModel
from django.db.models import Min, Max
class CustomOfferFilter(FilterSet):
    """ Custom filter class. Allows filtering of offers based specific params. """

    min_price = NumberFilter(field_name='details__price', lookup_expr='gte', method='filter_min_price')
    max_price = NumberFilter(field_name='details__price', lookup_expr='lte', method='filter_max_price')
    max_delivery_time = NumberFilter(field_name='details__delivery_time', lookup_expr='lte')
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

    def filter_min_price(self, queryset, name, value):
        """ Filters offers containing min_price in offer-detail biger or equal given value """
        if value is None:
            return queryset
        return queryset.annotate(
            min_detail_price=Min('details__price')
        ).filter(min_detail_price__gte=value).distinct()

    def filter_max_price(self, queryset, name, value):
        """ Filters offers containing min_price in offer-detail lower or equal given value. """
        if value is None:
            return queryset
        return queryset.exclude(
            details__price__gt=value
        ).distinct()