from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('carbon-footprint/', views.CarbonFootprintView.as_view(), name='carbon-footprint'),
    path('material-breakdown/', views.MaterialBreakdownView.as_view(), name='material-breakdown'),
    path('supplier-breakdown/', views.SupplierBreakdownView.as_view(), name='supplier-breakdown'),
    path('trends/', views.TrendsView.as_view(), name='trends'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
] 