from django.urls import path
from . import views

app_name = 'facturae'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('invoices/', views.facturae_invoices_list, name='invoices'),


    # FacturaeInvoice
    path('facturae_invoices/', views.facturae_invoices_list, name='facturae_invoices_list'),
    path('facturae_invoices/add/', views.facturae_invoice_add, name='facturae_invoice_add'),
    path('facturae_invoices/<uuid:pk>/edit/', views.facturae_invoice_edit, name='facturae_invoice_edit'),
    path('facturae_invoices/<uuid:pk>/delete/', views.facturae_invoice_delete, name='facturae_invoice_delete'),
    path('facturae_invoices/bulk/', views.facturae_invoices_bulk_action, name='facturae_invoices_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
