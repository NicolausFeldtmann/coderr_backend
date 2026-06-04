from django.contrib import admin
from .models import OrderModel

@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'offer_detail', 'offer_type', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'status', 'created_at', 'updated_at', 'get_customer')
    def get_customer(self, obj):
        return obj.customer_user
    get_customer.short_description = 'Customer'
    