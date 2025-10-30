from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.RecommendationListView.as_view(), name='recommendation-list'),
    path('<int:pk>/', views.RecommendationDetailView.as_view(), name='recommendation-detail'),
    path('generate/', views.GenerateRecommendationsView.as_view(), name='generate-recommendations'),
    path('<int:pk>/action/', views.RecommendationActionView.as_view(), name='recommendation-action'),
    path('stats/', views.RecommendationStatsView.as_view(), name='recommendation-stats'),
] 