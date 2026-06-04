from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderCountView, OrderCountCompletedView

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', OrderCountCompletedView.as_view(), name='completed-order-count')
]