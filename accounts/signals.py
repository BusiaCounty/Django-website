from __future__ import annotations

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


ROLE_GROUPS = {
    "Content Editor": [
        # Can add/change content, but cannot delete by default
        ("content", "add_page"),
        ("content", "change_page"),
        ("content", "add_newsitem"),
        ("content", "change_newsitem"),
        ("content", "add_service"),
        ("content", "change_service"),
        ("notices", "add_notice"),
        ("notices", "change_notice"),
        ("downloads", "add_document"),
        ("downloads", "change_document"),
    ],
    "Department Officer": [
        ("content", "add_newsitem"),
        ("content", "change_newsitem"),
        ("downloads", "add_document"),
        ("downloads", "change_document"),
        ("notices", "add_notice"),
        ("notices", "change_notice"),
    ],
}


@receiver(post_migrate)
def ensure_groups(sender, **kwargs):
    """
    Create default role groups and permissions after migrations.
    Super Admin uses Django's is_superuser.
    """

    # Only run once after auth/contenttypes are ready.
    if sender.name not in {"accounts", "auth", "contenttypes"}:
        return

    for group_name, perms in ROLE_GROUPS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = []
        for app_label, codename in perms:
            try:
                perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
            except Permission.DoesNotExist:
                continue
            permissions.append(perm)
        if permissions:
            group.permissions.add(*permissions)

