"""
Facturae (Spain) Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('facturae', 'dashboard')
@htmx_view('facturae/pages/dashboard.html', 'facturae/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('facturae', 'invoices')
@htmx_view('facturae/pages/invoices.html', 'facturae/partials/invoices_content.html')
def invoices(request):
    """Invoices view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('facturae', 'settings')
@htmx_view('facturae/pages/settings.html', 'facturae/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

