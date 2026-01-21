from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "user", "model_label", "object_id", "ip_address")
    list_filter = ("action", "model_label", "created_at")
    search_fields = ("user__username", "model_label", "object_id", "object_repr", "message", "ip_address", "user_agent")
    readonly_fields = [f.name for f in ActivityLog._meta.fields]

