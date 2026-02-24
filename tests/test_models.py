"""Tests for facturae models."""
import pytest
from django.utils import timezone

from facturae.models import FacturaeInvoice


@pytest.mark.django_db
class TestFacturaeInvoice:
    """FacturaeInvoice model tests."""

    def test_create(self, facturae_invoice):
        """Test FacturaeInvoice creation."""
        assert facturae_invoice.pk is not None
        assert facturae_invoice.is_deleted is False

    def test_soft_delete(self, facturae_invoice):
        """Test soft delete."""
        pk = facturae_invoice.pk
        facturae_invoice.is_deleted = True
        facturae_invoice.deleted_at = timezone.now()
        facturae_invoice.save()
        assert not FacturaeInvoice.objects.filter(pk=pk).exists()
        assert FacturaeInvoice.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, facturae_invoice):
        """Test default queryset excludes deleted."""
        facturae_invoice.is_deleted = True
        facturae_invoice.deleted_at = timezone.now()
        facturae_invoice.save()
        assert FacturaeInvoice.objects.filter(hub_id=hub_id).count() == 0


