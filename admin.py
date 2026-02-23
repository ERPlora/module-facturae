from django.contrib import admin

from .models import FacturaeInvoice

@admin.register(FacturaeInvoice)
class FacturaeInvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'recipient_name', 'recipient_tax_id', 'total_amount', 'status']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

