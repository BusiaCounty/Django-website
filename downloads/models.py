from __future__ import annotations

from django.db import models

from content.models import Department, AuthorTrackedModel, PublishableModel, TimeStampedModel


class DocumentCategory(models.TextChoices):
    FORMS = "FORMS", "Forms"
    REPORTS = "REPORTS", "Reports"
    POLICIES = "POLICIES", "Policies"
    TENDERS = "TENDERS", "Tenders"
    OTHER = "OTHER", "Other"


class Document(TimeStampedModel, AuthorTrackedModel, PublishableModel):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=16, choices=DocumentCategory.choices, default=DocumentCategory.OTHER, db_index=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="documents", null=True, blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="downloads/")

    class Meta:
        ordering = ("-published_at", "-created_at")

    def __str__(self) -> str:  # pragma: no cover
        return self.title
