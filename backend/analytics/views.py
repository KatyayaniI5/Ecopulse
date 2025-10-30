from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta

from .models import CarbonFootprint, MaterialBreakdown, SupplierBreakdown, SustainabilityGoal, EnvironmentalReport
from .serializers import (
    CarbonFootprintSerializer,
    MaterialBreakdownSerializer,
    SupplierBreakdownSerializer,
    SustainabilityGoalSerializer,
    EnvironmentalReportSerializer
)


class AnalyticsDashboardView(APIView):
    """View for analytics dashboard data."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get current month's data
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Carbon footprint summary
        current_footprint = CarbonFootprint.objects.filter(
            user=user,
            date__gte=current_month
        ).aggregate(
            total_carbon=Sum('total_carbon_footprint'),
            total_water=Sum('total_water_footprint'),
            total_energy=Sum('total_energy_footprint')
        )
        
        # Previous month for comparison
        prev_month = current_month - timedelta(days=1)
        prev_month = prev_month.replace(day=1)
        
        prev_footprint = CarbonFootprint.objects.filter(
            user=user,
            date__gte=prev_month,
            date__lt=current_month
        ).aggregate(
            total_carbon=Sum('total_carbon_footprint'),
            total_water=Sum('total_water_footprint'),
            total_energy=Sum('total_energy_footprint')
        )
        
        # Calculate percentage changes
        carbon_change = 0
        water_change = 0
        energy_change = 0
        
        if prev_footprint['total_carbon'] and current_footprint['total_carbon']:
            carbon_change = ((current_footprint['total_carbon'] - prev_footprint['total_carbon']) / prev_footprint['total_carbon']) * 100
        
        if prev_footprint['total_water'] and current_footprint['total_water']:
            water_change = ((current_footprint['total_water'] - prev_footprint['total_water']) / prev_footprint['total_water']) * 100
        
        if prev_footprint['total_energy'] and current_footprint['total_energy']:
            energy_change = ((current_footprint['total_energy'] - prev_footprint['total_energy']) / prev_footprint['total_energy']) * 100
        
        # Goals progress
        active_goals = SustainabilityGoal.objects.filter(user=user, is_active=True)
        goals_progress = []
        
        for goal in active_goals:
            progress = {
                'id': goal.id,
                'title': goal.title,
                'target_value': goal.target_value,
                'current_value': goal.current_value or 0,
                'unit': goal.unit,
                'progress_percentage': 0
            }
            
            if goal.target_value:
                progress['progress_percentage'] = min((progress['current_value'] / goal.target_value) * 100, 100)
            
            goals_progress.append(progress)
        
        dashboard_data = {
            'current_month': {
                'carbon_footprint': current_footprint['total_carbon'] or 0,
                'water_footprint': current_footprint['total_water'] or 0,
                'energy_footprint': current_footprint['total_energy'] or 0,
            },
            'changes': {
                'carbon_change': carbon_change,
                'water_change': water_change,
                'energy_change': energy_change,
            },
            'goals_progress': goals_progress,
            'summary': {
                'total_invoices_processed': 0,  # TODO: Get from invoices app
                'total_recommendations': 0,     # TODO: Get from recommendations app
                'total_simulations': 0,         # TODO: Get from simulations app
            }
        }
        
        return Response(dashboard_data, status=status.HTTP_200_OK)


class CarbonFootprintView(generics.ListCreateAPIView):
    """View for carbon footprint data."""
    serializer_class = CarbonFootprintSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CarbonFootprint.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MaterialBreakdownView(generics.ListCreateAPIView):
    """View for material breakdown data."""
    serializer_class = MaterialBreakdownSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MaterialBreakdown.objects.filter(carbon_footprint__user=self.request.user)


class SupplierBreakdownView(generics.ListCreateAPIView):
    """View for supplier breakdown data."""
    serializer_class = SupplierBreakdownSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SupplierBreakdown.objects.filter(carbon_footprint__user=self.request.user)


class TrendsView(APIView):
    """View for environmental impact trends."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        period = request.GET.get('period', '6months')  # 6months, 1year, 2years
        
        # Calculate date range
        end_date = timezone.now()
        if period == '6months':
            start_date = end_date - timedelta(days=180)
        elif period == '1year':
            start_date = end_date - timedelta(days=365)
        elif period == '2years':
            start_date = end_date - timedelta(days=730)
        else:
            start_date = end_date - timedelta(days=180)
        
        # Get monthly data
        footprints = CarbonFootprint.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')
        
        trends_data = []
        for footprint in footprints:
            trends_data.append({
                'date': footprint.date.strftime('%Y-%m'),
                'carbon_footprint': float(footprint.total_carbon_footprint or 0),
                'water_footprint': float(footprint.total_water_footprint or 0),
                'energy_footprint': float(footprint.total_energy_footprint or 0),
                'carbon_intensity': float(footprint.carbon_intensity or 0),
            })
        
        return Response({
            'period': period,
            'trends': trends_data
        }, status=status.HTTP_200_OK)


class ReportsView(generics.ListCreateAPIView):
    """View for environmental reports."""
    serializer_class = EnvironmentalReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EnvironmentalReport.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 