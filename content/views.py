from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from downloads.models import Document
from notices.models import Notice

from .models import (
    CareerPosting,
    Department,
    NewsItem,
    Page,
    PageKey,
    PublishStatus,
    Service,
    SiteSettings,
)


class HomeView(TemplateView):
    template_name = "public/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page"] = Page.objects.filter(key=PageKey.HOME).first()
        ctx["latest_notices"] = Notice.objects.filter(status=PublishStatus.PUBLISHED).order_by("-published_at")[:5]
        ctx["latest_news"] = NewsItem.objects.filter(status=PublishStatus.PUBLISHED).order_by("-published_at")[:5]
        ctx["latest_documents"] = Document.objects.filter(status=PublishStatus.PUBLISHED).order_by("-published_at")[:5]
        return ctx


class PageByKeyView(TemplateView):
    template_name = "public/page.html"
    key: str = ""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page"] = get_object_or_404(Page, key=self.key, status=PublishStatus.PUBLISHED)
        return ctx


class DepartmentsListView(ListView):
    template_name = "public/departments.html"
    model = Department
    context_object_name = "departments"


class ServicesListView(ListView):
    template_name = "public/services.html"
    model = Service
    context_object_name = "services"

    def get_queryset(self):
        return (
            Service.objects.select_related("department")
            .filter(status=PublishStatus.PUBLISHED)
            .order_by("department__name", "title")
        )


class NewsEventsListView(ListView):
    template_name = "public/news_events.html"
    model = NewsItem
    context_object_name = "items"

    def get_queryset(self):
        return NewsItem.objects.filter(status=PublishStatus.PUBLISHED).order_by("-published_at")


class NewsEventDetailView(DetailView):
    template_name = "public/news_event_detail.html"
    model = NewsItem
    context_object_name = "item"

    def get_queryset(self):
        return NewsItem.objects.filter(status=PublishStatus.PUBLISHED)


class CareersListView(ListView):
    template_name = "public/careers.html"
    model = CareerPosting
    context_object_name = "jobs"

    def get_queryset(self):
        return CareerPosting.objects.select_related("department").filter(status=PublishStatus.PUBLISHED).order_by("-published_at")


class CareerDetailView(DetailView):
    template_name = "public/career_detail.html"
    model = CareerPosting
    context_object_name = "job"

    def get_queryset(self):
        return CareerPosting.objects.select_related("department").filter(status=PublishStatus.PUBLISHED)

# Create your views here.
