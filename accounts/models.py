from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin (ICT/Admin)"
    CONTENT_EDITOR = "CONTENT_EDITOR", "Content Editor"
    DEPARTMENT_OFFICER = "DEPARTMENT_OFFICER", "Department Officer"


class User(AbstractUser):
    """
    Government institutional user.
    Use Django Admin for management, with an explicit role for policy decisions.
    """

    role = models.CharField(
        max_length=32,
        choices=UserRole.choices,
        default=UserRole.DEPARTMENT_OFFICER,
        db_index=True,
    )

    def __str__(self) -> str:  # pragma: no cover
        return self.get_full_name() or self.username
