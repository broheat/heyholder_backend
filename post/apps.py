from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PostConfig(AppConfig):
    name = 'post'
    verbose_name = _("Post")

    def ready(self):
        try:
            import post.signals  # noqa F401
        except ImportError:
            pass