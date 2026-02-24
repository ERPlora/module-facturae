from django.contrib import admin

from .models import FacturaeInvoice

@admin.register(FacturaeInvoice)
class FacturaeInvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'recipient_name', 'recipient_tax_id', 'total_amount', 'status', 'created_at']
    search_fields = ['invoice_number', 'recipient_name', 'recipient_tax_id', 'status']
    readonly_fields = ['created_at', 'updated_at']

