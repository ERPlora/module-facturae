    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'facturae'
    MODULE_NAME = _('Facturae (Spain)')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'document-lock-outline'
    MODULE_DESCRIPTION = _('Electronic invoicing for Spanish public administration')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'compliance'

    MENU = {
        'label': _('Facturae (Spain)'),
        'icon': 'document-lock-outline',
        'order': 81,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Invoices'), 'icon': 'document-lock-outline', 'id': 'invoices'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'facturae.view_facturaeinvoice',
'facturae.generate_facturae',
'facturae.submit_facturae',
'facturae.manage_settings',
    ]
