from django.contrib import admin

from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by_id") and not obj.created_by_id:
            obj.created_by = request.user
        if hasattr(obj, "updated_by_id"):
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
