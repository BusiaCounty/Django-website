import os

# Allows `DJANGO_SETTINGS_MODULE=config.settings` to keep working by delegating
# to the explicit environment setting, defaulting to development.
_default = os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.dev")
if _default.endswith("config.settings"):
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.dev"

