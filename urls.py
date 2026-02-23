from django.urls import path
from . import views

app_name = 'facturae'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('invoices/', views.invoices, name='invoices'),
    path('settings/', views.settings, name='settings'),
]
