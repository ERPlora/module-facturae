from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

FACT_STATUS = [
    ('draft', _('Draft')),
    ('generated', _('Generated')),
    ('submitted', _('Submitted')),
    ('accepted', _('Accepted')),
    ('rejected', _('Rejected')),
]

class FacturaeInvoice(HubBaseModel):
    invoice_number = models.CharField(max_length=50, verbose_name=_('Invoice Number'))
    recipient_name = models.CharField(max_length=255, verbose_name=_('Recipient Name'))
    recipient_tax_id = models.CharField(max_length=20, verbose_name=_('Recipient Tax Id'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Total Amount'))
    status = models.CharField(max_length=20, default='draft', choices=FACT_STATUS, verbose_name=_('Status'))
    xml_generated_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Xml Generated At'))
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Submitted At'))
    response_code = models.CharField(max_length=50, blank=True, verbose_name=_('Response Code'))

    class Meta(HubBaseModel.Meta):
        db_table = 'facturae_facturaeinvoice'

    def __str__(self):
        return str(self.id)

