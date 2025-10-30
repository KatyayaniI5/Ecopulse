from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

from .models import User, CompanyProfile
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    CompanyProfileSerializer,
    PasswordChangeSerializer
)


class UserRegistrationView(APIView):
    """View for user registration."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """View for user login."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Optional: Create session for web interface
            login(request, user)
            
            return Response({
                'message': 'Login successful',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """View for user logout."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            # Get refresh token from request
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Logout from session if user is authenticated
            if request.user.is_authenticated:
                logout(request)
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except TokenError:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Logout failed'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for user profile management."""
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class CompanyProfileView(generics.RetrieveUpdateAPIView):
    """View for company profile management."""
    
    serializer_class = CompanyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        # Get or create company profile
        profile, created = CompanyProfile.objects.get_or_create(user=self.request.user)
        return profile


class PasswordChangeView(APIView):
    """View for password change."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard_data(request):
    """Get user dashboard data."""
    user = request.user
    
    # Get basic user info
    user_data = UserProfileSerializer(user).data
    
    # Get company profile if exists
    try:
        company_profile = CompanyProfileSerializer(user.company_profile).data
    except CompanyProfile.DoesNotExist:
        company_profile = None
    
    return Response({
        'user': user_data,
        'company_profile': company_profile,
    }, status=status.HTTP_200_OK) 