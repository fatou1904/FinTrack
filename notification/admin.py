from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type', 'message', 'date_creation', 'est_vue')
    list_filter = ('type', 'est_vue', 'date_creation')
    search_fields = ('message', 'utilisateur__username')
    date_hierarchy = 'date_creation'
