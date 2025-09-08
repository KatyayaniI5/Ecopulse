from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('company-profile/', views.CompanyProfileView.as_view(), name='company-profile'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    
    # Dashboard data
    path('dashboard/', views.user_dashboard_data, name='dashboard'),
] 