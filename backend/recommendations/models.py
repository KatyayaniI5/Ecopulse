from django.db import models
from django.contrib.auth import get_user_model
from invoices.models import Invoice, MaterialCategory

User = get_user_model()


class Recommendation(models.Model):
    """Model for storing AI-generated sustainability recommendations."""
    
    RECOMMENDATION_TYPES = [
        ('material', 'Material Substitution'),
        ('supplier', 'Supplier Change'),
        ('process', 'Process Optimization'),
        ('energy', 'Energy Efficiency'),
        ('waste', 'Waste Reduction'),
        ('general', 'General Sustainability'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=200)
    description = models.TextField()
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    
    # Impact metrics
    potential_carbon_savings = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potential_cost_savings = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    implementation_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payback_period_months = models.IntegerField(null=True, blank=True)
    
    # Related data
    related_invoices = models.ManyToManyField(Invoice, blank=True)
    related_materials = models.ManyToManyField(MaterialCategory, blank=True)
    
    # Status tracking
    is_implemented = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_priority_display()}"


class RecommendationAction(models.Model):
    """Model for tracking actions taken on recommendations."""
    
    ACTION_TYPES = [
        ('implemented', 'Implemented'),
        ('dismissed', 'Dismissed'),
        ('scheduled', 'Scheduled for Implementation'),
        ('under_review', 'Under Review'),
    ]
    
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    notes = models.TextField(blank=True)
    scheduled_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.recommendation.title} - {self.get_action_type_display()}" 