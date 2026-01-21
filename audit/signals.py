from __future__ import annotations

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from audit.models import ActivityAction
from audit.utils import log_model_event
from content.models import CareerPosting, Department, NewsItem, Page, Service
from downloads.models import Document
from notices.models import Notice


TRACKED_MODELS = (Page, Department, Service, NewsItem, CareerPosting, Notice, Document)


@receiver(post_save)
def audit_save(sender, instance, created, **kwargs):
    if sender not in TRACKED_MODELS:
        return
    log_model_event(
        instance=instance,
        action=ActivityAction.CREATE if created else ActivityAction.UPDATE,
        message="Created" if created else "Updated",
    )


@receiver(post_delete)
def audit_delete(sender, instance, **kwargs):
    if sender not in TRACKED_MODELS:
        return
    log_model_event(
        instance=instance,
        action=ActivityAction.DELETE,
        message="Deleted",
    )

