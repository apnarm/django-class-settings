__all__ = ["Env", "Settings", "env", "setup"]
__version__ = "0.3.0-dev"

from .env import Env, env
from .settings import Settings


def setup():
    import sys
    from django.conf import settings
    from django.utils.functional import SimpleLazyObject
    from .importers import SettingsImporter, LazySettingsModule

    global _setup
    if _setup:
        return

    class SimpleLazySettings(SimpleLazyObject):

        def __repr__(self):
            return env('DJANGO_SETTINGS_MODULE')

    sys.meta_path.append(SettingsImporter)
    default_settings = LazySettingsModule()

    def default_settings_module():
        return default_settings.SETTINGS_MODULE

    settings_module = SimpleLazySettings(default_settings_module)
    settings.configure(default_settings, SETTINGS_MODULE=settings_module)

    _setup = True


_setup = False
