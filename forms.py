from django import forms
from django.utils.translation import gettext_lazy as _

from .models import FacturaeInvoice

class FacturaeInvoiceForm(forms.ModelForm):
    class Meta:
        model = FacturaeInvoice
        fields = ['invoice_number', 'recipient_name', 'recipient_tax_id', 'total_amount', 'status', 'xml_generated_at', 'submitted_at', 'response_code']
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'recipient_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'recipient_tax_id': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'total_amount': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'xml_generated_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'submitted_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'response_code': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
        }

