from rest_framework import serializers
from .models import CarbonFootprint, MaterialBreakdown, SupplierBreakdown, SustainabilityGoal, EnvironmentalReport


class CarbonFootprintSerializer(serializers.ModelSerializer):
    """Serializer for CarbonFootprint model."""
    
    class Meta:
        model = CarbonFootprint
        fields = [
            'id', 'date', 'period_type', 'total_carbon_footprint', 'scope1_carbon',
            'scope2_carbon', 'scope3_carbon', 'total_water_footprint', 'total_energy_footprint',
            'total_waste_footprint', 'revenue', 'employees', 'carbon_intensity',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MaterialBreakdownSerializer(serializers.ModelSerializer):
    """Serializer for MaterialBreakdown model."""
    
    class Meta:
        model = MaterialBreakdown
        fields = [
            'id', 'carbon_footprint', 'material_name', 'material_category',
            'quantity', 'unit', 'carbon_footprint_value', 'water_footprint_value',
            'energy_footprint_value', 'percentage_of_total'
        ]
        read_only_fields = ['id']


class SupplierBreakdownSerializer(serializers.ModelSerializer):
    """Serializer for SupplierBreakdown model."""
    
    class Meta:
        model = SupplierBreakdown
        fields = [
            'id', 'carbon_footprint', 'supplier_name', 'supplier_category',
            'carbon_footprint_value', 'water_footprint_value', 'energy_footprint_value',
            'percentage_of_total', 'sustainability_rating'
        ]
        read_only_fields = ['id']


class SustainabilityGoalSerializer(serializers.ModelSerializer):
    """Serializer for SustainabilityGoal model."""
    
    class Meta:
        model = SustainabilityGoal
        fields = [
            'id', 'title', 'description', 'goal_type', 'target_value', 'current_value',
            'unit', 'target_date', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EnvironmentalReportSerializer(serializers.ModelSerializer):
    """Serializer for EnvironmentalReport model."""
    
    class Meta:
        model = EnvironmentalReport
        fields = [
            'id', 'title', 'report_type', 'period_start', 'period_end',
            'report_data', 'generated_at'
        ]
        read_only_fields = ['id', 'generated_at'] 