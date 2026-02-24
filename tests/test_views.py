"""Tests for facturae views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('facturae:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('facturae:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('facturae:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestFacturaeInvoiceViews:
    """FacturaeInvoice view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('facturae:facturae_invoices_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('facturae:facturae_invoices_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('facturae:facturae_invoices_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('facturae:facturae_invoices_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('facturae:facturae_invoices_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('facturae:facturae_invoices_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('facturae:facturae_invoice_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('facturae:facturae_invoice_add')
        data = {
            'invoice_number': 'New Invoice Number',
            'recipient_name': 'New Recipient Name',
            'recipient_tax_id': 'New Recipient Tax Id',
            'total_amount': '100.00',
            'status': 'New Status',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, facturae_invoice):
        """Test edit form loads."""
        url = reverse('facturae:facturae_invoice_edit', args=[facturae_invoice.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, facturae_invoice):
        """Test editing via POST."""
        url = reverse('facturae:facturae_invoice_edit', args=[facturae_invoice.pk])
        data = {
            'invoice_number': 'Updated Invoice Number',
            'recipient_name': 'Updated Recipient Name',
            'recipient_tax_id': 'Updated Recipient Tax Id',
            'total_amount': '100.00',
            'status': 'Updated Status',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, facturae_invoice):
        """Test soft delete via POST."""
        url = reverse('facturae:facturae_invoice_delete', args=[facturae_invoice.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        facturae_invoice.refresh_from_db()
        assert facturae_invoice.is_deleted is True

    def test_bulk_delete(self, auth_client, facturae_invoice):
        """Test bulk delete."""
        url = reverse('facturae:facturae_invoices_bulk_action')
        response = auth_client.post(url, {'ids': str(facturae_invoice.pk), 'action': 'delete'})
        assert response.status_code == 200
        facturae_invoice.refresh_from_db()
        assert facturae_invoice.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('facturae:facturae_invoices_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('facturae:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('facturae:settings')
        response = client.get(url)
        assert response.status_code == 302

