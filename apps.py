from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FacturaeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'facturae'
    label = 'facturae'
    verbose_name = _('Facturae (Spain)')

    def ready(self):
        pass
