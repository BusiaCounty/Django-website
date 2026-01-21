from __future__ import annotations

from .threadlocals import set_audit_context


class AuditContextMiddleware:
    """
    Stores request context in thread-local storage so model signals can attach
    user/ip/user-agent to audit logs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip() or request.META.get("REMOTE_ADDR")
        ua = request.META.get("HTTP_USER_AGENT", "")[:255]
        user = getattr(request, "user", None)
        set_audit_context(user=user if getattr(user, "is_authenticated", False) else None, ip_address=ip, user_agent=ua)
        return self.get_response(request)

