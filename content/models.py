from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class PublishStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    ARCHIVED = "ARCHIVED", "Archived"


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuthorTrackedModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    status = models.CharField(max_length=16, choices=PublishStatus.choices, default=PublishStatus.DRAFT, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def publish(self):
        self.status = PublishStatus.PUBLISHED
        self.published_at = self.published_at or timezone.now()
        self.archived_at = None

    def archive(self):
        self.status = PublishStatus.ARCHIVED
        self.archived_at = timezone.now()


class Department(TimeStampedModel, AuthorTrackedModel):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    head_of_department = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:220]
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Service(TimeStampedModel, AuthorTrackedModel, PublishableModel):
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="services")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)

    class Meta:
        ordering = ("department__name", "title")
        unique_together = (("department", "slug"),)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class PageKey(models.TextChoices):
    HOME = "HOME", "Home"
    ABOUT = "ABOUT", "About Us"
    SERVICES = "SERVICES", "Services"
    DEPARTMENTS = "DEPARTMENTS", "Departments"
    CONTACT = "CONTACT", "Contact Us"


class Page(TimeStampedModel, AuthorTrackedModel, PublishableModel):
    key = models.CharField(max_length=32, choices=PageKey.choices, unique=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    body = models.TextField(blank=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ("key",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class NewsType(models.TextChoices):
    NEWS = "NEWS", "News"
    EVENT = "EVENT", "Event"


class NewsItem(TimeStampedModel, AuthorTrackedModel, PublishableModel):
    type = models.CharField(max_length=8, choices=NewsType.choices, default=NewsType.NEWS, db_index=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    cover_image = models.ImageField(upload_to="news/", blank=True, null=True)
    cover_image_alt = models.CharField(max_length=160, blank=True)
    starts_at = models.DateTimeField(null=True, blank=True)  # for events
    ends_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-published_at", "-created_at")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class CareerPosting(TimeStampedModel, AuthorTrackedModel, PublishableModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="careers")
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    closing_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ("-published_at", "-created_at")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class SiteSettings(TimeStampedModel, AuthorTrackedModel):
    """
    Singleton-ish site configuration editable in Admin.
    """

    site_name = models.CharField(max_length=120, default="Government Institution")
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    logo_alt = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return "Site Settings"
