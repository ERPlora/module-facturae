"""Pytest fixtures for facturae module tests."""
import uuid
import pytest
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from apps.accounts.models import LocalUser
from apps.configuration.models import HubConfig, StoreConfig
from facturae.models import FacturaeInvoice


@pytest.fixture
def hub_id():
    """Test hub_id."""
    return uuid.uuid4()


@pytest.fixture
def configured_hub(db, hub_id):
    """Configure HubConfig with test hub_id."""
    HubConfig._clear_cache()
    config = HubConfig.get_config()
    config.hub_id = hub_id
    config.is_configured = True
    config.save()
    return config


@pytest.fixture
def store_config(db):
    """StoreConfig for testing."""
    config = StoreConfig.get_solo()
    config.business_name = 'Test Store'
    config.tax_rate = Decimal('21.00')
    config.is_configured = True
    config.save()
    return config


@pytest.fixture
def admin_user(db, hub_id):
    """Admin user for testing."""
    return LocalUser.objects.create(
        hub_id=hub_id,
        name='Admin User',
        email='admin@test.com',
        role='admin',
        pin_hash=make_password('1234'),
        is_active=True,
    )


@pytest.fixture
def auth_client(client, admin_user, store_config):
    """Authenticated client with session."""
    session = client.session
    session['local_user_id'] = str(admin_user.id)
    session['user_name'] = admin_user.name
    session['user_email'] = admin_user.email
    session['user_role'] = admin_user.role
    session['hub_id'] = str(admin_user.hub_id)
    session['store_config_checked'] = True
    session.save()
    return client


@pytest.fixture
def facturae_invoice(db, hub_id):
    """Create a test FacturaeInvoice."""
    return FacturaeInvoice.objects.create(
        hub_id=hub_id,
        invoice_number='NUM-001',
        recipient_name='Test Recipient Name',
        recipient_tax_id='Test Recipient Tax Id',
        total_amount=Decimal('100.00'),
        status='Test Status',
        xml_generated_at=timezone.now(),
    )

