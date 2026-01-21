from django.views.generic import ListView

from content.models import PublishStatus

from .models import Document


class DownloadsListView(ListView):
    template_name = "public/downloads.html"
    model = Document
    context_object_name = "documents"

    def get_queryset(self):
        return Document.objects.select_related("department").filter(status=PublishStatus.PUBLISHED).order_by("-published_at")

# Create your views here.
