from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "department", "status", "published_at", "updated_at")
    list_filter = ("status", "category", "department")
    search_fields = ("title", "description")

    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by_id") and not obj.created_by_id:
            obj.created_by = request.user
        if hasattr(obj, "updated_by_id"):
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
