"""
URL configuration for eco_api project.
"""
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Root path - welcome message
    path('', lambda request: HttpResponse("Welcome to the EPICS Project API! 🚀<br><br>Available endpoints:<br>- /admin/ - Django admin<br>- /api/auth/ - Authentication endpoints<br>- /api/invoices/ - Invoice management<br>- /api/analytics/ - Analytics data<br>- /api/recommendations/ - Recommendations<br>- /api/simulations/ - Simulations", content_type="text/html"), name='home'),
    
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/invoices/', include('invoices.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/simulations/', include('simulations.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 