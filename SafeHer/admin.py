from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SubscriptionPlan, PromoCode, Payment


admin.site.register(SubscriptionPlan)
admin.site.register(PromoCode)
admin.site.register(Payment)