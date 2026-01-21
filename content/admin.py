from django.contrib import admin

from .models import CareerPosting, Department, NewsItem, Page, Service, SiteSettings, PublishStatus


class PublishActionsMixin:
    actions = ("make_published", "make_archived")

    @admin.action(description="Publish selected items")
    def make_published(self, request, queryset):
        for obj in queryset:
            if hasattr(obj, "publish"):
                obj.publish()
            obj.updated_by = request.user
            obj.save()

    @admin.action(description="Archive selected items")
    def make_archived(self, request, queryset):
        for obj in queryset:
            if hasattr(obj, "archive"):
                obj.archive()
            obj.updated_by = request.user
            obj.save()


class AuthorAdminMixin:
    def save_model(self, request, obj, form, change):
        if hasattr(obj, "created_by_id") and not obj.created_by_id:
            obj.created_by = request.user
        if hasattr(obj, "updated_by_id"):
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Department)
class DepartmentAdmin(AuthorAdminMixin, admin.ModelAdmin):
    list_display = ("name", "email", "phone", "updated_at")
    search_fields = ("name", "description", "head_of_department")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Service)
class ServiceAdmin(AuthorAdminMixin, PublishActionsMixin, admin.ModelAdmin):
    list_display = ("title", "department", "status", "published_at", "updated_at")
    list_filter = ("status", "department")
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Page)
class PageAdmin(AuthorAdminMixin, PublishActionsMixin, admin.ModelAdmin):
    list_display = ("key", "title", "status", "published_at", "updated_at")
    list_filter = ("status", "key")
    search_fields = ("title", "body", "meta_title", "meta_description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(NewsItem)
class NewsItemAdmin(AuthorAdminMixin, PublishActionsMixin, admin.ModelAdmin):
    list_display = ("title", "type", "status", "published_at", "updated_at")
    list_filter = ("status", "type")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(CareerPosting)
class CareerPostingAdmin(AuthorAdminMixin, PublishActionsMixin, admin.ModelAdmin):
    list_display = ("title", "department", "status", "closing_date", "published_at")
    list_filter = ("status", "department")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SiteSettings)
class SiteSettingsAdmin(AuthorAdminMixin, admin.ModelAdmin):
    list_display = ("site_name", "contact_email", "contact_phone", "updated_at")

