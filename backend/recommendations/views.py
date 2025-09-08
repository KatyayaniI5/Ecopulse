from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta

from .models import Recommendation, RecommendationAction
from .serializers import (
    RecommendationSerializer,
    RecommendationActionSerializer,
    RecommendationStatsSerializer
)


class RecommendationListView(generics.ListCreateAPIView):
    """View for listing and creating recommendations."""
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecommendationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a recommendation."""
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user)


class GenerateRecommendationsView(APIView):
    """View for generating AI-powered recommendations."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # TODO: Implement AI recommendation generation logic
        # This would analyze user's invoices and generate recommendations
        
        # Placeholder response
        return Response({
            'message': 'Recommendations generated successfully',
            'count': 0
        }, status=status.HTTP_200_OK)


class RecommendationActionView(APIView):
    """View for taking actions on recommendations."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            recommendation = Recommendation.objects.get(
                pk=pk, 
                user=request.user
            )
        except Recommendation.DoesNotExist:
            return Response(
                {'error': 'Recommendation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = RecommendationActionSerializer(data=request.data)
        if serializer.is_valid():
            action = serializer.save(recommendation=recommendation)
            
            # Update recommendation status based on action
            if action.action_type == 'implemented':
                recommendation.is_implemented = True
                recommendation.save()
            elif action.action_type == 'dismissed':
                recommendation.is_dismissed = True
                recommendation.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationStatsView(APIView):
    """View for recommendation statistics."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user_recommendations = Recommendation.objects.filter(user=request.user)
        
        # Calculate statistics
        total_recommendations = user_recommendations.count()
        implemented_count = user_recommendations.filter(is_implemented=True).count()
        dismissed_count = user_recommendations.filter(is_dismissed=True).count()
        pending_count = total_recommendations - implemented_count - dismissed_count
        
        # Priority breakdown
        priority_stats = user_recommendations.values('priority').annotate(
            count=Count('id')
        )
        
        # Type breakdown
        type_stats = user_recommendations.values('recommendation_type').annotate(
            count=Count('id')
        )
        
        # Recent activity (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_recommendations = user_recommendations.filter(
            created_at__gte=thirty_days_ago
        ).count()
        
        stats = {
            'total_recommendations': total_recommendations,
            'implemented_count': implemented_count,
            'dismissed_count': dismissed_count,
            'pending_count': pending_count,
            'implementation_rate': (implemented_count / total_recommendations * 100) if total_recommendations > 0 else 0,
            'priority_breakdown': list(priority_stats),
            'type_breakdown': list(type_stats),
            'recent_recommendations': recent_recommendations,
        }
        
        return Response(stats, status=status.HTTP_200_OK) 