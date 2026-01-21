from django.views.generic import DetailView, ListView

from content.models import PublishStatus

from .models import Notice


class NoticeListView(ListView):
    template_name = "public/notices.html"
    model = Notice
    context_object_name = "notices"

    def get_queryset(self):
        return Notice.objects.filter(status=PublishStatus.PUBLISHED).order_by("-published_at")


class NoticeDetailView(DetailView):
    template_name = "public/notice_detail.html"
    model = Notice
    context_object_name = "notice"

    def get_queryset(self):
        return Notice.objects.filter(status=PublishStatus.PUBLISHED)

# Create your views here.
