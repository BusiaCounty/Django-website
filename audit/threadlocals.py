from __future__ import annotations

import threading


_state = threading.local()


def set_audit_context(user=None, ip_address: str | None = None, user_agent: str | None = None):
    _state.user = user
    _state.ip_address = ip_address
    _state.user_agent = user_agent


def get_audit_context():
    return getattr(_state, "user", None), getattr(_state, "ip_address", None), getattr(_state, "user_agent", None)

