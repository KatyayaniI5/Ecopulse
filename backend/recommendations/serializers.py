from rest_framework import serializers
from .models import Recommendation, RecommendationAction


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for Recommendation model."""
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'title', 'description', 'recommendation_type', 'priority',
            'potential_carbon_savings', 'potential_cost_savings', 'implementation_cost',
            'payback_period_months', 'is_implemented', 'is_dismissed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RecommendationActionSerializer(serializers.ModelSerializer):
    """Serializer for RecommendationAction model."""
    
    class Meta:
        model = RecommendationAction
        fields = ['id', 'action_type', 'notes', 'scheduled_date', 'created_at']
        read_only_fields = ['id', 'created_at']


class RecommendationStatsSerializer(serializers.Serializer):
    """Serializer for recommendation statistics."""
    
    total_recommendations = serializers.IntegerField()
    implemented_count = serializers.IntegerField()
    dismissed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()
    implementation_rate = serializers.FloatField()
    priority_breakdown = serializers.ListField()
    type_breakdown = serializers.ListField()
    recent_recommendations = serializers.IntegerField() 