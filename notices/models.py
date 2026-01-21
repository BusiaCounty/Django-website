from __future__ import annotations

from django.db import models

from content.models import AuthorTrackedModel, PublishableModel, TimeStampedModel


class Notice(TimeStampedModel, AuthorTrackedModel, PublishableModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    attachment = models.FileField(upload_to="notices/", blank=True, null=True)

    class Meta:
        ordering = ("-published_at", "-created_at")

    def save(self, *args, **kwargs):
        from django.utils.text import slugify

        if not self.slug:
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return self.title
