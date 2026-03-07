"""
Facturae (Spain) Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import FacturaeInvoice

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('facturae', 'dashboard')
@htmx_view('facturae/pages/index.html', 'facturae/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_facturae_invoices': FacturaeInvoice.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# FacturaeInvoice
# ======================================================================

FACTURAE_INVOICE_SORT_FIELDS = {
    'status': 'status',
    'total_amount': 'total_amount',
    'invoice_number': 'invoice_number',
    'recipient_name': 'recipient_name',
    'recipient_tax_id': 'recipient_tax_id',
    'xml_generated_at': 'xml_generated_at',
    'created_at': 'created_at',
}

def _build_facturae_invoices_context(hub_id, per_page=10):
    qs = FacturaeInvoice.objects.filter(hub_id=hub_id, is_deleted=False).order_by('status')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'facturae_invoices': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'status',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_facturae_invoices_list(request, hub_id, per_page=10):
    ctx = _build_facturae_invoices_context(hub_id, per_page)
    return django_render(request, 'facturae/partials/facturae_invoices_list.html', ctx)

@login_required
@with_module_nav('facturae', 'invoices')
@htmx_view('facturae/pages/facturae_invoices.html', 'facturae/partials/facturae_invoices_content.html')
def facturae_invoices_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'status')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = FacturaeInvoice.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(invoice_number__icontains=search_query) | Q(recipient_name__icontains=search_query) | Q(recipient_tax_id__icontains=search_query) | Q(status__icontains=search_query))

    order_by = FACTURAE_INVOICE_SORT_FIELDS.get(sort_field, 'status')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['status', 'total_amount', 'invoice_number', 'recipient_name', 'recipient_tax_id', 'xml_generated_at']
        headers = ['Status', 'Total Amount', 'Invoice Number', 'Recipient Name', 'Recipient Tax Id', 'Xml Generated At']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='facturae_invoices.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='facturae_invoices.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'facturae/partials/facturae_invoices_list.html', {
            'facturae_invoices': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'facturae_invoices': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
@htmx_view('facturae/pages/facturae_invoice_add.html', 'facturae/partials/facturae_invoice_add_content.html')
def facturae_invoice_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        invoice_number = request.POST.get('invoice_number', '').strip()
        recipient_name = request.POST.get('recipient_name', '').strip()
        recipient_tax_id = request.POST.get('recipient_tax_id', '').strip()
        total_amount = request.POST.get('total_amount', '0') or '0'
        status = request.POST.get('status', '').strip()
        xml_generated_at = request.POST.get('xml_generated_at') or None
        submitted_at = request.POST.get('submitted_at') or None
        response_code = request.POST.get('response_code', '').strip()
        obj = FacturaeInvoice(hub_id=hub_id)
        obj.invoice_number = invoice_number
        obj.recipient_name = recipient_name
        obj.recipient_tax_id = recipient_tax_id
        obj.total_amount = total_amount
        obj.status = status
        obj.xml_generated_at = xml_generated_at
        obj.submitted_at = submitted_at
        obj.response_code = response_code
        obj.save()
        response = HttpResponse(status=204)
        response['HX-Redirect'] = reverse('facturae:facturae_invoices_list')
        return response
    return {}

@login_required
@htmx_view('facturae/pages/facturae_invoice_edit.html', 'facturae/partials/facturae_invoice_edit_content.html')
def facturae_invoice_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(FacturaeInvoice, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.invoice_number = request.POST.get('invoice_number', '').strip()
        obj.recipient_name = request.POST.get('recipient_name', '').strip()
        obj.recipient_tax_id = request.POST.get('recipient_tax_id', '').strip()
        obj.total_amount = request.POST.get('total_amount', '0') or '0'
        obj.status = request.POST.get('status', '').strip()
        obj.xml_generated_at = request.POST.get('xml_generated_at') or None
        obj.submitted_at = request.POST.get('submitted_at') or None
        obj.response_code = request.POST.get('response_code', '').strip()
        obj.save()
        return _render_facturae_invoices_list(request, hub_id)
    return {'obj': obj}

@login_required
@require_POST
def facturae_invoice_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(FacturaeInvoice, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_facturae_invoices_list(request, hub_id)

@login_required
@require_POST
def facturae_invoices_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = FacturaeInvoice.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_facturae_invoices_list(request, hub_id)


@login_required
@permission_required('facturae.manage_settings')
@with_module_nav('facturae', 'settings')
@htmx_view('facturae/pages/settings.html', 'facturae/partials/settings_content.html')
def settings_view(request):
    return {}

