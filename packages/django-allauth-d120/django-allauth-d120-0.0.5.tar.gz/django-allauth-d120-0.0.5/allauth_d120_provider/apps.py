from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class D120ProviderConfig(AppConfig):
    name = 'allauth_d120_provider'
    verbose_name = _("D120 Authentication Provider")

    def ready(self):
        # noinspection PyUnresolvedReferences
        from .signals import sig_sync_user_to_groups
