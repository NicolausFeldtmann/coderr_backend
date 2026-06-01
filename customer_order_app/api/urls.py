from django.urls import path
from .views import OrderViewSet, OrderDetailView, OrderCountView, OrderCountCompletedView

urlpatterns = [
    path('orders/', OrderViewSet.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', OrderCountCompletedView.as_view(), name='completed-order-count')
]