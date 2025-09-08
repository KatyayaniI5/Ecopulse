from django.urls import path
from . import views

app_name = 'simulations'

urlpatterns = [
    path('', views.SimulationListView.as_view(), name='simulation-list'),
    path('<int:pk>/', views.SimulationDetailView.as_view(), name='simulation-detail'),
    path('create/', views.CreateSimulationView.as_view(), name='create-simulation'),
    path('<int:pk>/run/', views.RunSimulationView.as_view(), name='run-simulation'),
    path('<int:pk>/results/', views.SimulationResultsView.as_view(), name='simulation-results'),
    path('templates/', views.SimulationTemplatesView.as_view(), name='simulation-templates'),
] 