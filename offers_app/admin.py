from django.contrib import admin
from .models import OfferModel, OfferDetails

@admin.register(OfferModel)
class OfferModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'title', 'description', 'created_at', 'updated_at', 'get_user')
    def get_user(self, obj):
        return obj.user
    get_user.short_description = 'User'

@admin.register(OfferDetails)
class OfferDetailsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'offer', 'title', 'revisions', 'delivery_time', 'price', 'features', 'offer_type', 'created_at', 'updated_at', 'get_offer')
    def get_offer(self, obj):
        return obj.offer
    get_offer.short_description = 'Offer' 