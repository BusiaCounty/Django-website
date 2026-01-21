from __future__ import annotations

from django.contrib.contenttypes.models import ContentType

from .models import ActivityAction, ActivityLog
from .threadlocals import get_audit_context


def log_model_event(*, instance, action: str, message: str = "", extra: dict | None = None):
    user, ip, ua = get_audit_context()
    ct = ContentType.objects.get_for_model(instance.__class__)
    ActivityLog.objects.create(
        user=user,
        action=action,
        model_label=f"{ct.app_label}.{ct.model}",
        object_id=str(getattr(instance, "pk", "")),
        object_repr=str(instance)[:255],
        ip_address=ip,
        user_agent=ua or "",
        message=message,
        extra=extra or {},
    )

