from .models import SiteSettings


def site_settings(request):
    # Keep it simple and resilient; admins can create a record later.
    settings_obj = SiteSettings.objects.order_by("-updated_at").first()
    return {"site_settings": settings_obj}

