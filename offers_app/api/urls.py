from django.urls import path
from .views import OfferListView, OfferDetailView, OfferDetailsRetrieveView

urlpatterns = [
    path('offers/', OfferListView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='single-view'),
    path('offerdetails/<int:pk>/', OfferDetailsRetrieveView.as_view(), name='offerdetails-detail')
]