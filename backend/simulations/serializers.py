from rest_framework import serializers
from .models import Simulation, SimulationParameter, SimulationResult


class SimulationParameterSerializer(serializers.ModelSerializer):
    """Serializer for SimulationParameter model."""
    
    class Meta:
        model = SimulationParameter
        fields = ['id', 'parameter_type', 'parameter_name', 'original_value', 'new_value', 'unit']


class SimulationResultSerializer(serializers.ModelSerializer):
    """Serializer for SimulationResult model."""
    
    class Meta:
        model = SimulationResult
        fields = [
            'id', 'carbon_breakdown', 'water_breakdown', 'energy_breakdown', 
            'cost_breakdown', 'recommendations', 'implementation_steps',
            'calculation_method', 'confidence_level', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SimulationSerializer(serializers.ModelSerializer):
    """Serializer for Simulation model."""
    parameters = SimulationParameterSerializer(many=True, read_only=True)
    
    class Meta:
        model = Simulation
        fields = [
            'id', 'name', 'description', 'simulation_type', 'status',
            'base_carbon_footprint', 'base_water_usage', 'base_energy_usage', 'base_cost',
            'simulated_carbon_footprint', 'simulated_water_usage', 'simulated_energy_usage', 'simulated_cost',
            'carbon_reduction', 'water_reduction', 'energy_reduction', 'cost_savings',
            'parameters', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CreateSimulationSerializer(serializers.ModelSerializer):
    """Serializer for creating simulations with parameters."""
    parameters = SimulationParameterSerializer(many=True, required=False)
    
    class Meta:
        model = Simulation
        fields = ['name', 'description', 'simulation_type', 'parameters']
    
    def create(self, validated_data):
        parameters_data = validated_data.pop('parameters', [])
        simulation = Simulation.objects.create(**validated_data)
        
        for param_data in parameters_data:
            SimulationParameter.objects.create(simulation=simulation, **param_data)
        
        return simulation 