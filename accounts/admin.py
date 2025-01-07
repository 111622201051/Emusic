from django.contrib import admin
from .models import SubscriptionPlan, SongCategory, Notification

# Define admin models
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Customize the admin display

@admin.register(SongCategory)
class SongCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')

# Alternatively, you can use admin.site.register for models without customizations:
# admin.site.register(SubscriptionPlan)
# admin.site.register(SongCategory)
# admin.site.register(Notification)
