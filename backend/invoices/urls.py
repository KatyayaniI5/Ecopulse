from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    # Invoice management
    path('upload/', views.InvoiceUploadView.as_view(), name='upload'),
    path('', views.InvoiceListView.as_view(), name='list'),
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='detail'),
    path('<int:invoice_id>/status/', views.InvoiceProcessingStatusView.as_view(), name='status'),
    path('<int:invoice_id>/reprocess/', views.reprocess_invoice, name='reprocess'),
    path('<int:invoice_id>/delete/', views.delete_invoice, name='delete'),
    
    # Statistics
    path('statistics/', views.invoice_statistics, name='statistics'),
    
    # Material categories and suppliers
    path('materials/', views.MaterialCategoryListView.as_view(), name='materials'),
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers'),
] 